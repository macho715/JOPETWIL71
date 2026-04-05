#!/usr/bin/env python3
"""
Flow Code v3.5 Validation Script
Validates AGI/DAS rules and Flow Code distribution in hvdc_status_v35.ttl
"""

from rdflib import Graph
import sys
import os

def main():
    # Load TTL file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ttl_file = os.path.join(script_dir, '../../output/hvdc_status_v35.ttl')
    if not os.path.exists(ttl_file):
        print(f"ERROR: TTL file not found: {ttl_file}")
        # Try alternative path
        ttl_file = os.path.join(script_dir, '../output/hvdc_status_v35.ttl')
        if not os.path.exists(ttl_file):
            print(f"ERROR: Alternative TTL file not found: {ttl_file}")
            sys.exit(1)

    print(f"Loading TTL file: {ttl_file}")
    g = Graph()
    g.parse(ttl_file, format='turtle')

    # Namespace
    hvdc_ns = 'http://samsung.com/project-logistics#'

    # Query 1: AGI/DAS cases and their Flow Codes
    print("\n=== Query 1: AGI/DAS Cases Flow Code Compliance ===")
    agi_das_query = f"""
    PREFIX hvdc: <{hvdc_ns}>
    SELECT ?case ?caseCode ?fc ?loc
    WHERE {{
        ?case a hvdc:Case ;
              hvdc:hasHvdcCode ?caseCode ;
              hvdc:hasFinalLocation ?loc ;
              hvdc:hasFlowCode ?fc .
        FILTER(?loc IN ("AGI", "DAS"))
    }}
    ORDER BY ?loc ?caseCode
    """

    agi_das_results = list(g.query(agi_das_query))
    print(f"Total AGI/DAS cases: {len(agi_das_results)}")

    # Check compliance
    compliant = 0
    non_compliant = []
    for row in agi_das_results:
        # SELECT ?case ?caseCode ?fc ?loc
        fc_str = str(row[2])  # Flow Code (string)
        fc = int(fc_str)
        if fc >= 3:
            compliant += 1
        else:
            non_compliant.append((row[1], row[3], fc))  # caseCode, location, fc

    print(f"Compliant (Flow >= 3): {compliant}")
    print(f"Non-compliant: {len(non_compliant)}")
    if non_compliant:
        print("Non-compliant cases:")
        for case, loc, fc in non_compliant:
            print(f"  {case} -> {loc}: Flow {fc} (REQUIRED: >= 3)")

    compliance_rate = 100.0 * compliant / len(agi_das_results) if agi_das_results else 0
    print(f"Compliance Rate: {compliance_rate:.1f}%")

    # Query 2: Flow Code distribution
    print("\n=== Query 2: Flow Code Distribution ===")
    flow_dist_query = f"""
    PREFIX hvdc: <{hvdc_ns}>
    SELECT ?fc (COUNT(?case) AS ?count)
    WHERE {{
        ?case a hvdc:Case ;
              hvdc:hasFlowCode ?fc .
    }}
    GROUP BY ?fc
    ORDER BY ?fc
    """

    flow_dist_results = list(g.query(flow_dist_query))
    total_cases = sum(int(row[1]) for row in flow_dist_results)

    print(f"Total cases: {total_cases}")
    print("\nFlow Code Distribution:")
    for row in flow_dist_results:
        fc = str(row[0])
        count = int(row[1])
        pct = 100.0 * count / total_cases if total_cases > 0 else 0
        flow_names = {
            "0": "Pre Arrival",
            "1": "Direct",
            "2": "WH",
            "3": "MOSB",
            "4": "Full",
            "5": "Mixed"
        }
        flow_name = flow_names.get(fc, "Unknown")
        print(f"  Flow {fc} ({flow_name}): {count:4d} cases ({pct:5.1f}%)")

    # Query 3: Flow Code overrides
    print("\n=== Query 3: Flow Code Override Cases ===")
    override_query = f"""
    PREFIX hvdc: <{hvdc_ns}>
    SELECT ?case ?caseCode ?orig ?final ?reason ?loc
    WHERE {{
        ?case a hvdc:Case ;
              hvdc:hasHvdcCode ?caseCode ;
              hvdc:hasFlowCodeOriginal ?orig ;
              hvdc:hasFlowCode ?final ;
              hvdc:hasFlowOverrideReason ?reason ;
              hvdc:hasFinalLocation ?loc .
        FILTER(?orig != ?final)
    }}
    ORDER BY ?loc ?caseCode
    LIMIT 10
    """

    override_results = list(g.query(override_query))
    print(f"Total override cases: {len(override_results)} (showing first 10)")
    for row in override_results[:5]:
        # SELECT ?case ?caseCode ?orig ?final ?reason ?loc
        print(f"  {row[1]}: {row[5]} Flow {row[2]} → {row[3]}: {row[4]}")

    # Query 4: Flow 5 cases
    print("\n=== Query 4: Flow 5 (Mixed/Incomplete) Cases ===")
    flow5_query = f"""
    PREFIX hvdc: <{hvdc_ns}>
    SELECT ?case ?caseCode ?desc
    WHERE {{
        ?case a hvdc:Case ;
              hvdc:hasHvdcCode ?caseCode ;
              hvdc:hasFlowCode "5" ;
              hvdc:hasFlowDescription ?desc .
    }}
    ORDER BY ?caseCode
    LIMIT 10
    """

    flow5_results = list(g.query(flow5_query))
    print(f"Total Flow 5 cases: {len(flow5_results)} (showing first 10)")
    for row in flow5_results:
        # SELECT ?case ?caseCode ?desc
        print(f"  {row[1]}: {row[2]}")

    # Summary
    print("\n=== Validation Summary ===")
    print("AGI/DAS Compliance Check:")
    if compliance_rate == 100.0:
        print(f"   PASS: 100% compliance ({compliant}/{len(agi_das_results)})")
    else:
        print(f"   FAIL: {compliance_rate:.1f}% compliance ({compliant}/{len(agi_das_results)})")

    print("\nFlow Code Distribution:")
    print(f"   Total cases analyzed: {total_cases}")

    print("\nOverride Tracking:")
    print(f"   Override cases found: {len(override_results)}")

    print("\nFlow 5 (Mixed) Cases:")
    print(f"   Mixed/Incomplete cases: {len(flow5_results)}")

if __name__ == '__main__':
    main()

