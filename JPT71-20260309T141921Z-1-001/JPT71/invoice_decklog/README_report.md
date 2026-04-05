# JPT71 운영 심층 보고서 (엑셀 기반)

## 실행 방법

```bash
cd JPT71/invoice_decklog
python jpt71_ops_report.py --out out/JPT71_ops_report.md --excel out/JPT71_ops_summary.xlsx
```

- **기본 출력**: `out/JPT71_ops_report.md` (Markdown)
- **선택**: `--excel out/JPT71_ops_summary.xlsx` → 항차별·Price Center별 시트 + **Data Spine 4시트** (Scorecard, Leakage, Exception, Collision) + `run_manifest.json`
- **옵션**: `--spine` (Spine만 실행 시에도 Excel 출력), `--charter-per-day AED` (Leakage 계산용), `--config PATH` (config YAML)

## 입력 파일

| 파일 | 시트 | 용도 |
|------|------|------|
| ofco detail.xlsx | OFCO INVOICE ALL | Voyage No별 총비용, 유류비(DIESEL_VESSEL_AMOUNT), Price Center 디테일 |
| INVOICE.xlsx | LIST_REV (2) | 계약/인보이스 목록 (참조) |
| decklog.xlsx | DailyDeckLog_* | 일별 활동 → TagMap v1.1 태깅, fact_daily_ops, Leakage Ledger |
| jpt71.xlsx | Sheet2 | Batch, Loading Date, Delivery Qty, OFCO INVOICE NO (기준 데이터) |

## Data Spine (plan §1~5, §11 P0/P1/P2)

- **키 정규화**: OFCO 인보이스 → `InvoiceDigits`(숫자만), `InvoiceKey` = VendorPrefix + ":" + Digits. `InvoiceKeyCollisionLedger`(동일 Digits·상이 Raw) 출력.
- **TagMap v1.1**: `TagMap_v1.1.csv` — Keyword, ReasonCode, ProductiveFlag, MatchType, Priority, NegativeKeywords, Category, SeverityWeight. decklog Activity → ReasonCode/ProductiveFlag. UNKNOWN > 5% → TAGMAP_DRIFT_WARN.
- **4산출물**: (1) Voyage_Scorecard (2) Leakage_Ledger (3) Exception_Ledger (4) InvoiceKey_Collision(있을 때). `run_manifest.json`: run_id, inputs(SHA-256), config_version, row_counts, unknown_rate, outputs.

## Excel 시트 구성 (--excel 시)

| 시트 | 내용 |
|------|------|
| By_Voyage | 항차별 인보이스 건수, 총비용, 유류비 |
| PriceCenter_Detail | Price Center별 금액·비중 |
| Voyage_Scorecard | VoyageKey, VoyageDays, DeliveredTon, Cost_Voyage_AED, Cost_Ton_AED |
| Leakage_Ledger | YearMonth, ReasonCode, IdleChargeableDays, NonChargeableDays, LeakageAED, Evidence |
| Exception_Ledger | Type, Key, Evidence, Severity (UNMATCHED_INVOICE, KEY_COLLISION, TAGMAP_DRIFT_WARN 등) |
| InvoiceKey_Collision | 동일 InvoiceDigits·상이 InvoiceRaw (있을 때) |
| bridge_voyage_month | VoyageKey, YearMonth, OpsDays_ratio (decklog에 Voyage/Trip/Batch 있을 때) |
| Dual_Value | LoadingDate_base, DeliveryTon_base, Delta_*, DATE_MISMATCH, TON_MISMATCH_* (j71·ofco 조인) |

## 설정

- `config_jpt71_report.yml`: config_version, tagmap.path, unknown_rate_warn, mismatch 임계치, charter (source, confidence), manifest.
- **Data Contract**: 시트/컬럼/타입 고정은 [DATA_CONTRACT.md](DATA_CONTRACT.md) 참조.

## Availability / Utilization 정의 (P0)

| 용어 | 정의 |
|------|------|
| **CalendarDays** | 달력 일수 (해당 기간 자연일). |
| **OnHireDays** | 계약상 hire 청구 일수. decklog만으로는 불완전 → 출처는 `OnHireDays_source`(CONTRACT/INVOICE/DERIVED/MANUAL) 기록. |
| **ProductiveDays** | TagMap에서 ProductiveFlag=1인 일수 (SAILING, DISCHARGE, LOADING 등). |
| **OffHireDays** | OFFHIRE, CLASS, MAJOR BREAKDOWN 등 계약 제외 일수. |

- **Availability %** = OnHireDays / CalendarDays (가능 시).
- **Utilization %** = ProductiveDays / OnHireDays.
- **Throughput** = TotalTon / OnHireDays 또는 TotalTon / ProductiveDays.

## 보고서 구성 (MD)

1. **Executive Summary** — 총비용, 유류비, 항차 수
2. **항차별 인보이스·총비용·유류비** — Voyage No별 테이블
3. **전체 기간 Price Center별 디테일 금액** — 서비스 유형별 합계·비중
4. **데이터 출처**

## 2026-02 Cost Allocation Rule Update

- Voyage scope for `Voyage_Scorecard` is now anchored by `jpt71.xlsx` `Sheet2` `Voyage No`.
- OFCO costs are scoped to voyages present in jpt71 only.
- Allocation rule:
1. Primary: allocate by `InvoiceKey` using jpt71 `DeliveryTon_base` weight per `(InvoiceKey, Voyage No)`.
2. Fallback: for OFCO rows not matched by `InvoiceKey`, apply direct `Voyage No` cost.
- Sum-preserving invariant:
1. `sum(Voyage_Scorecard.Cost_Voyage_AED)` equals scoped OFCO total (`Total_Amount_AED`) within `1e-6`.
2. Minor floating-point residual is corrected on the max-cost voyage row.
