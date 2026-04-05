지금까지 진행된 JPT71 종합 리포트 관련 작업을 정리하면 아래와 같습니다.

---

## 1. 예(Go) 뼈대 구현 (plan §1~5, §11)

### ① 기준키 정규화
- **`jpt71_spine.py`**
  - `normalize_ofco_inv()`: OFCO 인보이스 문자열 → `InvoiceDigits`(숫자만, 가변 길이), `InvoiceKey` = `VendorPrefix:Digits`, `InvoiceRaw` 유지
  - `build_invoice_keys_ofco()`: OFCO DataFrame에 InvoiceRaw, InvoiceDigits, VendorPrefix, InvoiceKey 추가
  - `build_invoice_collision_ledger()`: 동일 InvoiceDigits에 서로 다른 InvoiceRaw가 2건 이상이면 **InvoiceKey_Collision** 시트용 원장 생성
- **jpt71 Sheet2**: `load_jpt71_sheet2_with_keys()`로 LoadingDate_base, YearMonth, DeliveryTon_base, InvoiceKey 부여

### ② TagMap v1.1 + decklog 태깅
- **`TagMap_v1.1.csv`**: Keyword, ReasonCode, ProductiveFlag, MatchType, Priority, NegativeKeywords, Category, SeverityWeight
- **`config_jpt71_report.yml`**: tagmap 경로, unknown_rate_warn(0.05), mismatch 임계치
- `load_tagmap_v11()`, `tag_activity()`, `tag_decklog()`, `fact_daily_ops()`로 decklog Activity → ReasonCode/ProductiveFlag
- UNKNOWN 비중 > 5% 시 **TAGMAP_DRIFT_WARN**을 Exception Ledger에 기록

### ③ 4산출물 자동 생성
- **Voyage_Scorecard**: VoyageKey, VoyageDays, DeliveredTon, Cost_Voyage_AED, Cost_Ton_AED (OFCO Voyage No + j71 톤 집계)
- **Leakage_Ledger**: YearMonth, ReasonCode, IdleChargeableDays, NonChargeableDays, LeakageAED, Evidence
- **Exception_Ledger**: Type, Key, Evidence, Severity
- **InvoiceKey_Collision**: 동일 InvoiceDigits·상이 InvoiceRaw (충돌 있을 때만)
- **run_manifest.json**: run_id, inputs(SHA-256), config_version, row_counts, unknown_rate, unmatched_count, collision_count, outputs

---

## 2. 옵션 갭 구현 (plan “Optional gaps” / Option C)

### Dual-Value + 예외
- `_join_j71_ofco_for_dual_value()`: j71·ofco 조인 후 LoadingDate_base, DeliveryTon_base, (ofco에 해당 컬럼 있으면) LoadingDate_src_ofco, DeliveryTon_src, Delta_LoadingDate_days, Delta_Ton_pct, DATE_MISMATCH, TON_MISMATCH_WARN/HIGH 플래그 산출
- `collect_exceptions(..., dual_value_df=...)`에서 위 플래그 기반으로 **DATE_MISMATCH**, **TON_MISMATCH** 행 추가
- Excel에 **Dual_Value** 시트 출력

### VoyageDays in Scorecard
- decklog에 Voyage/Trip/Batch 컬럼이 없을 때: j71 LoadingDate_base와 ofco로 Voyage No 매핑 후, `voyage_window_from_loading_date()`로 Start/End 일자 계산 → **VoyageDays** = (end − start).days + 1 로 Scorecard에 반영

### 추가 Exception 유형
- **UNMATCHED_VOYAGE**: ofco Voyage No 중 j71 InvoiceKey가 하나도 없는 항차
- **DUPLICATE_KEY**: j71 또는 ofco에서 동일 InvoiceKey가 2건 이상인 경우
- **DATE_MISMATCH** / **TON_MISMATCH**: dual_value_df 플래그 기반

### Charter / CostType (P1)
- config에 **charter.source**, **charter.confidence** 추가
- Leakage_Ledger에 **CharterAED_per_day_source**, **CharterAED_per_day_confidence** 컬럼 추가
- **`derive_cost_type_ofco()`**: OFCO amount 컬럼명 키워드로 CostType(CHARTER/FUEL/PORT/OTHER/UNKNOWN) 부여, run_spine에서 ofco_df에 적용

### Data Contract (P2)
- **`DATA_CONTRACT.md`**: 출력 시트(By_Voyage, PriceCenter_Detail, Voyage_Scorecard, Leakage_Ledger, Exception_Ledger, InvoiceKey_Collision, bridge_voyage_month, Dual_Value) 및 run_manifest, TagMap v1.1의 시트/컬럼/타입 정의

### Availability/Utilization 정의 (P0)
- **README_report.md**에 “Availability / Utilization 정의 (P0)” 섹션 추가: CalendarDays, OnHireDays, ProductiveDays, OffHireDays 및 Availability %, Utilization %, Throughput 설명

---

## 3. 파일·실행 요약

| 구분 | 경로/명령 |
|------|-----------|
| 스크립트 | `JPT71/invoice_decklog/jpt71_ops_report.py`, `jpt71_spine.py` |
| 설정 | `config_jpt71_report.yml` |
| TagMap | `TagMap_v1.1.csv` |
| 문서 | `README_report.md`, `DATA_CONTRACT.md` |
| 실행 예시 | `python jpt71_ops_report.py --out out/JPT71_ops_report.md --excel out/JPT71_ops_summary.xlsx --charter-per-day 1` |

Excel 출력 시 By_Voyage, PriceCenter_Detail, Voyage_Scorecard, Leakage_Ledger, Exception_Ledger, InvoiceKey_Collision(있을 때), bridge_voyage_month(있을 때), Dual_Value(있을 때) 시트와 `run_manifest.json`이 생성되도록 되어 있습니다.