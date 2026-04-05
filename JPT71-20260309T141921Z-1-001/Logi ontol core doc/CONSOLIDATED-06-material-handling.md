---
title: "HVDC Material Handling Ontology - Consolidated"
type: "ontology-design"
domain: "material-handling"
sub-domains: ["workshop", "customs", "storage", "offshore", "receiving", "transformer", "bulk-cargo", "flow-code"]
version: "consolidated-1.1"
date: "2025-11-01"
tags: ["ontology", "hvdc", "material-handling", "flow-code", "flow-code-v35", "agi-das", "mosb", "consolidated"]
standards: ["RDF", "OWL", "SHACL", "SPARQL", "JSON-LD", "IMSBC", "SOLAS"]
status: "active"
source_files: [
  "2_EXT-08A-hvdc-material-handling-overview.md",
  "2_EXT-08B-hvdc-material-handling-customs.md",
  "2_EXT-08C-hvdc-material-handling-storage.md",
  "2_EXT-08D-hvdc-material-handling-offshore.md",
  "2_EXT-08E-hvdc-material-handling-site-receiving.md",
  "2_EXT-08F-hvdc-material-handling-transformer.md",
  "2_EXT-08G-hvdc-material-handling-bulk-integrated.md",
  "docs/flow_code_v35/FLOW_CODE_V35_ALGORITHM.md"
]
---

# hvdc-material-handling · CONSOLIDATED-06

## Executive Summary

This consolidated document merges 7 Material Handling ontology documents covering the complete logistics workflow for the Independent Subsea HVDC System Project (Project Lightning) in the UAE. It encompasses:

- **Overview**: Project logistics workflow and port information
- **Customs Clearance**: UAE customs procedures and documentation
- **Storage & Inland Transportation**: Storage standards and heavy equipment transport
- **Offshore Marine Transportation**: LCT operations and MOSB procedures
- **Site Receiving**: Material inspection and issuance procedures
- **Transformer Handling**: Specialized heavy equipment operations
- **Bulk Cargo Operations**: Integrated stowage, lashing, stability, and lifting

All content from the individual documents is preserved in their respective sections below.

---

## Flow Code v3.5 Integration in Material Handling

### Overview

Material handling operations in the HVDC project follow distinct **logistics flow patterns** that can be classified using **Flow Code v3.5 (0-5)**. Understanding these patterns is critical for optimizing material movement, especially for **AGI/DAS offshore sites** where MOSB transit is mandatory.

### Flow Code Patterns in Material Handling

#### Flow Code Distribution by Material Type

| Material Category | Primary Flow Code | Routing Pattern | Reason |
|-------------------|-------------------|-----------------|--------|
| **Container Cargo** | Flow 2, 4 | Port → WH → (MOSB) → Site | Standard containerized items via warehouse |
| **Bulk Cargo** | Flow 3, 4 | Port → (WH →) MOSB → Site | Large items requiring MOSB consolidation |
| **Transformer/Heavy** | Flow 3, 4 | Port → MOSB → AGI/DAS | Specialized heavy equipment, offshore delivery |
| **Direct to MIR/SHU** | Flow 1 | Port → Site | Onshore sites, no MOSB leg required |
| **AGI/DAS Materials** | Flow 3, 4 (강제) | Port → MOSB → AGI/DAS | **Mandatory MOSB leg** per domain rules |

#### AGI/DAS Domain Rule Application

**Critical Business Rule**: All materials destined for **AGI (Al Ghallan Island)** or **DAS (Das Island)** offshore sites **MUST** transit through MOSB, regardless of original routing.

```
Material Handling Flow Code Override:
- Destination = AGI OR DAS
  → Original Flow Code 0, 1, 2 → Auto-upgrade → Flow Code 3
  → Reason: "AGI/DAS mandatory MOSB leg"

Physical Constraint:
- AGI/DAS are offshore islands accessible only by LCT/barge
- MOSB serves as the marine transportation staging point
- No direct port-to-island routing is physically possible
```

### Material Handling Workflow with Flow Code

#### Phase A: Import & Customs (Flow 0-2)

```
Flow 0 (Pre Arrival):
- Cargo: Container/bulk shipments
- Location: International waters / Port approach
- Status: Awaiting port clearance
- Actions: Pre-customs documentation, MOIAT preparation

Flow 1 (Direct to Onshore Site):
- Cargo: MIR/SHU-bound materials
- Route: Khalifa/Zayed Port → MIR/SHU Site
- Transport: Direct trucking (no warehouse stop)
- Example: Urgent onshore equipment

Flow 2 (Warehouse Consolidation):
- Cargo: Container cargo requiring storage
- Route: Port → DSV Indoor/AAA Storage → Site
- Transport: Port truck → Warehouse → Site truck
- Example: Standard materials with lead time
```

#### Phase B: Offshore Transportation (Flow 3-4)

```
Flow 3 (MOSB Direct):
- Cargo: Bulk/heavy items for offshore
- Route: Port → MOSB → AGI/DAS
- Transport: Port truck → MOSB → LCT/barge
- Example: Transformer to AGI

Flow 4 (Warehouse + MOSB):
- Cargo: Containerized offshore materials
- Route: Port → Warehouse → MOSB → AGI/DAS
- Transport: Port truck → WH → MOSB truck → LCT
- Example: Containerized parts for DAS platform

Flow 5 (Mixed/Incomplete):
- Cargo: Materials in transit/awaiting routing
- Status: MOSB arrived but site not assigned
- Action: Review and re-assign to AGI/DAS
```

### RDF/OWL Implementation for Material Handling

#### Enhanced Ontology Classes

```turtle
@prefix mh: <https://hvdc-project.com/ontology/material-handling/> .
@prefix hvdc: <https://hvdc-project.com/ontology/core/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# Flow Code properties for Material Handling
mh:hasLogisticsFlowCode a owl:DatatypeProperty ;
    rdfs:label "Logistics Flow Code for Material" ;
    rdfs:comment "Flow Code (0-5) classification for material movement" ;
    rdfs:domain mh:Cargo ;
    rdfs:range xsd:integer ;
    sh:minInclusive 0 ;
    sh:maxInclusive 5 .

mh:requiresMOSBLeg a owl:DatatypeProperty ;
    rdfs:label "Requires MOSB Transit" ;
    rdfs:comment "Boolean flag for AGI/DAS materials requiring MOSB" ;
    rdfs:domain mh:Cargo ;
    rdfs:range xsd:boolean .

mh:hasDestinationSite a owl:ObjectProperty ;
    rdfs:label "Destination Site" ;
    rdfs:comment "Final delivery site (MIR/SHU/AGI/DAS)" ;
    rdfs:domain mh:Cargo ;
    rdfs:range mh:Site .

mh:hasTransportPhase a owl:ObjectProperty ;
    rdfs:label "Transport Phase" ;
    rdfs:comment "Phase A (Import) or Phase B (Offshore)" ;
    rdfs:domain mh:Cargo ;
    rdfs:range mh:Phase .

# SHACL Constraint: AGI/DAS MUST have Flow >= 3
mh:AGIDASSiteConstraint a sh:NodeShape ;
    sh:targetClass mh:Cargo ;
    sh:sparql [
        sh:message "AGI/DAS materials must have Flow Code >= 3 (MOSB leg required)" ;
        sh:select """
            PREFIX mh: <https://hvdc-project.com/ontology/material-handling/>
            SELECT $this
            WHERE {
                $this mh:hasDestinationSite ?site ;
                      mh:hasLogisticsFlowCode ?flowCode .
                ?site mh:siteCode ?siteCode .
                FILTER(?siteCode IN ("AGI", "DAS") && ?flowCode < 3)
            }
        """ ;
    ] .
```

#### Instance Example: Transformer to AGI

```turtle
# Material: Transformer destined for AGI
mh:cargo/TRANSFORMER-AGI-001 a mh:Cargo ;
    mh:cargoId "TRANSFORMER-AGI-001" ;
    mh:cargoType "Transformer" ;
    mh:weight 85000 ;  # kg
    mh:hasDestinationSite mh:site/AGI ;
    mh:hasTransportPhase mh:phase/PHASE_B ;
    mh:requiresMOSBLeg true ;
    mh:hasLogisticsFlowCode 3 ;
    mh:hasFlowCodeOriginal 1 ;
    mh:hasFlowOverrideReason "AGI offshore - mandatory MOSB leg" ;
    mh:hasFlowDescription "Port → MOSB → AGI (LCT transport)" .

# LCT Transport Event
mh:transport/LCT-AGI-001 a mh:TransportEvent ;
    mh:transportId "LCT-AGI-001" ;
    mh:transportType "LCT" ;
    mh:origin mh:location/MOSB ;
    mh:destination mh:site/AGI ;
    mh:carries mh:cargo/TRANSFORMER-AGI-001 ;
    mh:departureDate "2024-11-15"^^xsd:date ;
    mh:arrivalDate "2024-11-16"^^xsd:date .
```

### SPARQL Queries for Material Handling

#### 1. Materials by Destination Site and Flow Code

```sparql
PREFIX mh: <https://hvdc-project.com/ontology/material-handling/>

SELECT ?site ?flowCode (COUNT(?cargo) AS ?count)
WHERE {
    ?cargo a mh:Cargo ;
           mh:hasDestinationSite ?siteObj ;
           mh:hasLogisticsFlowCode ?flowCode .
    ?siteObj mh:siteCode ?site .
}
GROUP BY ?site ?flowCode
ORDER BY ?site ?flowCode
```

#### 2. Validate AGI/DAS MOSB Leg Compliance

```sparql
PREFIX mh: <https://hvdc-project.com/ontology/material-handling/>

SELECT ?cargo ?cargoId ?site ?flowCode ?compliant
WHERE {
    ?cargo a mh:Cargo ;
           mh:cargoId ?cargoId ;
           mh:hasDestinationSite ?siteObj ;
           mh:hasLogisticsFlowCode ?flowCode .
    ?siteObj mh:siteCode ?site .
    FILTER(?site IN ("AGI", "DAS"))
    BIND(IF(?flowCode >= 3, "PASS", "FAIL") AS ?compliant)
}
ORDER BY ?compliant ?site
```

#### 3. Flow 5 (Incomplete) Materials at MOSB

```sparql
PREFIX mh: <https://hvdc-project.com/ontology/material-handling/>

SELECT ?cargo ?cargoId ?currentLocation ?daysSinceMOSB
WHERE {
    ?cargo a mh:Cargo ;
           mh:cargoId ?cargoId ;
           mh:hasLogisticsFlowCode 5 ;
           mh:currentLocation ?currentLocation ;
           mh:mosbArrivalDate ?mosbDate .
    FILTER(?currentLocation = mh:location/MOSB)
    BIND((NOW() - ?mosbDate) AS ?daysSinceMOSB)
}
ORDER BY DESC(?daysSinceMOSB)
```

#### 4. Average Flow Code by Material Type

```sparql
PREFIX mh: <https://hvdc-project.com/ontology/material-handling/>

SELECT ?cargoType (AVG(?flowCode) AS ?avgFlow) (COUNT(?cargo) AS ?count)
WHERE {
    ?cargo a mh:Cargo ;
           mh:cargoType ?cargoType ;
           mh:hasLogisticsFlowCode ?flowCode .
}
GROUP BY ?cargoType
ORDER BY DESC(?avgFlow)
```

### Material Handling KPIs with Flow Code

| KPI Metric | Target | Calculation | Flow Code Relevance |
|------------|--------|-------------|---------------------|
| **MOSB Utilization** | 80-90% | (Flow 3 + Flow 4) / Total | Offshore transport efficiency |
| **Direct Shipping (Onshore)** | 30-40% | Flow 1 / Total | MIR/SHU direct delivery rate |
| **Warehouse Efficiency** | 50-60% | (Flow 2 + Flow 4) / Total | Consolidation & staging |
| **AGI/DAS Compliance** | 100% | AGI/DAS with Flow ≥3 / AGI/DAS Total | Mandatory MOSB leg compliance |
| **Flow 5 Resolution Time** | <3 days | Avg(Site Assignment Date - MOSB Arrival) | Incomplete routing resolution |
| **Average Flow Code** | 2.5-3.0 | Σ(Flow × Count) / Total | Overall routing complexity |

### Integration with Material Handling Sections

#### Section 1 (Overview): Flow Code Introduction
- Port arrival and initial Flow Code classification
- Phase A vs Phase B routing patterns

#### Section 3 (Storage & Inland): Flow 1, 2, 4
- DSV Indoor/AAA Storage → Flow 2, 4 (warehouse leg)
- Direct MIR/SHU delivery → Flow 1

#### Section 4 (Offshore Marine): Flow 3, 4
- MOSB staging operations
- LCT/barge transport to AGI/DAS
- Mandatory MOSB leg enforcement

#### Section 5 (Site Receiving): Flow Code Completion
- Final delivery confirmation
- Flow Code status update to "Delivered"

#### Section 6 (Transformer): Flow 3, 4 (Heavy Equipment)
- Specialized heavy equipment always via MOSB
- AGI transformer installation projects

#### Section 7 (Bulk Cargo): Flow 3, 4 (Bulk Operations)
- Bulk cargo consolidation at MOSB
- Barge loading and seafastening

---

## Table of Contents

1. [Overview](#section-1-overview) - Overall logistics workflow and port information
2. [Customs Clearance](#section-2-customs-clearance) - Customs procedures and documentation
3. [Storage & Inland Transportation](#section-3-storage--inland-transportation) - Storage standards and inland transport
4. [Offshore Marine Transportation](#section-4-offshore-marine-transportation) - LCT operations and MOSB procedures
5. [Site Receiving](#section-5-site-receiving) - Material inspection and issuance
6. [Transformer Handling](#section-6-transformer-handling) - Specialized transformer operations
7. [Bulk Cargo Operations](#section-7-bulk-cargo-operations) - Integrated bulk cargo handling

---

## Section 1: Overview

### Source

- **Original File**: 2_EXT-08A-hvdc-material-handling-overview.md
- **Version**: unified-1.0
- **Date**: 2024-11-19

## Part 1: Domain Ontology

### Core Classes

```turtle
@prefix hvdc: <https://hvdc-project.com/ontology/material-handling/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

@prefix hvdc: <https://hvdc-project.com/ontology/material-handling/> .

hvdc:Project a owl:Class ;
    rdfs:label "Project" ;
    rdfs:comment "Represents the HVDC project entity." .

hvdc:Phase a owl:Class ;
    rdfs:label "Phase" ;
    rdfs:comment "Logistics phases (A: Import, B: Offshore)." .

hvdc:Port a owl:Class ;
    rdfs:label "Port" ;
    rdfs:comment "Ports for cargo arrival (Khalifa, Zayed, Jebel Ali)." .

hvdc:MOSB a owl:Class ;
    rdfs:label "MOSB" ;
    rdfs:comment "Mussafah Offshore Supply Base - central logistics hub." .

hvdc:Site a owl:Class ;
    rdfs:label "Site" ;
    rdfs:comment "Onshore (MIR, SHU) and Offshore (DAS, AGI) sites." .

hvdc:Cargo a owl:Class ;
    rdfs:label "Cargo" ;
    rdfs:comment "Materials being handled in logistics operations." .
```

\```turtle
mh:LogisticsFlow a owl:Class ;
    rdfs:label "LogisticsFlow" ;
    rdfs:comment "Class representing logisticsflow" .

mh:Port a owl:Class ;
    rdfs:label "Port" ;
    rdfs:comment "Class representing port" .

mh:StorageLocation a owl:Class ;
    rdfs:label "StorageLocation" ;
    rdfs:comment "Class representing storagelocation" .

mh:Project a owl:Class ;
    rdfs:label "Project" ;
    rdfs:comment "Class representing project" .
\```

### Data Properties

```turtle
hvdc:hasPhase a owl:ObjectProperty ;
    rdfs:domain hvdc:Project ;
    rdfs:range hvdc:Phase .

hvdc:involves a owl:ObjectProperty ;
    rdfs:domain hvdc:Phase ;
    rdfs:range [ owl:unionOf (hvdc:Port hvdc:MOSB hvdc:Site) ] .

hvdc:handles a owl:ObjectProperty ;
    rdfs:domain hvdc:Port ;
    rdfs:range hvdc:Cargo .

hvdc:consolidates a owl:ObjectProperty ;
    rdfs:domain hvdc:MOSB ;
    rdfs:range hvdc:Cargo .

hvdc:dispatches a owl:ObjectProperty ;
    rdfs:domain hvdc:MOSB ;
    rdfs:range hvdc:Site .

hvdc:receives a owl:ObjectProperty ;
    rdfs:domain hvdc:Site ;
    rdfs:range hvdc:Cargo .

hvdc:projectName a owl:DatatypeProperty ;
    rdfs:domain hvdc:Project ;
    rdfs:range xsd:string .

hvdc:date a owl:DatatypeProperty ;
    rdfs:domain hvdc:Project ;
    rdfs:range xsd:date .

hvdc:phaseType a owl:DatatypeProperty ;
    rdfs:domain hvdc:Phase ;
    rdfs:range xsd:string .

hvdc:name a owl:DatatypeProperty ;
    rdfs:domain [ owl:unionOf (hvdc:Port hvdc:Site) ] ;
    rdfs:range xsd:string .

hvdc:type a owl:DatatypeProperty ;
    rdfs:domain [ owl:unionOf (hvdc:Port hvdc:Site hvdc:Cargo) ] ;
    rdfs:range xsd:string .

hvdc:areaSqm a owl:DatatypeProperty ;
    rdfs:domain [ owl:unionOf (hvdc:MOSB hvdc:Site) ] ;
    rdfs:range xsd:decimal .
```

\```turtle
mh:has_logisticsflowId a owl:DatatypeProperty ;
    rdfs:label "has logisticsflow ID" ;
    rdfs:domain mh:LogisticsFlow ;
    rdfs:range xsd:string .

mh:has_portId a owl:DatatypeProperty ;
    rdfs:label "has port ID" ;
    rdfs:domain mh:Port ;
    rdfs:range xsd:string .

mh:has_storagelocationId a owl:DatatypeProperty ;
    rdfs:label "has storagelocation ID" ;
    rdfs:domain mh:StorageLocation ;
    rdfs:range xsd:string .

\```

### Object Properties

\```turtle
# Example object properties
mh:locatedAt a owl:ObjectProperty ;
    rdfs:label "located at" ;
    rdfs:domain mh:Material ;
    rdfs:range mh:StorageLocation .
\```

---

## Part 2: Constraints & Validation

### SHACL Constraints

```turtle
hvdc:ProjectShape a sh:NodeShape ;
    sh:targetClass hvdc:Project ;
    sh:property [
        sh:path hvdc:projectName ;
        sh:minCount 1 ;
        sh:message "Project must have a name."
    ] ;
    sh:property [
        sh:path hvdc:date ;
        sh:minCount 1 ;
        sh:message "Project must have a date."
    ] .

hvdc:PhaseShape a sh:NodeShape ;
    sh:targetClass hvdc:Phase ;
    sh:property [
        sh:path hvdc:phaseType ;
        sh:in ("A" "B") ;
        sh:message "Phase type must be A or B."
    ] .

hvdc:PortShape a sh:NodeShape ;
    sh:targetClass hvdc:Port ;
    sh:property [
        sh:path hvdc:name ;
        sh:minCount 1 ;
        sh:message "Port must have a name."
    ] ;
    sh:property [
        sh:path hvdc:type ;
        sh:in ("Container" "Bulk" "Special") ;
        sh:message "Port type must be Container, Bulk, or Special."
    ] .

hvdc:MOSBShape a sh:NodeShape ;
    sh:targetClass hvdc:MOSB ;
    sh:property [
        sh:path hvdc:areaSqm ;
        sh:minInclusive 20000.0 ;
        sh:message "MOSB area must be at least 20,000 sqm."
    ] .

hvdc:SiteShape a sh:NodeShape ;
    sh:targetClass hvdc:Site ;
    sh:property [
        sh:path hvdc:name ;
        sh:minCount 1 ;
        sh:message "Site must have a name."
    ] ;
    sh:property [
        sh:path hvdc:type ;
        sh:in ("Onshore" "Offshore") ;
        sh:message "Site type must be Onshore or Offshore."
    ] ;
    sh:property [
        sh:path hvdc:areaSqm ;
        sh:minInclusive 10000.0 ;
        sh:message "Site laydown area must be at least 10,000 sqm."
    ] .
```

\```turtle
mh:LogisticsFlowShape a sh:NodeShape ;
    sh:targetClass mh:LogisticsFlow ;
    sh:property [
        sh:path mh:has_logisticsflowId ;
        sh:minCount 1 ;
        sh:message "LogisticsFlow must have ID"
    ] .

mh:PortShape a sh:NodeShape ;
    sh:targetClass mh:Port ;
    sh:property [
        sh:path mh:has_portId ;
        sh:minCount 1 ;
        sh:message "Port must have ID"
    ] .
\```

---

## Part 3: Examples & Queries

### JSON-LD Examples

```turtle
{
  "@context": {
    "hvdc": "https://hvdc-project.com/ontology/material-handling/",
    "owl": "http://www.w3.org/2002/07/owl#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#"
  },
  "@id": "hvdc:project-lightning",
  "@type": "hvdc:Project",
  "hvdc:projectName": "Independent Subsea HVDC System Project (Project Lightning)",
  "hvdc:date": "2024-11-19",
  "hvdc:hasPhase": [
    {
      "@type": "hvdc:Phase",
      "hvdc:phaseType": "A",
      "hvdc:involves": [
        {"@id": "hvdc:port-khalifa"},
        {"@id": "hvdc:port-zayed"}
      ]
    },
    {
      "@type": "hvdc:Phase",
      "hvdc:phaseType": "B",
      "hvdc:involves": [
        {"@id": "hvdc:mosb"},
        {"@id": "hvdc:site-das"}
      ]
    }
  ]
}
```

\```json
{
  "@context": {
    "mh": "https://hvdc-project.com/ontology/material-handling/",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#"
  },
  "@id": "mh:logisticsflow-001",
  "@type": "mh:LogisticsFlow",
  "mh:has_logisticsflowId": "MH-001",
  "mh:hasDescription": "Example logisticsflow"
}
\```

### SPARQL Queries

```turtle
PREFIX hvdc: <https://hvdc-project.com/ontology/material-handling/>

SELECT ?phaseType ?entityId
WHERE {
    ?project hvdc:hasPhase ?phase .
    ?phase hvdc:phaseType ?phaseType ;
           hvdc:involves ?entity .
    ?entity @id ?entityId .
}
ORDER BY ?phaseType
```

\```sparql
PREFIX mh: <https://hvdc-project.com/ontology/material-handling/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?logisticsflow ?description WHERE {
    ?logisticsflow a mh:LogisticsFlow .
    ?logisticsflow mh:hasDescription ?description .
}
LIMIT 10
\```

---



## Semantic KPI Layer

### Project Logistics KPIs
- **Phase Completion Rate**: Percentage of Phase A/B completions on schedule
- **Port Handling Efficiency**: Container/Bulk processing time vs. targets
- **MOSB Utilization**: Storage capacity utilization (%)
- **Site Receiving Timeliness**: Materials received vs. ETA
- **Document Compliance**: Customs clearance success rate (≥95%)


## Recommended Commands

/material-handling analyze --phase=A [Import stage analysis]
/material-handling predict-eta --site=MIR [ETA prediction with weather tie]
/material-handling kpi-dash --realtime [Real-time logistics dashboard]
/material-handling optimize-stowage --vessel=LCT [LCT stowage optimization]

---

## Original Content

### Main Text Content

### 1. Overview

### 1. Overview

Perform timely overseas and inland transportation for purchased materials.
DeugroKorea DSV UAE ADNOC L&S
Inland
### Shipping Customs Clearance Port Handling Storage LCT Site Offloading

### Transportation

A B
Overseas DAS / AGI
### 1. You can get comprehensive perspective of logistics in HVDC project. Port Remarks

### 2. Overseas importation (A stage) needs for customs clearance and port handling. Abu Dhabi Khalifa Container

### 3. Materials supplied in the UAE will be delivered to onshore Site. Abu Dhabi Mina zayed BULK

Dubai Jebel Ali CNTR/BULK
However, offshore site materials require B stage through using LCT.
### 4. When cargo arrives at the site, it is received according to the “Material Management Control

Procedure”.
5
### 1. Overview

UAE Port Information
- Heavy equipments in the Zayed Port, general containers in the Khalifa Port (Abu Dhabi)
- In special case suppliers will use via Jebel Ali free zone (Dubai)
- Offshore (DAS/AGI) marine transportation by ADNOC L&S (Mussafah base)
Zayed Port (ADB) Khalifa Port (ADB) Mussafah (ALS MOSB)
- Subsea Cable, Transformer, Land Cable - Most materials from overseas are imported in - Island material transportation base
- Heavy cargo operation containers. - ADNOC L&S (ALS) operation
- RORO berth for LCT or Barge - Container Terminal operation - Operation Yard (20,000sqm)
- SCT/JDN secured “storage area” - CCU (Cargo Carrying Unit) - Container, CCU
(Land cable, Transformer) total 80 ea
Addition
al
### Storage

Area
6
### 2. Customs Clearance


### Tables and Data

### Table 1

| 1. Overview |
| --- |

### Table 2

| 1. Overview |
| --- |
| Perform timely overseas and inland transportation for purchased materials.
DeugroKorea DSV UAE ADNOC L&S
Inland
Shipping Customs Clearance Port Handling Storage LCT Site Offloading
Transportation
A B
Overseas DAS / AGI
1. You can get comprehensive perspective of logistics in HVDC project. Port Remarks
2. Overseas importation (A stage) needs for customs clearance and port handling. Abu Dhabi Khalifa Container
3. Materials supplied in the UAE will be delivered to onshore Site. Abu Dhabi Mina zayed BULK
Dubai Jebel Ali CNTR/BULK
However, offshore site materials require B stage through using LCT.
4. When cargo arrives at the site, it is received according to the “Material Management Control
Procedure”.
5 |

### Table 3

| A |  |  |
| --- | --- | --- |
|  | A | Overseas |

### Table 4

| B |  |  |
| --- | --- | --- |
|  | B | DAS / AGI |

### Table 5

|  | Port | Remarks |
| --- | --- | --- |
| Abu Dhabi | Khalifa | Container |
| Abu Dhabi | Mina zayed | BULK |
| Dubai | Jebel Ali | CNTR/BULK |


*... and 2 more tables*

---

## Related Ontologies

- [Core Logistics Framework](../core/1_CORE-01-hvdc-core-framework.md)
- [Infrastructure Nodes](../core/1_CORE-02-hvdc-infra-nodes.md)
- [Warehouse Operations](../core/1_CORE-03-hvdc-warehouse-ops.md)


---

## Section 2: Customs Clearance

### Source

- **Original File**: 2_EXT-08B-hvdc-material-handling-customs.md
- **Version**: unified-1.0
- **Date**: 2024-11-19

## Part 1: Domain Ontology

### Core Classes

```turtle
@prefix hvdc: <https://hvdc-project.com/ontology/material-handling/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

hvdc:CustomsDeclaration a owl:Class ;
    rdfs:label "Customs Declaration" ;
    rdfs:comment "Customs clearance declaration process." .

hvdc:Document a owl:Class ;
    rdfs:label "Document" ;
    rdfs:comment "Shipping and customs documents (BL, Invoice, PL, CO)." .

hvdc:Consignee a owl:Class ;
    rdfs:label "Consignee" ;
    rdfs:comment "Recipient company (ADOPT/ADNOC codes)." .

hvdc:eDAS a owl:Class ;
    rdfs:label "eDAS System" ;
    rdfs:comment "Electronic Document Attestation System." .
```

\```turtle
mh:CustomsDocument a owl:Class ;
    rdfs:label "CustomsDocument" ;
    rdfs:comment "Class representing customsdocument" .

mh:AttestationInvoice a owl:Class ;
    rdfs:label "AttestationInvoice" ;
    rdfs:comment "Class representing attestationinvoice" .

mh:BLEndorsement a owl:Class ;
    rdfs:label "BLEndorsement" ;
    rdfs:comment "Class representing blendorsement" .

mh:CustomsDeclaration a owl:Class ;
    rdfs:label "CustomsDeclaration" ;
    rdfs:comment "Class representing customsdeclaration" .
\```

### Data Properties

```turtle
hvdc:submittedTo a owl:ObjectProperty ;
    rdfs:domain hvdc:Document ;
    rdfs:range hvdc:eDAS .

hvdc:endorses a owl:ObjectProperty ;
    rdfs:domain hvdc:Consignee ;
    rdfs:range hvdc:Document .

hvdc:declares a owl:ObjectProperty ;
    rdfs:domain hvdc:CustomsDeclaration ;
    rdfs:range hvdc:Document .

hvdc:codeNo a owl:DatatypeProperty ;
    rdfs:domain hvdc:CustomsDeclaration ;
    rdfs:range xsd:string .

hvdc:location a owl:DatatypeProperty ;
    rdfs:domain hvdc:CustomsDeclaration ;
    rdfs:range xsd:string .

hvdc:consigneeName a owl:DatatypeProperty ;
    rdfs:domain hvdc:Consignee ;
    rdfs:range xsd:string .
```

\```turtle
mh:has_customsdocumentId a owl:DatatypeProperty ;
    rdfs:label "has customsdocument ID" ;
    rdfs:domain mh:CustomsDocument ;
    rdfs:range xsd:string .

mh:has_attestationinvoiceId a owl:DatatypeProperty ;
    rdfs:label "has attestationinvoice ID" ;
    rdfs:domain mh:AttestationInvoice ;
    rdfs:range xsd:string .

mh:has_blendorsementId a owl:DatatypeProperty ;
    rdfs:label "has blendorsement ID" ;
    rdfs:domain mh:BLEndorsement ;
    rdfs:range xsd:string .

\```

### Object Properties

\```turtle
# Example object properties
mh:locatedAt a owl:ObjectProperty ;
    rdfs:label "located at" ;
    rdfs:domain mh:Material ;
    rdfs:range mh:StorageLocation .
\```

---

## Part 2: Constraints & Validation

### SHACL Constraints

```turtle
hvdc:CustomsDeclarationShape a sh:NodeShape ;
    sh:targetClass hvdc:CustomsDeclaration ;
    sh:property [
        sh:path hvdc:codeNo ;
        sh:minCount 1 ;
        sh:message "Customs declaration must have a code."
    ] .

hvdc:DocumentShape a sh:NodeShape ;
    sh:targetClass hvdc:Document ;
    sh:property [
        sh:path hvdc:type ;
        sh:in ("BL" "Invoice" "PL" "CO" "AWB") ;
        sh:message "Document type must be valid shipping/customs document."
    ] .

hvdc:ConsigneeShape a sh:NodeShape ;
    sh:targetClass hvdc:Consignee ;
    sh:property [
        sh:path hvdc:consigneeName ;
        sh:minCount 1 ;
        sh:message "Consignee must have a name."
    ] .
```

\```turtle
mh:CustomsDocumentShape a sh:NodeShape ;
    sh:targetClass mh:CustomsDocument ;
    sh:property [
        sh:path mh:has_customsdocumentId ;
        sh:minCount 1 ;
        sh:message "CustomsDocument must have ID"
    ] .

mh:AttestationInvoiceShape a sh:NodeShape ;
    sh:targetClass mh:AttestationInvoice ;
    sh:property [
        sh:path mh:has_attestationinvoiceId ;
        sh:minCount 1 ;
        sh:message "AttestationInvoice must have ID"
    ] .
\```

---

## Part 3: Examples & Queries

### JSON-LD Examples

```turtle
{
  "@context": {
    "hvdc": "https://hvdc-project.com/ontology/material-handling/"
  },
  "@id": "hvdc:customs-decl-001",
  "@type": "hvdc:CustomsDeclaration",
  "hvdc:codeNo": "CUSTOMS-ADNOC-47150",
  "hvdc:location": "Abu Dhabi",
  "hvdc:declares": {
    "@type": "hvdc:Document",
    "hvdc:type": "BL",
    "hvdc:submittedTo": "hvdc:edas-system"
  },
  "hvdc:endorses": {
    "@type": "hvdc:Consignee",
    "hvdc:consigneeName": "Abu Dhabi Offshore Power Transmission Company Limited LLC"
  }
}
```

\```json
{
  "@context": {
    "mh": "https://hvdc-project.com/ontology/material-handling/",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#"
  },
  "@id": "mh:customsdocument-001",
  "@type": "mh:CustomsDocument",
  "mh:has_customsdocumentId": "MH-001",
  "mh:hasDescription": "Example customsdocument"
}
\```

### SPARQL Queries

```turtle
PREFIX hvdc: <https://hvdc-project.com/ontology/material-handling/>

SELECT ?declarationCode ?location ?documentType
WHERE {
    ?declaration a hvdc:CustomsDeclaration ;
                 hvdc:codeNo ?declarationCode ;
                 hvdc:location ?location ;
                 hvdc:declares ?doc .
    ?doc hvdc:type ?documentType .
}
ORDER BY ?declarationCode
```

\```sparql
PREFIX mh: <https://hvdc-project.com/ontology/material-handling/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?customsdocument ?description WHERE {
    ?customsdocument a mh:CustomsDocument .
    ?customsdocument mh:hasDescription ?description .
}
LIMIT 10
\```

---



## Semantic KPI Layer

### Customs Clearance KPIs
- **Clearance Time**: Average time from submission to approval
- **Document Accuracy**: First-time approval rate (≥98%)
- **Duty Accuracy**: Duty calculation accuracy (100%)
- **Compliance Rate**: Regulations adherence (UAE customs)


## Recommended Commands

/customs-clearance verify --docs [Document validation]
/customs-clearance track --status [Status tracking]
/customs-clearance analyze --duty [Duty calculation analysis]

---

## Original Content

### Main Text Content

### 2. Customs Clearance

### Customs clearance is carried out in compliance with UAE customs regulations and

appropriate shipping documents.
### Shipping Document eDAS System BL Endorsement Customs Clearance Delivery

### - BL (Bill of lading) - Attestation Invoice - BL endorsement - Customs Declaration - Delivery plan

by ADOPT
### or AWB (Airway Bill) - QR code * Shipping document - Transportation

(only Stamp)
* Attestation Invoice
- Commercial Invoice * Review Commercial
* Consignee : ADOPT
### Invoice and Customs

- Packing List
approval
- CO (Certificate of Origin)
### 1. Consignee Name : Abu Dhabi Offshore Power Transmission Company Limited LLC.

Location Description Code No
### - ADNOC (47150) was used as Customs code.

Abu Dhabi ADNOC 47150
### 2. In case of import via Dubai, we will use ADOPT (Dubai) code.

Abu Dhabi ADOPT 1485718
- Contractor pay Duty and apply for reimbursement. Dubai ADOPT 89901
- e.g. ZENER (Fire Fighting materials), from Jebel Ali free zone
### 3. Once customs clearance is completed, the status will be shared to ADOPT for their information.

8
### 2. Customs Clearance

### eDAS (Attestation Invoice) Customs Declaration Duty payment Status

9
### 3. Storage & Inland Transportation

### 3. Storage & Inland Transportation

Materials that arrived at the site should be operated according to the “Material Management
### Control Procedure(SJT-19LT-QLT-PL-023)-05.Oct.2022”

### 1. Storage standards are operated according to Material Storage classification (Annex J)

### 2. In particular, materials from Hitachi are operated according to the standards settled by the

supplier. “operated' means that include all activities for offloading, material positioning and
storage, once cargos arrive at the site”
- It is specified in the “Case List” provided for each shipment.
### 3. Hitachi recommendation :

- Indoor : closed, controlled +5°to +40° C, maximum humidity 85%.
- Indoor heated : closed, controlled +15°to +25° C, maximum humidity 85%.
### 4. In addition, we plan to secure an indoor warehouse near MIR/SHU by September.

1
1
### 3. Storage & Inland Transportation

Delivery locations are designated and operated according to the characteristics of each site
and the conditions of storage.
Indoor warehouse Outdoor Yard Zayed port Yard MOSB Yard
- Temp controlled Indoor warehouse - Temporary storage for DAS/AGI - Temporary storage for DAS/AGI - Temporary storage for DAS/AGI
materials (eg. Hitachi) Transformer related materials
- Hitachi/Siemens electrical Materials
### - Mussafah Area (8,000sqm) - Port Storage (1,100sqm) - MOSB Storage (20,000sqm)

- Mussafah Area (6,000sqm)
- 10km from MOSB - While storage, preservation activity - Waiting for Loading operation
- 5km from MOSB
* Timely delivery as per installation * Timely delivery as per installation * Timely delivery as per installation
*SHU Indoor warehouse : 30th/Oct
time in sites time in sites time in sites
MIR Indoor warehouse : End of Nov
1
2

### Tables and Data

### Table 1

| 2. Customs Clearance |
| --- |
| Customs clearance is carried out in compliance with UAE customs regulations and
appropriate shipping documents.
Shipping Document eDAS System BL Endorsement Customs Clearance Delivery
- BL (Bill of lading) - Attestation Invoice - BL endorsement - Customs Declaration - Delivery plan
by ADOPT
or AWB (Airway Bill) - QR code * Shipping document - Transportation
(only Stamp)
* Attestation Invoice
- Commercial Invoice * Review Commercial
* Consignee : ADOPT
Invoice and Customs
- Packing List
approval
- CO (Certificate of Origin)
1. Consignee Name : Abu Dhabi Offshore Power Transmission Company Limited LLC.
Location Description Code No
- ADNOC (47150) was used as Customs code.
Abu Dhabi ADNOC 47150
2. In case of import via Dubai, we will use ADOPT (Dubai) code.
Abu Dhabi ADOPT 1485718
- Contractor pay Duty and apply for reimbursement. Dubai ADOPT 89901
- e.g. ZENER (Fire Fighting materials), from Jebel Ali free zone
3. Once customs clearance is completed, the status will be shared to ADOPT for their information.
8 |

### Table 2

| Location | Description | Code No |
| --- | --- | --- |
| Abu Dhabi | ADNOC | 47150 |
| Abu Dhabi | ADOPT | 1485718 |
| Dubai | ADOPT | 89901 |

### Table 3

| 2. Customs Clearance |
| --- |
| eDAS (Attestation Invoice) Customs Declaration Duty payment Status
9 |

### Table 4

| 3. Storage & Inland Transportation |
| --- |

### Table 5

| 3. Storage & Inland Transportation |
| --- |
| Materials that arrived at the site should be operated according to the “Material Management
Control Procedure(SJT-19LT-QLT-PL-023)-05.Oct.2022”
1. Storage standards are operated according to Material Storage classification (Annex J)
2. In particular, materials from Hitachi are operated according to the standards settled by the
supplier. “operated' means that include all activities for offloading, material positioning and
storage, once cargos arrive at the site”
- It is specified in the “Case List” provided for each shipment.
3. Hitachi recommendation :
- Indoor : closed, controlled +5°to +40° C, maximum humidity 85%.
- Indoor heated : closed, controlled +15°to +25° C, maximum humidity 85%.
4. In addition, we plan to secure an indoor warehouse near MIR/SHU by September.
1
1 |


*... and 1 more tables*

---

## Related Ontologies

- [Core Logistics Framework](../core/1_CORE-01-hvdc-core-framework.md)
- [Infrastructure Nodes](../core/1_CORE-02-hvdc-infra-nodes.md)
- [Warehouse Operations](../core/1_CORE-03-hvdc-warehouse-ops.md)


---

## Section 3: Storage & Inland Transportation

### Source

- **Original File**: 2_EXT-08C-hvdc-material-handling-storage.md
- **Version**: unified-1.0
- **Date**: 2024-11-19

## Part 1: Domain Ontology

### Core Classes

```turtle
@prefix hvdc: <https://hvdc-project.com/ontology/material-handling/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

hvdc:Storage a owl:Class ;
    rdfs:label "Storage Facility" ;
    rdfs:comment "Storage facility (Indoor/Outdoor/Port/MOSB yards) - Indoor warehouses (6,000-8,000 sqm) for sensitive materials, outdoor yards for general cargo." .

hvdc:Laydown a owl:Class ;
    rdfs:label "Laydown Area" ;
    rdfs:comment "Site laydown areas (MIR: 35,006㎡, SHU: 10,556㎡, DAS: 35,840㎡, AGI: 47,198㎡)" .

hvdc:InlandTransport a owl:Class ;
    rdfs:label "Inland Transport" ;
    rdfs:comment "Inland transportation operations requiring DOT permit for >90t heavy equipment (Transformers, Spare Cable)" .

hvdc:Preservation a owl:Class ;
    rdfs:label "Material Preservation" ;
    rdfs:comment "Material preservation following Hitachi guidelines (Indoor: +5° to +40°C, RH ≤85%; Indoor heated: +15° to +25°C)" .
```

### Core Properties

```turtle
hvdc:follows a owl:ObjectProperty ;
    rdfs:domain hvdc:Storage ;
    rdfs:range hvdc:Procedure ;
    rdfs:comment "Storage follows Material Management Control Procedure and Annex J classification." .

hvdc:hosts a owl:ObjectProperty ;
    rdfs:domain [ owl:unionOf (hvdc:Storage hvdc:Laydown) ] ;
    rdfs:range hvdc:Cargo ;
    rdfs:comment "Storage location hosts cargo materials." .

hvdc:transports a owl:ObjectProperty ;
    rdfs:domain hvdc:InlandTransport ;
    rdfs:range hvdc:Cargo ;
    rdfs:comment "Inland transport handles cargo delivery." .

hvdc:storageType a owl:DatatypeProperty ;
    rdfs:domain hvdc:Storage ;
    rdfs:range xsd:string ;
    rdfs:comment "Storage type: Indoor/Outdoor/Port/MOSB Yard." .

hvdc:areaSqm a owl:DatatypeProperty ;
    rdfs:domain [ owl:unionOf (hvdc:Storage hvdc:Laydown) ] ;
    rdfs:range xsd:decimal ;
    rdfs:comment "Storage/laydown area in square meters." .

hvdc:tempRange a owl:DatatypeProperty ;
    rdfs:domain hvdc:Preservation ;
    rdfs:range xsd:string ;
    rdfs:comment "Temperature range (e.g., +5° to +40°C)." .

hvdc:humidityMax a owl:DatatypeProperty ;
    rdfs:domain hvdc:Preservation ;
    rdfs:range xsd:decimal ;
    rdfs:comment "Maximum relative humidity (e.g., 85%)." .

hvdc:permitRequired a owl:DatatypeProperty ;
    rdfs:domain hvdc:InlandTransport ;
    rdfs:range xsd:boolean ;
    rdfs:comment "Whether DOT permit is required." .
```

---

## Part 2: Constraints & Validation

### SHACL Constraints

```turtle
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix hvdc: <https://hvdc-project.com/ontology/material-handling/> .

hvdc:StorageShape a sh:NodeShape ;
    sh:targetClass hvdc:Storage ;
    sh:property [
        sh:path hvdc:storageType ;
        sh:in ("Indoor" "Outdoor" "Port" "MOSB Yard") ;
        sh:message "Storage type must be Indoor, Outdoor, Port, or MOSB Yard."
    ] ;
    sh:property [
        sh:path hvdc:areaSqm ;
        sh:minInclusive 1000.0 ;
        sh:message "Storage area must be at least 1,000 sqm."
    ] .

hvdc:LaydownShape a sh:NodeShape ;
    sh:targetClass hvdc:Laydown ;
    sh:property [
        sh:path hvdc:areaSqm ;
        sh:minInclusive 10000.0 ;
        sh:message "Laydown area must be at least 10,000 sqm (per site requirements)."
    ] .

hvdc:PreservationShape a sh:NodeShape ;
    sh:targetClass hvdc:Preservation ;
    sh:property [
        sh:path hvdc:humidityMax ;
        sh:maxInclusive 85.0 ;
        sh:message "Maximum humidity must not exceed 85% (Hitachi requirement)."
    ] .

hvdc:InlandTransportShape a sh:NodeShape ;
    sh:targetClass hvdc:InlandTransport ;
    sh:property [
        sh:path hvdc:permitRequired ;
        sh:description "DOT permit required for cargo >90t."
    ] .
```

---

## Part 3: Examples & Queries

### JSON-LD Examples

**Indoor Warehouse Storage Example**

```json
{
  "@context": {
    "hvdc": "https://hvdc-project.com/ontology/material-handling/"
  },
  "@id": "hvdc:indoor-warehouse-mir",
  "@type": "hvdc:Storage",
  "hvdc:storageType": "Indoor",
  "hvdc:areaSqm": 8000,
  "hvdc:follows": {
    "@id": "hvdc:procedure-annex-j"
  },
  "hvdc:hosts": [
    {
      "@id": "hvdc:cargo-hitachi",
      "hvdc:type": "Electrical Equipment",
      "hvdc:requiresPreservation": {
        "@type": "hvdc:Preservation",
        "hvdc:tempRange": "+5 to +40°C",
        "hvdc:humidityMax": 85
      }
    }
  ]
}
```

**Laydown Area Example**

```json
{
  "@context": {
    "hvdc": "https://hvdc-project.com/ontology/material-handling/"
  },
  "@id": "hvdc:laydown-mir",
  "@type": "hvdc:Laydown",
  "hvdc:areaSqm": 35006,
  "hvdc:site": "MIR",
  "hvdc:dimensions": "373m x 193m"
}
```

### SPARQL Queries

**Available Storage Capacity Query**

```sparql
PREFIX hvdc: <https://hvdc-project.com/ontology/material-handling/>

SELECT ?site ?type ?areaSqm ?available
WHERE {
    ?storage a hvdc:Storage ;
             hvdc:areaSqm ?areaSqm ;
             hvdc:storageType ?type .
    OPTIONAL {
        ?storage hvdc:hosts ?cargo .
        ?cargo hvdc:weight ?weight .
    }
    BIND(COALESCE(?areaSqm - SUM(?weight * 0.01), ?areaSqm) AS ?available)
}
GROUP BY ?storage ?site ?type ?areaSqm
HAVING (?available > 1000)
ORDER BY DESC(?available)
```

**Preservation Compliance Check**

```sparql
PREFIX hvdc: <https://hvdc-project.com/ontology/material-handling/>

SELECT ?storage ?cargoType ?tempRange ?humidityMax ?compliant
WHERE {
    ?storage a hvdc:Storage ;
             hvdc:hosts ?cargo ;
             hvdc:follows ?procedure .
    ?cargo hvdc:type ?cargoType ;
           hvdc:requiresPreservation ?preservation .
    ?preservation hvdc:tempRange ?tempRange ;
                  hvdc:humidityMax ?humidityMax .
    BIND(IF(?humidityMax <= 85 && REGEX(?tempRange, "\\+5"), "COMPLIANT", "NON-COMPLIANT") AS ?compliant)
}
```

---

## Semantic KPI Layer

### Storage Operations KPIs

- **Storage Utilization Rate**: Percentage of available vs. used storage space (target: 70-85%)
- **Preservation Compliance Rate**: Adherence to temperature/humidity guidelines (Hitachi: ≥95%)
- **Heavy Transport Lead Time**: DOT permit approval to delivery time (SLA: ≤7 days)
- **Laydown Availability**: Site laydown readiness vs. construction schedule (≥95% availability)

---

## Recommended Commands

`/storage-plan optimize --site=MIR` [Site laydown optimization for MIR facility]
`/preservation check --material=Hitachi` [Preservation compliance verification for Hitachi equipment]
`/inland-transport permit --weight=120t` [DOT permit application for heavy cargo transport]
`/laydown-capacity query --site=DAS` [Available laydown capacity at DAS site]
`/storage-classification validate --annex-j` [Storage classification validation per Annex J]

---

## Original Content

### Main Text Content

### 3. Storage & Inland Transportation

These are the operation plans laydowns in each site.
Laydowns will be operated flexibly depending on the construction sequence.
Mirfa Shuweihat DAS Al Ghallan
### 1. 35,006 ㎡ (373m x 193m) 1. 10,556 ㎡ (203m x 52m) 1. 35,840 ㎡ (280m x 120m) 1. 47,198 ㎡ (3 areas)

### 2. For efficiency of Transformer 2. Transportation plan must be 2. Ground condition is good for 2. 3 laydowns need to be managed

delivery and to minimize interference, managed effectively due to narrow stable operation. separately.
### access road will be adjusted. space. 3. Sequence operation efficiency must 3. Security must be strengthened.

### 3. Storage container which is certified 3. Storage container which is certified be considered. Efficiency of sequence operation

### fire protection and equipped AC will fire protection and equipped AC will 4. Storage container which is certified efficiency must be considered.

be prepared in each site for be prepared in each site for fire protection and equipped AC will
chemical, dangerous cargo. chemical, dangerous cargo. be prepared in each site for
chemical, dangerous cargo.
.
1
3
### 3. Storage & Inland Transportation

Heavy equipments (Transformer, Spare Cable) transportation need a special permit (more
than 90TON) from DOT (Department of Transport).
Mina Zayed port
### Unloading/Storage LCT / Barge Inland Transport Site Offloading

MuggaraqPort
- Heavy vessel in Mina - Offloading by Vessel - Proper Vessel arrange - MIR/SHU - Preparation of Stool/Beam
Zayed Port (DAS/AGI/MIR) crane (LCT or Barge)
- From Mussafah Jetty to - Laydown Compaction
- SHU TR in the Muggaraq - Modular Trailer - Loading onto Vessel Site by Road
- Secure access Road
port
### - Stool & Beam for Storage - Sea fastening • Road survey

### - Storage / Preservation

- Preservation (DAS/AGI) • MIR to Mussafah Jetty, • DOT Permit
Inland transportation
• DAS/AGI to Island
1
4
### 4. Offshore Marine Transportation

(ADNOC L&S)
### 4. Offshore Marine Transportation

Comply with ADNOC Offshore HSE standards and carry out yard operation, loading, and
marine transportation in accordance with MOSB internal procedures.
Exit Gate Pass
STEP
1-Focal Point
06
2-Documents
Preparing Exit 3-Exit Gate (cargo)
STEP
1-Project BL Material
05
2-SCT Material
3-Returning Material
Operation LOLO & RORO
STEP
1-Request Crane ( Riggers )
04
Preparing both sides Shipping 2-Request Forklift
STEP
3-Lifting tools if required
1-Shipping (AGI & DAS) 03
2-Inspection by Lifting team
3-BL from Both Islands
Planning Documentation
STEP
Gate Pass 1-SCT-LDA ( receiving )
02
STEP 2-LDA Offloading
1-Focal Point
2-Documents 01 3-Filtering Planning(AGI-DAS)
3-Gate in (Visitors & Vendor cargo )
1
6
### 4. Offshore Marine Transportation

Through smooth communication with ADNOC L&S(ALS), we strive to comply with safety
regulations and ensure timely transportation. In island, ALS will handle same procedure for
offloading, inland transportation and site offloading.
Sub-con Email PL
1-Planning
2-Documents & Certificates.
Shift to Shipping yard
3-Checking Certificates.
4-Enter Gate Pass 1-ALS team collection loading from SCT-
LDA
Planning 2-load to vessel Before
Safety Check !!
Planning & PL
Operation
1-LDA Planning.
Lifting inspection & Certificates
2-Request Offloading Operation.
Inspection
3-coordinate with Island team. 1-Visit Lifting Inspection Office.
2-checking Certificates.
3-inspection SCT-LDA.
Shipping Schedule 4-Approval stamp to PL.
5-Handover Approval PL with Certificates.
1-receiving Priority Cargo Plan.
2-Arranging next Shipment According
Nearest Vessel Schedule. Wells Nu & Vessel Confirm
3-Preparing PL and Share with Island Team
1-Share PL with Certificates of Cargo.

### Tables and Data

### Table 1

| 3. Storage & Inland Transportation |
| --- |
| These are the operation plans laydowns in each site.
Laydowns will be operated flexibly depending on the construction sequence.
Mirfa Shuweihat DAS Al Ghallan
1. 35,006 ㎡ (373m x 193m) 1. 10,556 ㎡ (203m x 52m) 1. 35,840 ㎡ (280m x 120m) 1. 47,198 ㎡ (3 areas)
2. For efficiency of Transformer 2. Transportation plan must be 2. Ground condition is good for 2. 3 laydowns need to be managed
delivery and to minimize interference, managed effectively due to narrow stable operation. separately.
access road will be adjusted. space. 3. Sequence operation efficiency must 3. Security must be strengthened.
3. Storage container which is certified 3. Storage container which is certified be considered. Efficiency of sequence operation
fire protection and equipped AC will fire protection and equipped AC will 4. Storage container which is certified efficiency must be considered.
be prepared in each site for be prepared in each site for fire protection and equipped AC will
chemical, dangerous cargo. chemical, dangerous cargo. be prepared in each site for
chemical, dangerous cargo.
.
1
3 |

### Table 2

| Mirfa | Shuweihat | DAS | Al Ghallan |
| --- | --- | --- | --- |
| 1. 35,006 ㎡ (373m x 193m)
2. For efficiency of Transformer
delivery and to minimize interference,
access road will be adjusted.
3. Storage container which is certified
fire protection and equipped AC will
be prepared in each site for
chemical, dangerous cargo. | 1. 10,556 ㎡ (203m x 52m)
2. Transportation plan must be
managed effectively due to narrow
space.
3. Storage container which is certified
fire protection and equipped AC will
be prepared in each site for
chemical, dangerous cargo. | 1. 35,840 ㎡ (280m x 120m)
2. Ground condition is good for
stable operation.
3. Sequence operation efficiency must
be considered.
4. Storage container which is certified
fire protection and equipped AC will
be prepared in each site for
chemical, dangerous cargo.
. | 1. 47,198 ㎡ (3 areas)
2. 3 laydowns need to be managed
separately.
3. Security must be strengthened.
Efficiency of sequence operation
efficiency must be considered. |

### Table 3

| 3. Storage & Inland Transportation |
| --- |
| Heavy equipments (Transformer, Spare Cable) transportation need a special permit (more
than 90TON) from DOT (Department of Transport).
Mina Zayed port
Unloading/Storage LCT / Barge Inland Transport Site Offloading
MuggaraqPort
- Heavy vessel in Mina - Offloading by Vessel - Proper Vessel arrange - MIR/SHU - Preparation of Stool/Beam
Zayed Port (DAS/AGI/MIR) crane (LCT or Barge)
- From Mussafah Jetty to - Laydown Compaction
- SHU TR in the Muggaraq - Modular Trailer - Loading onto Vessel Site by Road
- Secure access Road
port
- Stool & Beam for Storage - Sea fastening • Road survey
- Storage / Preservation
- Preservation (DAS/AGI) • MIR to Mussafah Jetty, • DOT Permit
Inland transportation
• DAS/AGI to Island
1
4 |

### Table 4

| 4. Offshore Marine Transportation
(ADNOC L&S) |
| --- |

### Table 5

| 4. Offshore Marine Transportation |
| --- |
| Comply with ADNOC Offshore HSE standards and carry out yard operation, loading, and
marine transportation in accordance with MOSB internal procedures.
Exit Gate Pass
STEP
1-Focal Point
06
2-Documents
Preparing Exit 3-Exit Gate (cargo)
STEP
1-Project BL Material
05
2-SCT Material
3-Returning Material
Operation LOLO & RORO
STEP
1-Request Crane ( Riggers )
04
Preparing both sides Shipping 2-Request Forklift
STEP
3-Lifting tools if required
1-Shipping (AGI & DAS) 03
2-Inspection by Lifting team
3-BL from Both Islands
Planning Documentation
STEP
Gate Pass 1-SCT-LDA ( receiving )
02
STEP 2-LDA Offloading
1-Focal Point
2-Documents 01 3-Filtering Planning(AGI-DAS)
3-Gate in (Visitors & Vendor cargo )
1
6 |


*... and 3 more tables*

---

## Related Ontologies

- [Core Logistics Framework](../core/1_CORE-01-hvdc-core-framework.md)
- [Infrastructure Nodes](../core/1_CORE-02-hvdc-infra-nodes.md)
- [Warehouse Operations](../core/1_CORE-03-hvdc-warehouse-ops.md)


---

## Section 4: Offshore Marine Transportation

### Source

- **Original File**: 2_EXT-08D-hvdc-material-handling-offshore.md
- **Version**: unified-1.0
- **Date**: 2024-11-19

## Part 1: Domain Ontology

### Core Classes

```turtle
@prefix hvdc: <https://hvdc-project.com/ontology/material-handling/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

hvdc:MarineTransport a owl:Class ;
    rdfs:label "Marine Transport" ;
    rdfs:comment "Offshore marine transportation via LCT (MOSB-DAS: 20hrs, MOSB-AGI: 10hrs)" .

hvdc:OperationStep a owl:Class ;
    rdfs:label "Operation Step" ;
    rdfs:comment "MOSB operation steps (Gate pass → Planning → Operation LOLO/RORO → Exit)" .

hvdc:Inspection a owl:Class ;
    rdfs:label "Lifting Inspection" ;
    rdfs:comment "Lifting inspection and safety checks at MOSB and island sites" .

hvdc:HSEStandard a owl:Class ;
    rdfs:label "HSE Standard" ;
    rdfs:comment "ADNOC Offshore HSE compliance standards for ALS operations" .
```

### Core Properties

```turtle
hvdc:compliesWith a owl:ObjectProperty ;
    rdfs:domain hvdc:MarineTransport ;
    rdfs:range hvdc:HSEStandard ;
    rdfs:comment "Marine transport complies with ADNOC Offshore HSE standards." .

hvdc:requires a owl:ObjectProperty ;
    rdfs:domain hvdc:OperationStep ;
    rdfs:range [ owl:unionOf (hvdc:Document hvdc:Permit) ] ;
    rdfs:comment "Operation step requires documentation and permits." .

hvdc:validates a owl:ObjectProperty ;
    rdfs:domain hvdc:Inspection ;
    rdfs:range hvdc:Cargo ;
    rdfs:comment "Inspection validates cargo condition." .

hvdc:voyageTime a owl:DatatypeProperty ;
    rdfs:domain hvdc:MarineTransport ;
    rdfs:range xsd:integer ;
    rdfs:comment "Voyage time in hours (e.g., MOSB-DAS: 20hrs)" .

hvdc:vesselType a owl:DatatypeProperty ;
    rdfs:domain hvdc:MarineTransport ;
    rdfs:range xsd:string ;
    rdfs:comment "Vessel type: LCT or Barge" .

hvdc:stepNo a owl:DatatypeProperty ;
    rdfs:domain hvdc:OperationStep ;
    rdfs:range xsd:integer ;
    rdfs:comment "Operation step number (1-6)." .

hvdc:operationType a owl:DatatypeProperty ;
    rdfs:domain hvdc:OperationStep ;
    rdfs:range xsd:string ;
    rdfs:comment "Operation type: LOLO or RORO" .
```

---

## Part 2: Constraints & Validation

### SHACL Constraints

```turtle
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix hvdc: <https://hvdc-project.com/ontology/material-handling/> .

hvdc:MarineTransportShape a sh:NodeShape ;
    sh:targetClass hvdc:MarineTransport ;
    sh:property [
        sh:path hvdc:vesselType ;
        sh:in ("LCT" "Barge") ;
        sh:message "Vessel type must be LCT or Barge."
    ] ;
    sh:property [
        sh:path hvdc:voyageTime ;
        sh:minInclusive 1 ;
        sh:message "Voyage time must be positive (minimum 1 hour)."
    ] .

hvdc:OperationStepShape a sh:NodeShape ;
    sh:targetClass hvdc:OperationStep ;
    sh:property [
        sh:path hvdc:stepNo ;
        sh:minInclusive 1 ;
        sh:maxInclusive 6 ;
        sh:message "Step number must be between 1 and 6."
    ] ;
    sh:property [
        sh:path hvdc:operationType ;
        sh:in ("LOLO" "RORO") ;
        sh:message "Operation type must be LOLO or RORO."
    ] ;
    sh:property [
        sh:path hvdc:requires ;
        sh:minCount 1 ;
        sh:message "Operation step must have required documentation."
    ] .

hvdc:HSEStandardShape a sh:NodeShape ;
    sh:targetClass hvdc:HSEStandard ;
    sh:property [
        sh:path hvdc:complianceLevel ;
        sh:minCount 1 ;
        sh:message "HSE standard must have compliance level."
    ] .
```

---

## Part 3: Examples & Queries

### JSON-LD Examples

**LCT Voyage Example**

```json
{
  "@context": {
    "hvdc": "https://hvdc-project.com/ontology/material-handling/"
  },
  "@id": "hvdc:voyage-mosb-das-001",
  "@type": "hvdc:MarineTransport",
  "hvdc:vesselType": "LCT",
  "hvdc:voyageTime": 20,
  "hvdc:route": "MOSB to DAS",
  "hvdc:compliesWith": {
    "@type": "hvdc:HSEStandard",
    "@id": "hvdc:hse-adnoc-offshore"
  },
  "hvdc:operationSteps": [
    {
      "@type": "hvdc:OperationStep",
      "hvdc:stepNo": 1,
      "hvdc:operationType": "Gate Pass",
      "hvdc:requires": ["Focal Point", "Documents", "Gate in"]
    },
    {
      "@type": "hvdc:OperationStep",
      "hvdc:stepNo": 4,
      "hvdc:operationType": "LOLO",
      "hvdc:requires": ["Crane Request", "Forklift Request", "Lifting tools"]
    }
  ]
}
```

**MOSB Operation Flow Example**

```json
{
  "@context": {
    "hvdc": "https://hvdc-project.com/ontology/material-handling/"
  },
  "@id": "hvdc:operation-mosb-001",
  "@type": "hvdc:OperationStep",
  "hvdc:stepNo": 3,
  "hvdc:operationType": "Shipping",
  "hvdc:focalPoint": "ALS team",
  "hvdc:requires": {
    "@type": "hvdc:Document",
    "hvdc:type": "Packing List"
  },
  "hvdc:validates": {
    "@type": "hvdc:Inspection",
    "hvdc:type": "Lifting"
  }
}
```

### SPARQL Queries

**Marine Transport Schedule Query**

```sparql
PREFIX hvdc: <https://hvdc-project.com/ontology/material-handling/>

SELECT ?voyage ?route ?voyageTime ?vesselType ?delays
WHERE {
    ?voyage a hvdc:MarineTransport ;
             hvdc:route ?route ;
             hvdc:voyageTime ?voyageTime ;
             hvdc:vesselType ?vesselType .
    OPTIONAL {
        ?voyage hvdc:hasDelay ?delays .
    }
}
ORDER BY ?route
```

**HSE Compliance Check Query**

```sparql
PREFIX hvdc: <https://hvdc-project.com/ontology/material-handling/>

SELECT ?operation ?stepNo ?hseCompliant ?requiredDocs
WHERE {
    ?operation a hvdc:OperationStep ;
                hvdc:stepNo ?stepNo ;
                hvdc:requires ?document .
    ?operation hvdc:compliesWith ?hse .
    ?hse a hvdc:HSEStandard .
    OPTIONAL {
        ?operation hvdc:requires ?docList .
        ?docList hvdc:type ?requiredDocs .
    }
    BIND(IF(BOUND(?hse), "COMPLIANT", "NON-COMPLIANT") AS ?hseCompliant)
}
ORDER BY ?stepNo
```

---

## Semantic KPI Layer

### Offshore Marine Operations KPIs

- **Voyage Efficiency Rate**: Actual vs. planned transit times (MOSB-DAS: 20hrs, MOSB-AGI: 10hrs)
- **HSE Compliance Score**: ADNOC Offshore HSE adherence (target: ≥95%)
- **LOLO/RORO Operation Time**: Average operation duration per step (target: ≤4hrs)
- **Document Completeness Rate**: Required documentation availability (target: 100%)

---

## Recommended Commands

`/marine-transport schedule --voyage=MOSB-DAS` [Real-time LCT voyage scheduling from MOSB to DAS island]
`/hse-check validate --operation=LOLO` [HSE compliance validation for LOLO operations]
`/lct-tracking realtime --vessel=LCT-001` [Real-time LCT vessel tracking and status updates]
`/mosb-operation status --step=4` [MOSB operation step status and progress]
`/voyage-delay analyze --route=MOSB-AGI` [Voyage delay analysis and root cause identification]

---

## Original Content

### Main Text Content

### 5. Site Receiving

### 5. Site Receiving

Materials arriving on site are operated according to the “Material Management Control
### Procedure(SJT-19LT-QLT-PL-023)-05.Oct.2022”

### 1. Upon arrive the materials, inspection (with QA/QC) is performed while unpacking

at the time of installation.
### 2. Visual inspection is performed on materials that arrive before construction, and

when materials are released during construction, inspection is performed as above.
### 3. Upon request for inspection, following document will be attached

- Material Inspection Request (Logistic – Construction – Quality – OE)
### - Material Receiving inspection Report

### - Materials Receiving Inspection

- ITP (Inspection and Test plan)
- MAR (Material Approval Request)
- Product test certificate
### 4. As per the site requirement relevant Sub Con Submitting MRS (Material Request

Slip) with relevant drawings.
### 5. After verification and approval from Construction Team proceeding for MIS

(Material Issue Slip) as per the availability of materials.
### 6. Physical issuance of materials to as per the MIS and getting receiving

acknowledgement from Sub con representative in MIS
2
0
### 5. Site Receiving

Materials arriving on site are operated according to the “Material Management Control
### Procedure(SJT-19LT-QLT-PL-023)-05.Oct.2022”

Delivery Plan / Schedule
SUPPLIER / VENDOR SCT PREPARATION HSE SAFETY
•Supplier to provide the •Review packing List •HSE standards -to ensure safety of
workplace and organized process in
### delivery plan which includes •Material Storage Code

receiving materials, equipment, and
the following:
•Alignment of Equipment personnel on-site.
•➢ Packing List availability vs the proposed •➢Verification and Documentation:
Methodology > MS / FRA
•➢Delivery Truck Quantity delivery plan of the Supplier
•➢Hazard Assessment
•➢ETA at Site / Vendor
•➢Control of Entry Points
•➢Target Delivery •Unloading Location •➢Inspection and Compliance
Completion •➢Clear Communication
2
1
### 5. Site Receiving

### Material Receiving

PACKING LIST, LOADING & PERMITS, LIFTING EQUIPMENT & MATERIAL RECEIVING
MANPOWER
UNLOADING CHECKLIST REPORT & INSPECTION
• Collection of Packing • Permit to Work [PTW] •SCT to conduct material
receiving inspection
List, Delivery Notes, and • Tool Box Talk
•Thorough checking of Material
other shipping
• Inspection of Lifting received vs. Packing list.
documents
Equipment and Lifting •SCT to provide MRR if cargo
• Collection of Loading Gears found in good condition and
and Unloading Checklist acceptable
2
2
### 5. Site Receiving

Request for Inspection
MATERIAL IN GOOD DOCUMENTS TO JOINT INSPECTION WITH
CONDITION OE
PREPARE
•Material Inspection Request
• If the cargo is found to be • Joint inspection
(Logistic – Construction –
in good condition and the Quality – OE) together with OE to
### quantity matches packing •➢Material Receiving inspection ensure that material

Report
list, proceed with the received at site meet
### •➢Materials Receiving Inspection

request for inspection •➢ITP (Inspection and Test plan) the required standards
•➢MAR (Material Approval
and specifications as
Request)
per ITP / MAR
•➢Product test certificate [MTC,
SDS, TDS]
2
3
### 5. Site Receiving

Overage, Shortage & Damage Report
OVERAGE, SHORTAGE,
DOCUMENTS TO REVIEW and ACTION
DAMAGE
PREPARE
•If found any overage, shortage,
• Overage, Shortage, • OSD Report shall be
damage, during receiving, SCT
to file an OSDR Damage Report sent to the QA/QC add
documentation. Form Contranctor’s PMO for
•Thorough inspection carried • Commercial Invoice / subsequent action such
out together with Engineering Packing List as claim to the Vendor
Team, and QA/QC Team
/ Supplier
• Delivery Note
• Photo Proof

### Tables and Data

### Table 1

| 5. Site Receiving |
| --- |

### Table 2

| 5. Site Receiving |
| --- |
| Materials arriving on site are operated according to the “Material Management Control
Procedure(SJT-19LT-QLT-PL-023)-05.Oct.2022”
1. Upon arrive the materials, inspection (with QA/QC) is performed while unpacking
at the time of installation.
2. Visual inspection is performed on materials that arrive before construction, and
when materials are released during construction, inspection is performed as above.
3. Upon request for inspection, following document will be attached
- Material Inspection Request (Logistic – Construction – Quality – OE)
- Material Receiving inspection Report
- Materials Receiving Inspection
- ITP (Inspection and Test plan)
- MAR (Material Approval Request)
- Product test certificate
4. As per the site requirement relevant Sub Con Submitting MRS (Material Request
Slip) with relevant drawings.
5. After verification and approval from Construction Team proceeding for MIS
(Material Issue Slip) as per the availability of materials.
6. Physical issuance of materials to as per the MIS and getting receiving
acknowledgement from Sub con representative in MIS
2
0 |

### Table 3

| 5. Site Receiving |
| --- |
| Materials arriving on site are operated according to the “Material Management Control
Procedure(SJT-19LT-QLT-PL-023)-05.Oct.2022”
Delivery Plan / Schedule
SUPPLIER / VENDOR SCT PREPARATION HSE SAFETY
•Supplier to provide the •Review packing List •HSE standards -to ensure safety of
workplace and organized process in
delivery plan which includes •Material Storage Code
receiving materials, equipment, and
the following:
•Alignment of Equipment personnel on-site.
•➢ Packing List availability vs the proposed •➢Verification and Documentation:
Methodology > MS / FRA
•➢Delivery Truck Quantity delivery plan of the Supplier
•➢Hazard Assessment
•➢ETA at Site / Vendor
•➢Control of Entry Points
•➢Target Delivery •Unloading Location •➢Inspection and Compliance
Completion •➢Clear Communication
2
1 |

### Table 4

| 5. Site Receiving |
| --- |
| Material Receiving
PACKING LIST, LOADING & PERMITS, LIFTING EQUIPMENT & MATERIAL RECEIVING
MANPOWER
UNLOADING CHECKLIST REPORT & INSPECTION
• Collection of Packing • Permit to Work [PTW] •SCT to conduct material
receiving inspection
List, Delivery Notes, and • Tool Box Talk
•Thorough checking of Material
other shipping
• Inspection of Lifting received vs. Packing list.
documents
Equipment and Lifting •SCT to provide MRR if cargo
• Collection of Loading Gears found in good condition and
and Unloading Checklist acceptable
2
2 |

### Table 5

| 5. Site Receiving |
| --- |
| Request for Inspection
MATERIAL IN GOOD DOCUMENTS TO JOINT INSPECTION WITH
CONDITION OE
PREPARE
•Material Inspection Request
• If the cargo is found to be • Joint inspection
(Logistic – Construction –
in good condition and the Quality – OE) together with OE to
quantity matches packing •➢Material Receiving inspection ensure that material
Report
list, proceed with the received at site meet
•➢Materials Receiving Inspection
request for inspection •➢ITP (Inspection and Test plan) the required standards
•➢MAR (Material Approval
and specifications as
Request)
per ITP / MAR
•➢Product test certificate [MTC,
SDS, TDS]
2
3 |


*... and 2 more tables*

---

## Related Ontologies

- [Core Logistics Framework](../core/1_CORE-01-hvdc-core-framework.md)
- [Infrastructure Nodes](../core/1_CORE-02-hvdc-infra-nodes.md)
- [Warehouse Operations](../core/1_CORE-03-hvdc-warehouse-ops.md)


---

## Section 5: Site Receiving

### Source

- **Original File**: 2_EXT-08E-hvdc-material-handling-site-receiving.md
- **Version**: unified-1.0
- **Date**: 2024-11-19

## Part 1: Domain Ontology

### Core Classes

```turtle
@prefix hvdc: <https://hvdc-project.com/ontology/material-handling/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

hvdc:Receiving a owl:Class ;
    rdfs:label "Material Receiving" ;
    rdfs:comment "Site material receiving process following Material Management Control Procedure (Good/OSD classification)" .

hvdc:RequestSlip a owl:Class ;
    rdfs:label "Request Slip" ;
    rdfs:comment "Material request/issuance slips (MRS: Material Request Slip, MIS: Material Issue Slip)" .

hvdc:Inspection a owl:Class ;
    rdfs:label "Material Inspection" ;
    rdfs:comment "Material inspection documents (MRR: Material Receiving Report, MRI: Material Receiving Inspection, ITP: Inspection Test Plan, MAR: Material Approval Request)" .
```

### Core Properties

```turtle
hvdc:requires a owl:ObjectProperty ;
    rdfs:domain hvdc:Receiving ;
    rdfs:range hvdc:Inspection ;
    rdfs:comment "Receiving requires joint inspection with OE/QA." .

hvdc:approves a owl:ObjectProperty ;
    rdfs:domain hvdc:RequestSlip ;
    rdfs:range hvdc:Team ;
    rdfs:comment "Request slip approved by Construction Team." .

hvdc:appliesTo a owl:ObjectProperty ;
    rdfs:domain hvdc:Preservation ;
    rdfs:range hvdc:Cargo ;
    rdfs:comment "Preservation guidelines apply to cargo." .

hvdc:receivingType a owl:DatatypeProperty ;
    rdfs:domain hvdc:Receiving ;
    rdfs:range xsd:string ;
    rdfs:comment "Receiving type: Good or OSD (Overage, Shortage, Damage)." .

hvdc:slipType a owl:DatatypeProperty ;
    rdfs:domain hvdc:RequestSlip ;
    rdfs:range xsd:string ;
    rdfs:comment "Slip type: MRS or MIS." .

hvdc:inspectionResult a owl:DatatypeProperty ;
    rdfs:domain hvdc:Inspection ;
    rdfs:range xsd:string ;
    rdfs:comment "Inspection result status." .
```

---

## Part 2: Constraints & Validation

### SHACL Constraints

```turtle
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix hvdc: <https://hvdc-project.com/ontology/material-handling/> .

hvdc:ReceivingShape a sh:NodeShape ;
    sh:targetClass hvdc:Receiving ;
    sh:property [
        sh:path hvdc:receivingType ;
        sh:in ("Good" "OSD") ;
        sh:message "Receiving type must be Good or OSD."
    ] ;
    sh:property [
        sh:path hvdc:requires ;
        sh:minCount 1 ;
        sh:message "Receiving must have required inspection."
    ] .

hvdc:RequestSlipShape a sh:NodeShape ;
    sh:targetClass hvdc:RequestSlip ;
    sh:property [
        sh:path hvdc:slipType ;
        sh:in ("MRS" "MIS") ;
        sh:message "Slip type must be MRS or MIS."
    ] ;
    sh:property [
        sh:path hvdc:approves ;
        sh:minCount 1 ;
        sh:message "Request slip must have approving team."
    ] .

hvdc:InspectionShape a sh:NodeShape ;
    sh:targetClass hvdc:Inspection ;
    sh:property [
        sh:path hvdc:inspectionResult ;
        sh:minCount 1 ;
        sh:message "Inspection must have result status."
    ] .
```

---

## Part 3: Examples & Queries

### JSON-LD Examples

**Material Receiving with MRR Example**

```json
{
  "@context": {
    "hvdc": "https://hvdc-project.com/ontology/material-handling/"
  },
  "@id": "hvdc:receiving-001",
  "@type": "hvdc:Receiving",
  "hvdc:receivingType": "Good",
  "hvdc:requires": {
    "@type": "hvdc:Inspection",
    "@id": "hvdc:inspection-mrr-001",
    "hvdc:type": "MRR",
    "hvdc:inspectionResult": "Accepted"
  },
  "hvdc:cargo": {
    "@id": "hvdc:cargo-hitachi-001",
    "hvdc:type": "Electrical Equipment"
  }
}
```

**Material Request Slip Example**

```json
{
  "@context": {
    "hvdc": "https://hvdc-project.com/ontology/material-handling/"
  },
  "@id": "hvdc:slip-mrs-001",
  "@type": "hvdc:RequestSlip",
  "hvdc:slipType": "MRS",
  "hvdc:approves": {
    "@type": "hvdc:Team",
    "@id": "hvdc:team-construction"
  },
  "hvdc:status": "Approved"
}
```

### SPARQL Queries

**Receiving Status Query**

```sparql
PREFIX hvdc: <https://hvdc-project.com/ontology/material-handling/>

SELECT ?receiving ?type ?inspectionResult ?status
WHERE {
    ?receiving a hvdc:Receiving ;
               hvdc:receivingType ?type ;
               hvdc:requires ?inspection .
    ?inspection hvdc:inspectionResult ?inspectionResult .
    OPTIONAL {
        ?receiving hvdc:relatedTo ?slip .
        ?slip hvdc:status ?status .
    }
}
ORDER BY ?type
```

**OSD Incident Report Query**

```sparql
PREFIX hvdc: <https://hvdc-project.com/ontology/material-handling/>

SELECT ?receiving ?cargoType ?osdReason ?severity
WHERE {
    ?receiving a hvdc:Receiving ;
               hvdc:receivingType "OSD" ;
               hvdc:cargo ?cargo .
    ?cargo hvdc:type ?cargoType .
    ?receiving hvdc:hasDiscrepancy ?osdReason ;
               hvdc:severity ?severity .
}
ORDER BY DESC(?severity)
```

---

## Semantic KPI Layer

### Site Receiving KPIs

- **First-Time Acceptance Rate**: Percentage of cargo accepted without discrepancies (target: ≥90%)
- **Inspection Completion Time**: Average time from arrival to inspection completion (SLA: ≤24hrs)
- **OSD Incident Rate**: Overage, Shortage, Damage occurrences (target: ≤5%)
- **Request Slip Processing Time**: MRS to MIS issuance time (target: ≤48hrs)

---

## Recommended Commands

`/site-receiving inspect --cargo=TR-001` [Material inspection workflow for transformer cargo]
`/material-request generate --slip=MRS` [Material Request Slip generation and approval workflow]
`/preservation-check temperature --site=MIR` [Preservation temperature/humidity compliance check at site]
`/osd-report generate --type=damage` [OSD (Overage, Shortage, Damage) report generation]
`/inspection-document attach --type=ITP` [Joint inspection with OE/QA team, attach ITP/MAR documents]

---

---

## Original Content

### Main Text Content

### 5. Site Receiving

### Material Storage & Preservations

HANDLING &
INDOOR MATERIALS OUTDOOR &
PRESERVATION
OUTDOOR COVERED
•SCT to follow and implement
• The Manufacturer’s storage • Review of Manufacturer’s
### the Manufacturer’s storage instruction or guide shall be Storage Instructions and

instructions and guidelines reviewed before Guidelines
placing in storage and followed. • SCT to ensure that all OUTDOOR
•OUTDOOR,
• The air temperature shall be & OUTDOOR COVERED cases or
•OUTDOOR COVERED,
maintained as per boxes [HITACHI] are properly
•INDOOR Manufacturer’s Guidelines covered with tarpaulin or plastic
sheeting.
2
6
### 5. Site Receiving

FORMS
Loading & unloading checklist Material checklist
▪ For unloaded cargo, a visual check is
▪ For Loading and unloading checklist, this documents not only protect the cargo and the parties performed on the packaging and damage
involved in unloading works but also uphold the safety standards, and ensuring the compliance with status of the materials.
the transportation and safety regulation.
2
7
### 5. Site Receiving

FORMS
ITP
MRR
MAR
MRI
2
8
### 5. Site Receiving

FORMS
MATERIAL RECEIVING REPORT
MATERIAL REQUEST SLIP MATERIAL ISSUANCE SLIP
2
9
### 6. Material Handling

(Transformer)
### 6. Material Handling

Transformer Delivery Schedule [DAS Cluster]
▪ This transformer is manufactured in factory situated in Sweden.
▪ Hitachi transports to the relevant site. (SHU : Site, DAS: Zayed Port)
▪ Before arrival at the site, SCT prepares for receiving by submitting MS, approval and conducting FRA.
▪ Temporarily it is kept at Site or Zayed port before TR building complete
▪ During the storage, preservation is implemented according to Hitachi recommendations (Gauge measure - Dry air filling)
SHU DAS
Unit ETD ETA Arrival Port On-Site Unit ETD ETA Arrival Port On-Site
1 2024-04-09 2024-05-24 Mugharraq 2024-06-11 1 2024-02-19 2024-04-21 Mina Zayed 2024-11-03
2 2024-04-09 2024-05-24 Mugharraq 2024-06-11 2 2024-02-19 2024-04-21 Mina Zayed 2024-11-03
3 2024-04-09 2024-05-24 Mugharraq 2024-06-13 3 2024-07-11 2024-09-02 Mina Zayed Feb. 2025
4 2024-04-09 2024-05-24 Mugharraq 2024-06-13 4 2024-07-11 2024-09-02 Mina Zayed Feb. 2025
5 2024-05-16 2024-07-21 Mugharraq 2024-08-01 5 2024-07-11 2024-09-02 Mina Zayed Mar. 2025
6 2024-05-16 2024-07-21 Mugharraq 2024-08-01 6 2024-07-11 2024-09-02 Mina Zayed Mar. 2025
Spare 2024-05-16 2024-07-21 Mugharraq 2024-08-01 Spare 2024-07-11 2024-09-02 Mina Zayed Mar. 2025
3
1
### 6. Material Handling

Transformer Delivery Schedule [Zakum Cluster]
▪ This transformer is manufactured in a factory in Brazil.
▪ Hitachi is transporting to the relevant site. (MIR : Site, AGI: Zayed Port)
▪ Before arriving at the site, SCT prepare for receiving by submitting MS, approval and conducting FRA.
▪ Temporarily it is stored at Site or Zayed port before TR building is completed.
▪ During the storage, preservation is implemented according to Hitachi recommendations (Gauge measure – N2 gas flling)
MIR AGI
Unit ETD ETA Arrival Port On-Site Unit ETD ETA Arrival Port On-Site
1 2024-02-23 2024-03-31 Mina Zayed 2024-06-04 1 2024-08-01 2024-09-01 Mina Zayed Apr. 2025
2 2024-02-23 2024-03-31 Mina Zayed 2024-06-04 2 2024-08-01 2024-09-01 Mina Zayed Apr. 2025
3 2024-04-07 2024-04-29 Mina Zayed 2024-06-09 3 2024-09-30 2024-11-01 Mina Zayed May. 2025
4 2024-04-07 2024-04-29 Mina Zayed 2024-06-09 4 2024-09-30 2024-11-01 Mina Zayed May. 2025
5 2024-06-02 2024-07-25 Mina Zayed 2024-08-26 5 2024-09-30 2024-11-01 Mina Zayed May. 2025
6 2024-06-02 2024-07-25 Mina Zayed 2024-08-26 6 2024-10-25 2024-12-10 Mina Zayed Jun. 2025
Spare 2024-06-02 2024-07-25 Mina Zayed 2024-09-07 Spare 2024-10-25 2024-12-10 Mina Zayed Jun. 2025
3
2

### Tables and Data

### Table 1

| 5. Site Receiving |
| --- |
| Material Storage & Preservations
HANDLING &
INDOOR MATERIALS OUTDOOR &
PRESERVATION
OUTDOOR COVERED
•SCT to follow and implement
• The Manufacturer’s storage • Review of Manufacturer’s
the Manufacturer’s storage instruction or guide shall be Storage Instructions and
instructions and guidelines reviewed before Guidelines
placing in storage and followed. • SCT to ensure that all OUTDOOR
•OUTDOOR,
• The air temperature shall be & OUTDOOR COVERED cases or
•OUTDOOR COVERED,
maintained as per boxes [HITACHI] are properly
•INDOOR Manufacturer’s Guidelines covered with tarpaulin or plastic
sheeting.
2
6 |

### Table 2

| 5. Site Receiving |
| --- |
| FORMS
Loading & unloading checklist Material checklist
▪ For unloaded cargo, a visual check is
▪ For Loading and unloading checklist, this documents not only protect the cargo and the parties performed on the packaging and damage
involved in unloading works but also uphold the safety standards, and ensuring the compliance with status of the materials.
the transportation and safety regulation.
2
7 |

### Table 3

| 5. Site Receiving |
| --- |
| FORMS
ITP
MRR
MAR
MRI
2
8 |

### Table 4

| 5. Site Receiving |
| --- |
| FORMS
MATERIAL RECEIVING REPORT
MATERIAL REQUEST SLIP MATERIAL ISSUANCE SLIP
2
9 |

### Table 5

| 6. Material Handling
(Transformer) |
| --- |


*... and 6 more tables*

---

## Related Ontologies

- [Core Logistics Framework](../core/1_CORE-01-hvdc-core-framework.md)
- [Infrastructure Nodes](../core/1_CORE-02-hvdc-infra-nodes.md)
- [Warehouse Operations](../core/1_CORE-03-hvdc-warehouse-ops.md)


---

## Section 6: Transformer Handling

### Source

- **Original File**: 2_EXT-08F-hvdc-material-handling-transformer.md
- **Version**: unified-1.0
- **Date**: 2024-11-19

## Part 1: Domain Ontology

### Core Classes

```turtle
@prefix hvdc: <https://hvdc-project.com/ontology/material-handling/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

hvdc:Transformer a owl:Class ;
    rdfs:label "Transformer Cargo" ;
    rdfs:comment "Transformer cargo (200t, DAS/Zakum clusters) - specialized heavy equipment handling" .

hvdc:Procedure a owl:Class ;
    rdfs:label "Handling Procedure" ;
    rdfs:comment "Handling procedures (Top-Up, On-Foundation, Skidding) with PTW, FRA, risk assessments" .

hvdc:PreservationCheck a owl:Class ;
    rdfs:label "Preservation Check" ;
    rdfs:comment "Impact recorder and gas top-up checks (Dry air for DAS cluster, N2 for Zakum cluster)" .

hvdc:LiftingPlan a owl:Class ;
    rdfs:label "Lifting Plan" ;
    rdfs:comment "SPMT/crane lifting operations with rigging gear, sling angles, load sharing" .
```

### Core Properties

```turtle
hvdc:transportedBy a owl:ObjectProperty ;
    rdfs:domain hvdc:Transformer ;
    rdfs:range [ owl:unionOf (hvdc:SPMT hvdc:LCT hvdc:Crane) ] ;
    rdfs:comment "Transformer transported by SPMT, LCT, or Crane equipment." .

hvdc:requires a owl:ObjectProperty ;
    rdfs:domain hvdc:Procedure ;
    rdfs:range [ owl:unionOf (hvdc:Equipment hvdc:Document hvdc:Permit) ] ;
    rdfs:comment "Procedure requires equipment, documents, and PTW." .

hvdc:performsOn a owl:ObjectProperty ;
    rdfs:domain hvdc:PreservationCheck ;
    rdfs:range hvdc:Transformer ;
    rdfs:comment "Preservation check performed on transformer." .

hvdc:unitNo a owl:DatatypeProperty ;
    rdfs:domain hvdc:Transformer ;
    rdfs:range xsd:string ;
    rdfs:comment "Transformer unit number (e.g., DAS-1, AGI-1)." .

hvdc:ETD a owl:DatatypeProperty ;
    rdfs:domain hvdc:Transformer ;
    rdfs:range xsd:date ;
    rdfs:comment "Estimated Time of Departure from origin." .

hvdc:ETA a owl:DatatypeProperty ;
    rdfs:domain hvdc:Transformer ;
    rdfs:range xsd:date ;
    rdfs:comment "Estimated Time of Arrival at port." .

hvdc:gaugeLevel a owl:DatatypeProperty ;
    rdfs:domain hvdc:PreservationCheck ;
    rdfs:range xsd:decimal ;
    rdfs:comment "Preservation gauge level (weekly monitoring)." .

hvdc:method a owl:DatatypeProperty ;
    rdfs:domain hvdc:Procedure ;
    rdfs:range xsd:string ;
    rdfs:comment "Procedure method: Top-Up, On-Foundation, Skidding." .
```

---

## Part 2: Constraints & Validation

### SHACL Constraints

```turtle
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix hvdc: <https://hvdc-project.com/ontology/material-handling/> .

hvdc:TransformerShape a sh:NodeShape ;
    sh:targetClass hvdc:Transformer ;
    sh:property [
        sh:path hvdc:unitNo ;
        sh:minCount 1 ;
        sh:message "Transformer must have unit number."
    ] ;
    sh:property [
        sh:path hvdc:weight ;
        sh:minInclusive 100.0 ;
        sh:maxInclusive 250.0 ;
        sh:message "Transformer weight must be between 100-250t."
    ] .

hvdc:ProcedureShape a sh:NodeShape ;
    sh:targetClass hvdc:Procedure ;
    sh:property [
        sh:path hvdc:method ;
        sh:in ("Top-Up" "On-Foundation" "Skidding") ;
        sh:message "Procedure method must be Top-Up, On-Foundation, or Skidding."
    ] ;
    sh:property [
        sh:path hvdc:requires ;
        sh:minCount 1 ;
        sh:message "Procedure must have required equipment/documents."
    ] .

hvdc:PreservationCheckShape a sh:NodeShape ;
    sh:targetClass hvdc:PreservationCheck ;
    sh:property [
        sh:path hvdc:gaugeLevel ;
        sh:minInclusive 0.0 ;
        sh:message "Gauge level must be non-negative."
    ] .
```

---

## Part 3: Examples & Queries

### JSON-LD Examples

**Transformer with SPMT Transport Example**

```json
{
  "@context": {
    "hvdc": "https://hvdc-project.com/ontology/material-handling/"
  },
  "@id": "hvdc:transformer-das-1",
  "@type": "hvdc:Transformer",
  "hvdc:unitNo": "DAS-1",
  "hvdc:weight": 200.0,
  "hvdc:ETD": "2024-02-19",
  "hvdc:ETA": "2024-04-21",
  "hvdc:origin": "Sweden",
  "hvdc:arrivalPort": "Mina Zayed",
  "hvdc:transportedBy": {
    "@type": "hvdc:SPMT",
    "hvdc:capacity": 250,
    "hvdc:requires": {
      "@type": "hvdc:Document",
      "@id": "hvdc:ptw-001",
      "hvdc:type": "PTW"
    }
  },
  "hvdc:preservation": {
    "@type": "hvdc:PreservationCheck",
    "hvdc:gasType": "Dry air",
    "hvdc:gaugeLevel": 12.5
  }
}
```

**Lifting Plan Example**

```json
{
  "@context": {
    "hvdc": "https://hvdc-project.com/ontology/material-handling/"
  },
  "@id": "hvdc:lifting-plan-das-1",
  "@type": "hvdc:LiftingPlan",
  "hvdc:method": "Skidding",
  "hvdc:for": "hvdc:transformer-das-1",
  "hvdc:uses": {
    "@type": "hvdc:RiggingGear",
    "hvdc:type": "Sling",
    "hvdc:slingAngle": 45
  },
  "hvdc:loadShare": 50.0
}
```

### SPARQL Queries

**Transformer Delivery Schedule Query**

```sparql
PREFIX hvdc: <https://hvdc-project.com/ontology/material-handling/>

SELECT ?unit ?cluster ?ETD ?ETA ?onSite ?port ?status
WHERE {
    ?transformer a hvdc:Transformer ;
                 hvdc:unitNo ?unit ;
                 hvdc:cluster ?cluster ;
                 hvdc:ETD ?ETD ;
                 hvdc:ETA ?ETA ;
                 hvdc:arrivalPort ?port ;
                 hvdc:onSite ?onSite .
    OPTIONAL {
        ?transformer hvdc:transportStatus ?status .
    }
}
ORDER BY ?cluster ?unit
```

**Preservation Compliance Query**

```sparql
PREFIX hvdc: <https://hvdc-project.com/ontology/material-handling/>

SELECT ?transformer ?unitNo ?gasType ?gaugeLevel ?lastCheck ?compliant
WHERE {
    ?transformer a hvdc:Transformer ;
                 hvdc:unitNo ?unitNo ;
                 hvdc:preservation ?check .
    ?check hvdc:gasType ?gasType ;
           hvdc:gaugeLevel ?gaugeLevel ;
           hvdc:lastCheck ?lastCheck .
    BIND(IF(?gaugeLevel >= 10.0 && ?lastCheck >= NOW() - "P7D"^^xsd:duration, "COMPLIANT", "NON-COMPLIANT") AS ?compliant)
}
ORDER BY ?unitNo
```

---

## Semantic KPI Layer

### Transformer Handling KPIs

- **On-Time Delivery Rate**: Actual vs. planned arrival (target: ≥95%)
- **Preservation Compliance**: Gauge level maintenance and gas top-up adherence (target: 100%)
- **Safety Incident Rate**: Zero target in lifting/stowage operations
- **Document Compliance Rate**: PTW, FRA, stability calc completeness (target: 100%)

---

## Recommended Commands

`/transformer-handle preserve --check=gauge` [Transformer preservation gauge level check and gas top-up procedure]
`/transformer-schedule track --unit=DAS-1` [Real-time transformer delivery schedule tracking]
`/spmt-operation plan --weight=200t` [SPMT operation planning with load distribution calculations]
`/lifting-plan generate --method=Skidding` [Lifting plan generation with rigging gear specifications]
`/preservation-log weekly --cluster=DAS` [Weekly preservation log review for DAS cluster transformers]

---

---

## Original Content

### Main Text Content

### 6. Material Handling

### Transportation Process [On-Shore_MIR,SHU]

▪ Unloading of the Heavy vessel is carried out at the port using a crane within own Vessel.
▪ When unloading, load directly onto the SPMT or Hydraulic Trailer on which the beam is mounted.
▪ Temporarily storage (Steel Mat, Stool and Beam) at the port before transport.
▪ Mirfa TRs are transported Barge from Mina Zayed to Mussafah (not allowed inland in Mina Zayed Road)
▪ Proceed with inland transportation after DOT prior approval and police approval (only night time)
### Unloading from Vessel Temporary Storage at port Barge Transportation Inland Transportation

3
3
### 6. Material Handling

### Transportation Process [Off Shore _ DAS,AGI] :

Transformers using SMPT equipment shipped an LCT vessel.
①Transformers are carefully lifted from the Vessel using ②Multiple transformers are securely positioned and ③Mats and stools are installed on the LCT deck to evenly
a crane and placed onto SMPT equipment for transport. fastened onto SMPT trailers, prepared for roll-on distribute the load and prepare for safe transformer
operations. placement..
④The LCT ramp is aligned and secured to facilitate the ⑤The roll-on operation begins, with SMPT equipment ⑥Final lashing and sea fastening are performed to secure
smooth movement of SMPT trailers onto the vessel deck. transporting the transformers onto the LCT vessel via the transformers safely for marine transportation.
the ramp.
3
4
### 6. Material Handling

### Transportation Process [Off Shore _ DAS,AGI] :

These documents are mandatory to be submitted prior to the roll-on/off operation of the transformer at the port to ensure safe and
efficient handling of the equipment. (28 to 30 page)
### 1.1 Preparation and Approvals

### 2. HSE Documentation:

### 1.Permit to Work (PTW):

### 1.Risk Assessments: Covering all operational activities.

### 1.Hot Work Permit:For lashing/sea fastening and cutting activities.

### 2.Method Statements:Detailed operational and safety guidelines.

### 2.Working Over Water Permit:For all operations conducted over water.

### 3.ADNOC Tide Table: Approved tide schedules to align operations with safety

### 3.HSE Approvals: Comprehensive approval for safety and environmental plans.

standards.
Hot Work Permit Risk Assessments
3
5
### 6. Material Handling

### 1.2 Technical Documents

### 3.SPMT and Loading Operations: 5. Mooring Operations:

### 1.SPMT Certificates:Pre-and post-inspection reports. 1.Mooring Arrangement Plan:Layout and pull force details (MT/KN).

### 2.RoRo Ramp Strength Calculation:Based on trailer axle loads and load 2.Mooring Rope Certificates:Compliance certifications.

### distribution. 3.Bollard SWL Certificate:Strength verification of bollards.

### 3.Stowage Plan:Transformer configuration and load arrangement on LCT.

### 6. Vessel Specifications:

### 4.Stability and Ballasting: 1.GA Plan:General arrangement drawings of the LCT.

### 1.Ballast Calculation:Stability adjustments and contingency planning. 2.Deck Strength Data:Structural integrity information

### 2.Stability Booklet:Documentation for LCT stability and draft planning

RoRo Ramp
Ballast Calculation Mooring Arrangement Plan
Strength Calculation
3
6
### 6. Material Handling

### 1.3 Operational Documentation

7. Work Plans and Schedules:
### 1.Sequence of Operations:Step-by-step workflow for Roll-On operations.

### 2.Tug and Pilot Plans:Scheduling of tugboats and pilots.

8. Completion Documentation:
### 1.Post-Loading Inspection Reports.

### 2.Completion Certificate for Roll-On Operations.

Document Name: Certificate of Sail away Approval(C.O.A)
Purpose:
The purpose of this document is to certify the approval for the sail away of two transformers.
It confirms that a pre-sailaway inspection was conducted, and the vessel was found fit for
the voyage.
Usage:
This certificate serves as official approval from the Marine Warranty Surveyor for the
transportation of the cargo by sea. It is used to ensure compliance with safety standards
and operational procedures for the voyage, providing assurance to stakeholders, insurers,
and relevant authorities.
3
7
### 6. Material Handling

### Site Receiving & Storage

▪ Conduct Site survey before transportation (checking turning radius, obstacles, etc.)
▪ Laydown Ground compaction and Mat, Stool positioning
▪ Safety induction prior works.
▪ Unloading works (Jackdown) will be performed under supervision of technical engineer (Al Faris & Mammoet).
▪ During the storage, preservation is implemented according to Hitachi recommendations (Dry air or N2 gas flling)
### Laydown –Mat, Stool Setup Backward In Jackdown& Receiving Storage & Preservation

▪ Beam replacement (June.2024)
▪ HE (7.5 m, transportation)
### → MMT (5.8 m. long term storage)

3
8
### 6. Material Handling

Check Impact Recorder & Preservation
▪ Mobile scaffolding will be used to check impact recorder and the condition of top side.
▪ Open protection box → four incident lamps are placed on the measuring unit → Test button is located to the right of the
incident lamps → Push the test button and release (with Hitachi engineer)
▪ For preservation, check the gauge measuring on weekly and make the log sheet.
▪ If under standard level, refill dry air (DAS cluster) and N2 gas (Zakum cluster)
Checking Impact Recorder Preservation (Gauge check, etc)
3
9
### 6. Material Handling

DRY AIR PRESSURE TOP UP PROCEDURE (Continued)
▪ Lifting Personnel to the Top of the Transformer

### Tables and Data

### Table 1

| 6. Material Handling |
| --- |
| Transportation Process [On-Shore_MIR,SHU]
▪ Unloading of the Heavy vessel is carried out at the port using a crane within own Vessel.
▪ When unloading, load directly onto the SPMT or Hydraulic Trailer on which the beam is mounted.
▪ Temporarily storage (Steel Mat, Stool and Beam) at the port before transport.
▪ Mirfa TRs are transported Barge from Mina Zayed to Mussafah (not allowed inland in Mina Zayed Road)
▪ Proceed with inland transportation after DOT prior approval and police approval (only night time)
Unloading from Vessel Temporary Storage at port Barge Transportation Inland Transportation
3
3 |

### Table 2

| 6. Material Handling |
| --- |
| Transportation Process [Off Shore _ DAS,AGI] :
Transformers using SMPT equipment shipped an LCT vessel.
①Transformers are carefully lifted from the Vessel using ②Multiple transformers are securely positioned and ③Mats and stools are installed on the LCT deck to evenly
a crane and placed onto SMPT equipment for transport. fastened onto SMPT trailers, prepared for roll-on distribute the load and prepare for safe transformer
operations. placement..
④The LCT ramp is aligned and secured to facilitate the ⑤The roll-on operation begins, with SMPT equipment ⑥Final lashing and sea fastening are performed to secure
smooth movement of SMPT trailers onto the vessel deck. transporting the transformers onto the LCT vessel via the transformers safely for marine transportation.
the ramp.
3
4 |

### Table 3

| 6. Material Handling |
| --- |
| Transportation Process [Off Shore _ DAS,AGI] :
These documents are mandatory to be submitted prior to the roll-on/off operation of the transformer at the port to ensure safe and
efficient handling of the equipment. (28 to 30 page)
1.1 Preparation and Approvals
2. HSE Documentation:
1.Permit to Work (PTW):
1.Risk Assessments: Covering all operational activities.
1.Hot Work Permit:For lashing/sea fastening and cutting activities.
2.Method Statements:Detailed operational and safety guidelines.
2.Working Over Water Permit:For all operations conducted over water.
3.ADNOC Tide Table: Approved tide schedules to align operations with safety
3.HSE Approvals: Comprehensive approval for safety and environmental plans.
standards.
Hot Work Permit Risk Assessments
3
5 |

### Table 4


### Table 5



*... and 8 more tables*

---

## Related Ontologies

- [Core Logistics Framework](../core/1_CORE-01-hvdc-core-framework.md)
- [Infrastructure Nodes](../core/1_CORE-02-hvdc-infra-nodes.md)
- [Warehouse Operations](../core/1_CORE-03-hvdc-warehouse-ops.md)


---

## Section 7: Bulk Cargo Operations

### Source

- **Original File**: 2_EXT-08G-hvdc-material-handling-bulk-integrated.md
- **Version**: integrated-1.0
- **Date**: 2025-01-09

## Part 1: Integrated Domain Ontology

### Core Classes (Unified hvdc: Namespace)

```turtle
@prefix hvdc: <https://hvdc-project.com/ontology/integrated/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

# From Material Handling
hvdc:Project a owl:Class .
hvdc:Phase a owl:Class .
hvdc:Port a owl:Class .
hvdc:MOSB a owl:Class .
hvdc:Site a owl:Class .
hvdc:TransportMeans a owl:Class .
hvdc:Operation a owl:Class .
hvdc:Document a owl:Class .

# Bulk-Specific Classes (Unified with Material Handling)
hvdc:Cargo a owl:Class ;
    rdfs:comment "Unified cargo class for bulk and project cargo (transformers, steel structures, OOG)" .

hvdc:Vessel a owl:Class ;
    rdfs:subClassOf hvdc:TransportMeans ;
    rdfs:comment "Marine vessel (LCT, Barge) with deck areas for cargo stowage" .

hvdc:DeckArea a owl:Class ;
    rdfs:comment "Deck area on vessel with usable dimensions and load capacity" .

hvdc:LashingAssembly a owl:Class ;
    rdfs:comment "Lashing assembly securing cargo with calculated tension and safety factors" .

hvdc:LashingElement a owl:Class ;
    rdfs:comment "Individual lashing element (chain, wire, turnbuckle) within assembly" .

hvdc:StabilityCase a owl:Class ;
    rdfs:comment "Stability case evaluating vessel stability with GM, VCG, roll angles" .

hvdc:LiftingPlan a owl:Class ;
    rdfs:comment "Lifting plan with method, rigging gear, sling angles for cargo handling" .

hvdc:RiggingGear a owl:Class ;
    rdfs:comment "Rigging gear (sling, shackle, spreader) used in lifting operations" .

hvdc:Equipment a owl:Class ;
    rdfs:comment "Equipment (crane, forklift, SPMT) for cargo handling operations" .

hvdc:Manpower a owl:Class ;
    rdfs:comment "Manpower (riggers, operators, surveyors) for operations" .

hvdc:OperationTask a owl:Class ;
    rdfs:subClassOf hvdc:Operation ;
    rdfs:comment "Specific operation task (loading, discharging, lashing, inspection)" .

hvdc:Environment a owl:Class ;
    rdfs:comment "Environmental conditions (wind, sea state, temperature) affecting operations" .
```

### Core Properties (Integrated)

```turtle
# Material Handling Object Properties
hvdc:hasPhase a owl:ObjectProperty .
hvdc:involves a owl:ObjectProperty .
hvdc:handles a owl:ObjectProperty .
hvdc:consolidates a owl:ObjectProperty .
hvdc:dispatches a owl:ObjectProperty .
hvdc:receives a owl:ObjectProperty .
hvdc:transportedBy a owl:ObjectProperty .
hvdc:usedIn a owl:ObjectProperty .
hvdc:requires a owl:ObjectProperty .

# Bulk Cargo Object Properties (Integrated)
hvdc:placedOn a owl:ObjectProperty ;
    rdfs:domain hvdc:Cargo ;
    rdfs:range hvdc:DeckArea ;
    rdfs:comment "Cargo placed on specific deck area" .

hvdc:securedBy a owl:ObjectProperty ;
    rdfs:domain hvdc:Cargo ;
    rdfs:range hvdc:LashingAssembly ;
    rdfs:comment "Cargo secured by lashing assembly" .

hvdc:handledBy a owl:ObjectProperty ;
    rdfs:domain hvdc:Cargo ;
    rdfs:range hvdc:Equipment ;
    rdfs:comment "Cargo handled by specific equipment" .

hvdc:hasDeck a owl:ObjectProperty ;
    rdfs:domain hvdc:Vessel ;
    rdfs:range hvdc:DeckArea ;
    rdfs:comment "Vessel has deck areas" .

hvdc:carries a owl:ObjectProperty ;
    rdfs:domain hvdc:Vessel ;
    rdfs:range hvdc:Cargo ;
    rdfs:comment "Vessel carries cargo" .

hvdc:appliedTo a owl:ObjectProperty ;
    rdfs:domain hvdc:LashingAssembly ;
    rdfs:range hvdc:Cargo ;
    rdfs:comment "Lashing assembly applied to cargo" .

hvdc:uses a owl:ObjectProperty ;
    rdfs:domain [ owl:unionOf (hvdc:LashingAssembly hvdc:LiftingPlan) ] ;
    rdfs:range [ owl:unionOf (hvdc:LashingElement hvdc:RiggingGear) ] ;
    rdfs:comment "Assembly or plan uses elements/gear" .

hvdc:evaluates a owl:ObjectProperty ;
    rdfs:domain hvdc:StabilityCase ;
    rdfs:range hvdc:Vessel ;
    rdfs:comment "Stability case evaluates vessel" .

hvdc:considers a owl:ObjectProperty ;
    rdfs:domain hvdc:StabilityCase ;
    rdfs:range hvdc:Cargo ;
    rdfs:comment "Stability case considers cargo loading" .

hvdc:for a owl:ObjectProperty ;
    rdfs:domain hvdc:LiftingPlan ;
    rdfs:range hvdc:Cargo ;
    rdfs:comment "Lifting plan for specific cargo" .

hvdc:affects a owl:ObjectProperty ;
    rdfs:domain hvdc:Environment ;
    rdfs:range [ owl:unionOf (hvdc:LashingAssembly hvdc:StabilityCase) ] ;
    rdfs:comment "Environment affects assemblies/stability" .

# Material Handling Data Properties
hvdc:projectName a owl:DatatypeProperty .
hvdc:date a owl:DatatypeProperty .
hvdc:phaseType a owl:DatatypeProperty .
hvdc:name a owl:DatatypeProperty .
hvdc:type a owl:DatatypeProperty .
hvdc:areaSqm a owl:DatatypeProperty .
hvdc:weight a owl:DatatypeProperty .
hvdc:dims a owl:DatatypeProperty .
hvdc:voyageTime a owl:DatatypeProperty .

# Bulk Cargo Data Properties (Integrated)
hvdc:cargoId a owl:DatatypeProperty ;
    rdfs:domain hvdc:Cargo ;
    rdfs:range xsd:string ;
    rdfs:comment "Unique cargo identifier" .

hvdc:stackable a owl:DatatypeProperty ;
    rdfs:domain hvdc:Cargo ;
    rdfs:range xsd:boolean ;
    rdfs:comment "Whether cargo can be stacked" .

hvdc:deckStrength a owl:DatatypeProperty ;
    rdfs:domain hvdc:Vessel ;
    rdfs:range xsd:decimal ;
    rdfs:comment "Deck strength in t/m²" .

hvdc:requiredCapacity a owl:DatatypeProperty ;
    rdfs:domain hvdc:LashingAssembly ;
    rdfs:range xsd:decimal ;
    rdfs:comment "Required lashing capacity in tons" .

hvdc:safetyFactor a owl:DatatypeProperty ;
    rdfs:domain hvdc:LashingAssembly ;
    rdfs:range xsd:decimal ;
    rdfs:comment "Safety factor (≥1.0)" .

hvdc:disp a owl:DatatypeProperty ;
    rdfs:domain hvdc:StabilityCase ;
    rdfs:range xsd:decimal ;
    rdfs:comment "Displacement in tons" .

hvdc:vcg a owl:DatatypeProperty ;
    rdfs:domain hvdc:StabilityCase ;
    rdfs:range xsd:decimal ;
    rdfs:comment "Vertical center of gravity in meters" .

hvdc:gm a owl:DatatypeProperty ;
    rdfs:domain hvdc:StabilityCase ;
    rdfs:range xsd:decimal ;
    rdfs:comment "Metacentric height in meters (GM)" .

hvdc:rollAngle a owl:DatatypeProperty ;
    rdfs:domain hvdc:StabilityCase ;
    rdfs:range xsd:decimal ;
    rdfs:comment "Roll angle in degrees" .

hvdc:slingAngleDeg a owl:DatatypeProperty ;
    rdfs:domain hvdc:LiftingPlan ;
    rdfs:range xsd:decimal ;
    rdfs:comment "Sling angle in degrees" .

hvdc:wind a owl:DatatypeProperty ;
    rdfs:domain hvdc:Environment ;
    rdfs:range xsd:decimal ;
    rdfs:comment "Wind speed in m/s" .

hvdc:seaState a owl:DatatypeProperty ;
    rdfs:domain hvdc:Environment ;
    rdfs:range xsd:integer ;
    rdfs:comment "Sea state index (0-9)" .
```

---

## Part 2: SHACL Constraints

```turtle
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix hvdc: <https://hvdc-project.com/ontology/integrated/> .

# Material Handling Constraints (Excerpt)
hvdc:ProjectShape a sh:NodeShape ;
    sh:targetClass hvdc:Project ;
    sh:property [ sh:path hvdc:projectName ; sh:minCount 1 ] .

# Bulk Cargo Constraints (Integrated)
hvdc:CargoShape a sh:NodeShape ;
    sh:targetClass hvdc:Cargo ;
    sh:property [
        sh:path hvdc:cargoId ;
        sh:minCount 1 ;
        sh:message "Cargo must have ID"
    ] ;
    sh:property [
        sh:path hvdc:weight ;
        sh:minInclusive 0.01 ;
        sh:message "Weight must be positive"
    ] ;
    sh:property [
        sh:path hvdc:cogX ;
        sh:minInclusive 0.0 ;
        sh:message "COG X must be non-negative"
    ] .

hvdc:VesselShape a sh:NodeShape ;
    sh:targetClass hvdc:Vessel ;
    sh:property [
        sh:path hvdc:deckStrength ;
        sh:minInclusive 0.01 ;
        sh:message "Deck strength must be positive"
    ] .

hvdc:LashingAssemblyShape a sh:NodeShape ;
    sh:targetClass hvdc:LashingAssembly ;
    sh:property [
        sh:path hvdc:safetyFactor ;
        sh:minInclusive 1.0 ;
        sh:message "Safety factor must be at least 1.0"
    ] .

hvdc:StabilityCaseShape a sh:NodeShape ;
    sh:targetClass hvdc:StabilityCase ;
    sh:property [
        sh:path hvdc:gm ;
        sh:minInclusive 0.0 ;
        sh:message "GM must be non-negative"
    ] ;
    sh:property [
        sh:path hvdc:rollAngle ;
        sh:maxInclusive 90.0 ;
        sh:message "Roll angle must not exceed 90 degrees"
    ] .
```

---

## Part 3: Examples & Queries

### JSON-LD Examples

**Integrated Cargo Example (Steel Structure)**

```json
{
  "@context": {
    "hvdc": "https://hvdc-project.com/ontology/integrated/"
  },
  "@id": "hvdc:cargo-001",
  "@type": "hvdc:Cargo",
  "hvdc:cargoId": "CGO-2025-001",
  "hvdc:type": "Steel Structure",
  "hvdc:weight": 25.5,
  "hvdc:dimsL": 12.0,
  "hvdc:dimsW": 3.5,
  "hvdc:dimsH": 4.2,
  "hvdc:cogX": 6.0,
  "hvdc:cogY": 1.75,
  "hvdc:cogZ": 2.1,
  "hvdc:stackable": false,
  "hvdc:placedOn": {
    "@type": "hvdc:DeckArea",
    "@id": "hvdc:deck-a1",
    "hvdc:areaId": "DECK-A1",
    "hvdc:maxPointLoad": 50.0
  },
  "hvdc:securedBy": {
    "@type": "hvdc:LashingAssembly",
    "@id": "hvdc:lashing-001",
    "hvdc:requiredCapacity": 30.0,
    "hvdc:safetyFactor": 1.2
  },
  "hvdc:transportedBy": {
    "@type": "hvdc:TransportMeans",
    "@id": "hvdc:lct-001",
    "hvdc:vesselType": "LCT"
  }
}
```

**Transformer with Bulk Lifting**

```json
{
  "@context": {
    "hvdc": "https://hvdc-project.com/ontology/integrated/"
  },
  "@id": "hvdc:transformer-das-1",
  "@type": "hvdc:Cargo",
  "hvdc:cargoId": "TR-DAS-1",
  "hvdc:type": "Transformer",
  "hvdc:weight": 200.0,
  "hvdc:dimsL": 10.0,
  "hvdc:dimsW": 5.0,
  "hvdc:dimsH": 6.0,
  "hvdc:for": {
    "@type": "hvdc:LiftingPlan",
    "@id": "hvdc:lift-das-1",
    "hvdc:method": "Skidding",
    "hvdc:slingAngleDeg": 45,
    "hvdc:uses": {
      "@type": "hvdc:RiggingGear",
      "@id": "hvdc:rigging-sling-001",
      "hvdc:type": "Sling"
    }
  },
  "hvdc:preservation": {
    "@type": "hvdc:PreservationCheck",
    "hvdc:gasType": "Dry air",
    "hvdc:gaugeLevel": 12.5
  }
}
```

### SPARQL Queries

**Cargo Stability Query**

```sparql
PREFIX hvdc: <https://hvdc-project.com/ontology/integrated/>

SELECT ?cargoId ?weight ?gm ?stabilityStatus
WHERE {
    ?cargo hvdc:cargoId ?cargoId ;
           hvdc:weight ?weight .
    ?stability hvdc:considers ?cargo ;
               hvdc:gm ?gm .
    BIND(IF(?gm > 0.5, "STABLE", IF(?gm > 0.2, "MARGINAL", "UNSTABLE")) AS ?stabilityStatus)
}
ORDER BY DESC(?gm)
```

**Operation Documents Query**

```sparql
PREFIX hvdc: <https://hvdc-project.com/ontology/integrated/>

SELECT ?operationType ?documentType ?status
WHERE {
    ?operation hvdc:type ?operationType ;
               hvdc:requires ?document .
    ?document hvdc:type ?documentType .
    OPTIONAL {
        ?operation hvdc:status ?status .
    }
}
ORDER BY ?operationType ?documentType
```

**Integrated Lashing Safety Check**

```sparql
PREFIX hvdc: <https://hvdc-project.com/ontology/integrated/>

SELECT ?cargo ?cargoId ?requiredCapacity ?calcTension ?safetyFactor ?safe
WHERE {
    ?cargo hvdc:cargoId ?cargoId ;
           hvdc:securedBy ?lashing .
    ?lashing hvdc:requiredCapacity ?requiredCapacity ;
             hvdc:calcTension ?calcTension ;
             hvdc:safetyFactor ?safetyFactor .
    BIND(IF(?safetyFactor >= 1.0 && ?calcTension >= ?requiredCapacity, "SAFE", "UNSAFE") AS ?safe)
}
ORDER BY DESC(?safetyFactor)
```

---

## Semantic KPI Layer

### Integrated KPIs

- **Cargo Safety Index**: Stability compliance rate across all phases (target: ≥95%)
- **Lashing Efficiency**: Capacity vs. usage in marine transport (target: ≥85%)
- **Deck Utilization**: Area exploitation in MOSB/vessels (target: 70-85%)
- **Handling Incident Rate**: Zero target in lifting/stowage operations
- **Preservation Adherence**: Temp/RH compliance for bulk items (target: 100%)
- **Voyage Optimization**: Actual vs. planned times with stability factors (target: ≥90%)

---

## Recommended Commands

`/bulk-cargo plan --stowage=lct` [Bulk cargo stowage planning for LCT operations]
`/lashing-calc validate --safety-factor=1.2` [Lashing assembly calculation and safety factor validation]
`/stability-check evaluate --gm=0.5` [Vessel stability evaluation with GM/VCG/roll angle analysis]
`/lifting-plan optimize --method=Skidding` [Lifting plan optimization with rigging gear selection]
`/cargo-traceability track --cargo=cgo-001` [End-to-end cargo traceability from port to site]

---

## Related Ontologies

- [Material Handling Overview](./2_EXT-08A-hvdc-material-handling-overview.md) - Overall logistics workflow
- [Material Handling Customs](./2_EXT-08B-hvdc-material-handling-customs.md) - Customs clearance procedures
- [Material Handling Storage](./2_EXT-08C-hvdc-material-handling-storage.md) - Storage and inland transportation
- [Material Handling Offshore](./2_EXT-08D-hvdc-material-handling-offshore.md) - Offshore marine transportation
- [Material Handling Site Receiving](./2_EXT-08E-hvdc-material-handling-site-receiving.md) - Site receiving and inspection
- [Material Handling Transformer](./2_EXT-08F-hvdc-material-handling-transformer.md) - Transformer handling procedures
- [Bulk Cargo Operations](../core/1_CORE-05-hvdc-bulk-cargo-ops.md) - Core bulk cargo ontology

---

## Original Content

This integrated ontology document combines:

1. **Material Handling Workshop content** from `HVDC_Material Handling Workshop_(20241119_1).pdf` (6 sections covering Overview, Customs, Storage, Offshore Transport, Site Receiving, and Transformer handling)

2. **Bulk Cargo Operations ontology** from `1_CORE-05-hvdc-bulk-cargo-ops.md` (detailed stowage, lashing, stability, and lifting operations)

### Integration Benefits

- **Unified Knowledge Graph**: Single ontology namespace (`hvdc:`) for all material handling and bulk cargo operations
- **End-to-End Traceability**: Track cargo from port arrival through storage, transport, and installation
- **Automated Validation**: SHACL constraints ensure safety and compliance across all operations
- **Predictive Analytics**: Integrated KPIs support decision-making and risk management
- **Compliance Enforcement**: UAE customs, ADNOC HSE, IMSBC, SOLAS standards embedded in constraints

This consolidated approach enables comprehensive logistics management for the HVDC project, supporting both operational execution and strategic planning.



---

