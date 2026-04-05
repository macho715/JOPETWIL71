
엑셀 자료를 바탕으로 **JPT71 운영 심층 보고서**를 만들 때 참고할 수 있도록, 보고서 골격과 엑셀 매핑만 정리했습니다. (Ask 모드라 실제 파일 생성/수정은 하지 않습니다.)

---

## 1. 보고서 권장 구조 (온톨로지·KPI 기준)

JPT71 온톨로지의 **Data Sources → Graph Mapping**과 **KPIs & Dash Hooks**에 맞춰 섹션을 나누면 다음과 같이 가져갈 수 있습니다.

| 섹션 | 내용 | 참고 온톨로지/출처 |
|------|------|---------------------|
| **1. Executive Summary** | 기간, 총 Trip 수, 총 적재톤, KPI 요약(OTIF·Envelope 활용률 등) | LoadEvent 시계열, KPIs |
| **2. Vessel & Contract Context** | JPW71 제원, Charter/Amend 요약, Stability Rev.8 핵심 수치(800MT, Deck Strength 10 MT/m², 274 m²) | hvdc:Vessel, CharterParty, StabilityAddendum |
| **3. Trip별 적재 실적 (Load per Trip)** | 항차·일자·품목·톤수, Trip당 합계, Material별 합계 | hvdc:LoadEvent, `deliveredTon`, `hasMaterial`, `onTripNo` |
| **4. 시계열·트렌드** | 기간별 톤수 추이, 품목별 비중, 월/주 단위 집계 | Record/J71, LoadEvent 테이블 |
| **5. Envelope Utilization** | Trip별/기간별 actual vs permissible (Stability 800MT, Deck Strength 등), 초과/여유 | PermissibleLoad, `allowsMaxDeckAggregate` |
| **6. OTIF %** | 계획 대비 On-Time In Full(일자·수량 준수) 비율 | KPIs & Dash Hooks |
| **7. CEP/Vetting & MWS** | CEP 유효기간, Validity Days, MWS Observations Close-out 현황 | hvdc:VettingCEP, 알림(14일/7일) |
| **8. 위험·알림** | CEP 만료 14일 전, Vetting 7일 전, Sea State > limit 시 NO-GO | 알림 규칙 |
| **9. Invoice/비용 요약 (선택)** | INVOICE 시트와 연계 시 항차·서비스·금액 요약 | OFCO ontology 연계 |
| **10. Appendix** | 데이터 출처(엑셀 시트명·기간), 용어(Envelope, SWL, CEP 등) | Glossary |

---

## 2. 엑셀 자료 → 보고서 매핑

엑셀 파일 내용을 직접 보지 못해, **파일명·폴더 구조·온톨로지** 기준으로 추정 매핑만 제안합니다.

| 엑셀 파일 | 용도 추정 | 보고서 반영 방법 |
|-----------|-----------|------------------|
| **decklog.xlsx** | Deck Log(적재/하역 일지) | **Trip별 적재 실적**, 일자·품목·톤수 → LoadEvent 형태로 집계 후 섹션 3·4·5·6 입력 |
| **jpt71.xlsx** | Plan, Cross_Gantt, 일정 | **Trip 번호·일자·계획** → OTIF 비교, Envelope 계획 대비 활용률(섹션 5·6) |
| **INVOICE.xlsx** | 인보이스(항만/서비스 비용) | **비용·서비스 요약**(섹션 9), 필요 시 OFCO 관점(항만·Rotation#) 요약 |

실제로는 아래를 확인한 뒤 위 표를 수정하는 것이 좋습니다.

- **decklog.xlsx**: 컬럼명(예: Date, Trip, Material, Tonnage, Location 등)과 시트 구조
- **jpt71.xlsx**: `Plan` / `Cross_Gantt` 등 시트명과 컬럼(날짜, Trip, 이벤트 유형 등)
- **INVOICE.xlsx**: 인보이스 번호, Rotation#, 금액, 서비스명 등

---

## 3. 보고서 작성 시 필요한 계산·지표

온톨로지 **§11 KPIs & Dash Hooks** 기준으로, 엑셀에서 구할 수 있는 것만 정리하면:

- **Load per Trip (t)**  
  decklog(또는 동일 구조 시트)에서 Trip별 `deliveredTon` 합계.
- **OTIF %**  
  jpt71 Plan/Cross_Gantt의 “계획 일자·수량” vs decklog “실제 일자·수량” 비교 → 준수 건수/전체 건수 비율.
- **Envelope Utilization %**  
  `actual_tonnage / permissible_load` × 100.  
  permissible은 Stability Rev.8(800MT, Deck Strength 10 MT/m², 274 m²)과 현장/기상 제약을 반영할 수 있음(초기에는 800MT만 써도 됨).
- **CEP Validity Days**  
  CEP 만료일 − 보고일 → “D-14” 등 알림용.
- **MWS Observations Close-out**  
  미종결 관측 건수 또는 목록(엑셀에 해당 컬럼/시트가 있다면).

---

## 4. 구현 방식 제안 (스크립트·출력)

- **데이터 추출**  
  `pandas` + `openpyxl`로 `decklog.xlsx`, `jpt71.xlsx`, (선택) `INVOICE.xlsx` 시트 읽기.
- **집계**  
  Trip별/일자별/품목별 톤수, 계획 대비 실적, Envelope 대비 actual 계산.
- **보고서 출력**  
  - **Markdown(.md)** 또는 **HTML**: 1~10 섹션 구조로 작성하면 버전 관리·공유에 유리.
  - **Excel**: “Summary” 시트 + KPI 한 페이지, “Trip_Detail”, “Trend” 시트 등으로 구성하면 운영팀이 익숙하게 볼 수 있음.

기존 `jpt71_unified.py` / `jpt71_refresh_export_final.py`는 **일정·Cross_Gantt 갱신**용이므로, “심층 보고서”는 **별도 스크립트**(예: `jpt71_ops_report.py`)에서 위 집계를 수행하고, 그 결과를 위 섹션 구조에 채우는 방식을 추천합니다.

---

## 5. 다음 단계 (직접 하실 작업)

1. **엑셀 구조 확인**  
   decklog / jpt71 / INVOICE의 **시트명·컬럼명(첫 행)** 을 정리해 두면, “이 컬럼 → 이 지표/이 섹션” 매핑을 구체적으로 짤 수 있습니다.
2. **우선순위 정하기**  
   먼저 **Trip별 적재 실적 + Load per Trip + Envelope Utilization**만 해도 1·3·4·5 섹션은 채울 수 있습니다. OTIF는 jpt71 Plan 구조가 필요하고, CEP/MWS는 해당 데이터가 엑셀에 있을 때 7·8을 채울 수 있습니다.
3. **Agent 모드에서 구현 요청**  
   “엑셀 시트/컬럼 구조는 이렇게다”라고 알려주시면, Agent 모드에서 `jpt71_ops_report.py`(또는 노트북) 초안과 출력 포맷(MD/Excel)을 만들어 드릴 수 있습니다.

원하시면 “Executive Summary만 먼저”, “Envelope Utilization 계산식만”, “OTIF 정의만”처럼 구간별로도 더 쪼개서 설계해 드리겠습니다.


OFCO 인보이스·비용 구조를 반영해, **항차별 인보이스 금액·총비용·유류비·디테일 금액 분석**을 보고서에 넣는 설계만 정리했습니다.

---

## 1. 보고서에 넣을 “비용·금액” 섹션 (추가안)

아래 블록을 기존 “JPT71 운영 심층 보고서”에 **추가 섹션**으로 두면 됩니다.

---

### **신규 섹션: 항차별 인보이스·비용 분석**

| 하위 섹션 | 내용 | 데이터 소스/연결 |
|-----------|------|------------------|
| **항차별 인보이스 금액** | Trip별로 묶인 인보이스 총액 (AED), 건수, 인보이스 번호 목록 | INVOICE 시트 + **Rotation#** 또는 **SAMSUNG REF**(HVDC-AGI-GRM-**J71-xx**)로 Trip 매핑 |
| **항차별 총비용** | Trip당 `Σ(lineAmount)` = 해당 항차 총비용 (AED) | 동일 인보이스 라인 집계 |
| **유류비** | Trip별/전체 유류 관련 금액 (Bunker/MDO/IFO 등) | Subject/설명에서 “fuel/bunker/MDO/IFO/유류” 등 키워드로 필터한 라인 합계 |
| **Price Center별 디테일** | 항차별·전체를 **서비스 유형**으로 쪼갠 금액 | OFCO Price Center 매핑(Subject 패턴) 적용 |

---

## 2. OFCO 기준 디테일 금액 분류 (Price Center)

인보이스 라인을 **Subject(설명)** 또는 기존 Cost/Price Center 규칙으로 아래처럼 나누면 “디테일 금액분석”이 됩니다.

| Price Center (서비스 유형) | 설명 | Subject/키워드 예시 (OFCO v2.5) |
|---------------------------|------|----------------------------------|
| **Channel Transit** | 채널 통과 | SAFEEN, Channel Crossing |
| **Port Dues & Services** | 항만세·항만 서비스 | ADP INV, Port Dues |
| **Port Handling Charge (PHC)** | 항만 하역 등 | PHC, Bulk Handling |
| **Pilotage / Pilot Launch** | 조종·예인 | Pilotage, Pilot Launch |
| **Berthing** | 접안 | Berthing Arrangement |
| **Agency – Cargo Clearance** | 통관 대행 | Cargo Clearance, AF FOR CC |
| **Agency – FW Supply** | 담수 | FW Supply, Arranging FW, 5000 IG FW |
| **Agency – Berthing** | 접안 arrangements | Berthing Arrangement, AF FOR BA |
| **Equipment / Manpower** | 장비·인력 | Equipment Hire, Manpower |
| **Gate Pass / Document** | 게이트패스·문서 | Gate Pass, Doc Processing |
| **유류 (Bunker/Fuel)** | bunker, MDO, IFO | fuel, bunker, MDO, IFO, 유류 (실제 인보이스 용어에 맞게 조정) |
| **기타** | 위에 없는 항목 | 그 외 Subject |

- **항차별**로 위 항목별 합계를 내면 “항차별 디테일 금액분석”이 됩니다.
- **전체 기간** 합계도 동일 구조로 두면 “총비용 + 유류비 + 나머지 디테일”이 한 번에 보입니다.

---

## 3. 항차(Trip)와 인보이스 연결 방법

인보이스에는 **Rotation#** 또는 **SAMSUNG REF**가 있고, JPT71에는 **Trip**이 있으므로 아래 중 하나로 연결합니다.

- **SAMSUNG REF**  
  예: `HVDC-AGI-GRM-J71-50` → `J71` + **50**을 Trip 번호로 해석해 “Trip 50” 등으로 매핑.  
  (실제 규칙은 REF 체계에 맞게 조정)
- **Rotation#**  
  인보이스 라인/메타에 Rotation#이 있으면, 별도 매핑표(Rotation# ↔ Trip)로 Trip을 부여한 뒤 항차별 집계.

엑셀 구조가 **“인보이스 시트 + 라인별 Rotation# 또는 SAMSUNG REF”**만 있으면,  
→ **Trip = f(Rotation# 또는 SAMSUNG REF)** 로 그룹핑한 뒤  
→ **항차별 인보이스 금액, 항차별 총비용, 항차별 유류비, 항차별 Price Center 디테일**을 모두 계산할 수 있습니다.

---

## 4. 보고서용 표/요약 형태 (권장)

구체적으로는 아래처럼 “표 + 요약”으로 두면 됩니다.

- **표 1. 항차별 인보이스·총비용·유류비 요약**

| 항차(Trip) | 인보이스 건수 | 인보이스 번호 | 총비용(AED) | 유류비(AED) | 비유류(AED) | 비고 |
|------------|----------------|----------------|-------------|-------------|-------------|------|
| 1 | 2 | OFCO-xxx, OFCO-yyy | 12,345.00 | 3,000.00 | 9,345.00 | |
| 2 | 1 | OFCO-zzz | 8,200.00 | 2,500.00 | 5,700.00 | |
| **합계** | | | **20,545.00** | **5,500.00** | **15,045.00** | |

- **표 2. 항차별 Price Center 디테일 (예시: Trip 1)**

| Price Center | 금액(AED) | 비고 |
|--------------|-----------|------|
| Channel Transit | 6,182.52 | |
| Port Dues | 1,200.00 | |
| 유류 | 3,000.00 | |
| … | | |
| **소계** | **12,345.00** | |

- **표 3. 전체 기간 Price Center 합계 (디테일 금액분석)**

| Price Center | 금액(AED) | 비중(%) |
|--------------|-----------|---------|
| Channel Transit | xxx | xx% |
| Port Dues | xxx | xx% |
| 유류 | xxx | xx% |
| … | | |
| **총비용** | **xxx** | 100% |

- **요약 문단**  
  “보고 기간 총비용 xxx AED, 그중 유류비 xxx AED(xx%). 항차별로는 Trip N이 최대 xxx AED, …”

---

## 5. 구현 시 필요한 엑셀 컬럼(가정)

- **인보이스 시트**:  
  `NO.`, `SUBJECT`, `Amount (AED)`(또는 라인 금액 컬럼), `INVOICE NUMBER (OFCO)`(또는 인보이스번호), **Rotation#** 또는 **SAMSUNG REF**(또는 항차로 매핑 가능한 키).
- **유류비 식별**:  
  `SUBJECT`(또는 설명 컬럼)에 “fuel/bunker/MDO/IFO/유류” 등이 포함된 라인만 필터해 합계.

실제 시트명·컬럼명이 다르면 위 표의 “데이터 소스”만 그에 맞게 바꾸면 됩니다.

---

## 6. 한 줄 정리

- **항차별**: Trip(또는 Rotation#/SAMSUNG REF)로 인보이스 라인 그룹 → **항차별 인보이스 금액·총비용·유류비** 표와 **Price Center별 디테일** 표를 추가한다.  
- **총비용** = 항차별 총비용 합계 = 전체 인보이스 라인 금액 합계.  
- **유류비** = Subject(또는 설명)로 유류 관련 라인만 골라 항차별·전체 합계.  
- **디테일 금액분석** = OFCO Price Center(Subject 패턴)로 분류한 항차별·전체 표.

이렇게 하면 “항차별 인보이스 금액 대비, 총비용·유류비·디테일 금액분석”이 모두 한 보고서에 들어갑니다.  
실제 INVOICE/decklog 시트의 컬럼명을 알려주시면, 매핑(어떤 컬럼 → Trip, 어떤 컬럼 → 유류비)을 더 구체적으로 적어드릴 수 있습니다.