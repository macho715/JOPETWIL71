# Flow Code v3.5 - Quick Reference Card

**Version**: 1.0
**Date**: 2025-11-01
**Project**: HVDC Logistics Ontology

---

## Flow Code 0-5 Definitions

| Code | Name | Pattern | MOSB | AGI/DAS |
|------|------|---------|------|---------|
| **0** | Pre Arrival | - | N/A | N/A |
| **1** | Direct | Port → Site | ❌ No | ✅ Allowed |
| **2** | WH | Port → WH → Site | ❌ No | ✅ Allowed |
| **3** | MOSB | Port → MOSB → Site | ✅ Yes | ⚠️ **Required** |
| **4** | Full | Port → WH → MOSB → Site | ✅ Yes | ⚠️ **Required** |
| **5** | Mixed | Mixed/Waiting/Incomplete | ⚠️ Review | ⚠️ Review |

---

## AGI/DAS Mandatory Rules

### Core Rule

**All materials to AGI (Al Ghallan Island) or DAS (Das Island) MUST have Flow Code ≥ 3**

### Enforcement

- **Automatic Upgrade**: Flow 0/1/2 → Flow 3
- **Original Preserved**: `hasFlowCodeOriginal` retains pre-upgrade value
- **Reason Recorded**: `hasFlowOverrideReason` = "AGI/DAS requires MOSB leg"
- **SHACL Validation**: Automatic constraint enforcement

### Exceptions

- ❌ No exceptions for AGI/DAS
- ⚠️ Physical constraint: Offshore island access requires MOSB LCT transport

---

## 3 Essential SPARQL Queries

### 1. AGI/DAS Compliance Check

```sparql
PREFIX hvdc: <http://samsung.com/project-logistics#>

SELECT ?case ?caseCode ?flow ?loc
WHERE {
    ?case a hvdc:Case ;
          hvdc:hasHvdcCode ?caseCode ;
          hvdc:hasFinalLocation ?loc ;
          hvdc:hasFlowCode ?flow .
    FILTER(?loc IN ("AGI", "DAS") && ?flow < 3)
}
ORDER BY ?flow ?caseCode
```

**Expected**: 0 violations ✅

### 2. Flow 5 Review Flag Check

```sparql
PREFIX hvdc: <http://samsung.com/project-logistics#>

SELECT ?case ?caseCode ?flow
WHERE {
    ?case a hvdc:Case ;
          hvdc:hasHvdcCode ?caseCode ;
          hvdc:hasFlowCode 5 .
    FILTER NOT EXISTS { ?case hvdc:requiresReview ?flag }
}
ORDER BY ?caseCode
```

**Expected**: 0 missing flags ✅

### 3. Override Reason Check

```sparql
PREFIX hvdc: <http://samsung.com/project-logistics#>

SELECT ?case ?caseCode ?orig ?final
WHERE {
    ?case a hvdc:Case ;
          hvdc:hasHvdcCode ?caseCode ;
          hvdc:hasFlowCodeOriginal ?orig ;
          hvdc:hasFlowCode ?final .
    FILTER(?orig != ?final)
    FILTER NOT EXISTS { ?case hvdc:hasFlowOverrideReason ?reason }
}
ORDER BY ?caseCode
```

**Expected**: 0 missing reasons ✅

---

## OCR KPI Gates

| Gate | Threshold | Action | Location |
|------|-----------|--------|----------|
| **MeanConf** | ≥ 0.92 | ZERO mode if fail | CONSOLIDATED-03 |
| **TableAcc** | ≥ 0.98 | ZERO mode if fail | CONSOLIDATED-03 |
| **NumericIntegrity** | = 1.00 | ZERO mode if fail | CONSOLIDATED-03 |
| **EntityMatch** | ≥ 0.98 | ZERO mode if fail | CONSOLIDATED-03 |

**All gates**: SHACL enforced + automatic ZERO mode trigger

---

## Common Validation Commands

### Python Validation Script

```bash
# Run full validation
python "Logi ontol core doc/validate_flow_code_v35.py"

# Output includes:
# - AGI/DAS compliance check
# - Flow Code distribution
# - Override case tracking
# - Flow 5 review flag check
```

### RDFLib Direct Query

```python
from rdflib import Graph

g = Graph()
g.parse('output/hvdc_status_v35.ttl', format='turtle')

# Execute AGI/DAS query
results = list(g.query("""
    PREFIX hvdc: <http://samsung.com/project-logistics#>
    SELECT ?caseCode ?loc ?fc
    WHERE {
        ?case a hvdc:Case ;
              hvdc:hasHvdcCode ?caseCode ;
              hvdc:hasFinalLocation ?loc ;
              hvdc:hasFlowCode ?fc .
        FILTER(?loc IN ("AGI", "DAS"))
    }
    LIMIT 20
"""))

for row in results:
    print(f"{row[0]}: {row[1]} -> Flow {row[2]}")
```

---

## Property Reference

### Core Properties

- `hvdc:hasFlowCode` - Final Flow Code (0-5)
- `hvdc:hasFlowCodeOriginal` - Pre-upgrade value
- `hvdc:hasFlowOverrideReason` - Override explanation
- `hvdc:hasFlowDescription` - Human-readable description
- `hvdc:requiresMOSBLeg` - MOSB mandatory flag
- `hvdc:hasFinalLocation` - Final destination (MIR/SHU/AGI/DAS)
- `hvdc:hasWarehouseCount` - Warehouse transit count
- `hvdc:hasMOSBLeg` - MOSB transit flag
- `hvdc:hasSiteArrival` - Site arrival flag

### Domain Equivalents

- `mh:hasLogisticsFlowCode` ≡ `hvdc:hasFlowCode` (Material Handling)
- `debulk:hasLogisticsFlowCode` ≡ `hvdc:hasFlowCode` (Bulk Cargo)
- `port:assignedFlowCode` ≡ `hvdc:hasFlowCode` (Port Operations)
- `ldg:extractedFlowCode` ≡ `hvdc:hasFlowCode` (Document OCR)

---

## Current Distribution (755 Cases)

| Flow | Cases | % | Trend |
|------|-------|---|-------|
| 0 | 71 | 9.4% | ↓ Pre Arrival |
| 1 | 255 | 33.8% | ↑ **Most Common** |
| 2 | 152 | 20.1% | ↑ Warehouse |
| 3 | 131 | 17.4% | ↑ MOSB |
| 4 | 65 | 8.6% | → Full Chain |
| 5 | 81 | 10.7% | → Mixed/Incomplete |

**Total**: 755 cases

---

## Document Locations

| Document | Path | Flow Mentions |
|----------|------|---------------|
| Master Report | `Logi ontol core doc/FLOW_CODE_V35_INTEGRATION_REPORT.md` | Full details |
| TTL Schema | `Logi ontol core doc/flow-code-v35-schema.ttl` | 530 lines |
| Core Master | `Logi ontol core doc/CORE_DOCUMENTATION_MASTER.md` | 329 mentions |
| Algorithm Doc | `docs/flow_code_v35/FLOW_CODE_V35_ALGORITHM.md` | Complete logic |

---

## File Paths

### Data
- TTL: `output/hvdc_status_v35.ttl` (755 cases)
- JSON: `output/json/gpt_cache/cases_by_flow.json`

### Schema
- Core: `logiontology/configs/ontology/hvdc_ontology.ttl`
- Flow Code: `Logi ontol core doc/flow-code-v35-schema.ttl`

### Scripts
- Validation: `Logi ontol core doc/validate_flow_code_v35.py`
- Algorithm: `scripts/stage3_report/report_generator.py`

---

## Quick Actions

### Check Compliance

```bash
# AGI/DAS rule compliance
python "Logi ontol core doc/validate_flow_code_v35.py"
```

### Generate Report

```bash
# Full integration report
cat "Logi ontol core doc/FLOW_CODE_V35_INTEGRATION_REPORT.md"
```

### Load Schema

```python
# Load TTL schema
from rdflib import Graph
g = Graph()
g.parse("Logi ontol core doc/flow-code-v35-schema.ttl", format="turtle")
```

---

## Emergency Contacts

- **Validation Issues**: Check AGI/DAS override cases
- **Schema Errors**: Verify SHACL constraints
- **Query Failures**: Review SPARQL syntax (RDFLib 7.0+)
- **Data Issues**: Check TTL file path and namespace

---

**Quick Reference Generated**: 2025-11-01
**Status**: ✅ ACTIVE

