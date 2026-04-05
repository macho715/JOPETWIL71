# JPT71 HVDC Project — OFCO-Voyage Mapping & Operational Analysis
## Final Report v4 (Integrated)

**Project:** JOPETWIL 71 (JPT71) — HVDC Cable Transportation  
**Client:** ADNOC / Samsung C&T  
**Vessel:** LCT Fleet (GRM, J71, DEBRIS, 009, 010)  
**Period:** 2024-07 ~ 2026-01  
**Report Date:** 2026-03-10  
**Prepared by:** SCT Logistics / MACHO-GPT Engine v4

---

## 1. Executive Summary

This report consolidates the v4 OFCO invoice-to-voyage cost mapping results with operational fuel consumption and loading analysis for the JPT71 HVDC project.

**Key Findings:**

| Metric | Value | Status |
|--------|-------|--------|
| Total OFCO Lines | 1,303 | — |
| Total AED | 6,029,909 | — |
| Mapped Coverage (AED) | 88.2% | ▲ from v3 |
| Voyages Mapped | 106 | — |
| Blended AED/ton | 116.5 | Mean |
| Median AED/ton | 50.5 | — |
| Outlier Voyages (>241.6) | 9 | IQR×1.5 fence |
| Total Fuel Consumed | 179,525 L | 15 months |
| Fuel Efficiency (Blended) | 3.79 L/ton | — |
| Fuel Efficiency (Laden) | 2.16 L/ton | — |
| Trips Detected | 65 | DECKLOG analysis |
| MANUAL_REVIEW Remaining | 61 lines (4.7% AED) | Action needed |

---

## 2. Data Sources

| Source | Sheet | Rows × Cols | Description |
|--------|-------|-------------|-------------|
| JPT-reconciled.xlsx | OFCO INV | 1,303 × 130 | Invoice ledger |
| JPT-reconciled.xlsx | VOYAGE | 133 × 9 | Voyage manifest (tonnage, dates, sub-con) |
| JPT-reconciled.xlsx | DECKLOG | 413 × 33 | Daily vessel operations log |

---

## 3. OFCO-Voyage Mapping Engine (v4)

### 3.1 Allocation Method Distribution

| Allocation Type | Lines | % Lines | AED | % AED |
|-----------------|-------|---------|-----|-------|
| DIRECT | 1,031 | 79.1% | 4,049,014 | 67.1% |
| PRORATE_APPLIED | 37 | 2.8% | 1,071,661 | 17.8% |
| SEPARATE_OPS | 99 | 7.6% | 316,466 | 5.2% |
| MANUAL_REVIEW | 61 | 4.7% | 286,056 | 4.7% |
| MULTI_PRORATED | 34 | 2.6% | 168,105 | 2.8% |
| NEW_TYPE | 39 | 3.0% | 110,271 | 1.8% |
| DATE_INFER | 2 | 0.2% | 28,335 | 0.5% |
| **Total** | **1,303** | **100%** | **6,029,909** | **100%** |

### 3.2 Mapping Coverage

- **v4 Mapped (DIRECT + PRORATE + MULTI + DATE_INFER):** AED 5,317,115 → **88.2%**
- **Remaining (MANUAL_REVIEW + SEPARATE_OPS + NEW_TYPE):** AED 712,794 → **11.8%**

### 3.3 v3 → v4 Improvement

| Phase | Method | Lines Resolved | AED Added |
|-------|--------|----------------|-----------|
| v3 → v4 | MULTI_PRORATED | 34 | 168,105 |
| v3 → v4 | Resolution methods: PRORATE_CANDIDATES (26), ROT_CLUSTER (8) | — | — |

### 3.4 Voyage ID Naming Convention

- **GRM-71-001 ~ 046**: Standard GRM series (46 voyages)
- **GRM-J71-047 ~ 091**: J71-renamed series from entry #47 onward (45 voyages)
- **J71-001 ~ 005**: Separate J71 direct series (5 voyages)
- **DEBRIS-001 ~ 008**: Debris removal operations (8 voyages)
- **009, 010**: Standalone voyage codes (2 voyages)

---

## 4. Voyage Cost KPI Analysis

### 4.1 AED/ton Distribution (106 Voyages)

| Statistic | AED/ton |
|-----------|---------|
| Mean (Blended) | 116.5 |
| Median | 50.5 |
| Q1 (25th) | 25.1 |
| Q3 (75th) | 111.7 |
| IQR | 86.6 |
| Outlier Fence | 241.6 |
| Min | 6.6 |
| Max | 2,285.1 |

### 4.2 Vessel Group Performance

| Group | Voyages | Avg AED/ton | Median | Total Ton | Total AED |
|-------|---------|-------------|--------|-----------|-----------|
| GRM | 91 | 79.8 | 51.1 | 59,191 | 4,560,485 |
| J71 | 5 | 865.5 | 489.4 | 821 | 409,907 |
| DEBRIS | 8 | 25.2 | 23.3 | 3,975 | 98,830 |
| 009 | 1 | 223.9 | — | 405 | 90,691 |
| 010 | 1 | 337.5 | — | 249 | 83,911 |

**Observation:** J71 direct voyages show significantly elevated AED/ton (865.5 vs GRM 79.8) — primarily due to low tonnage per voyage (avg 164 ton vs GRM 651 ton) with fixed cost components.

### 4.3 Top 5 Costliest Voyages

| Rank | Voyage ID | Tonnage | Total AED | AED/ton |
|------|-----------|---------|-----------|---------|
| 1 | HVDC-AGI-J71-001 | 24.0 | 54,798 | 2,285.1 |
| 2 | HVDC-AGI-J71-002 | 100.6 | 85,182 | 846.9 |
| 3 | HVDC-AGI-GRM-J71-047 | 347.7 | 238,214 | 685.2 |
| 4 | HVDC-AGI-J71-003 | 170.5 | 83,438 | 489.4 |
| 5 | HVDC-AGI-J71-004 | 324.0 | 116,410 | 359.3 |

### 4.4 Monthly Cost Trend

| Month | Voyages | Avg AED/ton | Total Ton | Total AED |
|-------|---------|-------------|-----------|-----------|
| 2024-07 | 2 | 7.9 | 1,223 | 9,674 |
| 2024-08 | 10 | 53.2 | 6,066 | 322,965 |
| 2024-09 | 10 | 70.4 | 6,194 | 436,059 |
| 2024-10 | 8 | 87.0 | 4,095 | 320,802 |
| 2024-11 | 6 | 82.0 | 3,361 | 266,026 |
| 2024-12 | 8 | 50.6 | 5,031 | 265,199 |
| 2025-01 | 2 | 22.7 | 1,454 | 31,740 |
| 2025-02 | 3 | 1,272.4 | 472 | 378,194 |
| 2025-03 | 2 | 424.4 | 494 | 199,848 |
| 2025-04 | 3 | 181.3 | 2,036 | 371,130 |
| 2025-05 | 3 | 128.9 | 2,100 | 269,638 |
| 2025-07 | 5 | 79.0 | 3,639 | 291,332 |
| 2025-08 | 5 | 262.2 | 2,390 | 560,781 |
| 2025-09 | 8 | 93.3 | 6,095 | 559,534 |
| 2025-10 | 9 | 44.5 | 6,429 | 289,888 |
| 2025-11 | 5 | 52.9 | 3,610 | 191,763 |
| 2025-12 | 6 | 52.0 | 3,741 | 223,300 |
| 2026-01 | 9 | 44.2 | 4,911 | 233,322 |

**Note:** 2025-02 spike (1,272.4 AED/ton) driven by J71 low-tonnage voyages with accumulated fixed costs.

---

## 5. Fuel Consumption Analysis

### 5.1 Overall Fuel Summary (15 Months)

| Metric | Value |
|--------|-------|
| Total Operating Days | 413 |
| Total Fuel Consumed | 179,525 L |
| Average Daily Fuel | 434.7 L/day |
| Fuel by Laden State | Laden 65.1%, Port Ops 29.5%, Unknown 4.6%, Ballast 0.8% |

### 5.2 Activity-Based Fuel Consumption

| Activity | Days | Total Fuel (L) | Fuel/Day (L) | % of Total |
|----------|------|----------------|---------------|------------|
| AT_ANCHOR | 54 | 66,225 | **1,226.4** | 36.9% |
| DISCHARGING | 97 | 42,711 | 440.3 | 23.8% |
| LOADING | 119 | 38,938 | 327.2 | 21.7% |
| SAILING | 33 | 12,409 | 376.0 | 6.9% |
| SAILING_LADEN | 10 | 6,758 | 675.8 | 3.8% |
| OTHER | 47 | 7,055 | 150.1 | 3.9% |
| AT_BERTH | 33 | 3,086 | 93.5 | 1.7% |
| MAINTENANCE | 13 | 1,457 | 112.1 | 0.8% |
| BUNKERING | 7 | 888 | 126.9 | 0.5% |

**Critical Finding:** AT_ANCHOR consumes **1,226 L/day** — 3× higher than LOADING/DISCHARGING. This is the #1 fuel cost driver (36.9% of total fuel on just 13.1% of days).

### 5.3 Fuel Efficiency

| Metric | L/ton |
|--------|-------|
| Blended (Total Fuel ÷ Total Cargo) | 3.79 |
| Laden Only (Laden Fuel ÷ Total Cargo) | 2.16 |
| Total Cargo Transported | 47,337 ton |

---

## 6. Trip & Route Analysis (65 Trips)

### 6.1 Route Breakdown

| Destination | Trips | Avg Fuel/Trip (L) | Total Fuel (L) | % Fuel |
|-------------|-------|--------------------|----------------|--------|
| AGI Field | 46 | 2,436 | 112,045 | 62.3% |
| DAS Island | 5 | 3,057 | 15,284 | 8.5% |
| JPW Base | 4 | 10,209 | 40,836 | 22.7% |
| MW4 Musaffah | 8 | 1,129 | 9,034 | 5.0% |
| Other | 2 | 1,164 | 2,328 | 1.3% |

### 6.2 Root-Cause Findings (5 Key Insights)

1. **Anchor Wait = Top Fuel Driver**: AT_ANCHOR at 1,226 L/day accounts for 36.9% of total fuel on 13.1% of operating days. Berth scheduling optimization could yield 20-30% fuel savings.

2. **Discharge > Loading by 33%**: DISCHARGING (440 L/day) vs LOADING (327 L/day). Higher fuel during discharge likely due to crane operations and hydraulic systems running at full capacity.

3. **DAS Route +25% vs AGI**: DAS Island trips average 3,057 L vs AGI Field 2,436 L (+25%). Longer transit distance and deeper draft at DAS contribute to higher consumption.

4. **Ballast Data Insufficient**: Only 9 explicit BALLAST days in DECKLOG (2.2% of records). Laden/Ballast comparison unreliable. Recommend adding explicit ballast status to daily logs.

5. **Wind Indirect Factor**: Counter-intuitively, strong wind (>14 kts) correlates with lower fuel — because operations are suspended, vessels idle. Moderate wind (8-12 kts) shows highest fuel as ops continue under sub-optimal conditions.

---

## 7. LCT Monthly Loading Analysis

### 7.1 Sub-Contractor Comparison

| Sub-Con | Total Voyages | Total Tonnage | Avg Ton/Voyage | Market Share |
|---------|---------------|---------------|----------------|--------------|
| GRM | 103 | 61,412 | 619.0 | 84.9% |
| SCT | 30 | 10,898 | 367.1 | 15.1% |
| **Total** | **133** | **72,310** | — | **100%** |

**Observation:** GRM dominates with 84.9% of tonnage share and 68% higher average load per voyage (619 vs 367 ton).

---

## 8. Action Items

| # | Priority | Action | Owner | Status |
|---|----------|--------|-------|--------|
| 1 | HIGH | Resolve 61 MANUAL_REVIEW lines (AED 286,056) — verify voyage assignments | Finance/Ops | Open |
| 2 | HIGH | Investigate AT_ANCHOR fuel (36.9% total) — optimize berth scheduling | Marine Ops | Open |
| 3 | MEDIUM | Classify 39 NEW_TYPE entries (AED 110,271) — assign to new cost categories | Finance | Open |
| 4 | MEDIUM | Add BALLAST status to DECKLOG daily entries | Marine Ops | Open |
| 5 | MEDIUM | Review J71 voyage cost structure (865 AED/ton vs GRM 80) — assess fixed cost allocation | Commercial | Open |
| 6 | LOW | Resolve 99 SEPARATE_OPS entries (AED 316,466) — non-voyage operational costs | Finance | Open |
| 7 | LOW | Validate 2026-01 ROB Start 862,100 data entry error in DECKLOG | Marine Ops | Open |
| 8 | LOW | Consider DAS route optimization or consolidation to reduce fuel cost | Logistics | Open |

---

## 9. Deliverables Inventory

| File | Type | Size | Description |
|------|------|------|-------------|
| JPT71_OFCO_Voyage_Mapping_v4.xlsx | Excel | 132K | Full v4 mapping (6 sheets) |
| JPT71_Voyage_Cost_Heatmap_v4.html | Dashboard | 56K | Cost heatmap (106 voy × 5 types) |
| JPT71_Voyage_KPI_Dashboard_v4.html | Dashboard | 69K | KPI dashboard (3 tabs, interactive) |
| JPT71_Fuel_Loading_Analysis.xlsx | Excel | 17K | Fuel & loading data (6 sheets) |
| JPT71_Fuel_Loading_Dashboard.html | Dashboard | 22K | Fuel dashboard (4 tabs) |
| JPT71_Fuel_RootCause_Analysis.html | Dashboard | 22K | Root-cause analysis (5 tabs) |
| JPT71_Final_Package_v4.xlsx | Excel | — | Integrated all-in-one package |
| JPT71_Final_Report_v4.md | Report | — | This document |

---

## 10. Methodology Notes

- **Matching Engine**: 4-pass algorithm — Direct Subject→Voyage match, Date-range proration (Option A tonnage), Multi-candidate resolution (PRORATE_CANDIDATES + ROT_CLUSTER), Date inference
- **Proration Method**: Option A (tonnage-weighted) applied to multi-voyage months
- **Fuel Classification**: Activity text NLP parsing → 9 activity classes
- **Cargo State**: Combined activity + port detection heuristic (LADEN/BALLAST/PORT_OPS/UNKNOWN)
- **Trip Detection**: Non-LOADING → LOADING transition boundary via cumsum
- **Outlier Definition**: IQR × 1.5 fence method (Q3 + 1.5 × IQR = 241.6 AED/ton)

---

*Report generated by MACHO-GPT v3.4 / LATTICE+COST-GUARD Mode*  
*Data source: JPT-reconciled.xlsx (8 sheets) | Engine: v4 Multi-Prorated Resolution*
