# JPT71 Report — Data Contract (P2)

시트명·컬럼명·타입 고정 (API 취급). `config_version` 변경 시 이 문서와 run_manifest에 반영.

## Output sheets (Excel)

| Sheet | Column | Type | Description |
|-------|--------|------|-------------|
| **By_Voyage** | Voyage No | string | 항차 식별 |
| | Invoice_Count | int | 인보이스 건수 |
| | Line_Count | int | 라인 수 |
| | Total_AED | float | 총비용 AED |
| | Diesel_AED | float | 유류비 AED |
| | NonFuel_AED | float | 비유류 AED |
| **PriceCenter_Detail** | Price_Center | string | 서비스 유형 |
| | Amount_AED | float | 금액 AED |
| | Pct | float | 비중 % |
| **Voyage_Scorecard** | VoyageKey | string | 항차 키 |
| | VoyageDays | int | 항차 일수 (decklog/VoyageWindow) |
| | DeliveredTon | float | 인도 톤수 (jpt71 기준) |
| | Cost_Voyage_AED | float | 항차당 비용 AED |
| | Cost_Ton_AED | float | 톤당 비용 AED |
| **Leakage_Ledger** | YearMonth | string | YYYY-MM |
| | ReasonCode | string | TagMap 원인 코드 |
| | IdleChargeableDays | float | 청구 가능 유휴 일수 |
| | NonChargeableDays | float | 비청구(off-hire 등) 일수 |
| | LeakageAED | float | 누수 금액 AED |
| | Evidence | string | 근거(DateKey, ReasonCode) |
| | CharterAED_per_day_source | string | CONTRACT/INVOICE/DERIVED/MANUAL |
| | CharterAED_per_day_confidence | float | 0~1 |
| **Exception_Ledger** | Type | string | KEY_COLLISION, UNMATCHED_INVOICE, UNMATCHED_VOYAGE, DUPLICATE_KEY, DATE_MISMATCH, TON_MISMATCH, TAGMAP_DRIFT_WARN |
| | Key | string | 식별 키 |
| | Evidence | string | 파일/시트/행 또는 설명 |
| | Severity | string | INFO, WARN, HIGH, CRITICAL |
| **InvoiceKey_Collision** | InvoiceDigits | string | 숫자만 |
| | InvoiceRaw_List | object | 상이한 원문 목록 |
| | Count | int | 서로 다른 Raw 수 |
| | Severity | string | WARN |
| **bridge_voyage_month** | VoyageKey | string | 항차 키 |
| | YearMonth | string | YYYY-MM |
| | OpsDays_in_month | int | 해당 월 운항 일수 |
| | OpsDays_total | int | 항차 총 운항 일수 |
| | OpsDays_ratio | float | 월 비율 |
| **Dual_Value** | InvoiceKey | string | VendorPrefix:Digits |
| | LoadingDate_base | datetime | jpt71 기준 일자 |
| | DeliveryTon_base | float | jpt71 기준 톤수 |
| | Total_AED | float | ofco 합계 |
| | InvoiceRaw | string | ofco 원문 |
| | LoadingDate_src_ofco | datetime | ofco 일자(있을 때) |
| | DeliveryTon_src | float | ofco 톤(있을 때) |
| | Delta_LoadingDate_days | int | 일자 차이 |
| | Delta_Ton_pct | float | 톤 차이 비율 |
| | DATE_MISMATCH | bool | 일자 불일치 플래그 |
| | TON_MISMATCH_WARN | bool | 톤 불일치 1~3% |
| | TON_MISMATCH_HIGH | bool | 톤 불일치 >10% |

## Run manifest (run_manifest.json)

| Field | Type | Description |
|-------|------|-------------|
| run_id | string | UUID |
| config_version | string | config YAML version |
| inputs | object | filename → SHA-256 |
| row_counts | object | fact_daily_ops, voyage_scorecard, leakage_ledger, exception_ledger |
| unknown_rate | float | TagMap UNKNOWN 비율 |
| unmatched_count | int | Exception Ledger 행 수 |
| collision_count | int | InvoiceKey_Collision 행 수 |
| outputs | string[] | 출력 파일명 |

## TagMap v1.1 (input CSV)

| Column | Type | Description |
|--------|------|-------------|
| Keyword | string | Activity 매칭 키워드 |
| ReasonCode | string | SEA, PORT, WAIT, MAINT, OFFHIRE, … |
| ProductiveFlag | int | 0=Idle/Delay, 1=Productive |
| ConfidenceWeight | float | (optional) |
| MatchType | string | EXACT, CONTAINS, REGEX |
| Priority | int | 낮을수록 우선 |
| NegativeKeywords | string | 제외 조건 (; 구분) |
| Category | string | SEA, PORT, WAIT, MAINT, OFFHIRE, OTHER |
| SeverityWeight | float | 누수 가중치 |

## 2026-02 Cost Allocation Semantics (Spine)

- `By_Voyage.Total_AED` and `Voyage_Scorecard.Cost_Voyage_AED` are generated from a mixed allocation model.
- Scope: only OFCO rows whose `Voyage No` exists in jpt71 `Sheet2`.
- Allocation steps:
1. InvoiceKey-first weighted allocation by jpt71 `DeliveryTon_base` at `(InvoiceKey, Voyage No)` grain.
2. Unmatched InvoiceKey remainder allocated by direct OFCO `Voyage No`.
3. Final total is adjusted to satisfy sum-preserving invariant.
- Invariant: `abs(sum(Cost_Voyage_AED) - scoped_ofco_total) <= 1e-6`.
