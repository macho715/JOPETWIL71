# HVDC Logistics Ontology - Core Documentation Master

**Version**: 2.1
**Created**: 2025-11-01
**Updated**: 2025-11-01
**Purpose**: Complete unified reference for HVDC Ontology (9 CONSOLIDATED docs with Flow Code v3.5 fully integrated + 9 supporting docs)

This document consolidates the following source files:
- README_ontology_data_hub.md
- README_consolidated.md
- MASTER_INDEX.md
- ONTOLOGY_COVERAGE_MATRIX.md
- FLOW_CODE_LINEAGE.md
- DATA_FILES_GUIDE.md
- QUERY_TEMPLATES.md
- USAGE_GUIDE.md
- VALIDATION_REPORT.md

---

## Table of Contents

1. [Part 1: Overview and Introduction](#part-1-overview-and-introduction)
2. [Part 2: Master Index and Coverage](#part-2-master-index-and-coverage)
3. [Part 3: Flow Code System](#part-3-flow-code-system)
4. [Part 4: Data Files Guide](#part-4-data-files-guide)
5. [Part 5: Query Templates and Usage](#part-5-query-templates-and-usage)
6. [Part 6: Validation and Quality Assurance](#part-6-validation-and-quality-assurance)

---

# Part 1: Overview and Introduction

# HVDC Ontology Data Hub

**Version**: 1.0
**Created**: 2025-10-31
**Total Files**: 92 files | 906,980 lines

---

## Overview

The HVDC Ontology Data Hub provides a unified architecture bridging:

- **Conceptual Layer** (`01_ontology/`): Consolidated documentation (4,314 lines)
- **Schema Layer** (`02_schemas/`): TTL ontology definitions (1,296 lines)
- **Data Layer** (`03_data/`): TTL instances + JSON analytics
- **Archive** (`04_archive/`): Historical versions
- **Cross-References** (`05_cross_references/`): Integration documentation

---

## Quick Access

### Core Documentation

- **Flow Code v3.5**: `01_ontology/consolidated/CONSOLIDATED-02-warehouse-flow.md`
- **Latest Data**: `03_data/ttl/current/hvdc_status_v35.ttl` (755 cases)
- **Statistics**: `03_data/json/gpt_cache/cases_by_flow.json`
- **Full Index**: `05_cross_references/MASTER_INDEX.md`
- **Data Files Guide**: `DATA_FILES_GUIDE.md` (TTL & JSON 파일 설명)

### Key Features

- ✅ **Flow Code v3.5** fully implemented (0-5 classification)
- ✅ **AGI/DAS domain rules** enforced via SHACL
- ✅ **OCR KPI gates** (EntityMatch ≥0.98, TableAcc ≥0.98)
- ✅ **Complete traceability** across all layers
- ✅ **SPARQL-ready** TTL data

---

## Directory Structure

```
ontology_data_hub/
├── 01_ontology/          # Conceptual documentation (6 files)
│   └── consolidated/     # Core consolidated docs
├── 02_schemas/           # RDF/OWL definitions (9 files)
│   ├── core/             # Ontology TTL files
│   └── shapes/           # SHACL constraints
├── 03_data/              # Operational data (36 files)
│   ├── ttl/              # TTL instances
│   │   ├── current/      # Latest (hvdc_status_v35.ttl)
│   │   ├── finalized/    # Finalized projects
│   │   └── specialized/  # Project-specific
│   └── json/             # Analytics & reports
│       ├── validation/   # QA reports
│       ├── gpt_cache/    # Pre-computed stats
│       └── reports/      # Analysis outputs
├── 04_archive/           # Historical versions (23 files)
│   ├── ttl/              # Legacy TTL
│   └── json/             # Legacy JSON
└── 05_cross_references/  # Integration docs (5 files)
    ├── MASTER_INDEX.md
    ├── ONTOLOGY_COVERAGE_MATRIX.md
    ├── FLOW_CODE_LINEAGE.md
    ├── QUERY_TEMPLATES.md
    └── USAGE_GUIDE.md
```

---

## Usage Guide

**For complete usage instructions**: See `05_cross_references/USAGE_GUIDE.md`

**For SPARQL queries**: See `05_cross_references/QUERY_TEMPLATES.md`

**For file inventory**: See `05_cross_references/MASTER_INDEX.md`

**For ontology mappings**: See `05_cross_references/ONTOLOGY_COVERAGE_MATRIX.md`

**For TTL & JSON files**: See `DATA_FILES_GUIDE.md` (한글 가이드)

---

## Key Statistics

| Category | Files | Description |
|----------|-------|-------------|
| Ontology Docs | 6 | Conceptual models (4,314 lines) |
| TTL Schemas | 9 | Formal definitions (1,296 lines) |
| TTL Data | 18 | Instances (~430K lines) |
| JSON Analytics | 36 | Reports & validations |
| Archive | 23 | Historical versions |
| **Total** | **92** | **906,980 lines** |

---

## Integration

### With Existing Systems

- **MCP Server**: Load `03_data/ttl/current/hvdc_status_v35.ttl`
- **RDFLib**: All TTL files compatible
- **SPARQL**: Query any TTL file with standard SPARQL
- **JSON**: Pre-computed analytics for fast access

### Validation

- **SHACL**: All TTL data validated against `02_schemas/shapes/`
- **Flow Code**: Automatic validation via FlowCode.shape.ttl
- **OCR KPI**: Quality gates enforced via SHACL

---

## Maintenance

### Updating Files

1. Update source files in original locations
2. Copy updates to hub (preserves originals)
3. Regenerate JSON analytics if TTL data changes
4. Update cross-reference documentation

### Adding New Files

Follow existing directory structure and update `MASTER_INDEX.md`.

---

## Contact

For questions, see `01_ontology/consolidated/README.md` or `05_cross_references/USAGE_GUIDE.md`.

---

**Note**: All files are copies. Original files remain in their source locations for safety.



---

# Part 2: Master Index and Coverage

# HVDC Core Ontology - Consolidated Documentation

## Overview

This directory contains consolidated versions of the HVDC Core Ontology documentation, merging related concepts into comprehensive documents for better understanding and maintenance.

### 6 Categories

이 디렉토리는 9개 카테고리로 구성됩니다:
1. 코어 (Core Framework & Infrastructure)
2. 창고 (Warehouse Operations & Flow Code)
3. 문서 (Document Guardian & OCR)
4. 바지선 운영 및 벌크화물 (Barge & Bulk Cargo Operations)
5. 청구서 (Invoice & Cost Management)
6. 자재 처리 (Material Handling)
7. 항만 운영 (Port Operations)
8. 커뮤니케이션 (Communication)
9. 운영 관리 (Operations Management)

## File Mapping

| Consolidated File | Original Files | Description |
|------------------|----------------|-------------|
| `CONSOLIDATED-01-core-framework-infra.md` | `1_CORE-01-hvdc-core-framework.md`<br>`1_CORE-02-hvdc-infra-nodes.md` | Core logistics framework and infrastructure nodes |
| `CONSOLIDATED-02-warehouse-flow.md` | `1_CORE-03-hvdc-warehouse-ops.md`<br>`1_CORE-08-flow-code.md` | Warehouse operations and flow code algorithms |
| `CONSOLIDATED-03-document-ocr.md` | `1_CORE-06-hvdc-doc-guardian.md`<br>`1_CORE-07-hvdc-ocr-pipeline.md` | Document guardian and OCR pipeline |
| `CONSOLIDATED-04-barge-bulk-cargo.md` | `1_CORE-05-hvdc-bulk-cargo-ops.md` | Barge operations and bulk cargo handling |
| `CONSOLIDATED-05-invoice-cost.md` | `1_CORE-04-hvdc-invoice-cost.md` | Invoice verification and cost management |
| `CONSOLIDATED-06-material-handling.md` | `2_EXT-08A~G` (7 files) | Complete material handling workflow |
| `CONSOLIDATED-07-port-operations.md` | `2_EXT-01` (EN)<br>`2_EXT-02` (KO) | OFCO port operations (bilingual) |
| `CONSOLIDATED-08-communication.md` | `2_EXT-03-hvdc-comm-email.md`<br>`2_EXT-04-hvdc-comm-chat.md` | Email and chat communication systems |
| `CONSOLIDATED-09-operations.md` | `2_EXT-05-hvdc-ops-management.md` | Warehouse PJT operations management |

## Content Preservation

All consolidated files maintain the complete content from their original sources:

- **YAML Front Matter**: Combined metadata from source files
- **Part Structure**: Clear separation between original file contents
- **Source Attribution**: Each section includes source file information
- **Cross-References**: Internal links updated for consolidated structure
- **Ontology Definitions**: Complete RDF/OWL/SHACL definitions preserved

## Usage

### For Developers
- Use consolidated files for comprehensive understanding of related concepts
- Reference original files for specific implementation details
- Cross-reference between consolidated files for system-wide understanding

### For Documentation
- Consolidated files provide complete context for each domain
- Source file references maintain traceability
- Table of Contents provides quick navigation

## Verification

### Line Count Verification
Current consolidated files (as of 2025-11-01):

- `CONSOLIDATED-01`: 1,310 lines (Core Framework + Infrastructure) - v1.1
- `CONSOLIDATED-02`: 992 lines (Warehouse + Flow Code v3.5)
- `CONSOLIDATED-03`: 1,126 lines (Document Guardian + OCR Pipeline) - v1.1
- `CONSOLIDATED-04`: 332 lines (Bulk Cargo Operations) - v1.1
- `CONSOLIDATED-05`: 435 lines (Invoice & Cost Management) - v1.1
- `CONSOLIDATED-06`: 3,214 lines (Material Handling - complete workflow) - v1.1
- `CONSOLIDATED-07`: 407 lines (Port Operations - bilingual) - v1.1
- `CONSOLIDATED-08`: 483 lines (Communication systems)
- `CONSOLIDATED-09`: 539 lines (Operations Management) - v1.1
- **Total**: ~8,838 lines (+ Flow Code v3.5 integration)

### Flow Code v3.5 Integration Summary (2025-11-01)

**Status**: Flow Code v3.5 fully integrated across all 9 CONSOLIDATED documents

**Integration Statistics**:
- **Total Flow Code mentions**: 329 occurrences
- **Documents integrated**: 9/9 CONSOLIDATED files (100%)
- **Flow Code properties added**: 9 core properties across all domains
- **SHACL constraints**: AGI/DAS Flow ≥3 rule enforced
- **SPARQL queries**: 20+ domain-specific queries provided

**Integration by Document**:

| Document | Flow Code Mentions | Integration Type | Key Features |
|----------|-------------------|------------------|--------------|
| **CONSOLIDATED-01** | 11 | Core framework references | Framework context |
| **CONSOLIDATED-02** | 85 | Complete integration | Flow Code 0-5, AGI/DAS rules, SPARQL |
| **CONSOLIDATED-03** | 34 | Document-OCR integration | Extraction fields, validation pipeline |
| **CONSOLIDATED-04** | 27 | Bulk cargo integration | LCT operations, MOSB staging |
| **CONSOLIDATED-05** | 8 | Cost analysis integration | Flow Code-based cost structure |
| **CONSOLIDATED-06** | 23 | Material handling integration | Phase A/B routing, AGI/DAS patterns |
| **CONSOLIDATED-07** | 43 | Port operations integration | Origin point, clearance classification |
| **CONSOLIDATED-08** | 7 | TTL enhancement | Communication-enhanced.ttl |
| **CONSOLIDATED-09** | 36 | Operations management | KPI metrics, efficiency analysis |

**Key Flow Code v3.5 Features Integrated**:

1. **Flow Code Classification (0-5)**:
   - Flow 0: Pre Arrival (cargo awaiting port clearance)
   - Flow 1: Port → Site (direct delivery, optimal)
   - Flow 2: Port → WH → Site (warehouse consolidation)
   - Flow 3: Port → MOSB → Site (offshore delivery via MOSB)
   - Flow 4: Port → WH → MOSB → Site (full chain)
   - Flow 5: Mixed/Incomplete (abnormal patterns)

2. **AGI/DAS Domain Rules**:
   - All materials to AGI (Al Ghallan Island) or DAS (Das Island) **MUST** have Flow Code ≥ 3
   - Automatic upgrade: Flow 0/1/2 → Flow 3 (MOSB leg mandatory)
   - Original Flow Code preserved in `hasFlowCodeOriginal`
   - Override reason recorded in `hasFlowOverrideReason`

3. **Domain-Specific Implementations**:
   - **Material Handling**: Phase A (Import) vs Phase B (Offshore) routing
   - **Barge/Bulk**: LCT transport exclusively Flow 3, 4
   - **Port Operations**: Initial Flow Code assignment at customs clearance
   - **Document OCR**: Flow Code extraction and cross-document validation
   - **Invoice/Cost**: Flow Code-based cost structure analysis
   - **Operations**: KPI metrics (efficiency, compliance, utilization)

4. **RDF/OWL Properties**:
   ```turtle
   hvdc:hasLogisticsFlowCode (0-5 range)
   hvdc:hasFlowCodeOriginal (AGI/DAS pre-upgrade)
   hvdc:hasFlowOverrideReason (upgrade rationale)
   hvdc:hasFlowDescription (routing description)
   hvdc:requiresMOSBLeg (MOSB mandatory flag)
   hvdc:hasFinalLocation (MIR/SHU/AGI/DAS)
   hvdc:hasWarehouseCount (warehouse transit count)
   hvdc:hasMOSBLeg (MOSB transit boolean)
   hvdc:hasSiteArrival (site delivery boolean)
   ```

5. **SHACL Validation**:
   - Flow Code 0-5 range constraint
   - AGI/DAS → Flow ≥3 mandatory
   - Flow 5 → requiresReview flag required
   - FLOW_CODE_ORIG ≠ null → FLOW_OVERRIDE_REASON required

6. **SPARQL Query Coverage**:
   - Flow Code distribution analysis
   - AGI/DAS compliance verification
   - Flow 5 (incomplete) case review
   - Monthly efficiency trend analysis
   - Cross-document Flow Code consistency
   - MOSB staging duration analysis

**Integration Benefits**:
- ✅ Unified Flow Code reference across entire HVDC system
- ✅ Domain-specific routing patterns documented
- ✅ AGI/DAS business rules enforced via SHACL
- ✅ Consistent KPI metrics across all domains
- ✅ SPARQL-ready queries for operational analytics

### Content Integrity
- All original content preserved
- No information loss during consolidation
- Proper attribution maintained
- Cross-references updated

## Original File References

### Core Framework & Infrastructure
- **Source**: `core/1_CORE-01-hvdc-core-framework.md`
- **Source**: `core/1_CORE-02-hvdc-infra-nodes.md`
- **Consolidated**: `CONSOLIDATED-01-core-framework-infra.md`

### Warehouse Operations & Flow Codes
- **Source**: `core/1_CORE-03-hvdc-warehouse-ops.md`
- **Source**: `core/1_CORE-08-flow-code.md`
- **Consolidated**: `CONSOLIDATED-02-warehouse-flow.md`

### Document Guardian & OCR Pipeline
- **Source**: `core/1_CORE-06-hvdc-doc-guardian.md`
- **Source**: `core/1_CORE-07-hvdc-ocr-pipeline.md`
- **Consolidated**: `CONSOLIDATED-03-document-ocr.md`

### Barge Operations & Bulk Cargo
- **Source**: `core/1_CORE-05-hvdc-bulk-cargo-ops.md`
- **Consolidated**: `CONSOLIDATED-04-barge-bulk-cargo.md`

### Invoice & Cost Management
- **Source**: `core/1_CORE-04-hvdc-invoice-cost.md`
- **Consolidated**: `CONSOLIDATED-05-invoice-cost.md`

### Material Handling
- **Source**: `extended/2_EXT-08A~G` (7 files: overview, customs, storage, offshore, site-receiving, transformer, bulk-integrated)
- **Consolidated**: `CONSOLIDATED-06-material-handling.md`

### Port Operations
- **Source**: `extended/2_EXT-01-hvdc-ofco-port-ops-en.md`, `2_EXT-02-hvdc-ofco-port-ops-ko.md`
- **Consolidated**: `CONSOLIDATED-07-port-operations.md`

### Communication
- **Source**: `extended/2_EXT-03-hvdc-comm-email.md`, `2_EXT-04-hvdc-comm-chat.md`
- **Consolidated**: `CONSOLIDATED-08-communication.md`

### Operations Management
- **Source**: `extended/2_EXT-05-hvdc-ops-management.md`
- **Consolidated**: `CONSOLIDATED-09-operations.md`

## Maintenance

### Updates
- Update consolidated files when source files change
- Maintain source attribution and version information
- Update cross-references as needed

### Version Control
- Track changes to both source and consolidated files
- Maintain consistency between versions
- Document consolidation rationale

## Standards Compliance

All consolidated files maintain compliance with:
- **RDF/OWL**: Semantic web standards
- **SHACL**: Shape constraint validation
- **SPARQL**: Query language support
- **JSON-LD**: Linked data serialization
- **Turtle**: RDF serialization format

## KPI Gate Change History

### EntityMatch Threshold Update (2025-10-31)
- **Previous**: ≥ 0.90
- **Current**: ≥ 0.98
- **Reason**: Alignment with conservative operational guidelines for entity matching accuracy
- **Impact**: Stricter OCR quality gate, increased ZERO-fail-safe triggers
- **Related Files**: CONSOLIDATED-03-document-ocr.md (SHACL rule, policy table)

## Contact

For questions about consolidation or content updates, refer to the original source files or contact the HVDC project team.


---

# Part 3: Flow Code System

# HVDC Ontology Data Hub - Master Index

**Last Updated**: 2025-11-01
**Total Files**: 92 files | 906,980 lines
**Structure**: 5 main sections | 12 subdirectories

---

## Quick Navigation

| Section | Description | Files | Lines | Key Files |
|---------|-------------|-------|-------|-----------|
| [01_ontology](#01_ontology) | Conceptual documentation | 9 | 6,845 | Consolidated docs |
| [02_schemas](#02_schemas) | RDF/OWL definitions | 9 | 1,296 | Ontology + shapes |
| [03_data](#03_data) | Operational data | 36 | 443,181 | TTL instances + JSON analytics |
| [04_archive](#04_archive) | Historical versions | 23 | 407,585 | Legacy files |
| [05_cross_references](#05_cross_references) | Integration docs | 5 | New | This index |

---

## 01_ontology

### consolidated/ (9 files, 6,845 lines)

Conceptual model documentation - HVDC Core Ontology consolidated into 9 categories.

| File | Lines | Description |
|------|-------|-------------|
| `CONSOLIDATED-01-core-framework-infra.md` | 926 | Core logistics framework and infrastructure nodes |
| `CONSOLIDATED-02-warehouse-flow.md` | 824 | Warehouse operations and Flow Code v3.5 algorithm |
| `CONSOLIDATED-03-document-ocr.md` | 934 | Document Guardian and OCR pipeline |
| `CONSOLIDATED-04-barge-bulk-cargo.md` | 255 | Barge operations and bulk cargo handling |
| `CONSOLIDATED-05-invoice-cost.md` | 332 | Invoice verification and cost management |
| `CONSOLIDATED-06-material-handling.md` | 2,564 | Complete material handling workflow |
| `CONSOLIDATED-07-port-operations.md` | 354 | OFCO port operations (bilingual) |
| `CONSOLIDATED-08-communication.md` | 283 | Email and chat communication systems |
| `CONSOLIDATED-09-operations.md` | 373 | Warehouse PJT operations management |

**Key Features**:
- Flow Code v3.5 (0-5) algorithm documented
- SHACL validation rules for each domain
- Cross-domain relationships and dependencies
- Operational guidelines and best practices

**Related Files**:
- TTL Schemas: `02_schemas/core/` → Formal implementations
- TTL Data: `03_data/ttl/current/hvdc_status_v35.ttl` → Flow Code instances
- JSON Analytics: `03_data/json/gpt_cache/cases_by_flow.json` → Statistics

---

## 02_schemas

### core/ (5 files, 1,028 lines)

RDF/OWL ontology definitions - formal semantic web models.

| File | Lines | Key Classes | Purpose |
|------|-------|-------------|---------|
| `hvdc_event_schema.ttl` | 175 | StockEvent, TransportEvent | Event tracking |
| `hvdc_nodes.ttl` | 214 | Warehouse, Site, MOSB, Port | Location infrastructure |
| `hvdc_ontology.ttl` | 191 | Party, Asset, Document, Process | Core concepts |
| `flow_code.ttl` | 209 | FlowCode, LogisticsFlow | Flow Code v3.5 |
| `2_EXT-03-hvdc-comm-email-enhanced.ttl` | 239 | CommunicationEvent, Email | Communication ontology |

**Related Files**:
- Documentation: `01_ontology/consolidated/` → Conceptual models
- Shapes: `02_schemas/shapes/` → Validation constraints
- Data: `03_data/ttl/current/` → Instances

### shapes/ (4 files, 268 lines)

SHACL shape constraints - data validation rules.

| File | Lines | Constraints | Purpose |
|------|-------|-------------|---------|
| `FlowCode.shape.ttl` | 89 | FlowCode 0-5, AGI/DAS rules | Flow Code validation |
| `ShipmentOOG.shape.ttl` | 56 | Out-of-gauge dimensions | OOG cargo validation |
| `Shipment.shape.ttl` | 78 | General shipment rules | Shipment validation |
| `shacl_shapes.ttl` | 45 | Combined constraints | Unified validation |

**Related Files**:
- Documentation: `01_ontology/consolidated/CONSOLIDATED-02` (Lines 486-537) → SHACL rules
- Schemas: `02_schemas/core/` → Classes being validated
- Validation: `03_data/json/validation/` → Validation reports

---

## 03_data

### ttl/current/ (1 file, 9,844 lines) ⭐

**`hvdc_status_v35.ttl`** - Latest Flow Code v3.5 data

- **Instances**: 9,795+ cases
- **Classes**: Case, StockEvent, TransportEvent
- **Flow Codes**: 0-5 distribution
  - Flow 0 (Pre Arrival): 2.4%
  - Flow 1 (Port→Site): 1.6%
  - Flow 2 (Port→WH→Site): 34.9%
  - Flow 3 (Port→MOSB→Site): 21.5%
  - Flow 4 (Port→WH→MOSB→Site): 35.6%
  - Flow 5 (Mixed/Incomplete): 4.0%

**Properties**:
- `hvdc:hasFlowCode` - 9,795 (100%)
- `hvdc:hasFlowCodeOriginal` - 9,795 (100%)
- `hvdc:hasFlowDescription` - 9,795 (100%)
- `hvdc:hasInboundEvent` - 6,823 (69.7%)

**Related Files**:
- Schema: `02_schemas/core/flow_code.ttl` → Class definitions
- Validation: `02_schemas/shapes/FlowCode.shape.ttl` → Constraints
- Analytics: `03_data/json/gpt_cache/cases_by_flow.json` → Statistics

### ttl/finalized/ (2 files, 92,778 lines)

| File | Lines | Description |
|------|-------|-------------|
| `lightning_final.ttl` | 48,156 | Lightning project finalized data |
| `abu_final.ttl` | 44,622 | Abu Dhabi project finalized data |

### ttl/specialized/ (15 files, 326,175 lines)

Project-specific TTL instances:
- **Lightning**: 5 files (lightning_*.ttl)
- **Abu Dhabi**: 4 files (abu_*.ttl)
- **Invoices**: 3 files (invoice_*.ttl)
- **Sheet extracts**: 3 files (sheet_*.ttl)

### json/validation/ (5 files, 103 lines)

Quality assurance reports:
- `validation_summary.json` - Overall validation results
- `flow_event_patterns.json` - Flow event analysis
- `event_coverage_stats.json` - Event coverage metrics
- `human_gate_missing_dates.json` - Missing date issues
- `human_gate_flow23_no_inbound.json` - Flow 2/3 validation

### json/gpt_cache/ (3 files, 544 lines)

Pre-computed aggregations for GPT queries:
- `cases_by_flow.json` - Flow Code distribution
- `vendor_summary.json` - Vendor statistics
- `monthly_warehouse_inbound.json` - Warehouse inbound trends

**Usage**: MCP server uses these for fast GPT responses.

### json/integration/ (10 files, 11,265 lines)

Network integration data:
- `unified_network_data_v12_hvdc.json` - Main network data
- `unified_network_stats_v12_hvdc.json` - Network statistics
- `unified_network_meta_v12_hvdc.json` - Metadata
- `integration_data_meaningful.json` - Filtered meaningful data
- `abu_lightning_comparison_data.json` - Project comparison
- + 5 more integration files

### json/reports/ (18 files, 53,076 lines)

Analysis reports:
- **Lightning**: 6 analysis files (enhancement, enrichment, whatsapp)
- **Abu Dhabi**: 10 analysis files (comprehensive, LPO, whatsapp, etc.)
- **Tag dictionary**: 1 file (abu_dhabi_logistics_tag_dict_v1.json)

---

## 04_archive

Historical versions preserved for version control and reference.

### ttl/ (9 files, 149,677 lines)

Legacy TTL files from:
- `archive/legacy/mcp_v1.0/` - MCP v1.0 schemas and data
- `archive/legacy/mcp_v2.0/` - MCP v2.0 data
- `archive/legacy/event_ontology/` - Event ontology snapshots
- `archive/legacy/logiontology_v2.0.0_initial/` - Initial v2.0 configs

### json/ (14 files, 257,908 lines)

Legacy JSON analytics from:
- `archive/legacy/mcp_v1.0/` - Test results and sample outputs
- `archive/legacy/event_ontology/` - Output snapshots
- `archive/output_history/rdf_output_legacy/` - Historical RDF outputs
- `archive/legacy/logiontology_v2.0.0_initial/` - Initial test fixtures

---

## 05_cross_references

Integration documentation providing navigation and traceability.

| File | Purpose |
|------|---------|
| `MASTER_INDEX.md` | This file - complete inventory |
| `ONTOLOGY_COVERAGE_MATRIX.md` | Docs ↔ Schemas ↔ Data mapping |
| `FLOW_CODE_LINEAGE.md` | Flow Code v3.5 traceability |
| `QUERY_TEMPLATES.md` | SPARQL query examples |
| `USAGE_GUIDE.md` | How to navigate and use the hub |

---

## File Relationships

### Conceptual → Formal → Operational

```
01_ontology/consolidated/
    ├─ CONSOLIDATED-01 → 02_schemas/core/hvdc_ontology.ttl
    ├─ CONSOLIDATED-02 → 02_schemas/core/flow_code.ttl + shapes/FlowCode.shape.ttl
    ├─ CONSOLIDATED-03 → 02_schemas/core/hvdc_ontology.ttl (LDG classes)
    ├─ CONSOLIDATED-04 → 03_data/ttl/specialized/abu_*.ttl
    └─ CONSOLIDATED-05 → 03_data/ttl/specialized/invoice_*.ttl
                            ↓
                        03_data/ttl/current/hvdc_status_v35.ttl
                            ↓
                    03_data/json/gpt_cache/cases_by_flow.json
```

### Validation Flow

```
02_schemas/shapes/FlowCode.shape.ttl
    ↓ (validates)
03_data/ttl/current/hvdc_status_v35.ttl
    ↓ (generates)
03_data/json/validation/validation_summary.json
```

---

## Quick Access Guide

### I want to...

**Understand the ontology**: Start with `01_ontology/consolidated/README.md`

**Query Flow Code data**: Use `03_data/ttl/current/hvdc_status_v35.ttl` + SPARQL

**View validation results**: Check `03_data/json/validation/`

**Run pre-computed statistics**: Load `03_data/json/gpt_cache/`

**Find specific classes**: Search in `02_schemas/core/` + `05_cross_references/ONTOLOGY_COVERAGE_MATRIX.md`

**Cross-reference concepts**: Use `05_cross_references/FLOW_CODE_LINEAGE.md`

**See example queries**: Browse `05_cross_references/QUERY_TEMPLATES.md`

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2025-10-31 | 1.0 | Initial hub creation, 92 files consolidated |
| | | Flow Code v3.5 integration complete |
| | | OCR KPI hardening applied (EntityMatch ≥0.98) |

---

## Maintenance

### Updating Files

1. **Ontology docs**: Update in `01_ontology/consolidated/`, verify schemas match
2. **TTL schemas**: Update in `02_schemas/`, regenerate data if needed
3. **TTL data**: Update `03_data/ttl/current/`, run validation
4. **JSON analytics**: Regenerate from latest TTL data

### Adding New Files

Follow existing directory structure and update this index.

### Sync with Sources

Original files remain in source locations:
- `core_consolidated/` → `01_ontology/consolidated/`
- `logiontology/configs/ontology/` → `02_schemas/core/`
- `output/` → `03_data/ttl/current/` and `03_data/json/`
- `archive/legacy/` → `04_archive/`

---

**For detailed usage instructions, see**: `05_cross_references/USAGE_GUIDE.md`



---

# Part 4: Data Files Guide

# Ontology Coverage Matrix

**Purpose**: Maps conceptual documentation (MD) → formal schemas (TTL) → operational data (TTL instances) → analytics (JSON)

**Last Updated**: 2025-11-01

---

## Complete Mapping Table

| Ontology Doc | Lines | TTL Schema Files | TTL Data Files | JSON Analytics Files | Description | Key Classes/Concepts |
|--------------|-------|------------------|----------------|---------------------|-------------|---------------------|
| **CONSOLIDATED-01** | 1,310 | `hvdc_ontology.ttl`<br>`hvdc_nodes.ttl` | `hvdc_status_v35.ttl`<br>`lightning_final.ttl`<br>`abu_final.ttl` | `integration/unified_network_*.json` | Core framework, infrastructure nodes | Party, Asset, Document, Process, Location, Warehouse, Site, MOSB, Port |
| **CONSOLIDATED-02** | 992 | `flow_code.ttl`<br>`FlowCode.shape.ttl` | `hvdc_status_v35.ttl` | `gpt_cache/cases_by_flow.json`<br>`validation/flow_event_patterns.json` | Warehouse operations, Flow Code v3.5 | FlowCode, LogisticsFlow, TransportEvent, StockEvent, AGI/DAS domain rules |
| **CONSOLIDATED-03** | 1,126 | `hvdc_ontology.ttl`<br>`shacl_shapes.ttl` | `hvdc_status_v35.ttl`<br>`specialized/invoice_*.ttl` | `validation/validation_summary.json`<br>`reports/invoice_*.json` | Document Guardian, OCR pipeline, Flow Code extraction | LDG Document, Metric, Audit, TrustLayer, Flow Code OCR fields |
| **CONSOLIDATED-04** | 332 | `hvdc_ontology.ttl`<br>`Shipment.shape.ttl`<br>`ShipmentOOG.shape.ttl` | `abu_*.ttl`<br>`sheet_*.ttl` | `reports/abu_*.json` | Barge operations, bulk cargo, Flow 3/4 | Barge, BulkCargo, OOG, LCT, Flow Code MOSB patterns |
| **CONSOLIDATED-05** | 435 | `hvdc_ontology.ttl` | `specialized/invoice_*.ttl` | `reports/invoice_*.json` | Invoice verification, cost management, Flow Code cost analysis | Invoice, InvoiceLineItem, Flow Code cost structure |
| **CONSOLIDATED-06** | 3,214 | `hvdc_ontology.ttl`<br>`hvdc_nodes.ttl` | `hvdc_status_v35.ttl`<br>`lightning_final.ttl` | N/A | Material handling, Phase A/B, Flow Code routing | Cargo, Material, Flow Code (0-5), AGI/DAS rules |
| **CONSOLIDATED-07** | 407 | `hvdc_ontology.ttl` | N/A | N/A | Port operations, Flow Code origin point | PortCall, Flow Code assignment, clearance classification |
| **CONSOLIDATED-08** | 483 | `CONSOLIDATED-08-communication-enhanced.ttl` | N/A | N/A | Email and chat communication | Email_Message, Workgroup, Message, Tag, Action, SLAClock |
| **CONSOLIDATED-09** | 539 | `hvdc_ontology.ttl` | `hvdc_status_v35.ttl` | N/A | Operations management, Flow Code KPI metrics | TransportEvent, StockSnapshot, Flow Code (0-5) metrics |

---

## Detailed Mapping

### CONSOLIDATED-01: Core Framework & Infrastructure

**Document Section**: Lines 1-926
**Purpose**: Core logistics framework and infrastructure nodes

**TTL Schema Files**:

| File | Lines | Key Classes | Key Properties |
|------|-------|-------------|----------------|
| `hvdc_ontology.ttl` | 191 | Party, Asset, Document, Process, Event, Contract, Regulation, Location, KPI | hasDocument, references, involves, locatedAt, governs, measuredBy |
| `hvdc_nodes.ttl` | 214 | Warehouse, Site, OffshoreBase (MOSB), Port, Node | operatesFrom, dispatches, consolidates, handles |

**TTL Data Instances**:

| File | Triples | Coverage |
|------|---------|----------|
| `hvdc_status_v35.ttl` | ~50,000 | 100% cases have hvdc:Vendor (Party) |
| `lightning_final.ttl` | ~200,000 | Full network with lightning entities |
| `abu_final.ttl` | ~180,000 | Full network with Abu Dhabi entities |

**JSON Analytics**:

| File | Content | Description |
|------|---------|-------------|
| `unified_network_data_v12_hvdc.json` | Network graph data | Complete node and edge structure |
| `unified_network_stats_v12_hvdc.json` | Statistics | Node/edge counts, centrality metrics |
| `unified_network_meta_v12_hvdc.json` | Metadata | Provenance, version info |

---

### CONSOLIDATED-02: Warehouse & Flow Code ⭐

**Document Section**: Lines 1-991
**Purpose**: Warehouse operations and Flow Code v3.5 algorithm

**TTL Schema Files**:

| File | Lines | Key Concepts |
|------|-------|--------------|
| `flow_code.ttl` | 209 | FlowCode enum 0-5, LogisticsFlow class, FlowCode calculation rules |
| `FlowCode.shape.ttl` | 89 | SHACL constraints for Flow 0-5, AGI/DAS ban rules, Flow 5 detection |

**Flow Code v3.5 Mapping**:

| Flow Code | TTL Value | Documentation | TTL Schema | Data Instances | SHACL Validation |
|-----------|-----------|---------------|------------|----------------|------------------|
| **0** (Pre Arrival) | `xsd:string "0"` | Lines 62-64 | flow_code.ttl L45 | hvdc_status_v35.ttl | FlowCode.shape.ttl L12 |
| **1** (Port→Site) | `xsd:string "1"` | Lines 66-68 | flow_code.ttl L50 | 156 cases (1.6%) | FlowCode.shape.ttl L20 |
| **2** (Port→WH→Site) | `xsd:string "2"` | Lines 70-72 | flow_code.ttl L55 | 3,421 cases (34.9%) | FlowCode.shape.ttl L28 |
| **3** (Port→MOSB→Site) | `xsd:string "3"` | Lines 74-76 | flow_code.ttl L60 | 2,109 cases (21.5%) | FlowCode.shape.ttl L36 |
| **4** (Port→WH→MOSB→Site) | `xsd:string "4"` | Lines 78-80 | flow_code.ttl L65 | 3,487 cases (35.6%) | FlowCode.shape.ttl L44 |
| **5** (Mixed/Incomplete) | `xsd:string "5"` | Lines 82-89 | flow_code.ttl L70 | 388 cases (4.0%) | FlowCode.shape.ttl L52 |

**AGI/DAS Domain Rules**:

| Rule | Documentation | TTL Schema | SHACL Validation | Data Impact |
|------|---------------|------------|------------------|-------------|
| AGI/DAS Flow-1 Ban | Lines 486-506 | FlowCode.shape.ttl L62 | AGIDASFlow1BanShape | Blocks Flow 1 for AGI/DAS |
| AGI/DAS Flow 0/1/2 → 3 Override | Lines 253-261 | flow_code.ttl L75 | Auto-applied | Override reason tracked |
| Flow 5 Detection | Lines 506-537 | FlowCode.shape.ttl L84 | Flow5ExceptionDetectionShape | Requires override reason |

**TTL Data Instances**:

| File | Instances | Flow Distribution |
|------|-----------|-------------------|
| `hvdc_status_v35.ttl` | 9,795 cases | Complete Flow 0-5 distribution |
| 7,807 cases have AGI/DAS Final_Location |  | Subject to MOSB leg requirement |

**JSON Analytics**:

| File | Content | Description |
|------|---------|-------------|
| `cases_by_flow.json` | Flow distribution | 6 Flow Code buckets with counts/percentages |
| `flow_event_patterns.json` | Event patterns | WH/MOSB/Site event sequences |

---

### CONSOLIDATED-03: Document Guardian & OCR

**Document Section**: Lines 1-1,125
**Purpose**: Document processing, OCR pipeline, trust validation

**TTL Schema Files**:

| File | Lines | Key Classes | KPI Gates |
|------|-------|-------------|-----------|
| `hvdc_ontology.ttl` | LDG section | LDG Document, Metric, Audit, TrustLayer | MeanConf≥0.92, TableAcc≥0.98, NumericIntegrity=1.00, **EntityMatch≥0.98** |

**OCR KPI Gate Policy**:

| KPI | Threshold | SHACL Rule | Enforcement | Source |
|-----|-----------|------------|-------------|--------|
| MeanConf (평균 신뢰도) | ≥ 0.92 | OCRKPIGateShape | ZERO-fail-safe | Lines 854-880 |
| TableAcc (테이블 정확도) | ≥ 0.98 | OCRKPIGateShape | ZERO-fail-safe | Lines 1108-1111 |
| NumericIntegrity (수치 무결성) | = 1.00 | OCRKPIGateShape | ZERO-fail-safe | Lines 1110 |
| EntityMatch (엔티티 매칭률) | ≥ 0.98 ⭐ | OCRKPIGateShape | ZERO-fail-safe | Lines 1111 |

**Note**: EntityMatch threshold upgraded from 0.90 to 0.98 on 2025-10-31 (see README.md KPI Gate Change History).

**TTL Data Instances**:

| File | Coverage |
|------|----------|
| `hvdc_status_v35.ttl` | Document metadata embedded in Case instances |
| `specialized/invoice_*.ttl` | Invoice OCR results |

**JSON Analytics**:

| File | Content |
|------|---------|
| `validation_summary.json` | OCR quality metrics |
| `reports/invoice_*.json` | Invoice analysis with trust scores |

---

### CONSOLIDATED-04: Barge & Bulk Cargo

**Document Section**: Lines 1-331
**Purpose**: Barge operations, bulk cargo handling, OOG cargo

**TTL Schema Files**:

| File | Lines | Key Classes |
|------|-------|-------------|
| `hvdc_ontology.ttl` | Barge section | Barge, BulkCargo, Shipment, OOG Shipment |
| `Shipment.shape.ttl` | 78 | General shipment constraints |
| `ShipmentOOG.shape.ttl` | 56 | OOG dimension and weight constraints |

**Standards Compliance**:

| Standard | Coverage | TTL Schema | Data Instances |
|----------|----------|------------|----------------|
| IMSBC Code | Bulk cargo classification | hvdc_ontology.ttl | abu_*.ttl, sheet_*.ttl |
| SOLAS | Safety of Life at Sea | hvdc_ontology.ttl | abu_final.ttl |
| OOG Dimensions | Length/width/height limits | ShipmentOOG.shape.ttl | specialized/abu_*.ttl |

**TTL Data Instances**:

| File | Instances | Description |
|------|-----------|-------------|
| `abu_final.ttl` | Complete Abu Dhabi network | Includes barge operations |
| `specialized/abu_*.ttl` (4 files) | ~100K triples | Detailed barge and bulk cargo data |
| `specialized/sheet_*.ttl` (3 files) | ~50K triples | Sheet-based bulk cargo extracts |

**JSON Analytics**:

| File | Content |
|------|---------|
| `reports/abu_comprehensive_summary.json` | Comprehensive Abu Dhabi analysis |
| `reports/abu_lpo_analysis.json` | LPO (Large Project Operations) analysis |
| `reports/abu_guidelines_analysis.json` | Operational guidelines |

---

### CONSOLIDATED-05: Invoice & Cost Management

**Document Section**: Lines 1-434
**Purpose**: Invoice verification, cost guard, PRISM.KERNEL

**TTL Schema Files**:

| File | Lines | Key Classes |
|------|-------|-------------|
| `hvdc_ontology.ttl` | Invoice section | Invoice, InvoiceLineItem, CostGuard |

**Cost Guard Rules**:

| Rule | Value | Documentation | Enforcement |
|------|-------|---------------|-------------|
| Base Currency | USD | Lines 25-29 | Fixed |
| FX Rate | 3.6725 AED/USD | Lines 62-69 | Locked |
| Delta% Band | PASS: ±3%<br>WARN: ±5%<br>CRITICAL: ±8% | Lines 62-69 | SHACL validation |
| Lane Normalization | Standard lanes | Lines 84-90 | Auto-mapping |

**PRISM.KERNEL Format**:

| Component | Description | Example |
|-----------|-------------|---------|
| Recap (5 lines) | Summary with verdict | "INV-2025-001 \| DSV Logistics \| USD 15,000.00 \| Δ% 2.1% \| VERDICT: PASS" |
| Artifact (JSON) | Complete proof data | Line items, rate refs, calculations, proof hash |

**TTL Data Instances**:

| File | Instances |
|------|-----------|
| `specialized/invoice_*.ttl` (3 files) | ~30K triples |
| Invoice LineItems with CostGuard validation |

**JSON Analytics**:

| File | Content |
|------|---------|
| `reports/invoice_analysis_report.json` | Invoice analysis |
| `reports/invoice_data_summary.json` | Invoice statistics |
| `integration_data.json` | Includes invoice metadata |

---

## Cross-Domain Dependencies

### Flow Code → OCR → Invoice

```
CONSOLIDATED-02 (Flow Code)
    ↓ (cases have documents)
CONSOLIDATED-03 (Document OCR)
    ↓ (invoice validation)
CONSOLIDATED-05 (Invoice & Cost)
```

### Framework → Flow → Operations

```
CONSOLIDATED-01 (Core Framework)
    ↓ (defines infrastructure)
CONSOLIDATED-02 (Warehouse Flow)
    ↓ (operates on nodes)
CONSOLIDATED-04 (Barge & Bulk)
```

---

## Validation Coverage

| Validation Type | Source | Target | Files |
|-----------------|--------|--------|-------|
| SHACL Shape | `02_schemas/shapes/` | `03_data/ttl/current/` | All TTL data |
| Flow Code Rules | FlowCode.shape.ttl | hvdc_status_v35.ttl | 9,795 cases |
| OCR KPI Gates | CONSOLIDATED-03 | Invoice TTL files | All invoices |
| Cost Guard Bands | CONSOLIDATED-05 | Invoice TTL files | All invoice line items |

---

## Summary Statistics

| Category | Documentation | TTL Schemas | TTL Data | JSON Analytics | Validation |
|----------|---------------|-------------|----------|----------------|------------|
| Files | 5 consolidated | 9 TTL files | 18 TTL files | 36 JSON files | 5 reports |
| Lines | 4,190 | 1,296 | 428,797 | 65,016 | 103 |
| Coverage | 100% concepts | 100% ontologies | 100% instances | 100% analysis | Continuous |

---

**For implementation details, see**: `05_cross_references/FLOW_CODE_LINEAGE.md`

**For query examples, see**: `05_cross_references/QUERY_TEMPLATES.md`



---

# Part 5: Query Templates and Usage

# Flow Code v3.5 Lineage

**Purpose**: Complete traceability of Flow Code v3.5 across all layers
**Version**: v3.5
**Last Updated**: 2025-10-31

---

## Executive Summary

Flow Code v3.5 classifies logistics flow into 6 categories (0-5) based on warehouse hops, MOSB transit, and site arrival. It extends v3.4 by:
- Adding Flow 5 (Mixed/Incomplete) for exception cases
- Implementing AGI/DAS domain rules (MOSB leg required)
- Providing override tracking (FLOW_CODE_ORIG, FLOW_OVERRIDE_REASON)

---

## Layer-by-Layer Traceability

### 1. Documentation Layer

**File**: `01_ontology/consolidated/CONSOLIDATED-02-warehouse-flow.md`

| Section | Lines | Content |
|---------|-------|---------|
| Flow Code Definition | 62-100 | Flow 0-5 descriptions |
| AGI/DAS Domain Rules | 253-261 | Override 0/1/2 → 3 |
| SHACL Constraints | 486-537 | AGI/DAS Flow-1 ban, Flow-5 detection |
| Algorithm Overview | 1-991 | Complete v3.5 specification |

**Key Rules**:
- AGI/DAS cannot have Flow 1 (direct Port→Site)
- AGI/DAS with Flow 0/1/2 automatically upgraded to 3
- Flow 5 for mixed/incomplete/missing patterns

### 2. Schema Layer

**Files**:
- `02_schemas/core/flow_code.ttl` (209 lines)
- `02_schemas/shapes/FlowCode.shape.ttl` (89 lines)

**Classes Defined**:
```turtle
hvdc:FlowCode a rdfs:Class .
hvdc:LogisticsFlow a hvdc:FlowCode .
```

**Properties**:
```turtle
hvdc:hasFlowCode a owl:DatatypeProperty .
hvdc:hasFlowCodeOriginal a owl:DatatypeProperty .
hvdc:hasFlowOverrideReason a owl:DatatypeProperty .
```

**SHACL Rules**:
```turtle
hvdc:AGIDASFlow1BanShape
  - Prohibits Flow 1 for AGI/DAS destinations

hvdc:Flow5ExceptionDetectionShape
  - Detects mixed/multiple/incomplete patterns
  - Requires override reason
```

### 3. Data Layer

**File**: `03_data/ttl/current/hvdc_status_v35.ttl`

**Instances**: 9,795 cases

**Distribution**:

| Flow Code | Count | Percentage | Description |
|-----------|-------|------------|-------------|
| 0 | 234 | 2.4% | Pre Arrival |
| 1 | 156 | 1.6% | Port → Site |
| 2 | 3,421 | 34.9% | Port → WH → Site |
| 3 | 2,109 | 21.5% | Port → MOSB → Site |
| 4 | 3,487 | 35.6% | Port → WH → MOSB → Site |
| 5 | 388 | 4.0% | Mixed/Incomplete |

**Override Statistics**:
- Cases with override: ~7,807 (AGI/DAS destinations)
- Override reason tracked: 100%

### 4. Analytics Layer

**Files**:
- `03_data/json/gpt_cache/cases_by_flow.json` - Distribution stats
- `03_data/json/validation/flow_event_patterns.json` - Event analysis

### 5. Implementation Layer

**Files**:
- `scripts/core/flow_code_calc.py` - CLI tool (464 lines)
- `logiontology/src/ingest/flow_code_calculator.py` - Core library

**Algorithm Steps**:
1. Field validation and preprocessing
2. Observation calculation (WH cnt, MOSB presence, Site presence)
3. Basic Flow Code 0-4 calculation
4. AGI/DAS domain override (0/1/2 → 3)
5. Mixed case handling (→ 5)
6. Final output with tracking

---

## Flow Code Definitions

| Code | Pattern | Conditions | Example |
|------|---------|------------|---------|
| **0** | Pre Arrival | No inbound events observed | Before any port/WH/site arrival |
| **1** | Port → Site | WH=0, MOSB=0, Pre≠True | Direct MIR/SHU delivery |
| **2** | Port → WH → Site | WH≥1, MOSB=0, Pre≠True | Via DSV Indoor |
| **3** | Port → MOSB → Site | WH=0, MOSB=1, Pre≠True<br>OR AGI/DAS forced | Offshore delivery |
| **4** | Port → WH → MOSB → Site | WH≥1, MOSB=1, Pre≠True | Combined route |
| **5** | Mixed/Incomplete | MOSB without Site<br>OR WH 2+ without MOSB<br>OR timestamp violations | Exception cases |

---

## Domain Rules

### Rule 1: AGI/DAS Flow-1 Ban

**Documentation**: CONSOLIDATED-02 Lines 486-506
**SHACL**: FlowCode.shape.ttl Lines 62-89
**Enforcement**: Automatic violation detection

```turtle
hvdc:AGIDASFlow1BanShape a sh:NodeShape ;
    sh:targetClass hvdc:TransportEvent ;
    sh:sparql [
        sh:severity sh:Violation ;
        sh:message "AGI/DAS: Flow Code 1 (Port→Site) 금지 - MOSB 레그 필수" ;
        sh:select """
            PREFIX hvdc: <http://samsung.com/project-logistics#>
            SELECT $this ?site ?flowCode
            WHERE {
                $this hvdc:hasDestination ?site .
                FILTER(?site IN ("AGI", "DAS"))
                $this hvdc:hasFlowCode ?flowCode .
                FILTER(xsd:integer(?flowCode) = 1)
            }
        """
    ] .
```

### Rule 2: AGI/DAS Override

**Documentation**: CONSOLIDATED-02 Lines 253-261
**Implementation**: flow_code_calc.py Lines 241-262
**Tracking**: FLOW_CODE_ORIG, FLOW_OVERRIDE_REASON

**Logic**:
```python
if final_location in ["AGI", "DAS"] and flow_code in [0, 1, 2]:
    flow_code_orig = flow_code
    flow_code = 3
    override_reason = "AGI/DAS requires MOSB leg"
```

### Rule 3: Flow-5 Exception Detection

**Documentation**: CONSOLIDATED-02 Lines 506-537
**SHACL**: FlowCode.shape.ttl Lines 84-104

**Patterns**:
- `WH_EVENTS_MULTIPLE_MIXED`: WH events 2+ times mixed
- `MOSB_WITHOUT_SITE`: MOSB present but no Site arrival
- `TIMESTAMP_ORDER_VIOLATION`: Date sequence reversed/missing

---

## Usage Examples

### SPARQL Query

```sparql
PREFIX hvdc: <http://samsung.com/project-logistics#>
SELECT ?flowCode ?description (COUNT(?case) AS ?count)
WHERE {
  ?case hvdc:hasFlowCode ?flowCode ;
        hvdc:hasFlowDescription ?description .
}
GROUP BY ?flowCode ?description
ORDER BY ?flowCode
```

### Python CLI

```bash
python scripts/core/flow_code_calc.py \
    --input data/HVDC_STATUS.xlsx \
    --output output/flow_codes.csv \
    --stats-only
```

---

## Validation

### SHACL Validation

All Flow Code instances validated against:
- `FlowCode.shape.ttl` - Shape constraints
- `hvdc:AGIDASFlow1BanShape` - Domain rules
- `hvdc:Flow5ExceptionDetectionShape` - Exception patterns

### Data Quality

From `03_data/json/validation/`:
- Flow distribution validates
- Override reasons tracked
- No unauthorized Flow 1 → AGI/DAS

---

## Future Enhancements

1. **Phase 2**: MIR/SHU direct delivery distinction (currently both Flow 1)
2. **Flow 5 Refinement**: Sub-categorize exception patterns
3. **Event Count**: WH/MOSB event quantity tracking

---

**See Also**: `QUERY_TEMPLATES.md`, `ONTOLOGY_COVERAGE_MATRIX.md`



---

# Part 6: Validation and Quality Assurance

# 온톨로지 데이터 허브 - TTL & JSON 파일 가이드

**버전**: 1.0
**생성일**: 2025-11-01
**총 파일 수**: 68개 (TTL 18개 + JSON 50개)

---

## 목차

1. [개요](#개요)
2. [TTL 파일 설명](#ttl-파일-설명) (18개)
3. [JSON 파일 설명](#json-파일-설명) (50개)
4. [사용 예시](#사용-예시)
5. [빠른 참조](#빠른-참조)
6. [파일 간 관계](#파일-간-관계)

---

## 개요

### 전체 파일 인벤토리

| 카테고리 | 파일 수 | 설명 |
|----------|---------|------|
| **TTL - 현재 데이터** | 1 | Flow Code v3.5 최신 운영 데이터 |
| **TTL - 최종 확정** | 2 | 안정화된 참조 데이터 |
| **TTL - 특화 데이터** | 15 | 도메인별 상세 분석 |
| **JSON - GPT 캐시** | 3 | GPT 응답용 사전 계산 |
| **JSON - 통합 데이터** | 10 | 시스템 통합 및 비교 |
| **JSON - 리포트** | 18 | 도메인별 분석 보고서 |
| **JSON - 검증** | 5 | 데이터 품질 검증 |
| **TOTAL** | **68** | **종합 데이터 허브** |

### 파일 명명 규칙

**TTL 파일**:
- `[시스템]_[버전].ttl`: 예) `hvdc_status_v35.ttl`
- `[프로젝트]_[타입].ttl`: 예) `abu_logistics_data.ttl`
- `[도메인]_[날짜]_[시간].ttl`: 예) `invoice_SEPT_20251020_000829.ttl`

**JSON 파일**:
- `[설명]_[범위].json`: 예) `cases_by_flow.json`, `monthly_warehouse_inbound.json`
- `[시스템]_[목적].json`: 예) `abu_comprehensive_summary.json`
- `[타입]_summary.json`: 예) `validation_summary.json`

### 공통 데이터 패턴

**TTL (Turtle 포맷)**:
- RDF 그래프 구조 (Subject-Predicate-Object)
- Namespace: `hvdc:`, `abu:`, `lightning:` 등
- 표준 필드: `hasCBM`, `hasFlowCode`, `hasVendor` 등
- 이벤트 구조: `hasInboundEvent`, `hasOutboundEvent`

**JSON (표준 포맷)**:
- 배열: `[{...}, {...}]` (집계 데이터)
- 객체: `{...}` (요약 데이터)
- 공통 필드: `timestamp`, `count`, `status` 등

---

## TTL 파일 설명

### A. 현재 데이터 (1개 파일)

#### `hvdc_status_v35.ttl`

**위치**: `03_data/ttl/current/`
**크기**: 9,844줄, 9,904 트리플, 755 케이스
**버전**: Flow Code v3.5

**내용**:
HVDC 프로젝트의 최신 물류 데이터로, Flow Code v3.5 알고리즘으로 분류된 모든 케이스를 포함합니다.

**주요 속성**:
- `hasCBM`: 화물 용적 (Cubic Meter)
- `hasFlowCode`: 물류 흐름 코드 (0-5)
- `hasFlowCodeOriginal`: 원본 Flow Code (Override 추적용)
- `hasFlowDescription`: Flow 설명 (예: "Flow 2: Port → WH → Site")
- `hasFlowOverrideReason`: Override 사유 (예: "AGI/DAS requires MOSB leg")
- `hasHvdcCode`: HVDC 코드 (예: "HVDC-ADOPT-PPL-0001")
- `hasVendor`: 공급업체 (예: "Prysmian", "Hitachi")
- `hasFinalLocation`: 최종 도착지 (예: "DAS", "AGI")

**이벤트 구조**:
```
hasInboundEvent [
    hasEventDate "2024-01-20" ;
    hasLocationAtEvent "Vijay Tanks" ;
    hasQuantity 1.0
]
```

**Flow Code 분포** (755 케이스):
- Flow 0: 71 (9.4%) - Pre Arrival
- Flow 1: 255 (33.8%) - Port → Site
- Flow 2: 152 (20.1%) - Port → WH → Site
- Flow 3: 131 (17.4%) - Port → MOSB → Site
- Flow 4: 65 (8.6%) - Port → WH → MOSB → Site
- Flow 5: 81 (10.7%) - Mixed/Incomplete

**용도**:
- 실시간 물류 쿼리를 위한 주요 데이터 소스
- MCP 서버의 기본 데이터셋
- Flow Code 분포 및 AGI/DAS 규칙 검증

---

### B. 최종 확정 데이터 (2개 파일)

#### `abu_final.ttl`

**위치**: `03_data/ttl/finalized/`
**크기**: 923KB, 18,894 트리플, 500 엔티티

**내용**:
아부다비 시스템의 최종 통합 RDF 데이터로, 물류 데이터, LPO 데이터, 이미지 메타데이터를 포함합니다.

**주요 속성**:
- `abu:containerId`: 컨테이너 ID
- `abu:containerType`: 컨테이너 타입
- `abu:responsiblePerson`: 책임자 이름
- `abu:reportedBy`: 보고자 (예: "System", "- 상욱: 40ft OT Container")
- `abu:timestamp`: 타임스탬프

**Namespaces**:
- `abu:`: 아부다비 핵심 네임스페이스
- `abui:`: 아부다비 인스턴스
- `ns1:`: LPO 네임스페이스

**용도**:
- 아부다비 시스템 안정적 참조 데이터
- 책임자 추적 및 타임라인 분석
- 통합 보고서 생성

---

#### `lightning_final.ttl`

**위치**: `03_data/ttl/finalized/`
**크기**: 3.1MB, 67,000 트리플, 2,000 엔티티

**내용**:
Lightning 프로젝트의 최종 통합 RDF로, 이미지, 엔티티, WhatsApp 데이터를 통합했습니다.

**주요 속성**:
- `lightning:filename`: 파일명
- `lightning:fileSizeMB`: 파일 크기 (MB)
- `lightning:imageType`: 이미지 타입 (예: "WhatsApp_Image")
- `lightning:capturedDate`: 촬영일
- `lightning:filePath`: 파일 경로

**Namespaces**:
- `lightning:`: Lightning 핵심
- `lightningi:`: Lightning 인스턴스

**용도**:
- Lightning 프로젝트 최종 참조 데이터
- 이미지 메타데이터 추적
- WhatsApp 통합 분석

---

### C. 특화 데이터 (15개 파일)

#### 아부다비 시스템 파일 (6개)

**1. `abu_integrated_system.ttl`**
- 물류 + LPO + 이미지 통합 시스템
- 운영 데이터 총합

**2. `abu_logistics_data.ttl`** (0.1MB, 2,814 트리플)
- 기본 물류 데이터만
- 경량 쿼리용

**3. `abu_lpo_data.ttl`** (0.2MB, 5,779 트리플)
- LPO(Local Purchase Order) 전용 데이터
- 구매 주문 분석

**4. `abu_with_images.ttl`** (0.2MB, 5,070 트리플)
- 이미지 메타데이터 포함
- 시각 자료 추적

**5. `abu_comprehensive_summary.json`** (리포트, 3. 데이터 참조)
- 종합 분석 요약
- 통계 및 KPI

#### Lightning 시스템 파일 (6개)

**1. `lightning_integrated_system.ttl`** (3.0MB, 65,000 트리플)
- 기본 통합 시스템
- 엔티티 + 관계

**2. `lightning_enriched_system.ttl`** (3.0MB, 66,000 트리플)
- CSV 엔티티 보강
- 고유값: 243개 엔티티 추가

**3. `lightning_enhanced_system.ttl`** (3.0MB, 66,500 트리플)
- 주요 엔티티 상세 보강
- 타임태그 및 참조 추가

**4. `lightning_whatsapp_integrated.ttl`**
- WhatsApp 메시지 통합
- 4,671개 메시지

**5. `lightning_with_images.ttl`** (0.04MB, 904 트리플)
- 이미지 메타데이터만
- 321개 이미지 엔티티

#### 인보이스 데이터 (3개)

**1. `invoice_SEPT_20251020_000803.ttl`**
- 비어 있음 (삭제 권장)

**2. `invoice_SEPT_20251020_000829.ttl`** (0.02MB, 526 트리플)
- SEPT 인보이스 (2025-09)
- 처리 결과 초기 버전

**3. `invoice_SEPT_20251020_002513.ttl`** (0.02MB, 475 트리플)
- SEPT 인보이스 (2025-09) 수정본
- 최종 검증 버전

#### 시트 데이터 (3개)

**시트 9, 10, 12**:
- 각 0.003MB, 90 트리플
- 원본 Excel에서 추출
- HVDC 코드 6개 컬럼 포함

**용도**: 특정 시트 분석 및 검증용

---

## JSON 파일 설명

### A. GPT 캐시 (3개 파일)

#### `cases_by_flow.json`

**위치**: `03_data/json/gpt_cache/`
**구조**: Flow Code별 집계 배열

```json
[
  { "flow_code": "0", "case_count": 172 },
  { "flow_code": "1", "case_count": 3682 },
  { "flow_code": "2", "case_count": 4391 },
  { "flow_code": "3", "case_count": 750 }
]
```

**용도**: GPT가 빠르게 Flow 분포 조회 시 사용

---

#### `monthly_warehouse_inbound.json`

**위치**: `03_data/json/gpt_cache/`
**구조**: 월별/창고별 입고 집계

```json
[
  {
    "month": "2024-01",
    "warehouse": "MIR",
    "event_count": 5,
    "total_quantity": 5.0
  }
]
```

**주요 창고**:
- MIR (Mirfa), SHU (Shuweihat)
- MOSB (중앙 허브)
- AGI (Al Ghallan Island), DAS (Das Island)

**용도**: 월별 창고별 트래픽 분석

---

#### `vendor_summary.json`

**위치**: `03_data/json/gpt_cache/`
**구조**: 공급업체별 집계

```json
[
  {
    "vendor": "SAS Power",
    "month": "2025-05",
    "event_count": 20,
    "total_quantity": 20.0
  }
]
```

**용도**: 공급업체별 물류 현황 추적

---

### B. 통합 데이터 (10개 파일)

#### `unified_network_data_v12_hvdc.json`

**위치**: `03_data/json/integration/`
**크기**: 대용량 네트워크 그래프
**구조**: NetworkX 그래프 포맷

```json
{
  "directed": false,
  "multigraph": false,
  "graph": { "name": "UNIFIED_LOGISTICS_NETWORK_v12_HVDC" },
  "nodes": [
    {
      "type": "root",
      "ontology_class": "Project",
      "label": "HVDC Project",
      "level": 0,
      "color": "#ff0000",
      "community_id": 1,
      "id": "HVDC_Project"
    },
    {
      "type": "system",
      "ontology_class": "System",
      "label": "JPT71 System",
      "level": 1,
      "color": "#ff6b6b",
      "community_id": 0,
      "id": "JPT71_System"
    }
  ],
  "edges": [...]
}
```

**노드 타입**:
- `root`: 최상위 프로젝트
- `system`: 시스템 (ABU, JPT71, HVDC)
- `port`: 항만 (Zayed, Khalifa, Jebel Ali)
- `warehouse`: 창고 (DSV, DHL 등)
- `hub`: 허브 (MOSB)
- `site`: 현장 (MIR, SHU, AGI, DAS)

**용도**:
- 네트워크 시각화 (GraphX, Cytoscape)
- 도메인 분석 (community_id)
- 연결도 분석 (edges)

---

#### `metadata.json`

**위치**: `03_data/json/integration/`
**구조**: RDF 파일 메타데이터

```json
{
  "rdf_files_metadata": {
    "generated_date": "2025-10-22T10:00:00Z",
    "total_files": 16,
    "final_files": 2,
    "version_files": 14,
    "total_size_mb": 10.2,
    "files": { ... },
    "statistics": { ... },
    "organization_notes": { ... }
  }
}
```

**용도**: 파일 인벤토리 및 버전 관리

---

#### `processing_summary.json`

**위치**: `03_data/json/integration/`
**구조**: Excel 변환 처리 결과

```json
{
  "timestamp": "2025-10-19T20:35:09.184642",
  "input_file": "HVDC_입고로직_종합리포트_20251019_165153_v3.0-corrected.xlsx",
  "analysis": {
    "sheet_9": { "rows": 1000, "columns": 69, ... },
    "sheet_10": { "rows": 7161, "columns": 69, ... },
    "sheet_12": { "rows": 7161, "columns": 69, ... }
  },
  "results": { ... },
  "summary": {
    "total_sheets": 12,
    "hvdc_sheets_processed": 3,
    "success_count": 3,
    "success_rate": 1.0
  }
}
```

**용도**: TTL 변환 품질 추적

---

#### 기타 통합 파일

**`abu_lightning_comparison_data.json`**:
- ABU vs Lightning 비교 분석
- 시각화 준비 데이터

**`unified_network_stats*.json`** (4개):
- `_v12_hvdc`, `_meta`, `_stats`: 통계 변형
- 노드/엣지 수, 커뮤니티 분포

**`integration_data*.json`** (2개):
- `_meaningful`, 기본: 의미적 연결 데이터
- 크로스 도메인 매핑

---

### C. 리포트 (18개 파일)

#### 아부다비 리포트 (9개)

**1. `abu_comprehensive_summary.json`**
- 종합 요약: 모든 ABU 데이터
- 통계, 비율, 추세

**2. `abu_data_summary.json`**
- 데이터 요약: 행/컬럼/누락값
- 시트별 메타데이터

**3. `abu_dhabi_logistics_tag_dict_v1.json`**
- 태그 사전: 로직 태그 → 설명
- 표준화된 용어집

**4. `abu_guidelines_analysis.json`**
- 가이드라인 준수 분석
- 규정 위반 사례

**5. `abu_integrated_stats.json`**
- 통합 통계: 파일 종합
- 트리플/엔티티/관계 수

**6. `abu_lpo_analysis.json`**
- LPO 분석: 구매 주문 상세
- 책임자/날짜/양 추적

**7. `abu_responsible_persons_analysis.json`**
- 책임자 분석: 인물별 활동
- 타임라인 및 패턴

**8. `abu_sparql_analysis_data.json`**
- SPARQL 쿼리 결과
- 그래프 분석 산출물

**9. `abu_whatsapp_analysis.json`**
- WhatsApp 통신 분석
- 메시지 패턴 및 빈도

---

#### Lightning 리포트 (3개)

**1. `lightning_entities_stats.json`**
```json
{
  "total_entities": 321,
  "total_messages": 4671,
  "entity_counts": {
    "vessels": 33,
    "locations": 23,
    "operations": 31,
    "cargo": 27,
    "persons": 14,
    "times": 193
  }
}
```

**2. `lightning_images_stats.json`**
- 이미지 메타데이터 통계
- 파일 크기, 타입 분포

**3. `lightning_integrated_stats.json`**
- Lightning 통합 통계
- 엔티티/관계/이미지 총합

---

#### 인보이스 리포트 (2개)

**1. `invoice_analysis_report.json`**
- 인보이스 상세 분석 리포트
- 7,504줄, 1,000개 샘플 분석

**구조**:
```json
{
  "analysis": {
    "file_path": "data/invoice_sept2025.xlsm",
    "file_name": "invoice_sept2025.xlsm",
    "analysis_date": "2025-10-20T00:06:33",
    "sheets": {
      "SEPT": {
        "name": "SEPT",
        "dimensions": "34 rows x 27 columns",
        "total_cells": 918,
        "non_empty_cells": "548"
      }
    }
  }
}
```

**2. `invoice_data_summary.json`**
- 인보이스 데이터 요약
- 시트별 행/컬럼/비율

---

#### 강화/보완 통계 (2개)

**1. `enhancement_stats.json`**
- 데이터 강화 통계
- 보강된 필드 수

**2. `enrichment_stats.json`**
```json
{
  "original_triples": 65730,
  "enriched_triples": 66710,
  "new_triples": 980,
  "csv_stats": {
    "Document": { "unique": 22, "total_mentions": 1654 },
    "Equipment": { "unique": 23, "total_mentions": 1076 },
    "Operation": { "unique": 34, "total_mentions": 4552 },
    ...
  },
  "added_counts": { ... }
}
```

---

#### WhatsApp 분석 (2개)

**1. `whatsapp_images_analysis.json`**
- WhatsApp 이미지 분석
- 촬영일/파일명/크기 패턴

**2. `whatsapp_integration_stats.json`**
- WhatsApp 통합 통계
- 메시지 수, 엔티티 추출

---

### D. 검증 데이터 (5개 파일)

#### `validation_summary.json`

**위치**: `03_data/json/validation/`
**구조**: 전체 검증 지표

```json
{
  "timestamp": "2025-10-30T21:11:05.508832",
  "source_ttl": "rdf_output/test_data_wh_events.ttl",
  "total_triples": 72692,
  "validation_results": {
    "human_gate_flow23": {
      "count": 0,
      "file": "validation_results\\human_gate_flow23_no_inbound.json"
    },
    "missing_dates": {
      "count": 0,
      "file": "validation_results\\human_gate_missing_dates.json"
    },
    "coverage_stats": {
      "total_cases": 8995,
      "with_inbound": 5012,
      "with_outbound": 2381,
      "with_both": 1194,
      "with_neither": 2796,
      "inbound_coverage_pct": 55.72,
      "outbound_coverage_pct": 26.47
    },
    "flow_patterns": [
      {
        "flow_code": "0",
        "total_cases": 172,
        "with_inbound": 0,
        "with_outbound": 0,
        "inbound_pct": 0.0,
        "outbound_pct": 0.0
      },
      ...
    ]
  }
}
```

**검증 항목**:
1. **Human Gate Flow 2/3**: Inbound 이벤트 없는 Flow 2/3 사례
2. **Missing Dates**: 날짜 누락 사례
3. **Coverage Stats**: 이벤트 커버리지 통계
4. **Flow Patterns**: Flow별 이벤트 패턴

**용도**: 데이터 품질 보증 및 리포팅

---

#### `event_coverage_stats.json`

**구조**: 이벤트 커버리지 상세

```json
{
  "total_cases": 8995,
  "with_inbound": 5012,
  "with_outbound": 2381,
  "with_both": 1194,
  "with_neither": 2796,
  "inbound_coverage_pct": 55.72,
  "outbound_coverage_pct": 26.47
}
```

**의미**:
- `with_inbound`: 입고 이벤트 있음
- `with_outbound`: 출고 이벤트 있음
- `with_both`: 입고+출고 둘 다
- `with_neither`: 둘 다 없음 (Pre Arrival 가능)

---

#### `flow_event_patterns.json`

**구조**: Flow별 이벤트 패턴

각 Flow Code별로:
- 총 케이스 수
- Inbound 비율
- Outbound 비율

**패턴 예시**:
- Flow 1 (Port → Site): Inbound 100%, Outbound 0%
- Flow 3 (Port → MOSB → Site): Inbound 98.4%, Outbound 100%

---

#### Human Gate 파일 (2개)

**1. `human_gate_flow23_no_inbound.json`**
- Flow 2/3 중 Inbound 없는 사례
- 인간 검토 필요 항목

**2. `human_gate_missing_dates.json`**
- 날짜 누락 사례
- 데이터 보완 필요

---

## 사용 예시

### RDFLib로 TTL 파일 로드하기

```python
from rdflib import Graph, Namespace

# 그래프 로드
g = Graph()
g.parse("ontology_data_hub/03_data/ttl/current/hvdc_status_v35.ttl", format='turtle')

# Namespace 정의
hvdc = Namespace("http://samsung.com/project-logistics#")

# Flow Code 분포 쿼리
query = """
PREFIX hvdc: <http://samsung.com/project-logistics#>
SELECT ?case ?flowCode WHERE {
  ?case a hvdc:Case ;
        hvdc:hasFlowCode ?flowCode .
}
LIMIT 10
"""

for row in g.query(query):
    print(f"Case: {row.case}, Flow: {row.flowCode}")
```

### JSON으로 빠른 통계 조회하기

```python
import json

# Flow 분포 로드
with open('ontology_data_hub/03_data/json/gpt_cache/cases_by_flow.json') as f:
    flow_dist = json.load(f)

# 통계 출력
for item in flow_dist:
    print(f"Flow {item['flow_code']}: {item['case_count']} cases")
```

### TTL과 JSON 데이터 상호 참조

```python
import json
from rdflib import Graph, Namespace

# TTL 로드
g = Graph()
g.parse("ontology_data_hub/03_data/ttl/current/hvdc_status_v35.ttl", format='turtle')

# JSON 검증 데이터 로드
with open('ontology_data_hub/03_data/json/validation/validation_summary.json') as f:
    validation = json.load(f)

# 검증: TTL 케이스 수 vs JSON 통계
ttl_count = len(list(g.subjects(Namespace("http://samsung.com/project-logistics#").hasFlowCode, None)))
json_total = validation['validation_results']['coverage_stats']['total_cases']

print(f"TTL cases: {ttl_count}, JSON total: {json_total}")
```

### 주요 SPARQL 쿼리

**Flow 3 (AGI/DAS) 케이스 조회**:
```sparql
PREFIX hvdc: <http://samsung.com/project-logistics#>
SELECT ?case ?vendor ?location WHERE {
  ?case a hvdc:Case ;
        hvdc:hasFlowCode "3" ;
        hvdc:hasVendor ?vendor ;
        hvdc:hasFinalLocation ?location .
}
```

**월별 입고 집계**:
```sparql
PREFIX hvdc: <http://samsung.com/project-logistics#>
SELECT (YEAR(?date) AS ?year) (MONTH(?date) AS ?month)
       (COUNT(?event) AS ?count)
WHERE {
  ?case hvdc:hasInboundEvent ?event .
  ?event hvdc:hasEventDate ?date .
}
GROUP BY ?year ?month
ORDER BY ?year ?month
```

---

## 빠른 참조

### TTL 파일 요약

| 파일명 | 크기 | 트리플 | 용도 |
|--------|------|--------|------|
| `hvdc_status_v35.ttl` | 9.6MB | 9,904 | 현재 운영 데이터 |
| `abu_final.ttl` | 0.9MB | 18,894 | ABU 최종 |
| `lightning_final.ttl` | 3.1MB | 67,000 | Lightning 최종 |
| `abu_logistics_data.ttl` | 0.1MB | 2,814 | ABU 경량 |
| `lightning_integrated_system.ttl` | 3.0MB | 65,000 | Lightning 기본 |
| `sheet_10_hvdc_data.ttl` | 0.003MB | 90 | 시트 10 |

### JSON 파일 요약

| 파일명 | 카테고리 | 구조 | 용도 |
|--------|----------|------|------|
| `cases_by_flow.json` | GPT 캐시 | 배열 | Flow 분포 |
| `monthly_warehouse_inbound.json` | GPT 캐시 | 배열 | 월별 입고 |
| `vendor_summary.json` | GPT 캐시 | 배열 | 업체별 통계 |
| `unified_network_data_v12_hvdc.json` | 통합 | 그래프 | 네트워크 분석 |
| `metadata.json` | 통합 | 객체 | 파일 메타 |
| `validation_summary.json` | 검증 | 객체 | 품질 검증 |
| `abu_comprehensive_summary.json` | 리포트 | 객체 | ABU 종합 |
| `lightning_entities_stats.json` | 리포트 | 객체 | Lightning 통계 |

### TTL 속성 인덱스

| 속성 | 설명 | 타입 |
|------|------|------|
| `hasCBM` | 화물 용적 (㎥) | Float |
| `hasFlowCode` | 물류 흐름 코드 (0-5) | String |
| `hasFlowCodeOriginal` | 원본 Flow Code | Int |
| `hasFlowDescription` | Flow 설명 | String |
| `hasFlowOverrideReason` | Override 사유 | String |
| `hasHvdcCode` | HVDC 코드 | String |
| `hasVendor` | 공급업체 | String |
| `hasFinalLocation` | 최종 도착지 | String |
| `hasInboundEvent` | 입고 이벤트 | BlankNode |
| `hasOutboundEvent` | 출고 이벤트 | BlankNode |
| `hasEventDate` | 이벤트 날짜 | Date |
| `hasLocationAtEvent` | 이벤트 위치 | String |
| `hasQuantity` | 이벤트 수량 | Float |

### JSON 필드 인덱스

| 필드 | 설명 | 타입 | 파일 예시 |
|------|------|------|-----------|
| `flow_code` | Flow 코드 | String | `cases_by_flow.json` |
| `case_count` | 케이스 수 | Int | `cases_by_flow.json` |
| `month` | 월 (YYYY-MM) | String | `monthly_warehouse_inbound.json` |
| `warehouse` | 창고 코드 | String | `monthly_warehouse_inbound.json` |
| `event_count` | 이벤트 수 | Int | `monthly_warehouse_inbound.json` |
| `total_quantity` | 총 수량 | Float | `monthly_warehouse_inbound.json` |
| `vendor` | 공급업체 | String | `vendor_summary.json` |
| `total_cases` | 총 케이스 | Int | `validation_summary.json` |
| `with_inbound` | Inbound 있음 | Int | `validation_summary.json` |
| `with_outbound` | Outbound 있음 | Int | `validation_summary.json` |
| `inbound_coverage_pct` | Inbound 커버리지 | Float | `validation_summary.json` |
| `timestamp` | 타임스탬프 | String | `validation_summary.json` |
| `nodes` | 네트워크 노드 | Array | `unified_network_data*.json` |
| `edges` | 네트워크 엣지 | Array | `unified_network_data*.json` |

---

## 파일 간 관계

### 검증 체인

```
TTL 데이터
    ↓
[RDFLib 파싱]
    ↓
validation_summary.json
    ↓
human_gate_*.json
```

**예시**: `hvdc_status_v35.ttl` → `validation_summary.json` → `human_gate_flow23_no_inbound.json`

---

### 캐시 체인

```
TTL 데이터
    ↓
[SPARQL 집계]
    ↓
cases_by_flow.json
monthly_warehouse_inbound.json
vendor_summary.json
```

**예시**: TTL → Flow Code 집계 → `cases_by_flow.json`

---

### 리포트 체인

```
TTL 데이터
    ↓
[도메인 분석]
    ↓
abu_comprehensive_summary.json
lightning_entities_stats.json
invoice_analysis_report.json
```

**예시**: `abu_*.ttl` → ABU 분석 → `abu_comprehensive_summary.json`

---

### 통합 체인

```
여러 TTL 파일
    ↓
[네트워크 통합]
    ↓
unified_network_data_v12_hvdc.json
    ↓
metadata.json
processing_summary.json
```

**예시**: ABU + Lightning TTL → 네트워크 그래프 → `unified_network_data_v12_hvdc.json`

---

## 결론

이 가이드는 `ontology_data_hub`의 68개 TTL/JSON 파일을 체계적으로 설명합니다. 각 파일의 내용, 구조, 용도를 파악하고, 서로의 관계를 이해하여 효과적으로 데이터를 활용할 수 있도록 지원합니다.

**주요 활용 사례**:
1. 실시간 쿼리: `hvdc_status_v35.ttl` 사용
2. 빠른 집계: GPT 캐시 JSON 사용
3. 품질 검증: validation JSON 확인
4. 도메인 분석: 리포트 JSON 조회
5. 통합 분석: 통합 데이터 JSON 활용

**다음 단계**:
- [MASTER_INDEX.md](05_cross_references/MASTER_INDEX.md) - 전체 인덱스
- [QUERY_TEMPLATES.md](05_cross_references/QUERY_TEMPLATES.md) - SPARQL 예시
- [USAGE_GUIDE.md](05_cross_references/USAGE_GUIDE.md) - 사용 가이드

---

**생성**: 2025-11-01
**버전**: 1.0
**작성자**: AI Assistant




---

# SPARQL Query Templates

**Purpose**: Ready-to-use SPARQL queries organized by ontology category
**Last Updated**: 2025-10-31

---

## Warehouse Operations & Flow Code

### Flow Code Distribution

```sparql
PREFIX hvdc: <http://samsung.com/project-logistics#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT
    ?flowCode
    ?description
    (COUNT(?case) AS ?count)
    ((COUNT(?case) * 100.0 / (SELECT (COUNT(?c) AS ?total) WHERE { ?c a hvdc:Case })) AS ?percentage)
WHERE {
  ?case hvdc:hasFlowCode ?flowCode ;
        hvdc:hasFlowDescription ?description .
}
GROUP BY ?flowCode ?description
ORDER BY ?flowCode
```

### AGI/DAS Compliance Check

```sparql
PREFIX hvdc: <http://samsung.com/project-logistics#>

SELECT ?case ?finalLocation ?flowCode ?overrideReason
WHERE {
  ?case hvdc:hasFinalLocation ?finalLocation .
  FILTER(?finalLocation IN ("AGI", "DAS"))
  ?case hvdc:hasFlowCode ?flowCode .
  OPTIONAL {
    ?case hvdc:hasFlowOverrideReason ?overrideReason
  }
}
ORDER BY ?flowCode
```

### Flow 5 Analysis

```sparql
PREFIX hvdc: <http://samsung.com/project-logistics#>

SELECT ?case ?flowCode ?description ?overrideReason ?finalLocation
WHERE {
  ?case hvdc:hasFlowCode "5"^^xsd:string .
  ?case hvdc:hasFlowDescription ?description .
  OPTIONAL { ?case hvdc:hasFlowOverrideReason ?overrideReason }
  OPTIONAL { ?case hvdc:hasFinalLocation ?finalLocation }
}
ORDER BY ?case
LIMIT 100
```

---

## Document OCR & Trust Layer

### OCR Quality Metrics

```sparql
PREFIX ldg: <http://example.com/ldg#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT
    ?doc
    ?meanConf
    ?tableAcc
    ?numericInt
    ?entityMatch
WHERE {
  ?doc ldg:hasMetric ?metric .
  ?metric ldg:hasMeanConf ?meanConf ;
          ldg:hasTableAcc ?tableAcc ;
          ldg:hasNumericIntegrity ?numericInt ;
          ldg:hasEntityMatch ?entityMatch .
  FILTER(?meanConf >= 0.92 && ?tableAcc >= 0.98 && ?entityMatch >= 0.98)
}
ORDER BY DESC(?meanConf)
```

### KPI Gate Violations

```sparql
PREFIX ldg: <http://example.com/ldg#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?doc ?meanConf ?tableAcc ?numericInt ?entityMatch ?violation
WHERE {
  ?doc ldg:hasMetric ?metric .
  ?metric ldg:hasMeanConf ?meanConf ;
          ldg:hasTableAcc ?tableAcc ;
          ldg:hasNumericIntegrity ?numericInt ;
          ldg:hasEntityMatch ?entityMatch .
  BIND(
    IF(?meanConf < 0.92, "MEAN_CONF_BELOW_THRESHOLD",
    IF(?tableAcc < 0.98, "TABLE_ACC_BELOW_THRESHOLD",
    IF(?numericInt != 1.00, "NUMERIC_INTEGRITY_NOT_PERFECT",
    IF(?entityMatch < 0.98, "ENTITY_MATCH_BELOW_THRESHOLD", ""))))
    AS ?violation
  )
  FILTER(?violation != "")
}
```

---

## Invoice & Cost Management

### Cost Guard Analysis

```sparql
PREFIX hvdc: <http://samsung.com/project-logistics#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT
    ?invoice
    ?vendor
    ?totalUSD
    ?deltaPercent
    ?costGuardBand
WHERE {
  ?invoice hvdc:hasVendor ?vendor ;
           hvdc:hasTotalUSD ?totalUSD ;
           hvdc:hasDeltaPercent ?deltaPercent ;
           hvdc:hasCostGuardBand ?costGuardBand .
  FILTER(?deltaPercent > 3.0)
}
ORDER BY DESC(?deltaPercent)
```

### PRISM.KERNEL Audit Trail

```sparql
PREFIX hvdc: <http://samsung.com/project-logistics#>

SELECT ?invoice ?verdict ?deltaPercent ?proofHash
WHERE {
  ?invoice hvdc:hasPrismKernel [
      hvdc:hasVerdict ?verdict ;
      hvdc:hasDeltaPercent ?deltaPercent ;
      hvdc:hasProofHash ?proofHash
    ]
}
ORDER BY ?verdict
```

---

## Network Integration

### Node Coverage

```sparql
PREFIX hvdc: <http://samsung.com/project-logistics#>

SELECT
    (COUNT(DISTINCT ?warehouse) AS ?warehouseCount)
    (COUNT(DISTINCT ?site) AS ?siteCount)
    (COUNT(DISTINCT ?mosb) AS ?mosbCount)
WHERE {
  { ?warehouse a hvdc:Warehouse }
  UNION
  { ?site a hvdc:Site }
  UNION
  { ?mosb a hvdc:OffshoreBase }
}
```

### Vendor Distribution

```sparql
PREFIX hvdc: <http://samsung.com/project-logistics#>

SELECT
    ?vendor
    (COUNT(?case) AS ?caseCount)
    (AVG(?cbm) AS ?avgCBM)
WHERE {
  ?case hvdc:hasVendor ?vendor ;
        hvdc:hasCBM ?cbm .
}
GROUP BY ?vendor
ORDER BY DESC(?caseCount)
```

---

## Complex Cross-Domain Queries

### Flow Code + OCR Quality

```sparql
PREFIX hvdc: <http://samsung.com/project-logistics#>
PREFIX ldg: <http://example.com/ldg#>

SELECT
    ?case
    ?flowCode
    ?meanConf
    ?tableAcc
WHERE {
  ?case hvdc:hasFlowCode ?flowCode ;
        hvdc:hasDocument ?doc .
  ?doc ldg:hasMetric ?metric .
  ?metric ldg:hasMeanConf ?meanConf ;
          ldg:hasTableAcc ?tableAcc .
  FILTER(?meanConf >= 0.92 && ?tableAcc >= 0.98)
}
LIMIT 50
```

### AGI/DAS + Invoice Cost

```sparql
PREFIX hvdc: <http://samsung.com/project-logistics#>

SELECT
    ?case
    ?finalLocation
    ?flowCode
    ?totalUSD
    ?deltaPercent
WHERE {
  ?case hvdc:hasFinalLocation ?finalLocation .
  FILTER(?finalLocation IN ("AGI", "DAS"))
  ?case hvdc:hasFlowCode ?flowCode .
  ?case hvdc:hasInvoice ?invoice .
  ?invoice hvdc:hasTotalUSD ?totalUSD ;
           hvdc:hasDeltaPercent ?deltaPercent .
  FILTER(?deltaPercent > 3.0)
}
ORDER BY DESC(?deltaPercent)
```

---

## Data Quality Queries

### Missing Required Fields

```sparql
PREFIX hvdc: <http://samsung.com/project-logistics#>

SELECT ?case ?field
WHERE {
  VALUES ?field { "hasFlowCode" "hasVendor" "hasHvdcCode" }
  ?case a hvdc:Case .
  FILTER NOT EXISTS {
    ?case hvdc:hasFlowCode [] .
    ?case hvdc:hasVendor [] .
    ?case hvdc:hasHvdcCode [] .
  }
}
```

### Override Tracking

```sparql
PREFIX hvdc: <http://samsung.com/project-logistics#>

SELECT
    (COUNT(?case) AS ?totalWithOverride)
    (COUNT(DISTINCT ?reason) AS ?uniqueReasons)
WHERE {
  ?case hvdc:hasFlowOverrideReason ?reason .
}
```

---

## Statistical Aggregations

### Monthly Flow Distribution

```sparql
PREFIX hvdc: <http://samsung.com/project-logistics#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT
    ?month
    ?flowCode
    (COUNT(?case) AS ?count)
WHERE {
  ?case hvdc:hasFlowCode ?flowCode ;
        hvdc:hasDate ?date .
  BIND(STRBEFORE(STR(?date), "-") AS ?month)
}
GROUP BY ?month ?flowCode
ORDER BY ?month ?flowCode
```

### WH Handling Efficiency

```sparql
PREFIX hvdc: <http://samsung.com/project-logistics#>

SELECT
    ?warehouse
    (COUNT(DISTINCT ?case) AS ?caseCount)
    (AVG(?daysInWH) AS ?avgDays)
WHERE {
  ?case hvdc:hasInboundEvent [
      hvdc:hasLocationAtEvent ?warehouse ;
      hvdc:hasEventDate ?inDate
    ] .
  ?case hvdc:hasOutboundEvent [
      hvdc:hasEventDate ?outDate
    ] .
  BIND((?outDate - ?inDate) AS ?daysInWH)
}
GROUP BY ?warehouse
ORDER BY DESC(?caseCount)
```

---

## Notes

All queries assume standard HVDC namespaces:
- `PREFIX hvdc: <http://samsung.com/project-logistics#>`
- `PREFIX ldg: <http://example.com/ldg#>`
- `PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>`

**See Also**: `USAGE_GUIDE.md`, `FLOW_CODE_LINEAGE.md`



---

# HVDC Ontology Data Hub - Usage Guide

**Purpose**: Step-by-step guide for navigating and using the ontology data hub
**Last Updated**: 2025-10-31

---

## Quick Start

### For Ontology Developers

1. Start with `01_ontology/consolidated/README.md` for overview
2. Review `05_cross_references/ONTOLOGY_COVERAGE_MATRIX.md` for mappings
3. Check `02_schemas/core/` for TTL implementations
4. Query `03_data/ttl/current/hvdc_status_v35.ttl` for instances

### For Data Analysts

1. Use `03_data/json/gpt_cache/` for pre-computed aggregations
2. Browse `03_data/json/reports/` for analysis results
3. Query `03_data/ttl/current/hvdc_status_v35.ttl` with SPARQL
4. Check `05_cross_references/QUERY_TEMPLATES.md` for examples

### For MCP/GPT Integration

1. Load `03_data/ttl/current/hvdc_status_v35.ttl` into RDFLib
2. Use `03_data/json/gpt_cache/` for fast responses
3. Reference `05_cross_references/FLOW_CODE_LINEAGE.md` for context
4. Apply SHACL validation from `02_schemas/shapes/`

---

## Common Tasks

### Task 1: Understand Flow Code v3.5

**Documents**:
- `01_ontology/consolidated/CONSOLIDATED-02-warehouse-flow.md` (Lines 62-100)
- `02_schemas/core/flow_code.ttl`
- `02_schemas/shapes/FlowCode.shape.ttl`

**Data**:
- `03_data/ttl/current/hvdc_status_v35.ttl` (9,795 cases)
- `03_data/json/gpt_cache/cases_by_flow.json`

**Queries**:
- See `05_cross_references/QUERY_TEMPLATES.md` → Flow Code section

### Task 2: Query AGI/DAS Compliance

**Documents**:
- `01_ontology/consolidated/CONSOLIDATED-02-warehouse-flow.md` (Lines 486-537)
- `02_schemas/shapes/FlowCode.shape.ttl` (Lines 62-89)

**Data**:
- `03_data/ttl/current/hvdc_status_v35.ttl`

**Query**:
```sparql
PREFIX hvdc: <http://samsung.com/project-logistics#>
SELECT ?case ?flowCode ?overrideReason
WHERE {
  ?case hvdc:hasFinalLocation ?site .
  FILTER(?site IN ("AGI", "DAS"))
  ?case hvdc:hasFlowCode ?flowCode .
  OPTIONAL { ?case hvdc:hasFlowOverrideReason ?overrideReason }
}
ORDER BY ?flowCode
```

### Task 3: Validate OCR Quality

**Documents**:
- `01_ontology/consolidated/CONSOLIDATED-03-document-ocr.md` (Lines 849-880, 1102-1115)

**Constraints**:
- MeanConf ≥ 0.92
- TableAcc ≥ 0.98
- NumericIntegrity = 1.00
- EntityMatch ≥ 0.98 ⭐

**Validation**:
```sparql
PREFIX ldg: <http://example.com/ldg#>
SELECT ?doc ?meanConf ?tableAcc ?entityMatch
WHERE {
  ?doc ldg:hasMetric ?metric .
  ?metric ldg:hasMeanConf ?meanConf ;
          ldg:hasTableAcc ?tableAcc ;
          ldg:hasEntityMatch ?entityMatch .
  FILTER(?meanConf < 0.92 || ?tableAcc < 0.98 || ?entityMatch < 0.98)
}
```

---

## File Relationships

### Conceptual → Formal → Operational

```
Documentation (MD)        Schema (TTL)               Data (TTL/JSON)
─────────────────────────────────────────────────────────────────────
01_ontology/             02_schemas/                03_data/
├─ CONSOLIDATED-01  →    ├─ hvdc_ontology.ttl  →    ├─ ttl/current/
├─ CONSOLIDATED-02  →    ├─ flow_code.ttl      →    │  └─ hvdc_status_v35.ttl
├─ CONSOLIDATED-03  →    ├─ hvdc_nodes.ttl     →    │
├─ CONSOLIDATED-04  →    └─ shapes/            →    ├─ ttl/finalized/
└─ CONSOLIDATED-05  →       └─ FlowCode.shape  →    ├─ ttl/specialized/
                                                     └─ json/
                                                        ├─ gpt_cache/
                                                        ├─ integration/
                                                        └─ reports/
```

---

## Integration Points

### With MCP Server

Use `hvdc_status_v35.ttl` for SPARQL queries, `gpt_cache/*.json` for fast aggregations.

### With Validation

SHACL shapes from `02_schemas/shapes/` validate all TTL data.

### With Reporting

JSON analytics in `03_data/json/reports/` derived from TTL data.

---

**See Also**: `MASTER_INDEX.md`, `ONTOLOGY_COVERAGE_MATRIX.md`, `FLOW_CODE_LINEAGE.md`



---

# Ontology Data Hub - Validation Report

**Date**: 2025-11-01 01:11:17
**Status**: PASS
**Total Tests**: 58
**Passed**: 58
**Failed**: 0
**Success Rate**: 100.0%

---

## Test Categories

### File Integrity: PASS

- [OK] MD files: 13/13
- [OK] TTL files: 36/36
- [OK] JSON files: 50/50
- [OK] MD files present: 13

**Results**: 4/4 passed

### Ttl Schemas: PASS

- [OK] 2_EXT-03-hvdc-comm-email-enhanced.ttl: 162 triples
- [OK] flow_code.ttl: 122 triples
- [OK] hvdc_event_schema.ttl: 120 triples
- [OK] hvdc_nodes.ttl: 154 triples
- [OK] hvdc_ontology.ttl: 142 triples
- [OK] FlowCode.shape.ttl: 113 triples
- [OK] shacl_shapes.ttl: 6 triples
- [OK] Shipment.shape.ttl: 11 triples
- [OK] ShipmentOOG.shape.ttl: 5 triples

**Results**: 9/9 passed

### Ttl Data: PASS

- [OK] hvdc_status_v35.ttl: 9904 triples, 755 cases
- [OK] Case count: 755 (expected >=700)

**Results**: 2/2 passed

### Json Validity: PASS


**Results**: 36/36 passed

### Sparql Queries: PASS

- [OK] SPARQL query test: 755 cases found

**Results**: 1/1 passed

### Cross References: PASS

- [OK] MASTER_INDEX.md present
- [OK] ONTOLOGY_COVERAGE_MATRIX.md present
- [OK] FLOW_CODE_LINEAGE.md present
- [OK] QUERY_TEMPLATES.md present
- [OK] USAGE_GUIDE.md present
- [OK] README.md present

**Results**: 6/6 passed

---

## Summary

[OK] All validation tests passed successfully. The Ontology Data Hub is ready for production use.


## Next Steps

1. Review validation results
2. Address any failed tests
3. Re-run validation if fixes applied
4. Tag as "validated-v1.0" if all tests pass

---

**Generated by**: validate_hub.py
**RDFLib Available**: True

---

## Document Completion Summary

This master document successfully integrates all 9 source files into a single comprehensive reference for the HVDC Logistics Ontology system. All original content has been preserved, with minimal structural adjustments for consistency.

**Content Integrity**: 100% - All technical content, tables, diagrams, and code examples retained

**Original Files**: All 9 source files remain available in the same directory for reference and traceability.

---

**End of Core Documentation Master**

