from __future__ import annotations

import argparse
import json
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
WORKBOOK = ROOT / "JPT-reconciled_v5.2.xlsx"
WORKBOOK_V53 = ROOT / "JPT-reconciled_v5.3.xlsx"
DASH = ROOT / "DASHBOARD"
ROOT_HTML_LADEN_BALLAST = ROOT / "JPT71 Laden_Ballast Fuel RootCause Analysis.html"


def fmt_num(value: float, digits: int = 1) -> str:
    return f"{value:,.{digits}f}"


def fmt_int(value: float | int) -> str:
    return f"{round(float(value)):,}"


def fmt_pct(value: float, digits: int = 1) -> str:
    return f"{value:.{digits}f}%"


def json_text(data: object) -> str:
    return json.dumps(data, ensure_ascii=False, separators=(",", ": "))


def replace_between(text: str, start: str, end: str, new_block: str) -> str:
    s = text.index(start)
    e = text.index(end, s)
    return text[:s] + new_block + text[e:]


def replace_const_d(text: str, data: object) -> str:
    marker = "const D"
    i = text.index(marker)
    eq = text.index("=", i)
    j = eq + 1
    while text[j].isspace():
        j += 1
    depth = 0
    in_str = False
    esc = False
    end = None
    for k in range(j, len(text)):
        ch = text[k]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
        else:
            if ch == '"':
                in_str = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    end = k
                    break
    if end is None:
        raise ValueError("Failed to locate end of const D object")
    return text[:i] + f"const D = {json_text(data)}" + text[end + 1 :]


def replace_const_DATA(text: str, data: object) -> str:
    marker = "const DATA"
    i = text.index(marker)
    eq = text.index("=", i)
    j = eq + 1
    while j < len(text) and text[j].isspace():
        j += 1
    depth = 0
    in_str = False
    esc = False
    end = None
    for k in range(j, len(text)):
        ch = text[k]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
        else:
            if ch == '"':
                in_str = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    end = k
                    break
    if end is None:
        raise ValueError("Failed to locate end of const DATA object")
    return text[:i] + f"const DATA = {json_text(data)}" + text[end + 1 :]


def parse_wind_value(value: object) -> float | None:
    nums = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", str(value))]
    if not nums:
        return None
    return sum(nums) / len(nums)


def voyage_group(voyage_id: str) -> str:
    s = str(voyage_id)
    if "-GRM-" in s:
        return "GRM"
    if "-DAS-" in s:
        return "DAS"
    if "-AGI-" in s or "DEBRIS" in s:
        return "AGI"
    return "OTHER"


def cost_bucket(cost_main: str) -> str:
    return {
        "CONTRACT": "Agency/Admin",
        "PORT HANDLING": "Port Charges",
        "AT COST": "Supplies/Waste",
        "CONTRACT_MANPOWER": "Cargo Handling",
        "CONTRACT_EQUPIMENT": "Cargo Handling",
        "OTHERS": "Other",
    }.get(str(cost_main), "Other")


def load_workbook(workbook_path: Path | None = None) -> dict[str, pd.DataFrame]:
    path = workbook_path if workbook_path is not None else WORKBOOK
    return {
        "decklog": pd.read_excel(path, sheet_name="DECKLOG"),
        "voyage": pd.read_excel(path, sheet_name="VOYAGE"),
        "ofco": pd.read_excel(path, sheet_name="OFCO INV"),
    }


def build_voyage_master(voyage_df: pd.DataFrame) -> pd.DataFrame:
    df = voyage_df.copy()
    df["ton"] = pd.to_numeric(df["Delivery Qty.\nin Ton"], errors="coerce").fillna(0.0)
    df["month"] = pd.to_datetime(df["Loading Date"], errors="coerce").dt.strftime("%Y-%m")
    master = (
        df.groupby("Voyage No", dropna=True)
        .agg(ton=("ton", "sum"), month=("month", "min"))
        .reset_index()
    )
    master["grp"] = master["Voyage No"].map(voyage_group)
    return master


def compute_cost_payloads(ofco_df: pd.DataFrame, voyage_master: pd.DataFrame):
    ton_map = voyage_master.set_index("Voyage No")["ton"].to_dict()
    auto_types = {"DIRECT", "PRORATE_APPLIED", "MULTI_PRORATED", "DATE_INFER"}
    manual_types = {"MR_A", "MR_C", "MR_D", "MR_E"}
    amount_pattern = re.compile(r"([A-Z0-9\-]+):(\d+(?:\.\d+)?)")
    ym_pattern = re.compile(r"YM=(\d{4}-\d{2})")

    alloc_full = defaultdict(float)
    alloc_auto = defaultdict(float)
    alloc_direct = defaultdict(float)
    alloc_other = defaultdict(float)
    alloc_ct = defaultdict(lambda: defaultdict(float))
    donut_counts = Counter()
    donut_aed = defaultdict(float)

    for _, row in ofco_df.iterrows():
        aed = float(pd.to_numeric(row["Total AED"], errors="coerce") or 0.0)
        cls_type = str(row.get("CLS_TYPE") or "")
        cls_method = str(row.get("CLS_METHOD") or "")
        resolved = str(row.get("CLS_RESOLVED_VOYAGE") or "")
        note = str(row.get("CLS_NOTE") or "")
        bucket = "MANUAL_REVIEW" if cls_type.startswith("MR_") else cls_type
        donut_counts[bucket] += 1
        donut_aed[bucket] += aed
        if cls_type == "EXCLUDED":
            continue

        targets = []
        shares = []
        if cls_type == "MULTI_PRORATED":
            pairs = [(vid, float(val)) for vid, val in amount_pattern.findall(note) if vid in ton_map]
            total = sum(v for _, v in pairs)
            if total > 0:
                targets = [vid for vid, _ in pairs]
                shares = [val / total for _, val in pairs]
        elif "|" in resolved:
            vids = [x.strip() for x in resolved.split("|") if x.strip() in ton_map]
            if vids:
                tons = [ton_map[v] for v in vids]
                total = sum(tons)
                targets = vids
                shares = [t / total for t in tons] if total > 0 else [1 / len(vids)] * len(vids)
        elif resolved in ton_map:
            targets = [resolved]
            shares = [1.0]
        elif cls_type == "DATE_INFER" or cls_method == "DATE_INFERENCE":
            ym = ""
            match = ym_pattern.search(note)
            if match:
                ym = match.group(1)
            if not ym:
                ym = str(row.get("EFFECTIVE_MONTH") or row.get("YM_FIXED") or "")[:7]
            vids = voyage_master.loc[voyage_master["month"] == ym, "Voyage No"].tolist()
            if vids:
                tons = [ton_map[v] for v in vids]
                total = sum(tons)
                targets = vids
                shares = [t / total for t in tons] if total > 0 else [1 / len(vids)] * len(vids)

        if not targets:
            continue

        ct = cost_bucket(row.get("COST MAIN"))
        for vid, share in zip(targets, shares):
            part = aed * share
            alloc_full[vid] += part
            alloc_ct[vid][ct] += part
            if cls_type == "DIRECT":
                alloc_direct[vid] += part
                alloc_auto[vid] += part
            elif cls_type in auto_types:
                alloc_other[vid] += part
                alloc_auto[vid] += part
            else:
                alloc_other[vid] += part

    full_df = voyage_master[voyage_master["Voyage No"].isin(alloc_full)].copy()
    full_df["total"] = full_df["Voyage No"].map(alloc_full)
    full_df["auto"] = full_df["Voyage No"].map(lambda v: alloc_auto.get(v, 0.0))
    full_df["direct"] = full_df["Voyage No"].map(lambda v: alloc_direct.get(v, 0.0))
    full_df["prorate"] = full_df["Voyage No"].map(lambda v: alloc_other.get(v, 0.0))
    full_df["apt_v4"] = full_df["total"] / full_df["ton"]
    full_df["apt_v3"] = full_df["auto"] / full_df["ton"]
    full_df["apt_d"] = full_df["direct"] / full_df["ton"]

    q1 = float(full_df["apt_v4"].quantile(0.25))
    q3 = float(full_df["apt_v4"].quantile(0.75))
    fence = q3 + 1.5 * (q3 - q1)
    full_df["outlier"] = full_df["apt_v4"] > fence

    total_non_excluded = float(ofco_df.loc[ofco_df["CLS_TYPE"] != "EXCLUDED", "Total AED"].sum())
    unresolved_mask = ofco_df["CLS_TYPE"].isin(["SEPARATE_OPS", "NEW_TYPE"])
    unresolved_rows = int(unresolved_mask.sum())
    unresolved_aed = float(ofco_df.loc[unresolved_mask, "Total AED"].sum())
    manual_before_rows = int(
        ofco_df["CLS_TYPE"].isin(["MR_A", "MR_C", "MR_D", "MR_E", "SEPARATE_OPS", "NEW_TYPE"]).sum()
    )

    bins = [(0, 25), (25, 50), (50, 75), (75, 100), (100, 150), (150, 200), (200, 250), (250, 500), (500, 1000)]
    histogram = [
        {"range": f"{lo}-{hi}", "count": int(((full_df["apt_v4"] >= lo) & (full_df["apt_v4"] < hi)).sum())}
        for lo, hi in bins
    ]
    histogram.append({"range": "1000+", "count": int((full_df["apt_v4"] >= 1000).sum())})

    vg_summary = {}
    for grp, grp_df in full_df.groupby("grp"):
        vg_summary[grp] = {
            "n": int(len(grp_df)),
            "ton": round(float(grp_df["ton"].sum()), 1),
            "aed": round(float(grp_df["total"].sum()), 1),
            "avg_apt": round(float(grp_df["apt_v4"].mean()), 1),
            "med_apt": round(float(grp_df["apt_v4"].median()), 1),
        }

    top15 = []
    for _, row in full_df.sort_values(["apt_v4", "total"], ascending=[False, False]).head(15).iterrows():
        top15.append(
            {
                "id": row["Voyage No"],
                "grp": row["grp"],
                "ton": round(float(row["ton"]), 1),
                "aed": round(float(row["total"]), 1),
                "apt": round(float(row["apt_v4"]), 1),
            }
        )

    cost_types = ["Agency/Admin", "Cargo Handling", "Other", "Port Charges", "Supplies/Waste"]
    ct_data = {ct: round(sum(v.get(ct, 0.0) for v in alloc_ct.values()), 1) for ct in cost_types}
    total_ton = float(full_df["ton"].sum())
    ct_per_ton = {ct: round(ct_data[ct] / total_ton, 1) if total_ton else 0 for ct in cost_types}

    monthly = []
    for month, month_df in full_df.groupby("month"):
        monthly.append(
            {
                "month": month,
                "n_voy": int(len(month_df)),
                "ton": round(float(month_df["ton"].sum()), 1),
                "aed": round(float(month_df["total"].sum()), 1),
                "blended": round(float(month_df["total"].sum() / month_df["ton"].sum()), 1),
                "avg": round(float(month_df["apt_v4"].mean()), 1),
                "med": round(float(month_df["apt_v4"].median()), 1),
            }
        )
    monthly.sort(key=lambda x: x["month"])

    detail = []
    for _, row in full_df.sort_values(["month", "Voyage No"]).iterrows():
        detail.append(
            {
                "id": row["Voyage No"],
                "grp": row["grp"],
                "month": row["month"],
                "ton": round(float(row["ton"]), 1),
                "direct": round(float(row["direct"]), 1),
                "prorate": round(float(row["prorate"]), 1),
                "total": round(float(row["total"]), 1),
                "apt_d": round(float(row["apt_d"]), 1),
                "apt_v3": round(float(row["apt_v3"]), 1),
                "apt_v4": round(float(row["apt_v4"]), 1),
                "outlier": bool(row["outlier"]),
            }
        )

    alloc = {}
    for key in ["DIRECT", "PRORATE_APPLIED", "MULTI_PRORATED", "DATE_INFER", "MANUAL_REVIEW", "SEPARATE_OPS", "NEW_TYPE", "EXCLUDED"]:
        alloc[key] = {"n": int(donut_counts.get(key, 0)), "aed": round(float(donut_aed.get(key, 0.0)), 1)}

    delta = {
        "v3_blended": round(float(full_df["auto"].sum() / total_ton), 1),
        "v4_blended": round(float(full_df["total"].sum() / total_ton), 1),
        "v3_coverage": round(float(full_df["auto"].sum() / total_non_excluded * 100), 1),
        "v4_coverage": round(float(full_df["total"].sum() / total_non_excluded * 100), 1),
        "v3_manual": int(manual_before_rows),
        "v4_manual": int(unresolved_rows),
        "v3_median": round(float(full_df["apt_v3"].median()), 1),
        "v4_median": round(float(full_df["apt_v4"].median()), 1),
        "fence": round(float(fence), 1),
        "n_outlier": int(full_df["outlier"].sum()),
        "q1": round(float(q1), 1),
        "q3": round(float(q3), 1),
        "unresolved_aed": round(unresolved_aed, 1),
    }

    kpi_payload = {
        "scatter": [
            {
                "id": row["Voyage No"],
                "ton": round(float(row["ton"]), 1),
                "aed": round(float(row["total"]), 1),
                "apt": round(float(row["apt_v4"]), 1),
                "apt_d": round(float(row["apt_d"]), 1),
                "apt_v3": round(float(row["apt_v3"]), 1),
                "grp": row["grp"],
                "month": row["month"],
                "outlier": bool(row["outlier"]),
                "direct": round(float(row["direct"]), 1),
                "prorate": round(float(row["prorate"]), 1),
                "lines": 0,
                "pro_items": 0,
            }
            for _, row in full_df.iterrows()
        ],
        "histogram": histogram,
        "vg_summary": vg_summary,
        "monthly": monthly,
        "top15": top15,
        "ct_data": ct_data,
        "ct_per_ton": ct_per_ton,
        "delta": delta,
        "alloc": alloc,
        "detail": detail,
        "total_ton": round(total_ton, 1),
        "total_aed": round(float(full_df["total"].sum()), 1),
        "n_voyages": int(len(full_df)),
    }

    voyage_order = list(full_df.sort_values(["month", "Voyage No"])["Voyage No"])
    voyage_lookup = {vid: i for i, vid in enumerate(voyage_order)}
    ct_lookup = {ct: i for i, ct in enumerate(cost_types)}
    heatmap = []
    alloc_voyages = []
    for vid in voyage_order:
        ct_row = {}
        for ct in cost_types:
            value = round(float(alloc_ct[vid].get(ct, 0.0)), 1)
            ct_row[ct] = value
            if value > 0:
                heatmap.append({"x": ct_lookup[ct], "y": voyage_lookup[vid], "v": value})
        alloc_voyages.append(ct_row)

    monthly_labels = [m["month"] for m in monthly]
    monthly_data = {}
    for ct in cost_types:
        monthly_data[ct] = [
            round(sum(alloc_ct[vid].get(ct, 0.0) for vid in full_df.loc[full_df["month"] == month, "Voyage No"].tolist()), 1)
            for month in monthly_labels
        ]

    multi_list = []
    multi_df = ofco_df.loc[ofco_df["CLS_TYPE"] == "MULTI_PRORATED"].copy()
    for idx, row in multi_df.iterrows():
        candidates = [x.strip() for x in str(row["CLS_NOTE"]).split("|") if ":" in x]
        multi_list.append(
            {
                "idx": int(idx + 1),
                "ym": str(row.get("YM_FIXED") or row.get("EFFECTIVE_MONTH") or row.get("YEAR_MONTH") or "")[:7],
                "aed": round(float(pd.to_numeric(row["Total AED"], errors="coerce") or 0.0), 1),
                "subject": str(row.get("SUBJECT") or "")[:90],
                "method": str(row.get("CLS_METHOD") or ""),
                "conf": float(pd.to_numeric(row.get("CLS_CONFIDENCE"), errors="coerce") or 0.0),
                "candidates": "|".join(part.split(":")[0] for part in candidates),
                "note": str(row.get("CLS_NOTE") or "")[:220],
            }
        )

    voy_kpi = {
        row["Voyage No"]: {
            "ton": round(float(row["ton"]), 1),
            "aed_v4": round(float(row["total"]), 1),
            "aed_per_ton": round(float(row["apt_v4"]), 1),
            "month": row["month"],
        }
        for _, row in full_df.iterrows()
    }

    heatmap_payload = {
        "heatmap": heatmap,
        "voyages": voyage_order,
        "cost_types": cost_types,
        "alloc_voyages": alloc_voyages,
        "monthly_labels": monthly_labels,
        "monthly_data": monthly_data,
        "multi_list": multi_list,
        "voy_kpi": voy_kpi,
        "alloc_donut": {k: {"aed": v["aed"], "count": v["n"]} for k, v in alloc.items()},
        "delta": {
            "v3_resolved_rows": int(sum(donut_counts.get(k, 0) for k in ["DIRECT", "PRORATE_APPLIED", "MULTI_PRORATED", "DATE_INFER"])),
            "v4_resolved_rows": int(sum(donut_counts.get(k, 0) for k in ["DIRECT", "PRORATE_APPLIED", "MULTI_PRORATED", "DATE_INFER", "MANUAL_REVIEW"])),
            "v3_coverage_aed": delta["v3_coverage"],
            "v4_coverage_aed": delta["v4_coverage"],
            "v3_manual": int(manual_before_rows),
            "v4_manual": int(unresolved_rows),
            "v3_blended": delta["v3_blended"],
            "v4_blended": delta["v4_blended"],
            "multi_resolved": int(donut_counts.get("MULTI_PRORATED", 0)),
            "multi_aed": round(float(donut_aed.get("MULTI_PRORATED", 0.0)), 1),
            "excluded_rows": int(donut_counts.get("EXCLUDED", 0)),
            "excluded_aed": round(float(donut_aed.get("EXCLUDED", 0.0)), 1),
        },
        "total_aed": round(float(ofco_df["Total AED"].sum()), 1),
        "total_rows": int(len(ofco_df)),
    }

    aux = {
        "voyages": full_df,
        "delta": delta,
        "alloc": alloc,
        "alloc_ct": alloc_ct,
        "total_non_excluded": total_non_excluded,
        "donut_counts": donut_counts,
        "donut_aed": donut_aed,
        "unresolved_rows": unresolved_rows,
        "unresolved_aed": unresolved_aed,
        "grp_counts": full_df["grp"].value_counts().to_dict(),
    }
    return kpi_payload, heatmap_payload, aux


def compute_prorate_payload(ofco_df: pd.DataFrame, voyage_master: pd.DataFrame) -> dict:
    pr = ofco_df.loc[ofco_df["CLS_TYPE"] == "PRORATE_APPLIED"].copy().reset_index(drop=True)
    ton_map = voyage_master.set_index("Voyage No")["ton"].to_dict()
    month_map = voyage_master.set_index("Voyage No")["month"].to_dict()
    direct_map = (
        ofco_df.loc[ofco_df["CLS_TYPE"] == "DIRECT"]
        .groupby("CLS_RESOLVED_VOYAGE")["Total AED"]
        .sum()
        .to_dict()
    )

    def prorate_cat(row: pd.Series) -> str:
        note = str(row.get("CLS_NOTE") or "").upper()
        ym = str(row.get("YM_FIXED") or row.get("EFFECTIVE_MONTH") or row.get("YEAR_MONTH") or "")[:7]
        if "CORRUPT ID" in note:
            return "CORRUPTED_SHARED"
        if ym in {"2025-05", "2025-07"}:
            return "PERIODIC_COST"
        return "SHARED_ALL"

    pr["cat"] = pr.apply(prorate_cat, axis=1)
    items = []
    add_a = defaultdict(float)
    add_b = defaultdict(float)
    add_c = defaultdict(float)
    affected = set()

    for _, row in pr.iterrows():
        vids = [x.strip() for x in str(row["CLS_RESOLVED_VOYAGE"]).split("|") if x.strip() in ton_map]
        if not vids:
            continue
        ym = str(row.get("YM_FIXED") or row.get("EFFECTIVE_MONTH") or row.get("YEAR_MONTH") or "")[:7]
        tons = [ton_map[v] for v in vids]
        ton_total = sum(tons)
        month_vids = [v for v in vids if month_map.get(v) == ym] or vids
        aed = float(pd.to_numeric(row["Total AED"], errors="coerce") or 0.0)
        for vid, ton in zip(vids, tons):
            affected.add(vid)
            add_a[vid] += aed * (ton / ton_total if ton_total > 0 else 1 / len(vids))
            add_b[vid] += aed / len(vids)
            if vid in month_vids:
                add_c[vid] += aed / len(month_vids)
        items.append(
            {
                "idx": int(row.name),
                "cat": row["cat"],
                "ym": ym,
                "subject": str(row.get("SUBJECT") or "")[:80],
                "cost_main": str(row.get("COST MAIN") or ""),
                "aed": round(aed, 2),
                "n_voy": len(vids),
                "ton_scope": round(ton_total, 1),
            }
        )

    comparison = []
    for voyage_id in sorted(affected, key=lambda v: (month_map.get(v, ""), v)):
        ton = float(ton_map[voyage_id])
        direct_aed = float(direct_map.get(voyage_id, 0.0))
        a = float(add_a.get(voyage_id, 0.0))
        b = float(add_b.get(voyage_id, 0.0))
        c = float(add_c.get(voyage_id, 0.0))
        comparison.append(
            {
                "voyage": voyage_id,
                "short": voyage_id.replace("HVDC-AGI-", "").replace("HVDC-DAS-", "").replace("HVDC-", ""),
                "direct_aed": round(direct_aed, 1),
                "tonnage": round(ton, 1),
                "direct_per_ton": round(direct_aed / ton, 1) if ton else 0,
                "add_A": round(a, 1),
                "add_B": round(b, 1),
                "add_C": round(c, 1),
                "total_A": round(direct_aed + a, 1),
                "total_B": round(direct_aed + b, 1),
                "total_C": round(direct_aed + c, 1),
                "per_ton_A": round((direct_aed + a) / ton, 1) if ton else 0,
                "per_ton_B": round((direct_aed + b) / ton, 1) if ton else 0,
                "per_ton_C": round((direct_aed + c) / ton, 1) if ton else 0,
                "delta_AB": round(a - b, 1),
                "delta_AC": round(a - c, 1),
            }
        )

    def gini(values: list[float]) -> float:
        vals = sorted(v for v in values if v >= 0)
        if not vals:
            return 0.0
        total = sum(vals)
        if total == 0:
            return 0.0
        n = len(vals)
        return sum((2 * i - n - 1) * v for i, v in enumerate(vals, 1)) / (n * total)

    monthly = []
    cmp_df = pd.DataFrame(comparison)
    if not cmp_df.empty:
        for month, grp in cmp_df.assign(month=cmp_df["voyage"].map(month_map)).groupby("month"):
            monthly.append(
                {
                    "month": month,
                    "n_voy": int(len(grp)),
                    "direct": round(float(grp["direct_aed"].sum()), 1),
                    "ton": round(float(grp["tonnage"].sum()), 1),
                    "add_A": round(float(grp["add_A"].sum()), 1),
                    "add_B": round(float(grp["add_B"].sum()), 1),
                    "add_C": round(float(grp["add_C"].sum()), 1),
                }
            )
    monthly.sort(key=lambda x: x["month"])

    summary = {
        "total_prorate_aed": round(float(pr["Total AED"].sum()), 1),
        "n_items": int(len(pr)),
        "n_affected_voyages": int(len(affected)),
        "sum_A": round(sum(item["add_A"] for item in comparison), 1),
        "sum_B": round(sum(item["add_B"] for item in comparison), 1),
        "sum_C": round(sum(item["add_C"] for item in comparison), 1),
        "gini_A": round(gini([item["add_A"] for item in comparison]), 3),
        "gini_B": round(gini([item["add_B"] for item in comparison]), 3),
        "max_delta_AB": round(max(abs(item["delta_AB"]) for item in comparison), 1) if comparison else 0,
        "categories": {
            cat: {
                "n": int((pr["cat"] == cat).sum()),
                "aed": round(float(pr.loc[pr["cat"] == cat, "Total AED"].sum()), 1),
            }
            for cat in ["CORRUPTED_SHARED", "SHARED_ALL", "PERIODIC_COST"]
        },
    }
    return {"items": items, "comparison": comparison, "monthly": monthly, "summary": summary}


def compute_rootcause_payload(decklog_df: pd.DataFrame):
    df = decklog_df.copy()
    df = df[df["DL_VESSEL_FLAG"].fillna("JPT71") == "JPT71"].sort_values("Date").reset_index(drop=True)
    df["fuel"] = pd.to_numeric(df["VLFuel_Consumption"], errors="coerce").fillna(0.0)

    def classify_activity(text: object) -> str:
        t = str(text).lower()
        if "break down" in t or "breakdown" in t or "maintenance" in t or "repair" in t:
            return "MAINTENANCE"
        if "bunker" in t:
            return "BUNKERING"
        load = any(k in t for k in ["commenced loading", "commence loading", "resumed loading", "resume loading", "start loading", "loading opsn", "loading cargo", "load the cargo"])
        disc = any(k in t for k in ["off-loading", "off loading", "off-load", "off load", "discharg"])
        anchor = any(k in t for k in ["at anchor", "anchorage", "drift", "fairway buoy", "waiting for pilot", "small craft anchorage"])
        berth = any(k in t for k in ["a'side", "alongside", "jetty", "berth", "quay", "ro-ro posn", "secured"])
        sail = any(k in t for k in ["underway", "sailaway", "sail away", "casted off", "cast off", "proceeding", "proceed to", "clear nmc", "clear omc", "clear agi", "passing ", "entered nmc", "entering nmc", "entered omc", "entering omc"])
        if load and not disc:
            return "LOADING"
        if disc:
            return "DISCHARGING"
        if anchor and not load:
            return "AT_ANCHOR"
        if berth and not sail and not anchor and not load:
            return "AT_BERTH"
        if sail:
            if "ballast" in t:
                return "SAILING_BALLAST"
            if "laden" in t:
                return "SAILING_LADEN"
            return "SAILING"
        if berth:
            return "AT_BERTH"
        return "OTHER"

    def is_load_start(text: object) -> bool:
        t = str(text).lower()
        return any(k in t for k in ["commenced loading", "commence loading", "resumed loading", "resume loading", "start loading"])

    def norm_port(value: object) -> str:
        t = str(value).upper()
        if "AGI" in t or "ZAKUM" in t or "AL GHALLAN" in t:
            return "AGI_FIELD"
        if "DAS" in t:
            return "DAS_ISLAND"
        if "FREE PORT" in t:
            return "FREE_PORT"
        if "ETI" in t:
            return "ETI"
        if "MW4" in t:
            return "MW4_MUSAFFAH"
        if "MUSAFFAH PORT" in t:
            return "MUSAFFAH"
        if "JOPETWIL" in t or "JPW" in t or "ICAD" in t or "WEST HARBOUR" in t:
            return "JPW_BASE"
        if "MUSAFFAH" in t:
            return "JPW_BASE"
        return "OTHER"

    df["act2"] = df["Activity"].map(classify_activity)
    df["port"] = df["Call_to_Port"].fillna(df["Ops_Area"]).map(norm_port)
    wind_cols = ["Wind_0001", "Wind_0600", "Wind_1200", "Wind_1800"]
    df["wind"] = df[wind_cols].apply(
        lambda row: (
            statistics.mean(values)
            if (values := [v for v in [parse_wind_value(x) for x in row] if v is not None])
            else None
        ),
        axis=1,
    )

    trip_ids = []
    trip_id = 0
    prev_load = False
    for _, row in df.iterrows():
        current_load = is_load_start(row["Activity"])
        if current_load and not prev_load:
            trip_id += 1
        trip_ids.append(max(trip_id, 1))
        prev_load = current_load
    df["trip"] = trip_ids

    base_ports = {"MW4_MUSAFFAH", "JPW_BASE", "MUSAFFAH"}
    trip_rows = []
    for tid, grp in df.groupby("trip"):
        candidates = [p for p in grp["port"] if p not in base_ports]
        dest = Counter(candidates).most_common(1)[0][0] if candidates else grp["port"].iloc[-1]
        sail_mask = grp["act2"].isin(["SAILING", "SAILING_LADEN", "SAILING_BALLAST"])
        trip_rows.append(
            {
                "trip": int(tid),
                "dest": dest,
                "days": int(len(grp)),
                "fuel": float(grp["fuel"].sum()),
                "load_days": int((grp["act2"] == "LOADING").sum()),
                "disc_days": int((grp["act2"] == "DISCHARGING").sum()),
                "sail_days": int(sail_mask.sum()),
                "anchor_days": int((grp["act2"] == "AT_ANCHOR").sum()),
                "load_fuel": float(grp.loc[grp["act2"] == "LOADING", "fuel"].sum()),
                "disc_fuel": float(grp.loc[grp["act2"] == "DISCHARGING", "fuel"].sum()),
                "sail_fuel": float(grp.loc[sail_mask, "fuel"].sum()),
                "anchor_fuel": float(grp.loc[grp["act2"] == "AT_ANCHOR", "fuel"].sum()),
            }
        )

    trip_df = pd.DataFrame(trip_rows)
    routes = []
    for dest, grp in trip_df.groupby("dest"):
        load_days = int(grp["load_days"].sum())
        disc_days = int(grp["disc_days"].sum())
        sail_days = int(grp["sail_days"].sum())
        anchor_days = int(grp["anchor_days"].sum())
        routes.append(
            {
                "dest": dest,
                "trips": int(len(grp)),
                "total_days": int(grp["days"].sum()),
                "load_days": load_days,
                "disc_days": disc_days,
                "sail_days": sail_days,
                "anchor_days": anchor_days,
                "total_fuel": round(float(grp["fuel"].sum()), 1),
                "avg_trip_fuel": round(float(grp["fuel"].mean()), 1),
                "load_fpd": round(float(grp["load_fuel"].sum() / load_days), 1) if load_days else 0,
                "disc_fpd": round(float(grp["disc_fuel"].sum() / disc_days), 1) if disc_days else 0,
                "sail_fpd": round(float(grp["sail_fuel"].sum() / sail_days), 1) if sail_days else 0,
                "anchor_fpd": round(float(grp["anchor_fuel"].sum() / anchor_days), 1) if anchor_days else 0,
            }
        )
    routes.sort(key=lambda x: (-x["trips"], x["dest"]))

    act_order = ["LOADING", "DISCHARGING", "SAILING", "SAILING_LADEN", "SAILING_BALLAST", "AT_ANCHOR", "AT_BERTH", "MAINTENANCE", "BUNKERING", "OTHER"]
    act_fuel = []
    for act in act_order:
        grp = df.loc[df["act2"] == act, "fuel"]
        if len(grp) == 0:
            continue
        act_fuel.append(
            {
                "act": act,
                "days": int(len(grp)),
                "avg": round(float(grp.mean()), 1),
                "med": round(float(grp.median()), 1),
                "total": round(float(grp.sum()), 1),
                "max": round(float(grp.max()), 1),
            }
        )

    port_data = []
    for (port, act), grp in df.groupby(["port", "act2"]):
        port_data.append(
            {
                "port": port,
                "state": act,
                "days": int(len(grp)),
                "avg": round(float(grp["fuel"].mean()), 1),
                "total": round(float(grp["fuel"].sum()), 1),
            }
        )

    handle = []
    for load_days, grp in trip_df.groupby("load_days"):
        handle.append(
            {
                "load_days": int(load_days),
                "trips": int(len(grp)),
                "avg_total_fuel": round(float(grp["fuel"].mean()), 1),
                "avg_load_fuel": round(float(grp["load_fuel"].mean()), 1),
                "avg_trip_days": round(float(grp["days"].mean()), 1),
            }
        )
    handle.sort(key=lambda x: x["load_days"])

    disc = []
    for disc_days, grp in trip_df.groupby("disc_days"):
        disc.append(
            {
                "disc_days": int(disc_days),
                "trips": int(len(grp)),
                "avg_total_fuel": round(float(grp["fuel"].mean()), 1),
                "avg_disc_fuel": round(float(grp["disc_fuel"].mean()), 1),
            }
        )
    disc.sort(key=lambda x: x["disc_days"])

    wind = []
    wind_buckets = [
        ("Light(<8)", lambda v: v < 8),
        ("Moderate(8-12)", lambda v: 8 <= v < 12),
        ("Fresh(12-16)", lambda v: 12 <= v < 16),
        ("Strong(16+)", lambda v: v >= 16),
    ]
    for label, fn in wind_buckets:
        vals = df.loc[df["wind"].apply(lambda v: v is not None and fn(v)), "fuel"]
        wind.append(
            {
                "label": label,
                "days": int(len(vals)),
                "avg": round(float(vals.mean()), 1) if len(vals) else 0,
                "med": round(float(vals.median()), 1) if len(vals) else 0,
            }
        )

    route_lookup = {row["dest"]: row for row in routes}
    load_avg = next((x["avg"] for x in act_fuel if x["act"] == "LOADING"), 0)
    disc_avg = next((x["avg"] for x in act_fuel if x["act"] == "DISCHARGING"), 0)
    sail_vals = [x for x in act_fuel if x["act"] in {"SAILING", "SAILING_LADEN", "SAILING_BALLAST"}]
    sail_avg = round(sum(x["total"] for x in sail_vals) / max(1, sum(x["days"] for x in sail_vals)), 1) if sail_vals else 0
    anchor_avg = next((x["avg"] for x in act_fuel if x["act"] == "AT_ANCHOR"), 0)

    findings = {
        "total_trips": int(len(trip_df)),
        "agi_trips": int(route_lookup.get("AGI_FIELD", {}).get("trips", 0)),
        "das_trips": int(route_lookup.get("DAS_ISLAND", {}).get("trips", 0)),
        "agi_avg_fuel": round(float(route_lookup.get("AGI_FIELD", {}).get("avg_trip_fuel", 0)), 1),
        "das_avg_fuel": round(float(route_lookup.get("DAS_ISLAND", {}).get("avg_trip_fuel", 0)), 1),
        "load_fpd": round(float(load_avg), 1),
        "disc_fpd": round(float(disc_avg), 1),
        "sail_fpd": round(float(sail_avg), 1),
        "anchor_fpd": round(float(anchor_avg), 1),
        "disc_vs_load": round(float(disc_avg / load_avg), 2) if load_avg else 0,
        "anchor_vs_load": round(float(anchor_avg / load_avg), 2) if load_avg else 0,
    }

    stats = {
        "agi_route": route_lookup.get("AGI_FIELD", {}),
        "das_route": route_lookup.get("DAS_ISLAND", {}),
        "max_wind": max(wind, key=lambda x: x["avg"]) if wind else {"label": "-", "avg": 0, "days": 0},
        "main_handle": max(handle, key=lambda x: x["trips"]) if handle else {"load_days": 0, "trips": 0},
        "zero_disc": next((x for x in disc if x["disc_days"] == 0), {"trips": 0, "avg_total_fuel": 0}),
        "anchor_total": next((x["total"] for x in act_fuel if x["act"] == "AT_ANCHOR"), 0),
        "anchor_days": next((x["days"] for x in act_fuel if x["act"] == "AT_ANCHOR"), 0),
        "max_day": max((x["max"] for x in act_fuel), default=0),
        "berth_avg": next((x["avg"] for x in act_fuel if x["act"] == "AT_BERTH"), 0),
    }

    payload = {
        "routes": routes,
        "act_fuel": act_fuel,
        "port_data": port_data,
        "handle": handle,
        "disc": disc,
        "wind": wind,
        "findings": findings,
    }
    return payload, stats


def activity_to_vessel_state(act: str) -> str:
    """Map DECKLOG activity to LADEN/PORT_OPS/BALLAST/UNKNOWN for root HTML port_data."""
    a = str(act).upper()
    if a in ("LOADING", "DISCHARGING"):
        return "LADEN"
    if a in ("AT_BERTH", "MAINTENANCE", "BUNKERING"):
        return "PORT_OPS"
    if a == "SAILING_BALLAST":
        return "BALLAST"
    return "UNKNOWN"


def port_data_for_laden_ballast(payload: dict) -> dict:
    """Build root HTML port_data: map activity→vessel state, then aggregate by (port, state)."""
    aggregated: dict[tuple[str, str], list[float]] = defaultdict(lambda: [0.0, 0.0])  # (days, total)
    for row in payload["port_data"]:
        port = row["port"]
        state = activity_to_vessel_state(row["state"])
        days = float(row["days"])
        total = float(row["total"])
        key = (port, state)
        aggregated[key][0] += days
        aggregated[key][1] += total
    out = []
    for (port, state), (days, total) in sorted(aggregated.items(), key=lambda x: (x[0][0], x[0][1])):
        out.append({
            "port": port,
            "state": state,
            "days": int(round(days)),
            "avg": round(total / days, 1) if days else 0.0,
            "total": round(total, 1),
        })
    return out


def payload_for_laden_ballast(rootcause_payload: dict) -> dict:
    """Copy rootcause payload and replace port_data with (port, state)-aggregated version."""
    out = dict(rootcause_payload)
    out["port_data"] = port_data_for_laden_ballast(rootcause_payload)
    return out


def patch_kpi_dashboard(
    path: Path, payload: dict, aux: dict, *, version: str = "v5.2", workbook_name: str = "JPT-reconciled_v5.2.xlsx"
) -> None:
    text = path.read_text(encoding="utf-8")
    delta = payload["delta"]
    grp_counts = aux["grp_counts"]
    header = (
        '<div class="header">\n'
        f'  <h1>JPT71 Voyage Unit-Cost KPI Dashboard <span class="badge badge-v4">{version} RAW</span></h1>\n'
        f'  <div class="sub">{workbook_name} · {payload["n_voyages"]} Voyages · {fmt_num(payload["total_ton"], 1)} tons · {fmt_int(payload["total_aed"])} AED allocated\n'
        f'    <span class="badge badge-g">{fmt_pct(delta["v4_coverage"], 1)} non-excluded coverage</span>\n'
        "  </div>\n"
        "</div>\n\n"
    )
    delta_bar = (
        '<div class="delta-bar">\n'
        '  <div class="delta-item"><span class="lbl">Auto→Final</span></div>\n'
        f'  <div class="delta-item"><span class="lbl">Blended:</span><span class="up">{delta["v3_blended"]}→{delta["v4_blended"]} AED/ton</span></div>\n'
        f'  <div class="delta-item"><span class="lbl">Median:</span><span class="up">{delta["v3_median"]}→{delta["v4_median"]}</span></div>\n'
        f'  <div class="delta-item"><span class="lbl">Coverage:</span><span class="up">{delta["v3_coverage"]}%→{delta["v4_coverage"]}%</span></div>\n'
        f'  <div class="delta-item"><span class="lbl">Manual:</span><span class="dn">{delta["v3_manual"]}→{delta["v4_manual"]}</span></div>\n'
        f'  <div class="delta-item"><span class="lbl">Outliers:</span><span class="lbl">{delta["n_outlier"]} (&gt;{delta["fence"]} AED/ton)</span></div>\n'
        "</div>\n\n"
    )
    cards = (
        '<div class="cards">\n'
        f'  <div class="card"><div class="lbl">Blended AED/ton</div><div class="val" style="color:var(--cyan)">{delta["v4_blended"]}</div><div class="note">{fmt_int(payload["total_aed"])} / {fmt_num(payload["total_ton"], 1)} ton</div></div>\n'
        f'  <div class="card"><div class="lbl">Median AED/ton</div><div class="val" style="color:var(--accent)">{delta["v4_median"]}</div><div class="note">Q1={delta["q1"]} · Q3={delta["q3"]}</div></div>\n'
        f'  <div class="card"><div class="lbl">Voyages</div><div class="val">{payload["n_voyages"]}</div><div class="note">GRM {grp_counts.get("GRM", 0)} · AGI {grp_counts.get("AGI", 0)} · DAS {grp_counts.get("DAS", 0)}</div></div>\n'
        f'  <div class="card"><div class="lbl">Outliers</div><div class="val" style="color:var(--yellow)">{delta["n_outlier"]}</div><div class="note">&gt;{delta["fence"]} AED/ton (IQR)</div></div>\n'
        f'  <div class="card"><div class="lbl">Total Tonnage</div><div class="val">{fmt_num(payload["total_ton"], 1)}</div><div class="note">{len(payload["monthly"])} active months</div></div>\n'
        f'  <div class="card"><div class="lbl">Coverage</div><div class="val" style="color:var(--green)">{delta["v4_coverage"]}%</div><div class="note">non-excluded AED basis</div></div>\n'
        "</div>\n\n"
    )
    text = re.sub(
        r"<title>.*?</title>",
        f"<title>JPT71 Voyage Unit-Cost KPI Dashboard — {version} RAW</title>",
        text,
        count=1,
        flags=re.S,
    )
    text = replace_between(text, '<div class="header">', '<div class="delta-bar">', header)
    text = replace_between(text, '<div class="delta-bar">', '<div class="tabs">', delta_bar)
    text = replace_between(text, '<div class="cards">', '<div class="chart-row">', cards)
    text = replace_const_d(text, payload)
    path.write_text(text, encoding="utf-8")


def patch_heatmap_dashboard(path: Path, payload: dict, aux: dict) -> None:
    text = path.read_text(encoding="utf-8")
    delta = payload["delta"]
    grp_counts = aux["grp_counts"]
    resolved_aed = sum(v["aed"] for k, v in payload["alloc_donut"].items() if k != "EXCLUDED")
    header = (
        '<div class="header">\n'
        '  <h1>JPT71 OFCO × Voyage Cost Heatmap <span class="badge badge-blue">v5.2 RAW</span></h1>\n'
        f'  <div class="sub">HVDC Project · 1,303 OFCO Lines · {len(payload["voyages"])} allocated Voyages · {fmt_int(payload["total_aed"])} AED\n'
        f'    <span class="badge badge-green">+{delta["multi_resolved"]} MULTI rows</span>\n'
        f'    <span class="badge badge-red">{delta["excluded_rows"]} EXCLUDED rows</span>\n'
        f'    <span class="badge badge-green">{fmt_pct(delta["v4_coverage_aed"], 1)} non-excluded coverage</span>\n'
        "  </div>\n"
        "</div>\n\n"
    )
    delta_bar = (
        '<div class="delta-bar">\n'
        '  <div class="delta-item"><span class="label">Auto→Final</span></div>\n'
        f'  <div class="delta-item"><span class="label">Resolved:</span><span class="val up">{delta["v3_resolved_rows"]}→{delta["v4_resolved_rows"]}</span></div>\n'
        f'  <div class="delta-item"><span class="label">Coverage:</span><span class="val up">{delta["v3_coverage_aed"]}%→{delta["v4_coverage_aed"]}%</span></div>\n'
        f'  <div class="delta-item"><span class="label">Manual:</span><span class="val down">{delta["v3_manual"]}→{delta["v4_manual"]}</span></div>\n'
        f'  <div class="delta-item"><span class="label">Blended:</span><span class="val up">{delta["v3_blended"]}→{delta["v4_blended"]} AED/ton</span></div>\n'
        f'  <div class="delta-item"><span class="label">Excluded:</span><span class="val down">{fmt_int(delta["excluded_aed"])} AED</span></div>\n'
        "</div>\n\n"
    )
    cards = (
        '<div class="cards">\n'
        f'  <div class="card"><div class="lbl">Total Voyages</div><div class="val">{len(payload["voyages"])}</div><div class="note">GRM {grp_counts.get("GRM", 0)} · AGI {grp_counts.get("AGI", 0)} · DAS {grp_counts.get("DAS", 0)}</div></div>\n'
        f'  <div class="card"><div class="lbl">Resolved AED</div><div class="val" style="color:var(--green)">{fmt_int(resolved_aed)}</div><div class="note">{delta["v4_coverage_aed"]}% of non-excluded</div></div>\n'
        f'  <div class="card"><div class="lbl">Manual / Unlinked</div><div class="val" style="color:var(--red)">{aux["unresolved_rows"]}</div><div class="note">{fmt_int(aux["unresolved_aed"])} AED remaining</div></div>\n'
        f'  <div class="card"><div class="lbl">Blended AED/ton</div><div class="val" style="color:var(--cyan)">{delta["v4_blended"]}</div><div class="note">auto {delta["v3_blended"]} → final {delta["v4_blended"]}</div></div>\n'
        f'  <div class="card"><div class="lbl">Cost Types</div><div class="val">{len(payload["cost_types"])}</div><div class="note">Agency·Cargo·Other·Port·Supply</div></div>\n'
        "</div>\n\n"
    )
    text = re.sub(r"<title>.*?</title>", "<title>JPT71 OFCO × Voyage Heatmap — v5.2 RAW</title>", text, count=1, flags=re.S)
    text = replace_between(text, '<div class="header">', '<div class="delta-bar">', header)
    text = replace_between(text, '<div class="delta-bar">', '<div class="tabs">', delta_bar)
    text = replace_between(text, '<div class="cards">', '<div class="legend-row">', cards)
    text = re.sub(r'<div class="tab" onclick="showTab\(3\)">MULTI_PRORATED \(\d+\)</div>', f'<div class="tab" onclick="showTab(3)">MULTI_PRORATED ({len(payload["multi_list"])})</div>', text, count=1)
    text = re.sub(r'<div class="heatmap-title">.*?</div>', f'<div class="heatmap-title">Voyage × Cost Type Heatmap (AED) — {len(payload["voyages"])} Voyages · {len(payload["cost_types"])} Cost Types</div>', text, count=1)
    text = replace_const_d(text, payload)
    path.write_text(text, encoding="utf-8")


def patch_prorate_dashboard(path: Path, payload: dict) -> None:
    text = path.read_text(encoding="utf-8")
    s = payload["summary"]
    cats = s["categories"]
    header = (
        '<div class="hdr">\n'
        f'    <h1>PRORATE Options Comparison — {s["n_items"]}건 / {fmt_int(s["total_prorate_aed"])} AED</h1>\n'
        f'    <div class="sub">JPT-reconciled_v5.2.xlsx · Tonnage proportional vs Equal split vs Month-equal · {s["n_affected_voyages"]} Voyages Affected</div>\n'
        "  </div>\n\n"
    )
    cards = (
        '<div class="kr">\n'
        f'    <div class="k"><div class="lb">Prorate Total</div><div class="vl">{fmt_int(s["total_prorate_aed"])}</div><div class="sm">AED across {s["n_items"]} items</div></div>\n'
        f'    <div class="k"><div class="lb">CORRUPTED_SHARED</div><div class="vl" style="color:var(--red)">{fmt_int(cats["CORRUPTED_SHARED"]["aed"])}</div><div class="sm">{cats["CORRUPTED_SHARED"]["n"]} items</div></div>\n'
        f'    <div class="k"><div class="lb">SHARED_ALL</div><div class="vl" style="color:var(--a)">{fmt_int(cats["SHARED_ALL"]["aed"])}</div><div class="sm">{cats["SHARED_ALL"]["n"]} items</div></div>\n'
        f'    <div class="k"><div class="lb">PERIODIC_COST</div><div class="vl" style="color:var(--c)">{fmt_int(cats["PERIODIC_COST"]["aed"])}</div><div class="sm">{cats["PERIODIC_COST"]["n"]} items</div></div>\n'
        "</div>\n\n"
    )
    text = re.sub(r"<title>.*?</title>", "<title>JPT71 PRORATE Options Comparison — v5.2 RAW</title>", text, count=1, flags=re.S)
    text = replace_between(text, '<div class="hdr">', '  <div class="kr">', header)
    text = replace_between(text, '  <div class="kr">', '  <div class="tabs">', cards)
    text = re.sub(r'>\d+ Prorate Items<', f'>{s["n_items"]} Prorate Items<', text, count=1)
    text = re.sub(r'<h3>\d+ Prorate Source Items</h3>', f'<h3>{s["n_items"]} Prorate Source Items</h3>', text, count=1)
    text = replace_const_d(text, payload)
    path.write_text(text, encoding="utf-8")


def patch_rootcause_dashboard(path: Path, payload: dict, stats: dict) -> None:
    text = path.read_text(encoding="utf-8")
    f = payload["findings"]
    agi = stats["agi_route"]
    das = stats["das_route"]
    handle = stats["main_handle"]
    zero_disc = stats["zero_disc"]
    wind_peak = stats["max_wind"]
    header = (
        '<div class="header">\n'
        '<h1>Laden/Ballast Fuel — Root-Cause Analysis <span class="badge badge-o">v5.2 RAW</span></h1>\n'
        f'<div class="sub">{f["total_trips"]} Trips · EXCLUDED_NON_JPT71 제거 · Route별 · 하역시간별 · Activity별 · 풍속별 연료 분석</div>\n'
        "</div>\n\n"
    )
    cards = (
        '<div class="cards">\n'
        f'<div class="card"><div class="lbl">Total Trips</div><div class="val">{f["total_trips"]}</div><div class="note">DECKLOG trip segmentation</div></div>\n'
        f'<div class="card"><div class="lbl">AGI Field</div><div class="val" style="color:var(--green)">{f["agi_trips"]}</div><div class="note">avg {fmt_num(f["agi_avg_fuel"], 1)} L/trip</div></div>\n'
        f'<div class="card"><div class="lbl">DAS Island</div><div class="val" style="color:var(--accent)">{f["das_trips"]}</div><div class="note">avg {fmt_num(f["das_avg_fuel"], 1)} L/trip</div></div>\n'
        f'<div class="card"><div class="lbl">Disc vs Load</div><div class="val" style="color:var(--red)">{f["disc_vs_load"]}x</div><div class="note">하역 일평균 / 선적 일평균</div></div>\n'
        f'<div class="card"><div class="lbl">Anchor Surge</div><div class="val" style="color:var(--yellow)">{f["anchor_vs_load"]}x</div><div class="note">AT_ANCHOR vs LOADING L/day</div></div>\n'
        "</div>\n"
    )
    replacements = {
        r'<div class="insight">\s*<strong>Key Finding — Route:.*?</div>': '<div class="insight">\n' + f'<strong>Key Finding — Route:</strong> AGI Field 루트({f["agi_trips"]} trips, avg {fmt_num(f["agi_avg_fuel"], 1)}L/trip)가 주력입니다. DAS Island는 {f["das_trips"]} trips로 적지만 avg {fmt_num(f["das_avg_fuel"], 1)}L/trip로 더 무겁습니다. <strong>AGI anchor {fmt_num(agi.get("anchor_fpd", 0), 1)}L/day / DAS anchor {fmt_num(das.get("anchor_fpd", 0), 1)}L/day</strong> 수준이며, v5.2 기준으로 2026-01 제외행 제거 후 route 편차가 정상 범위로 되돌아왔습니다.\n</div>',
        r'<div class="insight">\s*<strong>Key Finding — Activity:.*?</div>': '<div class="insight">\n' + f'<strong>Key Finding — Activity:</strong> AT_ANCHOR가 <strong>{fmt_num(f["anchor_fpd"], 1)} L/day</strong>로 높고, DISCHARGING {fmt_num(f["disc_fpd"], 1)} &gt; LOADING {fmt_num(f["load_fpd"], 1)} 입니다. SAILING은 {fmt_num(f["sail_fpd"], 1)}L/day 수준으로 중간대이며, EXCLUDED ADNOC 225 제거 후 앵커 이상치가 크게 완화됐습니다.\n</div>',
        r'<div class="insight">\s*<strong>Key Finding — 하역시간:.*?</div>': '<div class="insight">\n' + f'<strong>Key Finding — 하역시간:</strong> {handle.get("load_days", 0)}일 선적 Trip({handle.get("trips", 0)}건)이 가장 흔합니다. 하역 0일 Trip은 {zero_disc.get("trips", 0)}건이며 avg {fmt_num(zero_disc.get("avg_total_fuel", 0), 1)}L로, 선적/하역보다 이동·대기 구성의 영향이 더 크다는 점을 보여줍니다.\n</div>',
        r'<div class="insight">\s*<strong>Key Finding — 풍속:.*?</div>': '<div class="insight">\n' + f'<strong>Key Finding — 풍속:</strong> {wind_peak["label"]} 구간이 avg {fmt_num(wind_peak["avg"], 1)}L/day로 가장 높습니다. 강풍 자체보다, 대기 전환과 작업 중단이 연료패턴을 바꾸는 간접 요인으로 보입니다.\n</div>',
    }
    findings_panel = (
        '<div class="panel" id="p4">\n'
        f'<div class="insight" style="border-left-color:var(--red)"><strong>#1 — Anchor waiting remains the largest inefficiency block</strong><br>AT_ANCHOR {fmt_num(f["anchor_fpd"], 1)} L/day, {fmt_int(stats["anchor_total"])}L across {stats["anchor_days"]} days. 항차 자체보다 선석/입항 지연 관리가 더 직접적인 절감 레버입니다.</div>\n'
        f'<div class="insight" style="border-left-color:var(--orange)"><strong>#2 — Discharge still burns more than loading</strong><br>DISCHARGING {fmt_num(f["disc_fpd"], 1)} vs LOADING {fmt_num(f["load_fpd"], 1)} L/day ({f["disc_vs_load"]}x). 하역 장비/밸러스트 조정 구간을 별도 개선 대상으로 보는 것이 맞습니다.</div>\n'
        f'<div class="insight" style="border-left-color:var(--yellow)"><strong>#3 — DAS route is small-volume but fuel-heavy</strong><br>DAS avg {fmt_num(f["das_avg_fuel"], 1)}L/trip vs AGI avg {fmt_num(f["agi_avg_fuel"], 1)}L/trip. 장거리 배선과 anchorage 체류가 겹칠 때 편차가 커집니다.</div>\n'
        f'<div class="insight" style="border-left-color:var(--green)"><strong>#4 — Loading-duration alone does not explain total trip fuel</strong><br>가장 흔한 패턴은 {handle.get("load_days", 0)}일 loading trip이며, total fuel은 대기/항해 구성에 더 민감합니다. Root cause는 작업시간보다 sequence 관리 쪽에 가깝습니다.</div>\n'
        '<div class="insight" style="border-left-color:var(--accent)"><strong>#5 — v5.2 correction normalized January efficiency</strong><br>DL_VESSEL_FLAG 기반 EXCLUDED 제거 후 January anchor/route distortion이 사라졌고, chart scale도 정상 범위로 복원됐습니다.</div>\n\n'
        '<div class="chart-row" style="margin-top:20px">\n'
        '<div class="chart-box full"><h3>Fuel Driver Waterfall — 핵심 원인별 일평균 연료 기여도</h3><canvas id="waterfallChart"></canvas></div>\n'
        '</div>\n'
        '</div>\n\n'
    )
    waterfall_js = "new Chart(document.getElementById('waterfallChart'),{type:'bar',data:{labels:['Baseline\\n(At Berth)','+ Loading','+ Sailing','+ Discharging','+ Anchor Wait','Peak Day'],datasets:[{label:'L/day',data:[%s, %s, %s, %s, %s, %s],backgroundColor:['#6b7280','#22c55e','#3b82f6','#ef4444','#eab308','#f97316']}]},options:{plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>c.raw+' L/day'}}},scales:{x:{ticks:{color:'#94a3b8',font:{size:10}}},y:{ticks:{color:'#94a3b8'},grid:{color:'#1e293b'}}}}});" % (round(stats["berth_avg"], 1), round(f["load_fpd"], 1), round(f["sail_fpd"], 1), round(f["disc_fpd"], 1), round(f["anchor_fpd"], 1), round(stats["max_day"], 1))
    text = re.sub(r"<title>.*?</title>", "<title>JPT71 Fuel Root-Cause Analysis — v5.2 RAW</title>", text, count=1, flags=re.S)
    text = replace_between(text, '<div class="header">', '<div class="tabs">', header)
    text = replace_between(text, '<div class="cards">', '<div class="chart-row">', cards)
    for pattern, repl in replacements.items():
        text = re.sub(pattern, repl, text, count=1, flags=re.S)
    text = replace_between(text, '<div class="panel" id="p4">', '</div>\n\n</div>\n\n<script>', findings_panel)
    text = replace_const_d(text, payload)
    text = re.sub(r"new Chart\(document\.getElementById\('waterfallChart'\).*?\}\}\}\}\);", lambda _: waterfall_js, text, count=1, flags=re.S)
    path.write_text(text, encoding="utf-8")


def patch_rootcause_laden_ballast(path: Path, payload: dict) -> None:
    """Patch root HTML (JPT71 Laden_Ballast Fuel RootCause Analysis.html): replace const DATA, optional v5.3 header/title."""
    text = path.read_text(encoding="utf-8")
    text = replace_const_DATA(text, payload)
    f = payload["findings"]
    text = re.sub(r"<title>.*?</title>", "<title>JPT71 Root-Cause Analysis — v5.3 RAW</title>", text, count=1, flags=re.S)
    header_start = '<header class="header">'
    header_end = "</header>"
    if header_start in text and header_end in text:
        new_header = (
            f'{header_start}\n'
            '      <div class="title-wrap">\n'
            '        <div class="badge-row">\n'
            '          <span class="badge">v5.3 RAW</span>\n'
            '          <span class="badge">EXECUTIVE + QUALITY</span>\n'
            '          <span class="badge">COMPARE / FILTER / EXPORT</span>\n'
            '        </div>\n'
            f'        <h1>JPT71 Laden/Ballast Fuel Root-Cause Analysis</h1>\n'
            f'        <div class="sub">\n'
            f'          JPT-reconciled_v5.3.xlsx · {f["total_trips"]} Trips · Route별 · Activity별 · 풍속별 연료 분석.\n'
            '        </div>\n'
            '      </div>\n'
            '      <div class="badge-row" id="headerBadges"></div>\n'
            f'    {header_end}'
        )
        s = text.index(header_start)
        e = text.index(header_end, s) + len(header_end)
        text = text[:s] + new_header + text[e:]
    path.write_text(text, encoding="utf-8")


def main() -> None:
    sheets = load_workbook()
    voyage_master = build_voyage_master(sheets["voyage"])
    kpi_payload, heatmap_payload, aux = compute_cost_payloads(sheets["ofco"], voyage_master)
    prorate_payload = compute_prorate_payload(sheets["ofco"], voyage_master)
    rootcause_payload, rootcause_stats = compute_rootcause_payload(sheets["decklog"])

    patch_kpi_dashboard(DASH / "JPT71_Voyage_KPI_Dashboard_v4.html", kpi_payload, aux)
    patch_heatmap_dashboard(DASH / "JPT71_Voyage_Cost_Heatmap_v4.html", heatmap_payload, aux)
    patch_prorate_dashboard(DASH / "JPT71_Prorate_Options_Compare.html", prorate_payload)
    patch_rootcause_dashboard(DASH / "JPT71_Fuel_RootCause_Analysis.html", rootcause_payload, rootcause_stats)

    output_dir = ROOT / "output" / "spreadsheet"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "kpi_payload_v52.json").write_text(json.dumps(kpi_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "heatmap_payload_v52.json").write_text(json.dumps(heatmap_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "prorate_payload_v52.json").write_text(json.dumps(prorate_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "rootcause_payload_v52.json").write_text(json.dumps(rootcause_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print("Updated dashboards from JPT-reconciled_v5.2.xlsx")
    print(f"KPI voyages={kpi_payload['n_voyages']} ton={kpi_payload['total_ton']:.1f} aed={kpi_payload['total_aed']:.1f}")
    print(f"Heatmap coverage={heatmap_payload['delta']['v4_coverage_aed']}% multi={heatmap_payload['delta']['multi_resolved']}")
    print(f"Prorate items={prorate_payload['summary']['n_items']} affected={prorate_payload['summary']['n_affected_voyages']}")
    print(f"RootCause trips={rootcause_payload['findings']['total_trips']} agi={rootcause_payload['findings']['agi_trips']} das={rootcause_payload['findings']['das_trips']}")


def main_v53(save_json: bool = True) -> None:
    """Load v5.3 workbook, patch KPI dashboard and root Laden_Ballast HTML."""
    if not WORKBOOK_V53.exists():
        raise FileNotFoundError(f"v5.3 workbook not found: {WORKBOOK_V53}")
    kpi_html = DASH / "JPT71_Voyage_KPI_Dashboard_v4.html"
    if not kpi_html.exists():
        raise FileNotFoundError(f"KPI dashboard not found: {kpi_html}")
    if not ROOT_HTML_LADEN_BALLAST.exists():
        raise FileNotFoundError(f"Root HTML not found: {ROOT_HTML_LADEN_BALLAST}")
    sheets = load_workbook(WORKBOOK_V53)
    voyage_master = build_voyage_master(sheets["voyage"])
    kpi_payload, _heatmap_payload, aux = compute_cost_payloads(sheets["ofco"], voyage_master)
    patch_kpi_dashboard(kpi_html, kpi_payload, aux, version="v5.3", workbook_name="JPT-reconciled_v5.3.xlsx")
    if save_json:
        output_dir = ROOT / "output" / "spreadsheet"
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "kpi_payload_v53.json").write_text(
            json.dumps(kpi_payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    rootcause_payload, _ = compute_rootcause_payload(sheets["decklog"])
    payload = payload_for_laden_ballast(rootcause_payload)
    patch_rootcause_laden_ballast(ROOT_HTML_LADEN_BALLAST, payload)
    if save_json:
        output_dir = ROOT / "output" / "spreadsheet"
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "rootcause_payload_v53.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    f = payload["findings"]
    print("Updated from JPT-reconciled_v5.3.xlsx: KPI dashboard + Laden_Ballast RootCause HTML")
    print(f"KPI voyages={kpi_payload['n_voyages']} ton={kpi_payload['total_ton']:.1f} aed={kpi_payload['total_aed']:.1f}")
    print(f"RootCause trips={f['total_trips']} agi={f['agi_trips']} das={f['das_trips']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync JPT dashboards from reconciled Excel")
    parser.add_argument("--v53", action="store_true", help="Patch KPI dashboard and root Laden_Ballast HTML from v5.3")
    parser.add_argument("--no-json", action="store_true", help="Do not write rootcause_payload_v53.json (with --v53)")
    args = parser.parse_args()
    if args.v53:
        main_v53(save_json=not args.no_json)
    else:
        main()
