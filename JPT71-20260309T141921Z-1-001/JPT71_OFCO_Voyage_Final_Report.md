# JPT71 OFCO × Voyage 매핑 최종 보고서

**프로젝트**: HVDC — Samsung C&T / ADNOC·DSV Partnership
**작성일**: 2026-03-09
**데이터 범위**: 2024-08 ~ 2026-12
**작성**: MACHO-GPT `/logi-master report`

---

## 1. Executive Summary

JPT71 프로젝트의 OFCO 상세 인보이스 1,303건(6,029,909 AED)을 Voyage 단위로 분리·매핑하는 작업을 수행했다. 다단계 매칭 엔진과 SUBJECT 텍스트 마이닝 기반 자동 추론을 통해 **79.1% (1,031건)을 DIRECT 매칭**하였으며, 106개 고유 Voyage에 대해 톤당 단가(AED/ton) KPI를 도출했다.

핵심 결과:

- **DIRECT 매칭**: 1,031건 / 4,049,014 AED (67.1%)
- **PRORATE 대상**: 37건 / 1,071,661 AED (17.8%) — 공유 비용, 배분 필요
- **MANUAL REVIEW 잔여**: 94건 / 453,961 AED (7.5%) — 34건 MULTI_CANDIDATE 포함
- **Blended 단가**: 62.6 AED/ton | Median: 28.4 AED/ton
- **Outlier**: 19 Voyages (>161.7 AED/ton) — AGI 소톤수 항차 집중

---

## 2. 데이터 소스 및 전처리

### 2.1 입력 데이터

| Sheet | Rows | Cols | 설명 |
|---|---|---|---|
| OFCO INV | 1,303 | 130 | OFCO 상세 인보이스 (23개 고유 청구서) |
| VOYAGE | 133 | 9 | Voyage loading 정보 (Loading Date, Tonnage) |
| DECKLOG | 414 | 33 | DSV charter 일일 활동 로그 |
| VOYAGE Rollup | 122 | 11 | Voyage 집계 |
| OFCO Rollup | 147 | 15 | OFCO 집계 |

### 2.2 핵심 전처리 이슈

**Voyage ID 명명 규칙 불일치**: VOYAGE 시트에서 001~046번은 `GRM-71`, 047번 이후는 `GRM-J71`을 사용하나, OFCO 시트는 전체를 `GRM-J71`로 표기한다. 이를 번호 구간별 선택적 정규화로 해결했다.

**Excel 시리얼 날짜 혼재**: INVOICE DATE와 YEAR_MONTH 컬럼에 Excel 시리얼 숫자(45505)와 문자열("2024-08")이 혼재되어 있어 통합 파싱 함수를 적용했다.

**손상된 Voyage ID**: `HVDC-AGI-GRM-HVDC-AGI-GRM-J7` 형태의 이중 접두사 오류(8건, 563K AED)를 감지하고 CORRUPTED_SHARED로 분류했다.

---

## 3. 매칭 엔진 구조

### 3.1 다단계 매칭 파이프라인

```
Step 1: EXACT Match         → 714건 (54.8%)
Step 2: NORM_GRM (J71→71)   → 270건 (20.7%)  [001-046 구간만]
Step 3: NORM_TYPO (AGU→AGI) → 23건  (1.8%)
Step 4: COMPOUND Split      → 24건  (1.8%)   [복합 ID 분리]
Step 5: Special Category    → 272건 (20.9%)  [아래 세부 분류]
```

### 3.2 Special Category 분류

| Category | 건수 | AED | 설명 |
|---|---|---|---|
| BUSHRA | 77 | 273,582 | BUSHRA 선박 별도 운영 |
| NOT_IN_VOYAGE | 58 | 287,145 | VOYAGE 시트에 미등록 |
| BLANK_NO_VOYAGE | 36 | 166,816 | Voyage No 공란 (2025-06 집중) |
| SHARED_ALL | 18 | 321,954 | 전체 공유 비용 (ALL 표기) |
| SPECIAL_CARGO | 19 | 34,602 | JUMBOBAG, DEBRIS 등 특수 화물 |
| PERIODIC_COST | 11 | 186,359 | Agency Fee, YARD 정기 비용 |
| CORRUPTED_SHARED | 8 | 563,349 | 손상 ID → proration 대상 |
| OFF_HIRE | 3 | 8,283 | Off Hire 기간 비용 |
| NEW_TRG_SUBCON | 23 | 50,890 | TRG 하청 신규 유형 |
| NEW_DSV_FP | 10 | 53,827 | DSV-FP 신규 유형 |
| NEW_UPC_MOSB | 6 | 5,554 | UPC-MOSB 신규 유형 |
| BLANK_DATE_INFERABLE | 3 | 28,535 | 공란이나 날짜 추론 가능 |

### 3.3 SUBJECT 텍스트 기반 자동 추론 (Audit Engine)

MANUAL_REVIEW 97건에 대해 5단계 추론 엔진 적용:

| Method | 건수 | AED | Confidence |
|---|---|---|---|
| SUBJECT_REF | 2 | 3,600 | 0.95 (SUBJECT 내 명시 Voyage ID) |
| DATE_PROXIMITY | 45 | 191,291 | 0.40~0.90 (SUBJECT 날짜 → 가장 가까운 Voyage) |
| MULTI_MONTH | 34 | 168,105 | — (동일 월 복수 후보, 미확정) |
| SHARED_SERVICE | 8 | 89,490 | — (Yard/Pass/FW 공유 서비스) |
| UNRESOLVED | 7 | 2,130 | — (정보 부족) |
| EMPTY_SUBJECT | 1 | 27,880 | — (SUBJECT 공란) |

---

## 4. Allocation Type 최종 분포

| Allocation Type | 건수 | 비율 | AED | AED 비율 | 상태 |
|---|---|---|---|---|---|
| **DIRECT** | 1,031 | 79.1% | 4,049,014 | 67.1% | ✅ 확정 |
| PRORATE | 37 | 2.8% | 1,071,661 | 17.8% | ⚠️ 배분 필요 |
| SEPARATE_OPS | 99 | 7.6% | 316,466 | 5.2% | ℹ️ BUSHRA 등 별도 |
| MANUAL_REVIEW | 94 | 7.2% | 453,961 | 7.5% | ❌ 수동 확인 필요 |
| NEW_TYPE | 39 | 3.0% | 110,271 | 1.8% | ℹ️ 신규 유형 |
| DATE_INFER | 3 | 0.2% | 28,535 | 0.5% | ⚠️ 저신뢰 추론 |
| **합계** | **1,303** | **100%** | **6,029,909** | **100%** | |

---

## 5. Voyage별 단가(AED/Ton) KPI 분석

### 5.1 전체 통계

| 지표 | 값 |
|---|---|
| 매칭 Voyage 수 | 106 |
| Total Direct AED | 4,049,014 |
| Total Tonnage | 64,641 ton |
| Blended AED/Ton | 62.6 |
| Average AED/Ton | 85.7 (σ=187.0) |
| Median AED/Ton | 28.4 |
| Q1 / Q3 | 23.4 / 78.7 |
| IQR Upper Fence | 161.7 |
| Outliers (>fence) | 19 voyages |

### 5.2 Vessel Group 비교

| Vessel | Voyages | AED | Tonnage | Avg AED/Ton | 특징 |
|---|---|---|---|---|---|
| **GRM** | 91 | 3,519,754 | 59,191 | 59.0 | 대량 정기 항차, 안정적 단가 |
| **AGI** | 14 | 459,180 | 5,247 | 240.6 | 소톤수 고단가, AT COST 비중 높음 |
| **DAS** | 1 | 70,080 | 202 | 346.6 | 단일 항차, 특수 운영 |

### 5.3 Outlier 분석 (19건)

Outlier의 공통 특징: 소톤수(<300ton) 항차에 AT COST·PORT HANDLING 고정비가 집중되어 단가가 급등한다. AGI-J71 시리즈 (001~003)가 대표적이며, 24~170톤 구간에서 304~1,783 AED/ton을 기록한다. GRM 정규 항차(600~840ton)는 대부분 7~80 AED/ton 범위로 안정적이다.

### 5.4 Cost Type별 톤당 기여

| Cost Type | Total AED | 비중 | Avg per Ton |
|---|---|---|---|
| PORT HANDLING | 1,806,953 | 44.6% | 주요 고정비 |
| AT COST | 1,345,465 | 33.2% | 항차별 변동 큼 |
| CONTRACT | 482,635 | 11.9% | 안정적 |
| OTHERS | 197,845 | 4.9% | 비정기 |
| CONTRACT_MANPOWER | 130,646 | 3.2% | 인력 비용 |
| CONTRACT_EQUIPMENT | 85,470 | 2.1% | 장비 비용 |

---

## 6. 미결 사항 및 Action Items

### 6.1 MULTI_CANDIDATE 34건 (168,105 AED)
동일 월에 복수 Voyage가 존재하여 자동 배정 불가. Voyage별 Loading Date와 실제 작업일 대조를 통한 수동 확인 또는 톤수 기반 비례 배분이 필요하다.

### 6.2 PRORATE 대상 37건 (1,071,661 AED)
SHARED_ALL, CORRUPTED_SHARED, PERIODIC_COST 등 공유 비용의 실제 배분 로직 결정이 필요하다. 방식 옵션: (A) 톤수 비례, (B) 항차 수 균등, (C) 기간(월) 균등.

### 6.3 2025-06월 공백 (36건, 166,816 AED)
VOYAGE 시트에 2025-06월 항차가 미등록되어 있다. 실제 운항 여부 확인 후 Voyage 추가 등록 또는 인접 항차 배분이 필요하다.

### 6.4 신규 유형 확인 (39건, 110,271 AED)
TRG_SUBCON, DSV-FP, UPC-MOSB 등 기존 분류에 없는 신규 Voyage 유형의 정식 등록 및 분류 체계 업데이트가 필요하다.

---

## 7. 산출물 목록

| 파일 | 설명 |
|---|---|
| `JPT71_OFCO_Voyage_Mapping_v2.xlsx` | 전체 매핑 결과 (5 sheets, color-coded) |
| `JPT71_Voyage_Cost_Heatmap.html` | Voyage × Cost Type 히트맵 대시보드 |
| `JPT71_Voyage_KPI_Dashboard.html` | AED/Ton KPI 대시보드 (scatter, trend, table) |
| `JPT71_OFCO_Final_Package.xlsx` | 최종 통합 Excel (본 보고서 동봉) |
| `JPT71_OFCO_Voyage_Final_Report.md` | 본 보고서 |

---

## 8. 방법론 신뢰도

| 항목 | 수준 | 근거 |
|---|---|---|
| EXACT+NORM 매칭 | **HIGH** (95%+) | Voyage ID 직접 대조 |
| SUBJECT_REF 추론 | **HIGH** (0.95) | SUBJECT 내 명시 ID |
| DATE_PROXIMITY | **MEDIUM** (0.40~0.90) | ±15일 이내 매칭 |
| MULTI_MONTH | **LOW** | 복수 후보, 수동 확인 필요 |
| Tonnage 데이터 | **HIGH** | VOYAGE 시트 원본 |
| AED/Ton KPI | **MEDIUM-HIGH** | DIRECT 매칭 기반, PRORATE 미포함 |

---

*End of Report — JPT71 OFCO × Voyage Mapping Analysis v2.0*
