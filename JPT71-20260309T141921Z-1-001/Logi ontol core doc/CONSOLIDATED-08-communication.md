---
title: "HVDC Communication System - Consolidated"
type: "ontology-design"
domain: "communication"
sub-domains: ["email", "chat", "multi-channel"]
version: "consolidated-1.0"
date: "2025-11-01"
tags: ["ontology", "hvdc", "communication", "consolidated", "email", "whatsapp", "telegram"]
standards: ["RDF", "OWL", "SHACL", "SPARQL", "JSON-LD", "PROV-O", "Time Ontology"]
status: "active"
source_files: [
  "2_EXT-03-hvdc-comm-email.md",
  "2_EXT-04-hvdc-comm-chat.md"
]
---

# hvdc-communication · CONSOLIDATED-08

## Executive Summary

HVDC Communication System은 이메일과 채팅(WhatsApp/Telegram)을 온톨로지 기반으로 통합하여 물류 커뮤니케이션을 의미 그래프로 표현합니다. 핵심은 메시지, 명령, 의도, 프로세스, 공문, 비용을 SHACL, SWRL, SPARQL로 검증·추론·질의하며, CIPL·BL 사전통제 흐름과 자연스럽게 결합합니다.

## Part 1: Email Communication (SCT-EMAIL)

**Source Files**: `2_EXT-03-hvdc-comm-email.md`

__1\) 요약__

- SCT\-EMAIL은 물류 커뮤니케이션을 __의미 그래프__로 표현한다\.
- 핵심 단위는 메시지, 명령, 의도, 프로세스, 공문, 비용이다\.
- LogiOntology와 __클래스·속성 정렬__로 상호운용한다\.
- SHACL, SWRL, SPARQL로 __검증·추론·질의__를 수행한다\.
- CIPL·BL 사전통제 흐름과 자연스럽게 결합된다\.

__2\) 상위 모델 정렬__

- __PROV\-O__: 행위 기록과 책임 추적에 사용한다\.
- __Time Ontology__: 일정, DDL, UAE 시간대 정규화에 사용한다\.
- __GS1/EPCIS 개념__: 이벤트형 화물 이력에 연결한다\.
- __UN/CEFACT 용어__: 선적 문서와 로지스틱스 어휘 정합을 맞춘다\.

__3\) 핵심 클래스 체계__

__제목__

__정의__

__예시__

Email\_Message

이메일 실체

Booking ETA 확인

Quick\_Message

짧은 메신저

WhatsApp 안내

Command

시스템 명령

/revise, /reply

Intent

발신 의도

inform, request

Logistics\_Process

물류 절차

Shipment, Customs

Stakeholder\_Role

역할

Shipper, Carrier

Document

공식 문서

BL, Invoice

Regulation

규범 항목

HS, Permit

Cost\_Item

비용 단위

DEM, DET

KPI\_Record

성과 지표

TAT, SLA

__4\) 핵심 속성 설계__

- hasIntent\(Communication\_Action → Intent\)
- about\(Communication\_Action → Logistics\_Process\)
- involves\(Logistics\_Process → Stakeholder\_Role\)
- refersTo\(Communication\_Action → Document\)
- hasAmount\(Cost\_Item → xsd:decimal\)
- hasCurrency\(Cost\_Item → xsd:string\)
- eventTime\(Communication\_Action → time:Instant\)
- projectTag\(Communication\_Action → xsd:string\)
- uom\(Cost\_Item → xsd:string\)
- requires\(Regulation → Document\)

__5\) 공리와 규칙 예시__

- Email\_Message ⊑ Communication\_Action
- Quick\_Message ⊑ Communication\_Action
- Command ⊑ prov:Activity
- Communication\_Action ⊑ ∃hasIntent\.Intent
- Cost\_Item ⊑ ∃hasAmount\.xsd:decimal

__SWRL 예시__

Email\_Message\(?m\) ^ hasIntent\(?m, request\) ^ refersTo\(?m, BL\)

→ triggers\(?m, PreArrival\_Check\)

__6\) SHACL 검증 스키마__

__Email 메시지 필수 항목__

sh:NodeShape  targetClass: Email\_Message

\- property: projectTag       datatype xsd:string   minCount 1

\- property: eventTime        datatype time:Instant minCount 1

\- property: hasIntent        class    Intent       minCount 1

__비용 항목 2자리 소수 규칙__

\- property: hasAmount datatype xsd:decimal pattern "^\[0\-9\]\+\(\\\.\[0\-9\]\{2\}\)$"

\- property: hasCurrency in \[USD, AED, EUR\]

__7\) 명령 모듈의 온톨로지 매핑__

__명령__

__클래스/속성__

__효과__

/revise

Command

문장 재구성, 용어 정합 유지

/reply

Command

의도 기반 응답 생성

/reply\-note

Command

응답 요지 생성

/costtable

Command \+ Cost\_Item

표 생성, 합계 계산

/doccheck

Verification\_Action

문서 규칙 확인

/ocr\-note

Document\_Ingest

문자 인식 정리

/logi\-master

Orchestrator

KPI·비용·스케줄 연동

/update\-lib

Regulation\_Update

규범 버전 갱신

__8\) LogiOntology 연계 방안__

- LogiOntology:Shipment ⊑ Logistics\_Process 로 매핑한다\.
- PortCall, VesselVisit 를 Logistics\_Process 하위로 연결한다\.
- 브리지 속성 예시:
	- lo:hasPortCallId ↔ projectTag 보조 식별자 매핑
	- lo:hasMilestone ↔ about 절차 연결
- namespace는 lo:로 고정한다\. 충돌은 owl:equivalentClass 로 해소한다\.

__9\) CIPL·BL 사전통제 결합__

- PreArrival\_Guard ⊑ Verification\_Action 으로 정의한다\.
- 트리거 규칙: BL 누락, CIPL 미제출, ETA 임박 시점\.
- 결과 액션: /reply\-note 생성, 담당자 알림, 체크리스트 업데이트\.

__10\) 이벤트 흐름 시나리오__

1. 사용자가 /revise를 호출한다\.
2. 시스템이 Intent를 고정한다\.
3. Email\_Message가 Document를 참조한다\.
4. SHACL로 형식 검증을 수행한다\.
5. 규칙이 PreArrival\_Guard를 유발한다\.
6. KPI\_Record가 TAT를 기록한다\.

__11\) 데이터 직렬화 권장__

- __RDF/Turtle__ 운영, __JSON\-LD__ 외부 연계 사용\.
- 시간은 Asia/Dubai 로 정규화한다\. 오프셋을 명시한다\.
- 금액은 두 자리 고정이다\. 예: 420\.00, 150\.00\.

__TTL 예시__

:msg123 a Email\_Message ;

  projectTag "HVDC\-001" ;

  eventTime "2025\-10\-19T09:00:00\+04:00"^^xsd:dateTime ;

  hasIntent :request ;

  refersTo :docBL8899 ;

  about :procShipmentA \.

:cost1 a Cost\_Item ;

  hasAmount "420\.00"^^xsd:decimal ;

  hasCurrency "USD" ;

  uom "Lot" \.

__12\) KPI와 SPARQL 질의__

__TAT 측정__

SELECT ?project \(AVG\(?minutes\) AS ?avgTATmin\)

WHERE \{

  ?m a :Email\_Message ; :projectTag ?project ;

     :eventTime ?t1 ; :hasIntent :request \.

  ?r a :Email\_Message ; :projectTag ?project ;

     :eventTime ?t2 ; :hasIntent :inform \.

  FILTER \(?t2 > ?t1\)

  BIND \( \(xsd:dateTime\(?t2\)\-xsd:dateTime\(?t1\)\) AS ?delta \)

  BIND \( \(?delta/60000\) AS ?minutes \)

\}

GROUP BY ?project

__Pre\-Arrival 미준수 목록__

SELECT ?bl ?eta

WHERE \{

  ?check a :PreArrival\_Guard ; :status "Open" ;

         :refersTo ?bl ; :eta ?eta \.

\}

ORDER BY ?eta

__DEM/DET 합계__

SELECT ?project \(SUM\(xsd:decimal\(?amt\)\) AS ?total\)

WHERE \{

  ?c a :Cost\_Item ; :projectTag ?project ;

     :type ?k ; :hasAmount ?amt \.

  FILTER \(?k IN \("DEM","DET"\)\)

\}

GROUP BY ?project

__13\) 거버넌스__

- 네임스페이스 버전: sct\-email/1\.0/, lo/1\.0/\.
- 변경 관리: owl:deprecated 적용, 마이그레이션 그래프 유지\.
- 규범 갱신은 /update\-lib 로 기록한다\. 버전 로그를 남긴다\.

__14\) 보안·감사__

- PII 마스킹 규칙을 SHACL로 강제한다\.
- 접근 제어는 그래프 레벨 태깅으로 분리한다\.
- 모든 명령 기록은 prov:wasAssociatedWith 로 남긴다\.

__15\) 시스템 배치 권장__

- 트리플 스토어는 ACID 보장 제품을 추천한다\.
- 메시지 버스는 명령 이벤트를 전달한다\.
- ETL은 JSON\-LD를 표준으로 고정한다\.

__16\) 이행 단계__

__단계__

__범위__

__산출물__

Phase 1

클래스·속성 최소셋

SHACL v1, SPARQL 5종

Phase 2

규칙·KPI 확장

SWRL v1, 대시보드

Phase 3

전사 연계

PreArrival 자동화

__17\) 위험 및 대응__

- HS 코드 8자리 초과 인식 오류 가능성이 높다\.
- UAE 이중용도 품목은 오검이 잦다\.
- 두 항목은 수동 검증 표시를 유지한다\.

__표시 예시__

- 🔍 Verification needed 속성을 부여한다\.

__18\) 운영 체크리스트__

- 메시지에 프로젝트 태그가 있는가\.
- 시간은 \+04:00 으로 저장되었는가\.
- 비용은 두 자리 소수인가\.
- 문서는 규범과 연결되었는가\.
- KPI 기록이 생성되었는가\.

__19\) 부록: 매핑 테이블__

__항목__

__SCT\-EMAIL__

__LogiOntology__

선적

Logistics\_Process

Shipment

입항

Logistics\_Process

PortCall

문서

Document

BL, Invoice

규범

Regulation

Permit, HS

행위

Communication\_Action

Event

원하면 TTL 파일 뼈대를 제공하겠다\.
샘플 그래프와 SHACL 패키지도 즉시 제공 가능하다\.

---

## Part 2: Chat Communication (WhatsApp/Telegram)

**Source Files**: `2_EXT-04-hvdc-comm-chat.md`

### 1) Executive Summary (3–5 lines)

- 본 시스템은 **Multi‑Key Identity Graph** 위에서 *그룹↔스레드↔메시지↔태그↔자산/사이트/화물/승인*을 연결한다. (*Any‑key in → Resolve → Cluster → Tasks*).
- **Master Policy**의 태그·SLA·파일명·보안 규칙을 **온톨로지 계층**으로 승격하여, **일관된 자동 분류·SLA 타이머·PII 마스킹·자동 리포트**를 실행한다.
- 각 그룹의 **고유 패턴(항만/타이드/장비/증빙)**은 *도메인 보카블러리(SKOS)*로 관리, **키워드→태스크**를 표준화한다.
- 결과물: RDF/OWL 온톨로지 + SHACL 검증 + JSON‑LD 컨텍스트 + SPARQL 질의 + 자동화 훅(08:30/17:30, 목 16:00).

### 2) Conceptual Model (개념)

- **hvdc:Workgroup** ⟶ hasMember **hvdc:Participant** (역할/RACI)
- **hvdc:Workgroup** ⟶ hasThread **hvdc:Thread** ⟶ hasMessage **hvdc:Message**
- **hvdc:Message** ⟶ hasTag **hvdc:Tag** (고정 9종 + 확장)
- **hvdc:Message** ⟶ about **hvdc:Asset | hvdc:Site | hvdc:Cargo | hvdc:Approval**
- **hvdc:Message** ⟶ evokes **hvdc:Action** (예: book_crane_100t, submit_gate_pass_list)
- **hvdc:Message** ⟶ hasAttachment **hvdc:Document** (CIPL/BL/DO/Permit 등)
- **hvdc:SLAClock** attachesTo **hvdc:Message/Action** (업무시간·오프타임 규칙 내장)
- **hvdc:Policy** governs **Workgroup/Message/Document** (보안·PII·파일명·언어)

### 3) Tagging & Controlled Vocabulary

**고정 태그(메타):** `[URGENT][ACTION][FYI][ETA][COST][GATE][CRANE][MANIFEST][RISK]`

**도메인 태그:**
- **Site:** `/sites/AGI-West-Harbor`, `/sites/MW4`, `/sites/MOSB`, `/sites/DAS-Island`, `/sites/GCC-yard`
- **Asset:** `Crane-100T`, `A-frame trailer`, `Forklift-10T`, `Wheel loader`
- **Cargo:** `Aggregate-5mm/10mm/20mm`, `Jumbo bag`, `HCS`, `Wall panel`
- **Approval:** `TPI`, `MWS`, `Lifting Plan`, `Gate pass`

### 4) Event/Message Model & SLA Semantics

- **업무시간**: 08:00–20:00 (GST). 오프타임: *URGENT만 에스컬레이션*.
- **SLA**: URGENT 10분, ACTION 2시간, FYI 당일.
- **헤더 규칙**: 메시지 첫줄 `[TAG][TAG] [SHPTNO]/[SITE]/[ITEM]/[ETA]/[ACTION]` 권장.
- **파일명 규칙**: `YYYYMMDD_[SHPTNO]_[DOC]_v##` (예: `20250808_HVDC-AGI-J71-047_CIPL_v02`).

### 5) Group Instantiation (도메인 인스턴스)

- **Abu Dhabi Logistics**: 중앙 오케스트레이션(게이트패스·크레인·컨테이너·ETA/ETD)
- **Jopetwil 71 Group**: AGI Jetty#3, RORO 타이드 윈도우(~10:30/12:00)
- **UPC – Precast Transportation**: A‑frame 3대 이상 상시, Dunnage 높이 규정
- **AGI – Wall Panel – GCC Storage**: 100T 크레인, GCC yard close(14:00/17:30 가변)
- **[HVDC] Project Lightning**: Program‑level SITREP 07:30/16:00, CCU/FR/OT 순환

### 6) Automation Hooks (운영)

- **일일 요약**: 08:30 / 17:30 — `Workgroup → Thread(scan 24h) → Action Board` 자동 생성·배포
- **주간 리포트**: 목 16:00 — KPI 카드(태그 사용률, SLA 준수율, 첨부 완전성, SITREP 정시율) 생성
- **Keyword→Task**: `[CRANE]`→ 장비 예약 시트, `[GATE]`→ 게이트패스 제출 폼, `[MANIFEST]`→ PL/Manifest 체크

---

**Confidential – SCT Internal Use**

**Recommended Next Commands**: /summary ▪ /logi-master ▪ /doccheck

