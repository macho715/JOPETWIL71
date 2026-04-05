---
title: "HVDC Port Operations - Consolidated"
type: "ontology-design"
domain: "port-operations"
sub-domains: ["ofco-system", "port-agency", "bilingual", "flow-code"]
version: "consolidated-1.1"
date: "2025-11-01"
tags: ["ontology", "hvdc", "port-operations", "flow-code", "flow-code-v35", "khalifa-port", "zayed-port", "consolidated", "ofco", "invoice", "bilingual"]
standards: ["RDF", "OWL", "SHACL", "SPARQL", "JSON-LD"]
status: "active"
source_files: [
  "2_EXT-01-hvdc-ofco-port-ops-en.md",
  "2_EXT-02-hvdc-ofco-port-ops-ko.md",
  "docs/flow_code_v35/FLOW_CODE_V35_ALGORITHM.md"
]
---

# hvdc-port-operations · CONSOLIDATED-07

## Executive Summary

**핵심 한 줄**: OFCO는 '항만 대행(Agency)·항만요금·장비/인력·수배(수자원/게이트패스) 서비스를 묶는 온톨로지 기반 Port Ops & Invoice 허브이며, 문서(Invoice)↔운영(PortCall/ServiceEvent)↔요율(Tariff/PriceCenter)을 Multi-Key Identity Graph로 한 번에 해석합니다. (EN-KR: Any-key in → Resolve → PortCall & Services → Rate & Cost mapping.)
0) Executive Summary (3–5)
• Multi‑Key Identity Graph: 입력 키는 OFCO/SAFEEN/ADP 인보이스번호, Rotation#, Samsung Ref,
hvdc_code 등 아무 키든 OK → 동일 실체(PortCall·Shipment·Invoice) 클러스터로 귀결.
• Ontology‑First: Invoice, InvoiceLine, ServiceEvent(채널크로싱/접안/예인/조종/PHC/장비/인력/수배/게
이트패스/문서수수료), PortCall, Rotation, TariffRef, PriceCenter, CostCenter(A/B/C) 클래스로 정규화.
• 검증 표준: LDG v8.2 ↔ OCR v2.4 연동, KPI(MeanConf≥0.92, TableAcc≥0.98,
NumericIntegrity=1.00), ZERO failsafe.
• 매핑 규칙: Cost Center v2.5 17‑Regex + Subject 패턴("SAFEEN"→Channel Transit, "ADP INV + Port
Dues"→Port Dues, "Cargo Clearance/Arranging FW/BA/5000 IG FW" 등) → Price Center 3‑Way(A/
B/C) 분개.
• 회계 일관성: EA×Rate 합=Amount(±0.01), Σ라인=Invoice Total(±2.00%), 통화/VAT 100.00% 일치,
[EXT] 메타 금액 집계 제외.

---

## Flow Code v3.5 Integration in Port Operations

### Port as Flow Code Origin Point

Port operations represent the **starting point** of the Flow Code classification system. Upon vessel arrival and cargo clearance at **Khalifa Port, Zayed Port, or Jebel Ali Port**, the initial Flow Code determination begins based on the **Final Destination** and **routing plan**.

**Key Flow Code Decision Points at Port:**
1. **Pre Arrival (Flow 0)**: Cargo still on vessel, awaiting port clearance
2. **Post-Clearance Classification**: Port operations team assigns initial Flow Code based on:
   - Final destination (MIR/SHU vs AGI/DAS)
   - Cargo type (container vs bulk)
   - Storage requirements (direct vs warehouse consolidation)
   - MOSB leg necessity (offshore delivery requirement)

### Port-Specific Flow Code Patterns

| Port | Primary Cargo Type | Typical Flow Code | Routing Pattern |
|------|-------------------|-------------------|-----------------|
| **Khalifa Port** | Containers | Flow 1, 2 | Direct or warehouse → Onshore sites |
| **Zayed Port** | Bulk/Heavy | Flow 3, 4 | MOSB staging → Offshore delivery |
| **Jebel Ali** | Mixed (Freezone) | Flow 1, 2, 4 | Varies by customs clearance |

### Flow Code Assignment Process at Port

#### Stage 1: Vessel Arrival (Flow 0)

```
Pre-Arrival Status:
- PortCall initiated with Rotation Number
- Cargo manifest reviewed
- Final destination extracted from Samsung Ref / HVDC Code
- Preliminary Flow Code assessment

Port Operations:
- Channel crossing (SAFEEN service)
- Berthing at designated terminal
- Pilotage and tug services
- Port dues calculation (ADP)

Flow Code = 0 (Pre Arrival) until customs clearance completed
```

#### Stage 2: Customs Clearance & Flow Code Determination

```
Clearance Process:
1. MOIAT customs documentation verified
2. FANR certification (if nuclear materials)
3. Gate pass issued (CICPA)
4. Final destination confirmed

Flow Code Assignment Logic:
IF Final_Location IN ["MIR", "SHU"]:
    IF Requires_Warehouse_Storage:
        Flow Code = 2 (Port → WH → Site)
    ELSE:
        Flow Code = 1 (Port → Site direct)

ELIF Final_Location IN ["AGI", "DAS"]:
    # AGI/DAS offshore → MOSB mandatory
    IF Requires_Warehouse_Storage:
        Flow Code = 4 (Port → WH → MOSB → Site)
    ELSE:
        Flow Code = 3 (Port → MOSB → Site)

ELSE:
    Flow Code = 5 (Awaiting destination assignment)
```

#### Stage 3: Port Departure & Initial Transport

```
Departure from Port:
- Cargo loaded onto trucks/transport
- Port handling charges finalized (OFCO invoice)
- Initial Flow Code recorded in HVDC tracking system
- Next location determined (Warehouse, MOSB, or direct to Site)

Port Operations Complete:
- PortCall status updated to "Departed"
- Flow Code locked for this cargo
- Transit tracking initiated
```

### RDF/OWL Implementation

#### Flow Code Properties for Port Operations

```turtle
@prefix port: <https://hvdc-project.com/ontology/port-operations/> .
@prefix hvdc: <https://hvdc-project.com/ontology/core/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# Port-assigned Flow Code
port:assignedFlowCode a owl:DatatypeProperty ;
    rdfs:label "Port-Assigned Flow Code" ;
    rdfs:comment "Initial Flow Code determined at port clearance" ;
    rdfs:domain port:PortCall ;
    rdfs:range xsd:integer ;
    sh:minInclusive 0 ;
    sh:maxInclusive 5 .

port:flowCodeAssignmentDate a owl:DatatypeProperty ;
    rdfs:label "Flow Code Assignment Date" ;
    rdfs:comment "Date when Flow Code was determined at port" ;
    rdfs:domain port:PortCall ;
    rdfs:range xsd:dateTime .

port:finalDestinationDeclared a owl:DatatypeProperty ;
    rdfs:label "Final Destination Declared" ;
    rdfs:comment "Destination declared at port (MIR/SHU/AGI/DAS)" ;
    rdfs:domain port:PortCall ;
    rdfs:range xsd:string .

port:requiresMOSBTransit a owl:DatatypeProperty ;
    rdfs:label "Requires MOSB Transit" ;
    rdfs:comment "Boolean flag set at port for MOSB requirement" ;
    rdfs:domain port:PortCall ;
    rdfs:range xsd:boolean .

port:portOfEntry a owl:ObjectProperty ;
    rdfs:label "Port of Entry" ;
    rdfs:comment "Entry port (Khalifa/Zayed/Jebel Ali)" ;
    rdfs:domain port:PortCall ;
    rdfs:range port:Port .

# SHACL Constraint: Flow Code Assignment Must Match Destination
port:FlowCodeDestinationConstraint a sh:NodeShape ;
    sh:targetClass port:PortCall ;
    sh:sparql [
        sh:message "AGI/DAS destination must have Flow Code ≥ 3 at port assignment" ;
        sh:select """
            PREFIX port: <https://hvdc-project.com/ontology/port-operations/>
            SELECT $this
            WHERE {
                $this port:finalDestinationDeclared ?dest ;
                      port:assignedFlowCode ?flowCode .
                FILTER(?dest IN ("AGI", "DAS") && ?flowCode < 3)
            }
        """ ;
    ] .
```

#### Instance Example: Port Clearance with Flow Code

```turtle
# Port Call: Container cargo to AGI
port:portcall/ROT-2504053298 a port:PortCall ;
    port:rotationNumber "2504053298" ;
    port:vesselName "MSC MAGNOLIA" ;
    port:portOfEntry port:port/KHALIFA ;
    port:arrivalDate "2024-11-10T08:00:00"^^xsd:dateTime ;
    port:clearanceDate "2024-11-11T14:00:00"^^xsd:dateTime ;
    port:departureDate "2024-11-12T06:00:00"^^xsd:dateTime ;
    port:finalDestinationDeclared "AGI" ;
    port:requiresMOSBTransit true ;
    port:assignedFlowCode 3 ;
    port:flowCodeAssignmentDate "2024-11-11T14:30:00"^^xsd:dateTime ;
    port:flowCodeRationale "AGI offshore destination - MOSB leg mandatory" .

# Port Services (OFCO Invoice Lines)
port:service/CHANNEL-CROSSING-ROT2504053298 a port:ServiceEvent ;
    port:serviceType "Channel Crossing" ;
    port:relatesToPortCall port:portcall/ROT-2504053298 ;
    port:provider "SAFEEN" ;
    port:cost "6621.52"^^xsd:decimal ;
    port:currency "AED" .

port:service/BERTHING-ROT2504053298 a port:ServiceEvent ;
    port:serviceType "Berthing" ;
    port:relatesToPortCall port:portcall/ROT-2504053298 ;
    port:provider "ADP" ;
    port:berth "Khalifa Container Terminal - Berth 3" ;
    port:cost "3500.00"^^xsd:decimal ;
    port:currency "AED" .
```

### SPARQL Queries for Port Operations Flow Code

#### 1. Flow Code Distribution by Port of Entry

```sparql
PREFIX port: <https://hvdc-project.com/ontology/port-operations/>

SELECT ?port ?flowCode (COUNT(?portCall) AS ?count)
WHERE {
    ?portCall a port:PortCall ;
              port:portOfEntry ?portObj ;
              port:assignedFlowCode ?flowCode .
    ?portObj port:portName ?port .
}
GROUP BY ?port ?flowCode
ORDER BY ?port ?flowCode
```

#### 2. AGI/DAS Port Clearance Compliance

```sparql
PREFIX port: <https://hvdc-project.com/ontology/port-operations/>

SELECT ?portCall ?rotationNumber ?destination ?flowCode ?compliant
WHERE {
    ?portCall a port:PortCall ;
              port:rotationNumber ?rotationNumber ;
              port:finalDestinationDeclared ?destination ;
              port:assignedFlowCode ?flowCode .
    FILTER(?destination IN ("AGI", "DAS"))
    BIND(IF(?flowCode >= 3, "PASS", "FAIL") AS ?compliant)
}
ORDER BY ?compliant ?destination
```

#### 3. Port Clearance Time by Flow Code

```sparql
PREFIX port: <https://hvdc-project.com/ontology/port-operations/>

SELECT ?flowCode (AVG(?clearanceTime) AS ?avgClearanceHours)
WHERE {
    ?portCall a port:PortCall ;
              port:assignedFlowCode ?flowCode ;
              port:arrivalDate ?arrival ;
              port:clearanceDate ?clearance .
    BIND((xsd:decimal(?clearance - ?arrival) / 3600) AS ?clearanceTime)
}
GROUP BY ?flowCode
ORDER BY ?flowCode
```

#### 4. MOSB Requirement Accuracy at Port

```sparql
PREFIX port: <https://hvdc-project.com/ontology/port-operations/>

SELECT ?destination (COUNT(?portCall) AS ?total)
       (SUM(?mosbRequired) AS ?mosbCount)
       (100.0 * SUM(?mosbRequired) / COUNT(?portCall) AS ?mosbPercentage)
WHERE {
    ?portCall a port:PortCall ;
              port:finalDestinationDeclared ?destination ;
              port:requiresMOSBTransit ?mosbFlag .
    BIND(IF(?mosbFlag = true, 1, 0) AS ?mosbRequired)
}
GROUP BY ?destination
ORDER BY ?destination
```

### Port Operations KPIs with Flow Code

| KPI Metric | Target | Calculation | Flow Code Relevance |
|------------|--------|-------------|---------------------|
| **Flow Code Assignment Accuracy** | 100% | Correct Flow assignments / Total | Initial classification correctness |
| **AGI/DAS MOSB Flag Accuracy** | 100% | AGI/DAS with MOSB flag / Total AGI/DAS | Offshore routing accuracy |
| **Khalifa Port Flow 1+2 Ratio** | 70-80% | (Flow 1 + Flow 2) / Total Khalifa | Container direct/warehouse routing |
| **Zayed Port Flow 3+4 Ratio** | 80-90% | (Flow 3 + Flow 4) / Total Zayed | Bulk cargo MOSB routing |
| **Average Clearance Time** | <48 hours | Avg(Clearance - Arrival) | Port efficiency |
| **Flow 5 (Unassigned) Rate** | <2% | Flow 5 / Total | Incomplete destination rate |

### Integration with Port Operations Workflow

#### Port Call Lifecycle with Flow Code

```
1. Pre-Arrival (Flow 0)
   - Vessel approaching UAE waters
   - Cargo manifest prepared
   - Samsung Ref / HVDC Code extracted

2. Channel Crossing & Berthing (Flow 0)
   - SAFEEN channel crossing service
   - ADP berthing at terminal
   - Awaiting customs clearance

3. Customs Clearance (Flow Code Assignment)
   - MOIAT documentation verified
   - Final destination confirmed
   - Flow Code assigned (1-5)
   - MOSB requirement flagged (if AGI/DAS)

4. Port Departure (Flow Code Active)
   - Cargo loaded on transport
   - OFCO invoice finalized
   - Flow Code tracked in system
   - Next waypoint determined

5. Post-Port Tracking
   - Flow Code guides routing decisions
   - Warehouse, MOSB, or Site dispatch
   - Flow Code remains fixed through journey
```

---

1) Ontology Core (RDF/OWL)
1.1 주요 클래스
• org:Organization ⟶ ofco:OFCO, adports:ADPorts, safeen:SAFEEN, sct:SCT
• vsl:Vessel / vsl:Voyage / port:PortCall(RotationNo 포함)
• fin:Invoice(source=OFCO), fin:InvoiceLine(최대 4 RatePair)
• ops:ServiceEvent ⟶ ops:ChannelCrossing, ops:Berthing, ops:Pilotage, ops:PilotLaunch,
ops:PHC_BulkHandling, ops:PortDues, ops:Waste, ops:FW_Supply, ops:EquipmentHire,
ops:Manpower, ops:GatePass, ops:DocProcessing
• rate:TariffRef / rate:RatePair(EA,Rate,Amount)
• cost:CostCenterA/B, cost:PriceCenter(A/B/C 3‑Way)
• id:Key ⟶ id:OFCOInvNo, id:SAFEENInvNo, id:ADPInvNo, id:RotationNo, id:SamsungRef,
id:HVDCCode
1.2 핵심 프로퍼티(요지)
• ops:relatesToPortCall(InvoiceLine→PortCall), ops:hasRotationNo, fin:belongsToInvoice,
fin:lineNo(NO.), fin:subject(SUBJECT), fin:currency(AED), fin:vat(0.00/5.00), rate:hasEA_i /
hasRate_i / lineAmount, cost:hasCostCenterA/B / hasPriceCenter,
prov:hasEvidence(file,page,line or ref‑row), id:hasSamsungRef / hasOFCOInvNo /
hasRotationNo / hasHVDCCode.
1

1.3 예시 IRI 정책(요지)
• ofco:invoice/OFCO-INV-0000181
• ofco:line/OFCO-INV-0000181#2015 (NO.=2015)
• ops:portcall/ROT-2504053298 (RotationNo)
• id:samsung/HVDC-AGI-GRM-J71-50
1.4 Mini‑TTL 예시
ofco:invoice/OFCO‑INV‑0000181afin:Invoice;
fin:currency"AED"; fin:total "2799.99"^^xsd:decimal .
ofco:line/OFCO‑INV‑0000181#2002afin:InvoiceLine;
fin:belongsToInvoiceofco:invoice/OFCO‑INV‑0000181;
fin:lineNo2002; fin:subject "SAFEEN … Channel Crossing – Rot# 2503123133" ;
rate:hasEA_12.00; rate:hasRate_1 3091.25 ;
rate:hasEA_22.00; rate:hasRate_2 100.00 ;
rate:hasEA_31.00; rate:hasRate_3 239.00 ;
fin:lineAmount6621.52;
ops:relatesToPortCallops:portcall/ROT‑2503123133;
cost:hasCostCenterAcost:PORT_HANDLING_CHARGE;
cost:hasCostCenterBcost:CHANNEL_TRANSIT_CHARGES;
cost:hasPriceCenter cost:CHANNEL_TRANSIT_CHARGES.
2) Multi‑Key Identity Graph
문제: 단일 키 의존 시 연쇄조인 실패·누락 위험.
해법: id:Key 슈퍼클래스 아래 모든 키를 동등 1급 엔터티로 수집하고, Same‑As/LinkSet으로 실체를 클러스터링.
링크 소스(예) ‑ InvoiceNo(OFCO/SAFEEN/ADP), RotationNo, SamsungRef(HVDC‑AGI‑…), HVDCCode,
Vessel+ETA.
클러스터링 규칙(요지) 1) RotationNo 같고, 날짜 창(±7d)·항만 동일 → 같은 PortCall 후보. 2) SamsungRef
동일 + Subject 패턴 일치 → 같은 Operation Batch. 3) InvoiceNo 묶음 Σ(lineAmount) = Invoice
Total(±2.00%) → 같은 Invoice.
3) SHACL 검증(요약)
• InvoiceLineShape
• rate:hasEA_* × rate:hasRate_* 의 합 = fin:lineAmount ±0.01
• RatePair 최대 4, 결측 시 0.00 채움
• fin:currency = "AED" , fin:vat ∈ {0.00, 5.00}
• prov:hasEvidence 필수
• InvoiceShape
• Σ(InvoiceLine.fin:lineAmount) = fin:total ±2.00%
• [EXT] 라벨 행 금액 집계 제외
2

• PortCallLinkShape
• Subject에 Rot# 있으면 ops:relatesToPortCall 필수
4) Cost/Price Center 매핑 규칙(OFCO 전용)
• Regex v2.5 + Subject 패턴(요지)
• "SAFEEN" → PORT HANDLING CHARGE / CHANNEL TRANSIT CHARGES
• "ADP INV" + "Port Dues" → PORT HANDLING CHARGE / PORT DUES & SERVICES
CHARGES
• "Cargo Clearance" → CONTRACT / AF FOR CC
• "Arranging FW Supply"|"FW Supply" → CONTRACT / AF FOR FW SA
• "Berthing Arrangement" → CONTRACT / AF FOR BA
• "5000 IG FW" → AT COST / AT COST(WATER SUPPLY)
• PRICE CENTER 3‑Way
• A/B: Tariff·키워드 기반(예: Channel Crossing/Port Dues/PHC/Equipment/Manpower)
• C: 수수료/Pass/Document(예: Gate Pass, Doc Processing)
• 규칙: C=0 의심 재검토, A>B 또는 B<0 시 일부 C로 이동, A+B+C=Original_TOTAL, Diff=0.00
5) 파이프라인(운영·검증)
1) Pre‑Prep: 회전/데스큐/샤프닝(DPI<300 경고) 2) OCR v2.4: 레이아웃·토큰 conf 수집 3) Smart Table Parser
2.1: 병합셀 해제·세로표 가로화·단위/통화 분리 4) NLP Refine: NULL/단위 보정, 추정 금지 5) Field Tagger:
Parties/IDs/Incoterms/Rotation/Subject 6) LDG Payload Build: 해시·CrossLinks·Evidence 7) Mapping &
QC: EA×Rate 분해, Cost/Price Center 적용, VAT·통화·합계 검증 8) COST‑GUARD: 기준요율 대비 Δ% 밴드
(PASS/WARN/HIGH/CRITICAL) 9) Report(7+2): Discrepancy Table, Compliance Matrix, DEM/DET Forecast
등
KPI 게이트: MeanConf≥0.92, TableAcc≥0.98, NumericIntegrity=1.00 → 미달 시 ZERO 중단 로그.
6) 데이터 맵(Excel/JSON → Ontology)
Source Field Ontology Property Note
NO. fin:lineNo Row key
SUBJECT fin:subject 패턴 매핑 트리거
SAMSUNG REF id:hasSamsungRef 클러스터 anchor
Channel Crossing fin:lineAmount 또는 금액→Line, EA/
Charges… 등 금액열 rate:hasRate_i / rate:hasEA_i Rate 분해
EA_1..4 rate:hasEA_i 최대 4 쌍
3

Source Field Ontology Property Note
Rate_1..4 rate:hasRate_i 금액=Σ(EA×Rate)
Amount (AED) fin:lineAmount 2 decimals
INVOICE NUMBER (OFCO) id:hasOFCOInvNo Invoice join
Rotation# (Subject 내) ops:hasRotationNo PortCall link
7) Report 표준(7+2)
1) Auto Guard Summary
1.5) Risk Assessment(등급/동인/신뢰도)
2) Discrepancy Table(Δ·허용오차·상태)
3) Compliance Matrix(UAE·근거 링크)
4) Auto‑Fill(Freight/Insurance)
5) Auto Action Hooks(명령·가이드)
6) DEM/DET & Gate‑Out Forecast
7) Evidence & Citations
8) Weak Spot & Improvements
9) Changelog
8) 운영 명령 & 자동화 훅
• 인식/검증: /ocr_basic {file} mode:LDG+ → KPI Pass 확인 → /ocr_table / /ocr_retry
• 코스트가드: /switch_mode COST-GUARD + /logi-master invoice-audit --AEDonly
• 매핑: /mapping run → /run pricecenter map → /mapping update pricecenter
• 규제 체크: /logi-master cert-chk (MOIAT/FANR/TRA)
• 배치: /workflow bulk … → /export excel
9) 운영 규칙(정합성)
• Σ(BB:BI)=BJ ±2.00% / EA 결측 시 EA=1.00 & Rate=Amount 규칙 허용(내 ±2.00%)
• VAT=0.00% 또는 5.00% 외 [MISMATCH]
• [EXT] 메타는 금액 집계 제외, 근거(M열) 필수
• 증거(Evidence): 파일명/페이지/라인 또는 참조시트(Row) 필수 기록
10) 로드맵 (P→Pi→B→O→S + KPI)
• Prepare(2주): 스키마/네임스페이스/IRI 설계, SHACL 초안, 키‑링크 룰 정의
KPI: 스키마 커버리지 ≥90.00%
• Pilot(3주): 1개 인보이스 묶음(예: OFCO‑INV‑0000181) E2E, Δ오차≤2.00%
KPI: ZERO 트리거=0, Evidence 100.00%
4

• Build(4주): CostCenter v2.5·3‑Way 분개·COST‑GUARD 통합
KPI: Pass율≥95.00%
• Operate(지속): 배치 처리 및 리포트(7+2) 자동 발행
KPI: TAT ≤ 0.50h/건
• Scale(지속): SAFEEN/ADP 직조인, PortCall API, DEM/DET 2.0 연계
KPI: 오탐율 ≤ 2.00%
11) 리스크 & 완화
• 키 불일치/누락: Multi‑Key 흡수 + 휴리스틱 윈도우(±7d)
• OCR 품질 저하: KPI 게이트 + /ocr_lowres_fix + ZERO 중단
• 요율 변동: TariffRef 버전드(유효일) + COST‑GUARD Δ% 밴드
12) 부록 — Subject→Cost/PriceCenter 예시(발췌)
Subject 큐 Cost A Cost B PriceCenter
SAFEEN … Channel PORT HANDLING CHANNEL TRANSIT CHANNEL TRANSIT
Crossing CHARGE CHARGES CHARGES
ADP INV … Port PORT HANDLING PORT DUES &
PORT DUES
Dues CHARGE SERVICES CHARGES
Agency fee: Cargo AGENCY FEE FOR CARGO
CONTRACT AF FOR CC
Clearance CLEARANCE
Arranging FW
CONTRACT AF FOR FW SA SUPPLY WATER 5000IG
Supply
Berthing CONTRACT(AF FOR AGENCY FEE FOR BERTHING
CONTRACT
Arrangement BA) ARRANGEMENT
AT COST(WATER
5000 IG FW AT COST SUPPLY WATER 5000IG
SUPPLY)
13) 구현 노트
• 코드베이스: logiontology/ (mapping/validation/reasoning/rdfio/report/pipeline)
• SHACL Runner 옵션, JSON‑LD 컨텍스트 제공, RDFLib + DuckDB로 라인‑레벨 집계 검증.
• 외부 연계: PortCall(AD Ports)·SAFEEN 청구 스냅샷 → TariffRef Evidence로 보관.
끝. (숫자 2 decimals, ISO 날짜 사용, NDA/PII 마스킹 준수)
5

---

## Part 2: OFCO 시스템 (한국어)

### Source

- **Original File**: 2_EXT-02-hvdc-ofco-port-ops-ko.md
- **Version**: 4.1
- **Date**: 2025-01-19
- **Language**: Korean

---

> 핵심 한 줄: **OFCO는 '항만 대행(Agency)·항만요금·장비/인력·수배(수자원/게이트패스) 서비스**를 묶는 **온톨로지 기반 Port Ops & Invoice 허브**이며, 문서(Invoice)↔운영(PortCall/ServiceEvent)↔요율(Tariff/PriceCenter)을 **Multi-Key Identity Graph**로 한 번에 해석합니다. (EN-KR: Any-key in → Resolve → PortCall & Services → Rate & Cost mapping.)

---

## 0) Executive Summary (3–5)
- **Multi‑Key Identity Graph**: 입력 키는 *OFCO/SAFEEN/ADP 인보이스번호, Rotation#, Samsung Ref, hvdc_code* 등 아무 키든 OK → **동일 실체(PortCall·Shipment·Invoice) 클러스터**로 귀결.
- **Ontology‑First**: *Invoice, InvoiceLine, ServiceEvent(채널크로싱/접안/예인/조종/PHC/장비/인력/수배/게이트패스/문서수수료), PortCall, Rotation, TariffRef, PriceCenter, CostCenter(A/B/C)* 클래스로 정규화.
- **검증 표준**: **LDG v8.2 ↔ OCR v2.4** 연동, KPI(MeanConf≥0.92, TableAcc≥0.98, NumericIntegrity=1.00), **ZERO failsafe**.
- **매핑 규칙**: Cost Center v2.5 **17‑Regex** + Subject 패턴("SAFEEN"→Channel Transit, "ADP INV + Port Dues"→Port Dues, "Cargo Clearance/Arranging FW/BA/5000 IG FW" 등) → **Price Center 3‑Way(A/B/C)** 분개.
- **회계 일관성**: EA×Rate 합=Amount(±0.01), Σ라인=Invoice Total(±2.00%), 통화/VAT 100.00% 일치, **[EXT] 메타 금액 집계 제외**.

---

## 1) Ontology Core (RDF/OWL)
### 1.1 주요 클래스
- **org:Organization** ⟶ *ofco:OFCO, adports:ADPorts, safeen:SAFEEN, sct:SCT*
- **vsl:Vessel / vsl:Voyage / port:PortCall** *(RotationNo 포함)*
- **fin:Invoice** *(source=OFCO)*, **fin:InvoiceLine** *(최대 4 RatePair)*
- **ops:ServiceEvent** ⟶ *ops:ChannelCrossing, ops:Berthing, ops:Pilotage, ops:PilotLaunch, ops:PHC_BulkHandling, ops:PortDues, ops:Waste, ops:FW_Supply, ops:EquipmentHire, ops:Manpower, ops:GatePass, ops:DocProcessing*
- **rate:TariffRef / rate:RatePair(EA,Rate,Amount)**
- **cost:CostCenterA/B, cost:PriceCenter** *(A/B/C 3‑Way)*
- **id:Key** ⟶ *id:OFCOInvNo, id:SAFEENInvNo, id:ADPInvNo, id:RotationNo, id:SamsungRef, id:HVDCCode*

### 1.2 핵심 프로퍼티(요지)
- **ops:relatesToPortCall**(InvoiceLine→PortCall), **ops:hasRotationNo**, **fin:belongsToInvoice**, **fin:lineNo**(NO.), **fin:subject**(SUBJECT), **fin:currency**(AED), **fin:vat**(0.00/5.00), **rate:hasEA_i / hasRate_i / lineAmount**, **cost:hasCostCenterA/B / hasPriceCenter**, **prov:hasEvidence**(file,page,line or ref‑row), **id:hasSamsungRef / hasOFCOInvNo / hasRotationNo / hasHVDCCode**.

### 1.3 예시 IRI 정책(요지)
- `ofco:invoice/OFCO-INV-0000181`
- `ofco:line/OFCO-INV-0000181#2015` *(NO.=2015)*
- `ops:portcall/ROT-2504053298` *(RotationNo)*
- `id:samsung/HVDC-AGI-GRM-J71-50`

### 1.4 Mini‑TTL 예시
```ttl
ofco:invoice/OFCO-INV-0000181 a fin:Invoice ;
  fin:currency "AED" ; fin:total "2799.99"^^xsd:decimal .

ofco:line/OFCO-INV-0000181#2002 a fin:InvoiceLine ;
  fin:belongsToInvoice ofco:invoice/OFCO-INV-0000181 ;
  fin:lineNo 2002 ; fin:subject "SAFEEN … Channel Crossing – Rot# 2503123133" ;
  rate:hasEA_1 2.00 ; rate:hasRate_1 3091.25 ;
  rate:hasEA_2 2.00 ; rate:hasRate_2 100.00 ;
  rate:hasEA_3 1.00 ; rate:hasRate_3 239.00 ;
  fin:lineAmount 6621.52 ;
  ops:relatesToPortCall ops:portcall/ROT-2503123133 ;
  cost:hasCostCenterA cost:PORT_HANDLING_CHARGE ;
  cost:hasCostCenterB cost:CHANNEL_TRANSIT_CHARGES ;
  cost:hasPriceCenter  cost:CHANNEL_TRANSIT_CHARGES .
```

---

## 2) Multi‑Key Identity Graph
**문제**: 단일 키 의존 시 연쇄조인 실패·누락 위험.
**해법**: **id:Key** 슈퍼클래스 아래 모든 키를 동등 1급 엔터티로 수집하고, **Same‑As/LinkSet**으로 실체를 클러스터링.

**링크 소스(예)**
- *InvoiceNo(OFCO/SAFEEN/ADP)*, *RotationNo*, *SamsungRef(HVDC‑AGI‑…)*, *HVDCCode*, *Vessel+ETA*.

**클러스터링 규칙(요지)**
1) `RotationNo` 같고, 날짜 창(±7d)·항만 동일 → 같은 **PortCall** 후보.
2) `SamsungRef` 동일 + Subject 패턴 일치 → 같은 **Operation Batch**.
3) `InvoiceNo` 묶음 Σ(lineAmount) = Invoice Total(±2.00%) → 같은 **Invoice**.

---

## 3) SHACL 검증(요약)
- **InvoiceLineShape**
  - `rate:hasEA_* × rate:hasRate_*`의 합 = `fin:lineAmount` ±0.01
  - RatePair 최대 4, 결측 시 0.00 채움
  - `fin:currency = "AED"`, `fin:vat ∈ {0.00, 5.00}`
  - `prov:hasEvidence` **필수**
- **InvoiceShape**
  - Σ(InvoiceLine.fin:lineAmount) = `fin:total` ±2.00%
  - `[EXT]` 라벨 행 금액 **집계 제외**
- **PortCallLinkShape**
  - Subject에 `Rot#` 있으면 `ops:relatesToPortCall` **필수**

---

## 4) Cost/Price Center 매핑 규칙(OFCO 전용)
- **Regex v2.5 + Subject 패턴**(요지)
  - `"SAFEEN"` → `PORT HANDLING CHARGE / CHANNEL TRANSIT CHARGES`
  - `"ADP INV"`+`"Port Dues"` → `PORT HANDLING CHARGE / PORT DUES & SERVICES CHARGES`
  - `"Cargo Clearance"` → `CONTRACT / AF FOR CC`
  - `"Arranging FW Supply"|"FW Supply"` → `CONTRACT / AF FOR FW SA`
  - `"Berthing Arrangement"` → `CONTRACT / AF FOR BA`
  - `"5000 IG FW"` → `AT COST / AT COST(WATER SUPPLY)`

- **PRICE CENTER 3‑Way**
  - **A/B**: Tariff·키워드 기반(예: Channel Crossing/Port Dues/PHC/Equipment/Manpower)
  - **C**: 수수료/Pass/Document(예: Gate Pass, Doc Processing)
  - **규칙**: *C=0 의심 재검토*, *A>B 또는 B<0 시 일부 C로 이동*, *A+B+C=Original_TOTAL, Diff=0.00*

---

## 5) 파이프라인(운영·검증)
1) **Pre‑Prep**: 회전/데스큐/샤프닝(DPI<300 경고)
2) **OCR v2.4**: 레이아웃·토큰 conf 수집
3) **Smart Table Parser 2.1**: 병합셀 해제·세로표 가로화·단위/통화 분리
4) **NLP Refine**: NULL/단위 보정, 추정 금지
5) **Field Tagger**: Parties/IDs/Incoterms/Rotation/Subject
6) **LDG Payload Build**: 해시·CrossLinks·Evidence
7) **Mapping & QC**: EA×Rate 분해, Cost/Price Center 적용, VAT·통화·합계 검증
8) **COST‑GUARD**: 기준요율 대비 Δ% 밴드(PASS/WARN/HIGH/CRITICAL)
9) **Report(7+2)**: Discrepancy Table, Compliance Matrix, DEM/DET Forecast 등

**KPI 게이트**: MeanConf≥0.92, TableAcc≥0.98, NumericIntegrity=1.00 → 미달 시 **ZERO** 중단 로그.

---

## 6) 데이터 맵(Excel/JSON → Ontology)
| Source Field | Ontology Property | Note |
|---|---|---|
| `NO.` | `fin:lineNo` | Row key |
| `SUBJECT` | `fin:subject` | 패턴 매핑 트리거 |
| `SAMSUNG REF` | `id:hasSamsungRef` | 클러스터 anchor |
| `Channel Crossing Charges…` 등 금액열 | `fin:lineAmount` 또는 `rate:hasRate_i`/`rate:hasEA_i` | 금액→Line, EA/Rate 분해 |
| `EA_1..4` | `rate:hasEA_i` | 최대 4 쌍 |
| `Rate_1..4` | `rate:hasRate_i` | 금액=Σ(EA×Rate) |
| `Amount (AED)` | `fin:lineAmount` | 2 decimals |
| `INVOICE NUMBER (OFCO)` | `id:hasOFCOInvNo` | Invoice join |
| `Rotation#`(Subject 내) | `ops:hasRotationNo` | PortCall link |

---

## 7) Report 표준(7+2)
1) **Auto Guard Summary**
1.5) **Risk Assessment**(등급/동인/신뢰도)
2) **Discrepancy Table**(Δ·허용오차·상태)
3) **Compliance Matrix**(UAE·근거 링크)
4) **Auto‑Fill**(Freight/Insurance)
5) **Auto Action Hooks**(명령·가이드)
6) **DEM/DET & Gate‑Out Forecast**
7) **Evidence & Citations**
8) **Weak Spot & Improvements**
9) **Changelog**

---

## 8) 운영 명령 & 자동화 훅
- **인식/검증**: `/ocr_basic {file} mode:LDG+` → KPI Pass 확인 → `/ocr_table`/`/ocr_retry`
- **코스트가드**: `/switch_mode COST-GUARD + /logi-master invoice-audit --AEDonly`
- **매핑**: `/mapping run` → `/run pricecenter map` → `/mapping update pricecenter`
- **규제 체크**: `/logi-master cert-chk`(MOIAT/FANR/TRA)
- **배치**: `/workflow bulk …` → `/export excel`

---

## 9) 운영 규칙(정합성)
- `Σ(BB:BI)=BJ` ±2.00% / EA 결측 시 EA=1.00 & Rate=Amount 규칙 허용(내 ±2.00%)
- VAT=0.00% 또는 5.00% 외 **[MISMATCH]**
- `[EXT]` 메타는 **금액 집계 제외**, 근거(M열) 필수
- **증거(Evidence)**: 파일명/페이지/라인 또는 참조시트(Row) **필수 기록**

---

## 10) 로드맵 (P→Pi→B→O→S + KPI)
- **Prepare(2주)**: 스키마/네임스페이스/IRI 설계, SHACL 초안, 키‑링크 룰 정의
  KPI: 스키마 커버리지 ≥90.00%
- **Pilot(3주)**: 1개 인보이스 묶음(예: OFCO‑INV‑0000181) E2E, Δ오차≤2.00%
  KPI: ZERO 트리거=0, Evidence 100.00%
- **Build(4주)**: CostCenter v2.5·3‑Way 분개·COST‑GUARD 통합
  KPI: Pass율≥95.00%
- **Operate(지속)**: 배치 처리 및 리포트(7+2) 자동 발행
  KPI: TAT ≤ 0.50h/건
- **Scale(지속)**: SAFEEN/ADP 직조인, PortCall API, DEM/DET 2.0 연계
  KPI: 오탐율 ≤ 2.00%

---

## 11) 리스크 & 완화
- **키 불일치/누락**: Multi‑Key 흡수 + 휴리스틱 윈도우(±7d)
- **OCR 품질 저하**: KPI 게이트 + `/ocr_lowres_fix` + ZERO 중단
- **요율 변동**: TariffRef 버전드(유효일) + COST‑GUARD Δ% 밴드

---

## 12) 부록 — Subject→Cost/PriceCenter 예시(발췌)
| Subject 큐 | Cost A | Cost B | PriceCenter |
|---|---|---|
| SAFEEN … Channel Crossing | PORT HANDLING CHARGE | CHANNEL TRANSIT CHARGES | CHANNEL TRANSIT CHARGES |
| ADP INV … Port Dues | PORT HANDLING CHARGE | PORT DUES & SERVICES CHARGES | PORT DUES |
| Agency fee: Cargo Clearance | CONTRACT | AF FOR CC | AGENCY FEE FOR CARGO CLEARANCE |
| Arranging FW Supply | CONTRACT | AF FOR FW SA | SUPPLY WATER 5000IG |
| Berthing Arrangement | CONTRACT(AF FOR BA) | CONTRACT | AGENCY FEE FOR BERTHING ARRANGEMENT |
| 5000 IG FW | AT COST | AT COST(WATER SUPPLY) | SUPPLY WATER 5000IG |

---

## 13) 구현 노트
- 코드베이스: `logiontology/`(mapping/validation/reasoning/rdfio/report/pipeline)
- SHACL Runner 옵션, JSON‑LD 컨텍스트 제공, RDFLib + DuckDB로 라인‑레벨 집계 검증.
- 외부 연계: PortCall(AD Ports)·SAFEEN 청구 스냅샷 → `TariffRef` Evidence로 보관.

---

### 끝. (숫자 2 decimals, ISO 날짜 사용, NDA/PII 마스킹 준수)

