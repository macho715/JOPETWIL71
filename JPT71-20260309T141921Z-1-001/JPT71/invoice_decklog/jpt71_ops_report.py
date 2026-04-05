# Py3.11+
"""
JPT71 운영 심층 보고서 생성
- OFCO detail, INVOICE, decklog, jpt71 시트 기반
- 항차(Voyage No)별 인보이스 금액, 총비용, 유류비, Price Center 디테일
- Data Spine: Voyage_Scorecard, Leakage_Ledger, Exception_Ledger, run_manifest (plan §1~5, §11)

Usage:
  py jpt71_ops_report.py [--out REPORT.md] [--excel SUMMARY.xlsx] [--spine] [--charter-per-day AED]
  (기본: --out out/JPT71_ops_report.md; --excel 시 4시트+manifest 포함)
"""

import argparse
import os
from pathlib import Path

import pandas as pd

try:
    from jpt71_spine import (
        run_spine,
        write_run_manifest,
        load_config,
        _file_sha256,
    )
except ImportError:
    run_spine = None
    write_run_manifest = None
    load_config = None
    _file_sha256 = None


def _numeric_sum(series):
    return pd.to_numeric(series, errors="coerce").fillna(0).sum()


def load_ofco_detail(path: str) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name="OFCO INVOICE ALL")
    # Voyage No 정규화: 공백/빈값 제거
    df["Voyage No"] = df["Voyage No"].astype(str).str.strip()
    df = df[df["Voyage No"].str.len() > 0]
    return df


def get_amount_columns(df: pd.DataFrame):
    """AMOUNT 접미사 컬럼만 (총액/라인합 제외한 디테일)"""
    amt_cols = [c for c in df.columns if isinstance(c, str) and c.endswith("_AMOUNT")]
    if "Total_Amount_AED" in df.columns:
        amt_cols = [c for c in amt_cols if c != "Total_Amount_AED"]
    return amt_cols


def aggregate_by_voyage(df: pd.DataFrame) -> pd.DataFrame:
    """Voyage No별 총비용, 유류비, 인보이스 건수, 라인 수."""
    total_col = "Total_Amount_AED" if "Total_Amount_AED" in df.columns else None
    diesel_col = "DIESEL_VESSEL_AMOUNT" if "DIESEL_VESSEL_AMOUNT" in df.columns else None
    inv_col = "INVOICE NUMBER" if "INVOICE NUMBER" in df.columns else None

    by_voyage = df.groupby("Voyage No").agg(
        Total_AED=("Total_Amount_AED", lambda s: _numeric_sum(s)) if total_col else ("NO", "count"),
        Invoice_Count=(inv_col or "NO", "nunique") if inv_col else ("NO", "count"),
        Line_Count=("NO", "count"),
    ).reset_index()
    if not total_col:
        by_voyage["Total_AED"] = 0.0

    if diesel_col:
        diesel_sum = df.groupby("Voyage No")[diesel_col].apply(_numeric_sum).reset_index()
        diesel_sum.columns = ["Voyage No", "Diesel_AED"]
        by_voyage = by_voyage.merge(diesel_sum, on="Voyage No", how="left")
    else:
        by_voyage["Diesel_AED"] = 0.0
    by_voyage["Diesel_AED"] = pd.to_numeric(by_voyage["Diesel_AED"], errors="coerce").fillna(0)
    by_voyage["NonFuel_AED"] = by_voyage["Total_AED"] - by_voyage["Diesel_AED"]

    return by_voyage


def build_detail_summary(df: pd.DataFrame) -> pd.DataFrame:
    """전체 기간 Price Center(AMOUNT 컬럼)별 합계"""
    amt_cols = get_amount_columns(df)
    rows = []
    for c in amt_cols:
        s = pd.to_numeric(df[c], errors="coerce").fillna(0)
        total = s.sum()
        if total == 0:
            continue
        name = c.replace("_AMOUNT", "").replace("_", " ")
        rows.append({"Price_Center": name, "Amount_AED": total})
    if not rows:
        return pd.DataFrame(columns=["Price_Center", "Amount_AED", "Pct"])
    detail_df = pd.DataFrame(rows).sort_values("Amount_AED", ascending=False)
    tot = detail_df["Amount_AED"].sum()
    if "Total_Amount_AED" in df.columns:
        tot = pd.to_numeric(df["Total_Amount_AED"], errors="coerce").fillna(0).sum()
    if tot > 0:
        detail_df["Pct"] = (detail_df["Amount_AED"] / tot * 100).round(1)
    else:
        detail_df["Pct"] = 0.0
    return detail_df


def load_invoice_list(path: str) -> pd.DataFrame:
    if not os.path.isfile(path):
        return pd.DataFrame()
    try:
        return pd.read_excel(path, sheet_name=0)
    except Exception:
        return pd.DataFrame()


def load_decklog(path: str) -> pd.DataFrame:
    if not os.path.isfile(path):
        return pd.DataFrame()
    try:
        xl = pd.ExcelFile(path)
        return pd.read_excel(path, sheet_name=xl.sheet_names[0])
    except Exception:
        return pd.DataFrame()


def load_jpt71_sheet2(path: str) -> pd.DataFrame:
    if not os.path.isfile(path):
        return pd.DataFrame()
    try:
        return pd.read_excel(path, sheet_name="Sheet2")
    except Exception:
        return pd.DataFrame()


def write_md_report(
    by_voyage: pd.DataFrame,
    detail_df: pd.DataFrame,
    invoice_df: pd.DataFrame,
    out_path: str,
    data_dir: str,
) -> None:
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    total_aed = by_voyage["Total_AED"].sum()
    total_diesel = by_voyage["Diesel_AED"].sum()

    lines = [
        "# JPT71 운영 심층 보고서 (엑셀 기반)",
        "",
        "## 1. Executive Summary",
        "",
        f"- **데이터 경로**: `{data_dir}`",
        f"- **항차(Voyage) 수**: {len(by_voyage)}",
        f"- **총비용(AED)**: {total_aed:,.2f}",
        f"- **유류비(AED)**: {total_diesel:,.2f} ({100*total_diesel/total_aed:.1f}%)" if total_aed else "- 유류비: -",
        "",
        "## 2. 항차별 인보이스·총비용·유류비",
        "",
        "| 항차(Voyage No) | 인보이스 건수 | 라인 수 | 총비용(AED) | 유류비(AED) | 비유류(AED) |",
        "|-----------------|---------------|---------|-------------|-------------|-------------|",
    ]
    for _, r in by_voyage.iterrows():
        lines.append(
            f"| {r['Voyage No']} | {int(r['Invoice_Count'])} | {int(r['Line_Count'])} | "
            f"{r['Total_AED']:,.2f} | {r['Diesel_AED']:,.2f} | {r['NonFuel_AED']:,.2f} |"
        )
    lines.append(f"| **합계** | | | **{by_voyage['Total_AED'].sum():,.2f}** | **{by_voyage['Diesel_AED'].sum():,.2f}** | **{by_voyage['NonFuel_AED'].sum():,.2f}** |")
    lines.extend(["", "## 3. 전체 기간 Price Center별 디테일 금액", ""])
    if not detail_df.empty:
        lines.append("| Price Center | 금액(AED) | 비중(%) |")
        lines.append("|--------------|-----------|---------|")
        for _, r in detail_df.head(30).iterrows():
            pct = r.get("Pct", 0)
            lines.append(f"| {r['Price_Center']} | {r['Amount_AED']:,.2f} | {pct} |")
    else:
        lines.append("(집계 없음)")
    lines.extend(["", "## 4. 데이터 출처", ""])
    lines.append("- OFCO detail: `ofco detail.xlsx` → OFCO INVOICE ALL")
    lines.append("- INVOICE: `INVOICE.xlsx` → LIST_REV (계약/인보이스 목록)")
    lines.append("- decklog: `decklog.xlsx` → DailyDeckLog (일별 활동)")
    lines.append("- jpt71: `jpt71.xlsx` → Sheet2 (Batch, Delivery Qty, OFCO INVOICE NO)")
    lines.append("")
    Path(out_path).write_text("\n".join(lines), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="JPT71 운영 심층 보고서 생성")
    base = Path(__file__).resolve().parent
    ap.add_argument("--data-dir", default=str(base), help="엑셀 파일 위치")
    ap.add_argument("--out", default=str(base / "out" / "JPT71_ops_report.md"), help="보고서 MD 출력 경로")
    ap.add_argument("--excel", default="", help="요약 엑셀 출력 경로 (선택)")
    ap.add_argument("--spine", action="store_true", help="Data Spine 실행 (Scorecard/Leakage/Exception/Manifest)")
    ap.add_argument("--charter-per-day", type=float, default=0, help="Charter AED/day (Leakage 계산용)")
    ap.add_argument("--config", default="", help="config YAML 경로 (기본: data-dir/config_jpt71_report.yml)")
    args = ap.parse_args()
    data_dir = Path(args.data_dir)
    ofco_path = data_dir / "ofco detail.xlsx"
    if not ofco_path.is_file():
        print(f"Not found: {ofco_path}")
        return 1
    df = load_ofco_detail(str(ofco_path))
    by_voyage = aggregate_by_voyage(df)
    detail_df = build_detail_summary(df)
    invoice_df = load_invoice_list(str(data_dir / "INVOICE.xlsx"))
    out_md = args.out
    write_md_report(by_voyage, detail_df, invoice_df, out_md, str(data_dir))
    print(f"Report written: {out_md}")

    run_spine_result = None
    if run_spine is not None and (args.excel or args.spine):
        config_path = args.config or str(data_dir / "config_jpt71_report.yml")
        run_spine_result = run_spine(str(data_dir), config_path, args.charter_per_day or 1.0)
        if args.spine and not args.excel:
            out_dir = data_dir / "out"
            out_dir.mkdir(parents=True, exist_ok=True)
            excel_path = out_dir / "JPT71_ops_summary.xlsx"
            args.excel = str(excel_path)

    if args.excel:
        Path(args.excel).parent.mkdir(parents=True, exist_ok=True)
        with pd.ExcelWriter(args.excel, engine="openpyxl") as w:
            by_voyage.to_excel(w, sheet_name="By_Voyage", index=False)
            detail_df.to_excel(w, sheet_name="PriceCenter_Detail", index=False)
            if run_spine_result:
                sc = run_spine_result.get("voyage_scorecard")
                if sc is not None and not sc.empty:
                    sc.to_excel(w, sheet_name="Voyage_Scorecard", index=False)
                leak = run_spine_result.get("leakage_ledger")
                if leak is not None and not leak.empty:
                    leak.to_excel(w, sheet_name="Leakage_Ledger", index=False)
                exc = run_spine_result.get("exception_ledger")
                if exc is not None and not exc.empty:
                    exc.to_excel(w, sheet_name="Exception_Ledger", index=False)
                coll = run_spine_result.get("collision_ledger")
                if coll is not None and not coll.empty:
                    coll.to_excel(w, sheet_name="InvoiceKey_Collision", index=False)
                bridge = run_spine_result.get("bridge_voyage_month")
                if bridge is not None and not bridge.empty:
                    bridge.to_excel(w, sheet_name="bridge_voyage_month", index=False)
                dual = run_spine_result.get("dual_value_df")
                if dual is not None and not dual.empty:
                    dual.to_excel(w, sheet_name="Dual_Value", index=False)
        print(f"Excel summary: {args.excel}")

        if run_spine_result and write_run_manifest is not None and load_config is not None and _file_sha256 is not None:
            config = run_spine_result.get("config", {})
            config_ver = config.get("config_version", "1.0")
            inputs = {}
            for name, rel in [("ofco detail.xlsx", "ofco detail.xlsx"), ("decklog.xlsx", "decklog.xlsx"), ("jpt71.xlsx", "jpt71.xlsx")]:
                p = data_dir / rel
                if p.is_file():
                    inputs[name] = _file_sha256(p)
            row_counts = {}
            for key in ("fact_daily_ops", "voyage_scorecard", "leakage_ledger", "exception_ledger"):
                tbl = run_spine_result.get(key)
                row_counts[key] = len(tbl) if tbl is not None and not tbl.empty else 0
            exc_df = run_spine_result.get("exception_ledger")
            unmatched = len(exc_df) if isinstance(exc_df, pd.DataFrame) else 0
            coll_df = run_spine_result.get("collision_ledger")
            collision = len(coll_df) if isinstance(coll_df, pd.DataFrame) else 0
            manifest_path = Path(args.excel).parent / "run_manifest.json"
            write_run_manifest(
                manifest_path,
                inputs=inputs,
                config_version=config_ver,
                row_counts=row_counts,
                unknown_rate=run_spine_result.get("unknown_rate", 0),
                unmatched_count=unmatched,
                collision_count=collision,
                outputs=[str(Path(args.excel).name), "run_manifest.json"],
            )
            print(f"Manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
