# Py3.11+
"""
JPT71 Data Spine — 키 정규화, TagMap v1.1, VoyageWindow, bridge_voyage_month,
Voyage Scorecard, Leakage Ledger, Exception Ledger, run_manifest.
plan §1~5, §11 P0/P1/P2 반영.
"""

import hashlib
import json
import re
from pathlib import Path
from typing import Any

import pandas as pd

try:
    import yaml
except ImportError:
    yaml = None


def _file_sha256(path: Path) -> str:
    if not path.is_file():
        return ""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_config(config_path: str | Path) -> dict[str, Any]:
    p = Path(config_path)
    if not p.is_file():
        return {}
    if yaml is None:
        return {}
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


# --- OFCO Invoice key normalization (P0) ---

def normalize_ofco_inv(raw: str, vendor_prefix: str = "OFCO") -> tuple[str, str, str]:
    """
    OFCO 인보이스 문자열 → InvoiceDigits(숫자만 가변길이), InvoiceKey, VendorPrefix.
    Returns: (invoice_digits, invoice_key, vendor_prefix).
    """
    if pd.isna(raw) or raw is None:
        return "", "", vendor_prefix
    s = str(raw).strip().upper()
    digits = "".join(re.findall(r"\d+", s))
    inv_key = f"{vendor_prefix}:{digits}" if digits else ""
    return digits, inv_key, vendor_prefix


def build_invoice_keys_ofco(df: pd.DataFrame, inv_col: str = "INVOICE NUMBER") -> pd.DataFrame:
    """OFCO DataFrame에 InvoiceRaw, InvoiceDigits, VendorPrefix, InvoiceKey 추가."""
    out = df.copy()
    out["InvoiceRaw"] = out[inv_col].astype(str) if inv_col in out.columns else ""
    digits_list = []
    key_list = []
    prefix_list = []
    for raw in out["InvoiceRaw"]:
        d, k, p = normalize_ofco_inv(raw)
        digits_list.append(d)
        key_list.append(k)
        prefix_list.append(p)
    out["InvoiceDigits"] = digits_list
    out["InvoiceKey"] = key_list
    out["VendorPrefix"] = prefix_list
    return out


def build_invoice_collision_ledger(df: pd.DataFrame) -> pd.DataFrame:
    """동일 InvoiceDigits에 서로 다른 InvoiceRaw가 2건 이상이면 기록."""
    if "InvoiceDigits" not in df.columns or "InvoiceRaw" not in df.columns:
        return pd.DataFrame(columns=["InvoiceDigits", "InvoiceRaw_List", "Count", "Severity"])
    g = df.groupby("InvoiceDigits").agg(
        InvoiceRaw_List=("InvoiceRaw", lambda x: list(x.dropna().unique())),
        Count=("InvoiceRaw", "nunique"),
    ).reset_index()
    g = g[g["Count"] >= 2]
    g["Severity"] = "WARN"
    return g[["InvoiceDigits", "InvoiceRaw_List", "Count", "Severity"]]


# --- jpt71 Sheet2: Base keys, YearMonth ---

def load_jpt71_sheet2_with_keys(path: str | Path) -> pd.DataFrame:
    if not Path(path).is_file():
        return pd.DataFrame()
    try:
        df = pd.read_excel(path, sheet_name="Sheet2")
    except Exception:
        return pd.DataFrame()
    if df.empty:
        return df
    if "Voyage No" not in df.columns:
        for c in ["Item No", "Item No.", "ITEM NO", "ID Number", "ID No", "Batch"]:
            if c in df.columns:
                df = df.rename(columns={c: "Voyage No"})
                break
    if "Voyage No" in df.columns:
        voyage = df["Voyage No"].astype(str).str.strip()
        df["Voyage No"] = voyage.replace({"": pd.NA, "nan": pd.NA, "None": pd.NA, "NAN": pd.NA})
    # Base columns (jpt71 is source of truth)
    date_col = None
    for c in ["Loading Date", "LoadingDate", "LOADING DATE"]:
        if c in df.columns:
            date_col = c
            break
    if date_col:
        df["LoadingDate_base"] = pd.to_datetime(df[date_col], errors="coerce")
        df["YearMonth"] = df["LoadingDate_base"].dt.to_period("M").astype(str)
    else:
        df["LoadingDate_base"] = pd.NaT
        df["YearMonth"] = ""
    ton_col = None
    for c in ["Delivery Qty(Ton)", "Delivery Qty (Ton)", "Delivery_Qty_Ton"]:
        if c in df.columns:
            ton_col = c
            break
    if ton_col:
        df["DeliveryTon_base"] = pd.to_numeric(df[ton_col], errors="coerce").fillna(0)
    else:
        df["DeliveryTon_base"] = 0.0
    inv_col = None
    for c in ["OFCO INVOICE NO", "OFCO INVOICE NO.", "OFCO_INVOICE_NO"]:
        if c in df.columns:
            inv_col = c
            break
    if inv_col:
        raw = df[inv_col].astype(str)
        df["InvoiceRaw"] = raw
        df["InvoiceDigits"] = raw.map(lambda x: "".join(re.findall(r"\d+", str(x))))
        df["InvoiceKey"] = "OFCO:" + df["InvoiceDigits"]
    return df


# --- TagMap v1.1 ---

def load_tagmap_v11(path: str | Path) -> pd.DataFrame:
    p = Path(path)
    if not p.is_file():
        return pd.DataFrame()
    try:
        if p.suffix.lower() in (".csv", ".txt"):
            df = pd.read_csv(p, encoding="utf-8")
        else:
            df = pd.read_excel(p, sheet_name=0)
    except Exception:
        return pd.DataFrame()
    required = ["Keyword", "ReasonCode", "ProductiveFlag"]
    for c in required:
        if c not in df.columns:
            return pd.DataFrame()
    df["Priority"] = pd.to_numeric(df.get("Priority", 99), errors="coerce").fillna(99).astype(int)
    df["MatchType"] = df.get("MatchType", "CONTAINS").fillna("CONTAINS").str.upper()
    df["SeverityWeight"] = pd.to_numeric(df.get("SeverityWeight", 1.0), errors="coerce").fillna(1.0)
    df["NegativeKeywords"] = df.get("NegativeKeywords", "").fillna("").astype(str)
    return df.sort_values("Priority").reset_index(drop=True)


def tag_activity(activity: str, tagmap_df: pd.DataFrame) -> dict[str, Any]:
    """단일 Activity 문자열에 TagMap v1.1 적용. Priority 오름차순, 첫 매칭."""
    if not isinstance(activity, str) or not activity.strip():
        return {"ReasonCode": "UNKNOWN", "ProductiveFlag": 0, "Category": "OTHER", "SeverityWeight": 1.0}
    norm = " ".join(str(activity).upper().strip().split())
    if tagmap_df.empty:
        return {"ReasonCode": "UNKNOWN", "ProductiveFlag": 0, "Category": "OTHER", "SeverityWeight": 1.0}
    for _, row in tagmap_df.iterrows():
        kw = str(row["Keyword"]).upper().strip()
        if not kw:
            continue
        neg = str(row.get("NegativeKeywords", "") or "").upper()
        if neg and any(n in norm for n in neg.split(";")):
            continue
        match_type = str(row.get("MatchType", "CONTAINS")).upper()
        if match_type == "EXACT" and norm != kw:
            continue
        if match_type in ("CONTAINS", "CONTAINS ") and kw not in norm:
            continue
        if match_type == "REGEX" and not re.search(kw, norm):
            continue
        pv = pd.to_numeric(row["ProductiveFlag"], errors="coerce")
        pv = 0 if pd.isna(pv) else int(pv)
        sw = pd.to_numeric(row.get("SeverityWeight", 1.0), errors="coerce")
        sw = 1.0 if pd.isna(sw) else float(sw)
        return {
            "ReasonCode": str(row["ReasonCode"]),
            "ProductiveFlag": pv,
            "Category": str(row.get("Category", "OTHER")),
            "SeverityWeight": sw,
        }
    return {"ReasonCode": "UNKNOWN", "ProductiveFlag": 0, "Category": "OTHER", "SeverityWeight": 1.0}


def tag_decklog(df: pd.DataFrame, tagmap_df: pd.DataFrame, activity_col: str = "Activity") -> pd.DataFrame:
    """decklog에 ReasonCode, ProductiveFlag, Category, SeverityWeight 컬럼 추가."""
    if df.empty or activity_col not in df.columns:
        return df
    out = df.copy()
    tagged = [tag_activity(a, tagmap_df) for a in out[activity_col]]
    out["ReasonCode"] = [t["ReasonCode"] for t in tagged]
    out["ProductiveFlag"] = [t["ProductiveFlag"] for t in tagged]
    out["Category"] = [t["Category"] for t in tagged]
    out["SeverityWeight"] = [t["SeverityWeight"] for t in tagged]
    return out


def fact_daily_ops(decklog_df: pd.DataFrame, tagmap_df: pd.DataFrame) -> pd.DataFrame:
    """fact_daily_ops: DateKey, YearMonth, ActivityRaw, ReasonCode, ProductiveFlag, Category, SeverityWeight."""
    if decklog_df.empty:
        return pd.DataFrame()
    date_col = None
    for c in ["Date", "DATE", "date"]:
        if c in decklog_df.columns:
            date_col = c
            break
    if not date_col:
        return pd.DataFrame()
    act_col = "Activity" if "Activity" in decklog_df.columns else [c for c in decklog_df.columns if "activ" in c.lower()]
    if isinstance(act_col, list):
        act_col = act_col[0] if act_col else None
    if not act_col:
        return pd.DataFrame()
    tagged = tag_decklog(decklog_df, tagmap_df, act_col)
    tagged["DateKey"] = pd.to_datetime(tagged[date_col], errors="coerce").dt.strftime("%Y-%m-%d")
    tagged["YearMonth"] = pd.to_datetime(tagged[date_col], errors="coerce").dt.to_period("M").astype(str)
    tagged["ActivityRaw"] = tagged[act_col].astype(str)
    cols = ["DateKey", "YearMonth", "ActivityRaw", "ReasonCode", "ProductiveFlag", "Category", "SeverityWeight"]
    extra = [c for c in tagged.columns if c not in cols and c in ["VLFuel_Consumption", "VLFW_Consumption"]]
    return tagged[cols + extra] if extra else tagged[cols]


# --- VoyageWindow (P0) ---

def voyage_window_from_loading_date(
    loading_date: pd.Timestamp,
    decklog_df: pd.DataFrame,
    start_keywords: list[str],
    end_keywords: list[str],
    fallback_days: int = 7,
) -> tuple[pd.Timestamp | None, pd.Timestamp | None, int]:
    """
    decklog에서 LoadingDate 전후로 Start/End 일자 찾기.
    Returns (start_date, end_date, fallback_flag: 0 or 1).
    """
    if decklog_df.empty or loading_date is pd.NaT:
        return None, None, 1
    date_col = "Date" if "Date" in decklog_df.columns else [c for c in decklog_df.columns if "date" in c.lower()]
    if isinstance(date_col, list):
        date_col = date_col[0] if date_col else None
    act_col = "Activity" if "Activity" in decklog_df.columns else None
    if not date_col or not act_col:
        return None, None, 1
    decklog_df = decklog_df.copy()
    decklog_df["_dt"] = pd.to_datetime(decklog_df[date_col], errors="coerce")
    decklog_df = decklog_df.dropna(subset=["_dt"]).sort_values("_dt")
    act_upper = decklog_df[act_col].astype(str).str.upper()
    start_dates = []
    end_dates = []
    for kw in start_keywords:
        mask = act_upper.str.contains(kw, na=False)
        start_dates.extend(decklog_df.loc[mask, "_dt"].tolist())
    for kw in end_keywords:
        mask = act_upper.str.contains(kw, na=False)
        end_dates.extend(decklog_df.loc[mask, "_dt"].tolist())
    ld = pd.Timestamp(loading_date)
    before = [d for d in start_dates if d <= ld + pd.Timedelta(days=2)]
    after = [d for d in end_dates if d >= ld - pd.Timedelta(days=2)]
    start = max(before) if before else (ld - pd.Timedelta(days=fallback_days))
    end = min(after) if after else (ld + pd.Timedelta(days=fallback_days))
    fallback = 0 if (before or after) else 1
    return start, end, fallback


# --- bridge_voyage_month ---

def build_bridge_voyage_month(
    voyage_days_by_voyage: dict[str, int],
    voyage_days_by_voyage_month: dict[tuple[str, str], int],
) -> pd.DataFrame:
    """
    voyage_days_by_voyage: VoyageKey -> total ops days
    voyage_days_by_voyage_month: (VoyageKey, YearMonth) -> ops days in that month
    """
    rows = []
    for (vk, ym), days_in in voyage_days_by_voyage_month.items():
        total = voyage_days_by_voyage.get(vk, 0) or 1
        ratio = days_in / total if total else 0
        rows.append({"VoyageKey": vk, "YearMonth": ym, "OpsDays_in_month": days_in, "OpsDays_total": total, "OpsDays_ratio": round(ratio, 4)})
    return pd.DataFrame(rows)


# --- Voyage Scorecard ---

def build_voyage_scorecard(
    jpt71_agg: pd.DataFrame,
    ofco_agg: pd.DataFrame,
    voyage_col_j71: str = "VoyageKey",
    voyage_col_ofco: str = "Voyage No",
) -> pd.DataFrame:
    """VoyageKey, VoyageDays, DeliveredTon, Cost_Voyage_AED, Cost_Ton_AED."""
    if jpt71_agg.empty and ofco_agg.empty:
        return pd.DataFrame()
    score = []
    if not jpt71_agg.empty:
        for _, r in jpt71_agg.iterrows():
            vk = r.get(voyage_col_j71, r.get("Voyage No", r.get("Batch", "")))
            ton = float(r.get("DeliveryTon_base", r.get("DeliveredTon", 0)) or 0)
            score.append({"VoyageKey": str(vk), "DeliveredTon": ton})
    else:
        score = [{"VoyageKey": str(r.get(voyage_col_ofco, "")), "DeliveredTon": 0} for _, r in ofco_agg.iterrows()]
    sc_df = pd.DataFrame(score)
    if not ofco_agg.empty and voyage_col_ofco in ofco_agg.columns:
        cost_map = ofco_agg.set_index(voyage_col_ofco)["Total_AED"].to_dict()
        sc_df["Cost_Voyage_AED"] = sc_df["VoyageKey"].map(lambda x: cost_map.get(x, cost_map.get(str(x), 0)))
    else:
        sc_df["Cost_Voyage_AED"] = 0
    sc_df["Cost_Voyage_AED"] = pd.to_numeric(sc_df["Cost_Voyage_AED"], errors="coerce").fillna(0)
    sc_df["VoyageDays"] = 0  # caller can fill from decklog/voyage window
    sc_df["Cost_Ton_AED"] = sc_df.apply(
        lambda r: r["Cost_Voyage_AED"] / r["DeliveredTon"] if r["DeliveredTon"] and r["DeliveredTon"] > 0 else 0,
        axis=1,
    )
    return sc_df


def _allocate_cost_by_voyage_mixed(
    j71_df: pd.DataFrame,
    ofco_df: pd.DataFrame,
    tolerance: float = 1e-6,
) -> tuple[pd.DataFrame, float]:
    """Allocate OFCO costs to j71 voyages with InvoiceKey-first + Voyage fallback.
    The total allocated amount is forced to equal the OFCO scoped total."""
    if j71_df.empty or "Voyage No" not in j71_df.columns:
        return pd.DataFrame(columns=["Voyage No", "Total_AED"]), 0.0

    j71_base = j71_df.copy()
    j71_base["Voyage No"] = j71_base["Voyage No"].astype(str).str.strip()
    j71_base = j71_base[j71_base["Voyage No"].str.len() > 0]
    if j71_base.empty:
        return pd.DataFrame(columns=["Voyage No", "Total_AED"]), 0.0

    voyage_base = pd.DataFrame({"Voyage No": sorted(j71_base["Voyage No"].dropna().astype(str).unique())})
    if ofco_df.empty or "Voyage No" not in ofco_df.columns or "Total_Amount_AED" not in ofco_df.columns:
        voyage_base["Total_AED"] = 0.0
        return voyage_base, 0.0

    ofco_scope = ofco_df.copy()
    ofco_scope["Voyage No"] = ofco_scope["Voyage No"].astype(str).str.strip()
    ofco_scope = ofco_scope[ofco_scope["Voyage No"].isin(set(voyage_base["Voyage No"]))]
    ofco_scope["Total_AED_row"] = pd.to_numeric(ofco_scope["Total_Amount_AED"], errors="coerce").fillna(0)
    ofco_target_total = float(ofco_scope["Total_AED_row"].sum())
    if ofco_scope.empty:
        voyage_base["Total_AED"] = 0.0
        return voyage_base, 0.0

    invoice_alloc = pd.DataFrame(columns=["Voyage No", "Invoice_AED"])
    matched_keys: set[str] = set()
    if "InvoiceKey" in ofco_scope.columns and "InvoiceKey" in j71_base.columns:
        invoice_total = (
            ofco_scope.groupby("InvoiceKey", dropna=True)["Total_AED_row"]
            .sum()
            .reset_index(name="Invoice_Total_AED")
        )
        invoice_total["InvoiceKey"] = invoice_total["InvoiceKey"].astype(str).str.strip()
        invoice_total = invoice_total[invoice_total["InvoiceKey"].str.len() > 0]

        j71_iv = j71_base[["InvoiceKey", "Voyage No", "DeliveryTon_base"]].copy()
        j71_iv["InvoiceKey"] = j71_iv["InvoiceKey"].astype(str).str.strip()
        j71_iv = j71_iv[j71_iv["InvoiceKey"].str.len() > 0]
        j71_iv["DeliveryTon_base"] = pd.to_numeric(j71_iv["DeliveryTon_base"], errors="coerce").fillna(0)
        j71_iv = (
            j71_iv.groupby(["InvoiceKey", "Voyage No"], as_index=False)["DeliveryTon_base"]
            .sum()
        )

        matched = j71_iv.merge(invoice_total, on="InvoiceKey", how="inner")
        if not matched.empty:
            matched_keys = set(matched["InvoiceKey"].dropna().astype(str))
            matched["WeightSum"] = matched.groupby("InvoiceKey")["DeliveryTon_base"].transform("sum")
            matched["VoyageCount"] = matched.groupby("InvoiceKey")["Voyage No"].transform("count")
            matched["Invoice_AED"] = matched.apply(
                lambda r: (
                    r["Invoice_Total_AED"] * r["DeliveryTon_base"] / r["WeightSum"]
                    if r["WeightSum"] > 0
                    else (r["Invoice_Total_AED"] / r["VoyageCount"] if r["VoyageCount"] > 0 else 0.0)
                ),
                axis=1,
            )
            invoice_alloc = matched.groupby("Voyage No", as_index=False)["Invoice_AED"].sum()

    fallback_scope = ofco_scope
    if "InvoiceKey" in ofco_scope.columns and matched_keys:
        key_series = ofco_scope["InvoiceKey"].fillna("").astype(str).str.strip()
        fallback_scope = ofco_scope[~key_series.isin(matched_keys)]
    fallback_alloc = (
        fallback_scope.groupby("Voyage No", as_index=False)["Total_AED_row"]
        .sum()
        .rename(columns={"Total_AED_row": "Fallback_AED"})
    )

    by_voyage = voyage_base.merge(invoice_alloc, on="Voyage No", how="left")
    by_voyage = by_voyage.merge(fallback_alloc, on="Voyage No", how="left")
    by_voyage["Invoice_AED"] = pd.to_numeric(by_voyage["Invoice_AED"], errors="coerce").fillna(0)
    by_voyage["Fallback_AED"] = pd.to_numeric(by_voyage["Fallback_AED"], errors="coerce").fillna(0)
    by_voyage["Total_AED"] = by_voyage["Invoice_AED"] + by_voyage["Fallback_AED"]
    by_voyage = by_voyage[["Voyage No", "Total_AED"]]

    allocated_total = float(by_voyage["Total_AED"].sum())
    diff = ofco_target_total - allocated_total
    if abs(diff) > tolerance and not by_voyage.empty:
        idx = by_voyage["Total_AED"].idxmax()
        by_voyage.loc[idx, "Total_AED"] = float(by_voyage.loc[idx, "Total_AED"]) + diff

    final_total = float(by_voyage["Total_AED"].sum())
    if abs(final_total - ofco_target_total) > tolerance:
        raise AssertionError(
            f"Cost allocation mismatch: allocated={final_total:.6f} target={ofco_target_total:.6f}"
        )
    return by_voyage, ofco_target_total


# --- Leakage Ledger (P1) ---

def build_leakage_ledger(
    fact_ops: pd.DataFrame,
    charter_aed_per_day: float,
    config: dict,
) -> pd.DataFrame:
    """IdleChargeableDays, NonChargeableDays, LeakageAED, ReasonCode, Evidence.
    P1: Adds CharterAED_per_day_source, CharterAED_per_day_confidence from config."""
    charter_cfg = config.get("charter", {})
    charter_source = str(charter_cfg.get("source", "MANUAL"))
    charter_confidence = float(charter_cfg.get("confidence", 0.8))
    if fact_ops.empty:
        return pd.DataFrame(columns=["YearMonth", "ReasonCode", "IdleChargeableDays", "NonChargeableDays", "LeakageAED", "Evidence", "CharterAED_per_day_source", "CharterAED_per_day_confidence"])
    cfg = config.get("tagmap", {})
    default_sev = float(cfg.get("default_severity_weight", 1.0))
    ops = fact_ops.copy()
    if "ProductiveFlag" not in ops.columns:
        ops["ProductiveFlag"] = 0
    if "ReasonCode" not in ops.columns:
        ops["ReasonCode"] = "UNKNOWN"
    if "SeverityWeight" not in ops.columns:
        ops["SeverityWeight"] = default_sev
    if "YearMonth" not in ops.columns and "DateKey" in ops.columns:
        ops["YearMonth"] = pd.to_datetime(ops["DateKey"], errors="coerce").dt.to_period("M").astype(str)
    idle = ops[ops["ProductiveFlag"] == 0].copy()
    idle["IdleChargeableDays"] = 1
    idle["NonChargeableDays"] = idle["Category"].apply(lambda c: 1 if str(c).upper() in ("OFFHIRE", "OFF-HIRE") else 0)
    idle["IdleChargeableDays"] = idle["IdleChargeableDays"] - idle["NonChargeableDays"]
    idle["LeakageAED"] = idle["IdleChargeableDays"] * charter_aed_per_day * idle["SeverityWeight"]
    idle["Evidence"] = idle.apply(lambda r: f"DateKey={r.get('DateKey','')} ReasonCode={r.get('ReasonCode','')}", axis=1)
    agg = idle.groupby(["YearMonth", "ReasonCode"]).agg(
        IdleChargeableDays=("IdleChargeableDays", "sum"),
        NonChargeableDays=("NonChargeableDays", "sum"),
        LeakageAED=("LeakageAED", "sum"),
        Evidence=("Evidence", lambda x: "; ".join(x.dropna().astype(str).head(3))),
    ).reset_index()
    agg["CharterAED_per_day_source"] = charter_source
    agg["CharterAED_per_day_confidence"] = charter_confidence
    return agg


def derive_cost_type_ofco(ofco_df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """Add CostType column to ofco from column names / keywords. CHARTER, FUEL, PORT, OTHER, UNKNOWN."""
    if ofco_df.empty:
        return ofco_df
    keywords = config.get("charter", {}).get("cost_type_keywords", {})
    cost_type_map = {}
    for col in ofco_df.columns:
        if not isinstance(col, str):
            continue
        c_upper = col.upper().replace("_", " ")
        ct = "UNKNOWN"
        for cost_type, kws in keywords.items():
            if any(kw.upper() in c_upper for kw in kws):
                ct = cost_type
                break
        if "AMOUNT" in c_upper or "AED" in c_upper:
            cost_type_map[col] = ct
    out = ofco_df.copy()
    out["CostType"] = "UNKNOWN"
    amt_cols = [c for c in cost_type_map if c in out.columns]
    for col in amt_cols:
        vals = pd.to_numeric(out[col], errors="coerce").fillna(0)
        out.loc[vals > 0, "CostType"] = cost_type_map[col]
    out.loc[out["CostType"] == "UNKNOWN", "CostType"] = "OTHER"
    return out


# --- Exception Ledger ---

def _join_j71_ofco_for_dual_value(
    j71_df: pd.DataFrame,
    ofco_df: pd.DataFrame,
    config: dict,
) -> pd.DataFrame:
    """Join jpt71 and ofco on InvoiceKey; add LoadingDate_base, DeliveryTon_base, Delta_*, flags.
    When ofco has no date/ton columns, Delta and mismatch flags stay 0/False."""
    if j71_df.empty or ofco_df.empty or "InvoiceKey" not in j71_df.columns or "InvoiceKey" not in ofco_df.columns:
        return pd.DataFrame()
    ofco_agg = ofco_df.groupby("InvoiceKey").agg(
        Total_AED=("Total_Amount_AED", lambda s: pd.to_numeric(s, errors="coerce").fillna(0).sum()) if "Total_Amount_AED" in ofco_df.columns else ("InvoiceKey", "count"),
    ).reset_index()
    j71_agg = j71_df.groupby("InvoiceKey").agg(
        LoadingDate_base=("LoadingDate_base", "min"),
        DeliveryTon_base=("DeliveryTon_base", "sum"),
    ).reset_index()
    merged = j71_agg.merge(ofco_agg, on="InvoiceKey", how="left")
    merged["InvoiceRaw"] = merged["InvoiceKey"].map(
        ofco_df.groupby("InvoiceKey").first().get("InvoiceRaw", pd.Series(dtype=object)).to_dict()
    )
    ton_warn = float(config.get("mismatch", {}).get("ton_mismatch_warn_pct", 0.03))
    ton_high = float(config.get("mismatch", {}).get("ton_mismatch_high_pct", 0.10))
    merged["LoadingDate_src_ofco"] = pd.NaT
    merged["DeliveryTon_src"] = 0.0
    merged["Delta_LoadingDate_days"] = 0
    merged["Delta_Ton_pct"] = 0.0
    merged["DATE_MISMATCH"] = False
    merged["TON_MISMATCH_WARN"] = False
    merged["TON_MISMATCH_HIGH"] = False
    if "LoadingDate" in ofco_df.columns or "LOADING_DATE" in ofco_df.columns:
        date_col = "LoadingDate" if "LoadingDate" in ofco_df.columns else "LOADING_DATE"
        src_dates = ofco_df.groupby("InvoiceKey")[date_col].first()
        merged["LoadingDate_src_ofco"] = merged["InvoiceKey"].map(src_dates)
        merged["LoadingDate_src_ofco"] = pd.to_datetime(merged["LoadingDate_src_ofco"], errors="coerce")
        delta_days = (merged["LoadingDate_base"] - merged["LoadingDate_src_ofco"]).dt.days
        merged["Delta_LoadingDate_days"] = delta_days.fillna(0).astype(int)
        merged["DATE_MISMATCH"] = merged["Delta_LoadingDate_days"].fillna(0) != 0
    for qcol in ["Delivery_Qty", "Delivery Qty(Ton)", "SHPT_QTY", "Quantity"]:
        if qcol in ofco_df.columns:
            src_ton = ofco_df.groupby("InvoiceKey")[qcol].apply(lambda s: pd.to_numeric(s, errors="coerce").fillna(0).sum()).reindex(merged["InvoiceKey"]).fillna(0).values
            merged["DeliveryTon_src"] = src_ton
            base = merged["DeliveryTon_base"].fillna(0).replace(0, 1)
            merged["Delta_Ton_pct"] = ((merged["DeliveryTon_base"].fillna(0) - merged["DeliveryTon_src"]) / base).fillna(0)
            merged["TON_MISMATCH_WARN"] = merged["Delta_Ton_pct"].abs().between(ton_warn, ton_high)
            merged["TON_MISMATCH_HIGH"] = merged["Delta_Ton_pct"].abs() > ton_high
            break
    return merged


def collect_exceptions(
    collision_ledger: pd.DataFrame,
    jpt71_df: pd.DataFrame,
    ofco_df: pd.DataFrame,
    fact_ops: pd.DataFrame,
    tagmap_unknown_rate: float,
    config: dict,
    dual_value_df: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Type, Key, Evidence, Severity. Includes KEY_COLLISION, UNMATCHED_INVOICE, UNMATCHED_VOYAGE,
    DUPLICATE_KEY, DATE_MISMATCH, TON_MISMATCH, TAGMAP_DRIFT_WARN."""
    rows = []
    # KEY_COLLISION
    if not collision_ledger.empty:
        for _, r in collision_ledger.iterrows():
            rows.append({"Type": "KEY_COLLISION", "Key": str(r.get("InvoiceDigits", "")), "Evidence": str(r.get("InvoiceRaw_List", "")), "Severity": str(r.get("Severity", "WARN"))})
    # UNMATCHED_INVOICE (jpt71 InvoiceKey not in ofco)
    if not jpt71_df.empty and "InvoiceKey" in jpt71_df.columns and not ofco_df.empty and "InvoiceKey" in ofco_df.columns:
        j71_keys = set(jpt71_df["InvoiceKey"].dropna().astype(str))
        ofco_keys = set(ofco_df["InvoiceKey"].dropna().astype(str))
        for k in j71_keys:
            if k and k not in ofco_keys:
                rows.append({"Type": "UNMATCHED_INVOICE", "Key": k, "Evidence": "jpt71 Sheet2", "Severity": "INFO"})
    # UNMATCHED_VOYAGE (ofco Voyage No with no j71 InvoiceKey linked)
    if not ofco_df.empty and "Voyage No" in ofco_df.columns and not jpt71_df.empty and "InvoiceKey" in jpt71_df.columns:
        ofco_inv_per_voyage = ofco_df.groupby("Voyage No")["InvoiceKey"].apply(lambda x: set(x.dropna().astype(str))).to_dict()
        j71_keys = set(jpt71_df["InvoiceKey"].dropna().astype(str))
        for voyage, inv_set in ofco_inv_per_voyage.items():
            if not inv_set or not any(inv in j71_keys for inv in inv_set):
                rows.append({"Type": "UNMATCHED_VOYAGE", "Key": str(voyage), "Evidence": "ofco Voyage No has no jpt71 InvoiceKey", "Severity": "INFO"})
    # DUPLICATE_KEY
    if not jpt71_df.empty and "InvoiceKey" in jpt71_df.columns:
        j71_dup = jpt71_df[jpt71_df.duplicated(subset=["InvoiceKey"], keep=False)]["InvoiceKey"].dropna().astype(str).unique()
        for k in j71_dup:
            if k:
                rows.append({"Type": "DUPLICATE_KEY", "Key": k, "Evidence": "jpt71 Sheet2 duplicate InvoiceKey", "Severity": "WARN"})
    if not ofco_df.empty and "InvoiceKey" in ofco_df.columns:
        ofco_dup = ofco_df[ofco_df.duplicated(subset=["InvoiceKey"], keep=False)]["InvoiceKey"].dropna().astype(str).unique()
        for k in ofco_dup:
            if k and not any(r.get("Key") == k and r.get("Type") == "DUPLICATE_KEY" for r in rows):
                rows.append({"Type": "DUPLICATE_KEY", "Key": k, "Evidence": "ofco duplicate InvoiceKey", "Severity": "WARN"})
    # DATE_MISMATCH / TON_MISMATCH from dual_value
    if dual_value_df is not None and not dual_value_df.empty:
        if "DATE_MISMATCH" in dual_value_df.columns and dual_value_df["DATE_MISMATCH"].any():
            for _, r in dual_value_df[dual_value_df["DATE_MISMATCH"]].iterrows():
                rows.append({"Type": "DATE_MISMATCH", "Key": str(r.get("InvoiceKey", "")), "Evidence": f"Delta_LoadingDate_days={r.get('Delta_LoadingDate_days', 0)}", "Severity": "WARN"})
        if "TON_MISMATCH_HIGH" in dual_value_df.columns and dual_value_df["TON_MISMATCH_HIGH"].any():
            for _, r in dual_value_df[dual_value_df["TON_MISMATCH_HIGH"]].iterrows():
                rows.append({"Type": "TON_MISMATCH", "Key": str(r.get("InvoiceKey", "")), "Evidence": f"Delta_Ton_pct={r.get('Delta_Ton_pct', 0):.2%} HIGH", "Severity": "HIGH"})
        if "TON_MISMATCH_WARN" in dual_value_df.columns and dual_value_df["TON_MISMATCH_WARN"].any():
            high_col = dual_value_df["TON_MISMATCH_HIGH"] if "TON_MISMATCH_HIGH" in dual_value_df.columns else pd.Series(False, index=dual_value_df.index)
            for _, r in dual_value_df[dual_value_df["TON_MISMATCH_WARN"] & ~high_col].iterrows():
                rows.append({"Type": "TON_MISMATCH", "Key": str(r.get("InvoiceKey", "")), "Evidence": f"Delta_Ton_pct={r.get('Delta_Ton_pct', 0):.2%} WARN", "Severity": "WARN"})
    # TAGMAP_DRIFT_WARN
    unknown_warn = float(config.get("tagmap", {}).get("unknown_rate_warn", 0.05))
    if tagmap_unknown_rate > unknown_warn:
        rows.append({"Type": "TAGMAP_DRIFT_WARN", "Key": "UNKNOWN", "Evidence": f"UNKNOWN rate {tagmap_unknown_rate:.2%} > {unknown_warn:.2%}", "Severity": "WARN"})
    if not rows:
        out = pd.DataFrame(columns=["Type", "Key", "Evidence", "Severity"])
    else:
        out = pd.DataFrame(rows)
    return out


# --- run_manifest (P2) ---

def write_run_manifest(
    out_path: str | Path,
    inputs: dict[str, str],
    config_version: str,
    row_counts: dict[str, int],
    unknown_rate: float,
    unmatched_count: int,
    collision_count: int,
    outputs: list[str],
    run_id: str | None = None,
) -> None:
    import uuid
    manifest = {
        "run_id": run_id or str(uuid.uuid4()),
        "config_version": config_version,
        "inputs": inputs,
        "row_counts": row_counts,
        "unknown_rate": unknown_rate,
        "unmatched_count": unmatched_count,
        "collision_count": collision_count,
        "outputs": outputs,
    }
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    return None


# --- Run full spine ---

def run_spine(
    data_dir: str | Path,
    config_path: str | Path | None = None,
    charter_aed_per_day: float = 0.0,
) -> dict[str, Any]:
    """
    데이터 폴더 기준으로 Data Spine 실행.
    Returns: {
      fact_daily_ops, fact_delivery, fact_cost (optional),
      voyage_scorecard, leakage_ledger, exception_ledger, collision_ledger,
      bridge_voyage_month (optional),
      tagmap_drift_warn, unknown_rate,
      config, run_manifest_path
    }
    """
    data_dir = Path(data_dir)
    if config_path is None:
        config_path = data_dir / "config_jpt71_report.yml"
    config = load_config(config_path)
    tagmap_path = data_dir / config.get("tagmap", {}).get("path", "TagMap_v1.1.csv")
    tagmap_df = load_tagmap_v11(tagmap_path)

    # Load sources
    ofco_path = data_dir / "ofco detail.xlsx"
    deck_path = data_dir / "decklog.xlsx"
    j71_path = data_dir / "jpt71.xlsx"

    ofco_df = pd.DataFrame()
    if ofco_path.is_file():
        ofco_df = pd.read_excel(ofco_path, sheet_name="OFCO INVOICE ALL")
        ofco_df["Voyage No"] = ofco_df["Voyage No"].astype(str).str.strip()
        ofco_df = ofco_df[ofco_df["Voyage No"].str.len() > 0]
        ofco_df = build_invoice_keys_ofco(ofco_df)
        ofco_df = derive_cost_type_ofco(ofco_df, config)

    collision_ledger = build_invoice_collision_ledger(ofco_df) if not ofco_df.empty else pd.DataFrame()

    j71_df = load_jpt71_sheet2_with_keys(str(j71_path))

    deck_df = pd.DataFrame()
    if deck_path.is_file():
        xl = pd.ExcelFile(deck_path)
        deck_df = pd.read_excel(deck_path, sheet_name=xl.sheet_names[0])
    fact_ops = fact_daily_ops(deck_df, tagmap_df) if not deck_df.empty else pd.DataFrame()

    unknown_rate = 0.0
    if not fact_ops.empty and "ReasonCode" in fact_ops.columns:
        unknown_rate = (fact_ops["ReasonCode"] == "UNKNOWN").mean()

    j71_voyage_rows = pd.DataFrame(columns=["Voyage No", "LoadingDate_base", "DeliveryTon_base", "InvoiceKey"])
    if not j71_df.empty and "Voyage No" in j71_df.columns:
        j71_voyage_rows = j71_df.copy()
        j71_voyage_rows["Voyage No"] = j71_voyage_rows["Voyage No"].astype(str).str.strip()
        j71_voyage_rows = j71_voyage_rows[j71_voyage_rows["Voyage No"].str.len() > 0]

    by_voyage, ofco_target_total = _allocate_cost_by_voyage_mixed(j71_voyage_rows, ofco_df)
    if not j71_voyage_rows.empty:
        voyage_ton = (
            j71_voyage_rows.groupby("Voyage No", as_index=False)["DeliveryTon_base"]
            .sum()
            .rename(columns={"DeliveryTon_base": "DeliveredTon"})
        )
    else:
        voyage_ton = pd.DataFrame(columns=["Voyage No", "DeliveredTon"])
    scorecard = by_voyage.merge(voyage_ton, on="Voyage No", how="left")
    scorecard["DeliveredTon"] = pd.to_numeric(scorecard["DeliveredTon"], errors="coerce").fillna(0)
    scorecard["VoyageKey"] = scorecard["Voyage No"]
    scorecard["Cost_Voyage_AED"] = pd.to_numeric(scorecard["Total_AED"], errors="coerce").fillna(0)
    scorecard["VoyageDays"] = 0
    scorecard["Cost_Ton_AED"] = scorecard.apply(
        lambda r: r["Cost_Voyage_AED"] / r["DeliveredTon"] if r["DeliveredTon"] and r["DeliveredTon"] > 0 else 0,
        axis=1,
    )
    scorecard = scorecard[["VoyageKey", "VoyageDays", "DeliveredTon", "Cost_Voyage_AED", "Cost_Ton_AED"]]

    # VoyageDays from VoyageWindow when decklog has no Voyage column
    vw_cfg = config.get("voyage_window", {})
    start_kw = vw_cfg.get("start_keywords", ["SAILING", "DEPARTURE", "CASTED OFF", "UNDERWAY"])
    end_kw = vw_cfg.get("end_keywords", ["DISCHARGE", "DELIVERY COMPLETE", "ARRIVAL", "SECURED", "OFF-LOADING COMP"])
    fallback_days = int(vw_cfg.get("fallback_days", 7))
    dcol = next((c for c in ["Date", "DATE", "date"] if c in deck_df.columns), None)
    vcol = next((c for c in ["VoyageKey", "Voyage", "Trip", "Batch"] if c in deck_df.columns), None)
    if not scorecard.empty and not deck_df.empty and dcol and not vcol and not j71_voyage_rows.empty and "LoadingDate_base" in j71_voyage_rows.columns:
        voyage_min_date = j71_voyage_rows.groupby("Voyage No")["LoadingDate_base"].min()
        vdays = {}
        for vk, ld in voyage_min_date.items():
            if pd.isna(ld):
                continue
            start_d, end_d, _ = voyage_window_from_loading_date(ld, deck_df, start_kw, end_kw, fallback_days)
            if start_d is not None and end_d is not None:
                vdays[str(vk)] = max(0, (end_d - start_d).days + 1)
        if vdays:
            scorecard["VoyageDays"] = scorecard["VoyageKey"].map(vdays).fillna(0).astype(int)

    dual_value_df = _join_j71_ofco_for_dual_value(j71_df, ofco_df, config) if not j71_df.empty and not ofco_df.empty else pd.DataFrame()
    leakage = build_leakage_ledger(fact_ops, charter_aed_per_day or 1.0, config)
    exceptions = collect_exceptions(collision_ledger, j71_df, ofco_df, fact_ops, unknown_rate, config, dual_value_df=dual_value_df)

    # bridge_voyage_month: when decklog has Voyage/Trip/Batch we fill OpsDays per (VoyageKey, YearMonth)
    voyage_days_by_voyage = {}
    voyage_days_by_voyage_month = {}
    dcol = next((c for c in ["Date", "DATE", "date"] if c in deck_df.columns), None)
    vcol = next((c for c in ["VoyageKey", "Voyage", "Trip", "Batch"] if c in deck_df.columns), None)
    if dcol and vcol:
        deck_df = deck_df.copy()
        deck_df["_ym"] = pd.to_datetime(deck_df[dcol], errors="coerce").dt.to_period("M").astype(str)
        for (vk, ym), grp in deck_df.groupby([vcol, "_ym"]):
            voyage_days_by_voyage_month[(str(vk), str(ym))] = len(grp)
            voyage_days_by_voyage[str(vk)] = voyage_days_by_voyage.get(str(vk), 0) + len(grp)
    bridge = build_bridge_voyage_month(voyage_days_by_voyage, voyage_days_by_voyage_month) if voyage_days_by_voyage else pd.DataFrame()

    return {
        "fact_daily_ops": fact_ops,
        "voyage_scorecard": scorecard,
        "leakage_ledger": leakage,
        "exception_ledger": exceptions,
        "collision_ledger": collision_ledger,
        "dual_value_df": dual_value_df,
        "bridge_voyage_month": bridge,
        "tagmap_drift_warn": unknown_rate > float(config.get("tagmap", {}).get("unknown_rate_warn", 0.05)),
        "unknown_rate": unknown_rate,
        "config": config,
        "ofco_target_total": ofco_target_total,
        "by_voyage": by_voyage,
        "j71_df": j71_df,
        "ofco_df": ofco_df,
    }
