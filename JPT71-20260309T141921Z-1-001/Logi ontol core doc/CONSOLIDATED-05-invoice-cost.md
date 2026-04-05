---
title: "HVDC Invoice & Cost Management Ontology"
type: "ontology-design"
domain: "invoice-cost-management"
sub-domains: ["invoice-verification", "cost-guard", "rate-reference", "flow-code"]
version: "consolidated-1.1"
date: "2025-11-01"
tags: ["ontology", "hvdc", "invoice", "cost-management", "verification", "flow-code", "consolidated"]
standards: ["RDF", "OWL", "SHACL", "SPARQL", "JSON-LD", "Turtle", "XSD"]
status: "active"
source_files: ["1_CORE-04-hvdc-invoice-cost.md", "docs/flow_code_v35/FLOW_CODE_V35_ALGORITHM.md"]
---

# hvdc-invoice-cost · CONSOLIDATED-05

## Invoice & Cost Management

### Source
- **Original File**: `1_CORE-04-hvdc-invoice-cost.md`
- **Version**: unified-1.0
- **Date**: 2025-01-19

## Executive Summary

**온톨로지-퍼스트 청구서 시스템**은 "**멀티-키 아이덴티티 그래프**(BL/Container/DO/Invoice/Case/Booking/ShipmentID/.../hvdc_code 아무 키든 OK)" 위에서 **Invoice→Line→OD Lane→RateRef→Δ%→Risk**로 한 번에 캐스케이드합니다.

### Flow Code v3.5 in Cost Analysis

**Flow Code directly impacts logistics costs** in the HVDC project. Different Flow Codes indicate different routing patterns, each with distinct cost structures:

| Flow Code | Routing | Cost Components | Cost Impact |
|-----------|---------|-----------------|-------------|
| **Flow 1** | Port → Site | Port fees + Direct trucking | **Lowest** (single hop) |
| **Flow 2** | Port → WH → Site | Port + Warehouse + 2× Trucking | **Medium** (warehouse handling) |
| **Flow 3** | Port → MOSB → Site | Port + MOSB + LCT/Barge | **High** (offshore transport) |
| **Flow 4** | Port → WH → MOSB → Site | Port + WH + MOSB + Trucking + LCT | **Highest** (full chain) |
| **Flow 5** | Incomplete | Variable (staging costs) | **Unpredictable** |

**Cost Verification by Flow Code**:
- Flow Code extracted from invoice documents (OCR)
- Cost structure validated against Flow Code routing
- MOSB leg charges verified for Flow 3/4
- Warehouse charges validated for Flow 2/4

--- \(EN\-KR: Any\-key in → Resolve → Lane&Rate join → Δ% risk band\.\)
표준요율은 __Air/Container/Bulk 계약 레퍼런스__와 __Inland Trucking\(OD×Unit\) 테이블__을 온톨로지 클래스로 들고, 모든 계산은 __USD 기준·고정환율 1\.00 USD=3\.6725 AED__ 규칙을 따릅니다\.
OD 정규화·조인은 __ApprovedLaneMap/RefDestinationMap__을 통해 수행되고, 결과는 \*\*COST\-GUARD Δ% 밴드\(PASS/WARN/HIGH/CRITICAL\)\*\*로 귀결됩니다\.
감사 트레이스는 __PRISM\.KERNEL__ 포맷\(5\-line recap \+ proof\.artifact JSON\)으로 고정 형식으로 남깁니다\.

### Glossary

- **PRISM.KERNEL**: 감사 트레이스 포맷 (5-line recap + proof.artifact JSON)
  - Recap: 요약 정보 (Invoice ID, Vendor, Total, Delta%, Verdict)
  - Artifact: 상세 증빙 데이터 (Rate 조인 소스, Lane 매핑, 계산 과정)

__Visual — 핵심 클래스/관계\(요약\)__

__Class__

__핵심 속성__

__관계__

__근거/조인 소스__

__결과__

hvdc:Invoice

docId, vendor, issueDate, currency

hasLine → InvoiceLine

—

상태, 총액, proof

hvdc:InvoiceLine

chargeDesc, qty, unit, draftRateUSD

hasLane → ODLane / uses → RateRef

Inland Trucking/Table, Air/Container/Bulk Rate

Δ%, cg\_band

hvdc:ODLane

origin\_norm, destination\_norm, vehicle, unit

joinedBy → ApprovedLaneMap

RefDestinationMap, Lane stats

median\_rate\_usd

hvdc:RateRef

rate\_usd, tolerance\(±3%\), source\(contract/market/special\)

per Category/Port/Dest/Unit

Air/Container/Bulk/Trucking tables

ref\_rate\_usd

hvdc:CurrencyPolicy

base=USD, fx=3\.6725

validates Invoice/Line

currency\_mismatch rule

환산/락

hvdc:RiskResult

delta\_pct, cg\_band, verdict

from Line vs Ref

COST\-GUARD bands

PASS/FAIL

자료: 표준요율 테이블\(계약\)·고정 FX 규정·Lane 정규화 지도\.

__How it works \(flow\)__

1. __키 해석\(Identity\)__: BL/Container/DO/Invoice/… 입력 → 동일 실체\(Shipment/Doc\) 클러스터 식별\. \(멀티\-키 그래프\)
2. __Lane 정규화__: 원지/착지 명칭을 __RefDestinationMap__으로 정규화 → __ApprovedLaneMap__에서 lane 통계/표준요율 후보 추출\.
3. __Rate 조인__: 라인별 __Category\+Port\+Destination\+Unit__로 계약 요율 테이블 매칭\(±3% 톨러런스\)\.
4. __Δ% & 밴드 산정__: Δ%=\(draft−ref\)/ref×100 → __PASS/WARN/HIGH/CRITICAL__ \(COST\-GUARD\)\. FX는 USD 고정\(3\.6725\)로 비교\.
5. __감사 아티팩트__: __PRISM\.KERNEL__로 5\-라인 요약 \+ JSON 증빙\(입력/계산/판정 해시\)\.

__Options \(설계 선택지\)__

1. __OWL/SHACL 엄격형__: 스키마·제약\(단위/Currency/OD 필수\)로 하드 밸리데이션\. *Pros* 규정준수↑ / *Cons* 초기 모델링 비용↑\.
2. __하이브리드형\(권장\)__: OWL\+Lane Map\+계약요율\+Δ% 밴드, 부족 구간은 유사 레인 추천\. *Pros* 커버리지↑ / *Cons* Ref 미보유 구간 튜닝 필요\.
3. __마켓레이트 보강형__: Market API\(At\-cost 항목\)에 한정 보조\. *Pros* 현실성↑ / *Cons* 출처 관리·증빙 필요\.

__Roadmap \(P→Pi→B→O→S \+ KPI\)__

- __Prepare__: RefDestinationMap 최신화, Lane 조인율≥80% 달성\.
- __Pilot__: /switch\_mode COST\-GUARD \+ /logi\-master invoice\-audit \-\-deep \-\-highlight\-mismatch로 월간 샘플 1회전\. KPI: 검증정확도 ≥97%, 자동화 ≥94%\.
- __Build__: 라인별 Δ%·밴드·증빙\(표준요율 근거 링크\) 자동 표기, 통화정책 락\.
- __Operate__: High/CrITICAL 즉시 TG 알림 \+ 반려 사유 템플릿\.
- __Scale__: Lane 그래프 스냅샷/변동 추적, 분기별 임계치 튜닝\.

__Automation notes__

- __입력 감지 →__ /switch\_mode COST\-GUARD \+ /logi\-master invoice\-audit \(OD 정규화→Rate 조인→Δ% 밴드→PASS/FAIL 표\)\.
- __표준 근거__: Air/Container/Bulk/Trucking 계약표 \+ Inland Ref\(정리본\)\.
- __감사 포맷__: PRISM 5\-라인 \+ JSON proof\(해시\)\.

__QA / Gap 체크__

- Line 단위가 __per truck vs per RT__ 혼재 시 단위환산 룰 적용? \(컨/Bulk 교차 구간\)
- __CURRENCY\_MISMATCH__/고정 FX\(3\.6725\) 락 확인?
- Lane 조인 실패\(REF\_MISSING\) 건은 유사도≥0\.60 Top\-3 제안 출력?
- 증빙 링크\(표준요율 원천, Lane 통계\)와 PRISM proof 동시 첨부?

가정: \(i\) 계약표는 최신판으로 동기화됨, \(ii\) 환율 고정 정책 유지, \(iii\) SHACL Shapes는 내부 표준에 따라 배포됨\.

__원한다면, 너한테 맞춘 "클래스·프로퍼티 TTL 스켈레톤 \+ SHACL" 바로 뽑아줄게\.__

---

# Part 2: Draft Invoice Verification Framework

좋아, "Verify draft Invoice"를 온톨로지\(ontology\) 관점으로 깔끔히 잡아볼게\. 핵심은 "규칙이 흩어져 있지 않고, 전부 그래프 위에 '의미\(클래스/속성/제약\)'로 올라간다"는 점이야\. 그러면 규칙·문서·흐름·승인 근거까지 한 그래프에서 검증·추적·설명 가능해진다\.

__1\) 개념 스키마\(TBox\): 무대 세팅__

- __문서 계층__
	- hvdc:Document 상위에 hvdc:Invoice, hvdc:DeliveryOrder, hvdc:StowagePlan, hvdc:WarehouseDoc, hvdc:StatusDoc\.
	- 키\(식별자\)는 hvdc:Key의 서브클래스: hvdc:InvoiceKey, hvdc:DOKey, hvdc:StowageKey, hvdc:WHKey, hvdc:StatusKey, hvdc:ShipmentIDKey, hvdc:BookingKey, hvdc:BLKey, hvdc:ContainerKey 등\.
→ 모든 문서 연결은 이 키들로 그래프 엣지를 만든다\.
- __금액/통화__
	- hvdc:MonetaryAmount \(액수·통화·단위\), hvdc:Currency\(예: "USD", "AED"\)\.
- __레이트/출처__
	- hvdc:RateSource = \{Contract, MarketRate, Quotation, SpecialRate\} \(열거형\)\.
	- hvdc:hasRate, hvdc:hasQuantity, hvdc:hasTotal, hvdc:rateSource\.
- __검증 메타__
	- hvdc:VerificationStatus = \{VERIFIED, PARTIALLY\_VERIFIED, RATE\_MISMATCH, CURRENCY\_MISMATCH, MULTI\_CURRENCY, REFERENCE\_MISSING, DATA\_MISSING, DOCUMENT\_ALERT, PENDING\_REVIEW\}\.
	- hvdc:Discrepancy\(유형·사유·차이율\), hvdc:hasDiscrepancy\.
- __흐름/승인/근거\(정합성\)__
	- 코스트가드 플로우: hvdc:Flow ⟶ hvdc:InvoiceAuditStep \(HVDC Logistics Unified v3\.7 내 일부\)\.
	- 승인·근거는 __PROV\-O__ 정렬: prov:Entity\(문서\), prov:Activity\(검증\), prov:wasDerivedFrom\(참조문서\), prov:wasAssociatedWith\(담당자\)\.

__2\) 제약\(Shapes\)와 규칙: 그래프 위에서 "검증"을 말로 하지 않고 모델로 한다__

- __SHACL__로 필수 필드, 단위, 포맷을 강제\(Invoice/DO/Stowage/WH/Status용 shape\)\. 숫자 필드\(레이트·수량\)는 0 이상, 소수점 자릿수, 누락 시 DATA\_MISSING, 음수/비수치면 FORMAT\_ERROR\.
- __동적 허용오차\(레이트 출처별\)__
	- Contract: ±3%
	- Market Rate/Quotation: ±5%
	- Special Rate: ±10%
	- 그리고 ±10% 이내는 PENDING\_REVIEW 2차 판정\(사람 확인\)
	- 합계는 rate × quantity 재계산, 합계 오차 0\.01까지 허용
- __통화 규칙__
	- 원문서 통화 유지\(환산 금지\), 1 USD = 3\.6725 AED는 "참고 정보" 어노테이션\.
	- 한 인보이스에 다중 통화면 MULTI\_CURRENCY, 참조문서와 통화 다르면 CURRENCY\_MISMATCH\.
- __교차문서 일치__
	- 계약/견적/DO 등과 수량·레이트·통화 매칭\. 근거 누락·불일치 시 REFERENCE\_MISSING\.
위 규칙 묶음은 시스템 매뉴얼의 "검증 단계, 상태 코드, 통화 처리, 사전 점검"에 그대로 대응된다\.

__3\) 워크플로우\(그래프 연산 시퀀스\)__

1. __사전 점검__: 문서 완전성·통화 일관성·레이트 소스 존재 여부 스캔 → shape 위반나면 즉시 라벨\(DATA\_MISSING 등\)\.
2. __콘텐츠 검증__: rate × quantity 재계산, 참조문서 레이트와 비교\(출처별 허용오차 반영\), 상태 라벨링\(VERIFIED/RATE\_MISMATCH/PENDING\_REVIEW…\)\.
3. __교차문서 정합성__: 키로 링크된 계약/견적/DO의 값·승인정보 매칭, 불일치·누락 시 REFERENCE\_MISSING\.
4. __요약/리포트 노드__: 총 검증 건수, 상태 분포, 문제 항목 하이라이트\(사유 포함\)\.

__4\) 그래프 예시\(축약 Turtle\)__

@prefix hvdc: <https://example\.com/hvdc\#> \.

@prefix prov: <http://www\.w3\.org/ns/prov\#> \.

@prefix xsd:  <http://www\.w3\.org/2001/XMLSchema\#> \.

hvdc:Invoice123 a hvdc:Invoice ;

  hvdc:invoiceKey "INV\-123" ;

  hvdc:currency "AED" ;

  hvdc:rateSource hvdc:Contract ;

  hvdc:hasRate "150\.00"^^xsd:decimal ;

  hvdc:hasQuantity "10"^^xsd:decimal ;

  hvdc:hasTotal "1500\.00"^^xsd:decimal ;

  hvdc:references hvdc:Contract789 ;

  prov:wasDerivedFrom hvdc:Quotation456 \.

\# 검증 결과\(예\)

hvdc:Invoice123\_Validation a hvdc:ValidationActivity ;

  hvdc:verificationStatus hvdc:PENDING\_REVIEW ;

  hvdc:hasDiscrepancy \[

    a hvdc:Discrepancy ;

    hvdc:discrepancyType hvdc:RateTolerance ;

    hvdc:deltaPercent "0\.045"^^xsd:decimal ; \# 4\.5% 차이

  \] ;

  prov:used hvdc:Contract789 ; prov:generated hvdc:Invoice123 \.

__5\) SHACL로 "규칙=데이터"화\(간단 스케치\)__

- __필드 존재·형식__: sh:minCount 1, sh:datatype xsd:decimal, sh:minInclusive 0\.
- __통화 일관성__: 인보이스 통화와 참조문서 통화 비교\(대응 속성에 sh:equals/SPARQL constraints\)\.
- __출처별 허용오차__: SPARQL constraint에서 ?rateSource에 따라 허용오차 분기\(Contract 0\.03, Market/Quotation 0\.05, Special 0\.10\)\. ±0\.10 이내면 상태를 PENDING\_REVIEW로 마킹\.
- __합계 재계산__: 계산식으로 산출값과 제출값의 차이가 0\.01 이하인지 확인\.

__6\) 운영·통합 포인트__

- __키로 연결되는 전사 링크__: hvdc:InvoiceKey 등 키 클래스로 시스템 간 조인 없이 그래프에서 즉시 추론 가능\.
- __SCT\-EMAIL 매핑__: 메일을 hvdc:Communication\(또는 schema:EmailMessage\)로 모델링해 승인/합의 근거를 prov:wasDerivedFrom로 인보이스에 귀속\.
- __COST\-GUARD 플로우__: hvdc:Flow 안에 hvdc:InvoiceAuditStep을 명시해 "어느 단계에서 무슨 규칙으로 걸렸나"를 설명가능하게\.
- __명령 ↔ 검증 모드__: /logi\-master invoice\-audit \-\-deep \-\-highlight\-mismatch \-\-ToT\_mode deep
	- \-\-deep: 모든 SHACL shape \+ SPARQL constraints 전부 실행
	- \-\-highlight\-mismatch: hvdc:hasDiscrepancy를 가진 트리플에 태그\(또는 리포트에 강조 필드\)
	- \-\-ToT\_mode deep: 다단계 규칙\(계약→견적→시장가→특수레이트\) 체인을 순차 추론
- __ML 연계__: 그래프에서 파생 피처\(차이율, 다중통화 여부, 링크 강도, shape 위반 카운트\)를 뽑아 이상치 모델에 투입\. 모델 결과는 다시 hvdc:AnomalyScore/hvdc:AnomalyFlag로 지식그래프에 적재\(설명가능성↑\)\.
- __레포트 스키마__: 리포트도 그래프화\(열/요약/상세를 노드로\)\. Excel/대시보드는 그래프 질의 결과의 뷰일 뿐\.

원하는 결로 정리하면: \*\*규칙·근거·흐름을 온톨로지로 "고정"\*\*해 두고, SHACL/SPARQL로 검증하고, 키 클래스로 문서를 촘촘히 연결, 통화·출처별 허용오차는 상태코드로 귀결\. 그 위에 ML을 얹어 "규칙이 놓치는 패턴"을 보강\.
필요하면 이 스키마/SHACL 초안을 macho715/ontology\-insight 스타일에 맞춰 모듈화해서 바로 리포에 붙일 수 있게 만들어줄게\.

---

# Part 3: PRISM.KERNEL 감사 트레이스 샘플

## PRISM.KERNEL 포맷 설명

PRISM.KERNEL 감사 트레이스는 **5-line recap + proof.artifact JSON** 구조로 구성됩니다:
- **Recap (5-line 요약)**: Invoice ID, Vendor, Total, Delta%, Verdict
- **Artifact (JSON 증빙)**: Rate 조인 소스, Lane 매핑, 계산 과정, 해시

## 샘플 1: PASS 케이스 (Delta% 2.1%)

```json
{
  "recap": [
    "INV-2025-001 | DSV Logistics | USD 15,000.00 | Δ% 2.1% | VERDICT: PASS",
    "Lane: MOSB→MIR Site | Unit: TEU | Quantity: 2.0",
    "Rate Source: Contract | Ref Rate: USD 7,350.00 | Draft Rate: USD 7,500.00",
    "COST-GUARD Band: PASS | Tolerance: ±3% | Within Limit",
    "PRISM Proof Hash: sha256:abc123def456..."
  ],
  "artifact": {
    "invoiceId": "INV-2025-001",
    "vendor": "DSV Logistics",
    "total": 15000.00,
    "currency": "USD",
    "fxRate": 3.6725,
    "lineItems": [
      {
        "chargeDesc": "Inland Transportation",
        "quantity": 2.0,
        "unit": "TEU",
        "draftRateUSD": 7500.00,
        "lane": {
          "originNorm": "MOSB",
          "destinationNorm": "MIR Site",
          "vehicle": "Truck",
          "unit": "TEU"
        },
        "rateRef": {
          "source": "Contract",
          "rateUSD": 7350.00,
          "tolerance": 0.03
        },
        "riskResult": {
          "deltaPercent": 2.1,
          "costGuardBand": "PASS",
          "verdict": "ACCEPTABLE"
        }
      }
    ],
    "calculation": {
      "deltaCalculation": "(7500 - 7350) / 7350 * 100 = 2.1",
      "bandAssignment": "|2.1| < 3.0 → PASS",
      "timestamp": "2025-10-31T14:23:00Z"
    },
    "proofHash": "sha256:abc123def456..."
  }
}
```

## 샘플 2: WARN 케이스 (Delta% 4.8%)

```json
{
  "recap": [
    "INV-2025-002 | ALS Logistics | USD 32,500.00 | Δ% 4.8% | VERDICT: WARN",
    "Lane: Zayed Port→DSV Indoor→MIR Site | Unit: TEU | Quantity: 5.0",
    "Rate Source: Contract | Ref Rate: USD 6,200.00 | Draft Rate: USD 6,500.00",
    "COST-GUARD Band: WARN | Tolerance: ±3% | Exceeded by 1.8%",
    "PRISM Proof Hash: sha256:def789ghi012..."
  ],
  "artifact": {
    "invoiceId": "INV-2025-002",
    "vendor": "ALS Logistics",
    "total": 32500.00,
    "currency": "USD",
    "fxRate": 3.6725,
    "lineItems": [
      {
        "chargeDesc": "Port to Warehouse Transportation",
        "quantity": 5.0,
        "unit": "TEU",
        "draftRateUSD": 6500.00,
        "lane": {
          "originNorm": "Zayed Port",
          "destinationNorm": "MIR Site",
          "intermediate": "DSV Indoor",
          "vehicle": "Truck",
          "unit": "TEU"
        },
        "rateRef": {
          "source": "Contract",
          "rateUSD": 6200.00,
          "tolerance": 0.03
        },
        "riskResult": {
          "deltaPercent": 4.8,
          "costGuardBand": "WARN",
          "verdict": "REVIEW_REQUIRED",
          "reason": "Delta exceeds contract tolerance by 1.8%, requires approval"
        }
      }
    ],
    "calculation": {
      "deltaCalculation": "(6500 - 6200) / 6200 * 100 = 4.8",
      "bandAssignment": "|4.8| > 3.0 → WARN",
      "timestamp": "2025-10-31T15:45:00Z"
    },
    "proofHash": "sha256:def789ghi012..."
  }
}
```

## 샘플 3: CRITICAL 케이스 (Delta% 12.5%)

```json
{
  "recap": [
    "INV-2025-003 | Vendor XYZ | USD 85,000.00 | Δ% 12.5% | VERDICT: CRITICAL",
    "Lane: Khalifa Port→MOSB→AGI | Unit: TEU | Quantity: 10.0",
    "Rate Source: Contract | Ref Rate: USD 7,550.00 | Draft Rate: USD 8,500.00",
    "COST-GUARD Band: CRITICAL | Tolerance: ±3% | Exceeded by 9.5%",
    "PRISM Proof Hash: sha256:ghi345jkl678..."
  ],
  "artifact": {
    "invoiceId": "INV-2025-003",
    "vendor": "Vendor XYZ",
    "total": 85000.00,
    "currency": "USD",
    "fxRate": 3.6725,
    "lineItems": [
      {
        "chargeDesc": "Marine Transportation (MOSB→AGI)",
        "quantity": 10.0,
        "unit": "TEU",
        "draftRateUSD": 8500.00,
        "lane": {
          "originNorm": "Khalifa Port",
          "destinationNorm": "AGI",
          "intermediate": "MOSB",
          "vehicle": "LCT",
          "unit": "TEU"
        },
        "rateRef": {
          "source": "Contract",
          "rateUSD": 7550.00,
          "tolerance": 0.03
        },
        "riskResult": {
          "deltaPercent": 12.5,
          "costGuardBand": "CRITICAL",
          "verdict": "REJECT",
          "reason": "Delta exceeds contract tolerance by 9.5%, immediate escalation required",
          "actionRequired": "MANUAL_APPROVAL_MANDATORY"
        }
      }
    ],
    "calculation": {
      "deltaCalculation": "(8500 - 7550) / 7550 * 100 = 12.5",
      "bandAssignment": "|12.5| >> 3.0 → CRITICAL",
      "timestamp": "2025-10-31T16:12:00Z"
    },
    "proofHash": "sha256:ghi345jkl678...",
    "escalation": {
      "triggered": true,
      "severity": "CRITICAL",
      "notified": ["cost-guard-team@samsungct.com", "finance-team@samsungct.com"],
      "deadline": "2025-10-31T18:00:00Z"
    }
  }
}
```
