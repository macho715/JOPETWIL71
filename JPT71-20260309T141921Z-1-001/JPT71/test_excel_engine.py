#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel Python Engine 테스트 및 사용 예제
"""

import sys
import io
from pathlib import Path
from excel_python_engine import ExcelWorkbook, ExcelSheet, ExcelCell, CellType, FormulaEngine, CellReference

# UTF-8 출력 설정 (이미 excel_python_engine에서 설정됨)
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass


def test_basic_usage():
    """기본 사용 예제"""
    print("=" * 60)
    print("기본 사용 예제")
    print("=" * 60)
    
    # Excel 파일 로드
    excel_path = "content-calendar.xlsx"
    if not Path(excel_path).exists():
        print(f"파일을 찾을 수 없습니다: {excel_path}")
        return
    
    print(f"\n1. Excel 파일 로드: {excel_path}")
    workbook = ExcelWorkbook.load_from_excel(excel_path)
    
    print(f"   - 시트 수: {len(workbook.sheets)}")
    for sheet_name in workbook.sheets:
        sheet = workbook.sheets[sheet_name]
        print(f"   - {sheet_name}: {sheet.rows}행 × {sheet.cols}열, {len(sheet.cells)}개 셀")
    
    # 함수 계산
    print("\n2. 함수 계산 중...")
    workbook.calculate_all()
    print("   계산 완료!")
    
    # 결과 확인 (일부 셀)
    print("\n3. 계산 결과 샘플:")
    for sheet_name in list(workbook.sheets.keys())[:2]:  # 처음 2개 시트만
        sheet = workbook.sheets[sheet_name]
        formula_cells = [c for c in sheet.cells.values() if c.formula]
        if formula_cells:
            print(f"\n   [{sheet_name}]")
            for cell in formula_cells[:5]:  # 처음 5개만
                print(f"   {cell.coordinate}: {cell.formula[:50]}...")
                print(f"      → {cell.calculated_value}")


def test_cell_reference():
    """셀 참조 테스트"""
    print("\n" + "=" * 60)
    print("셀 참조 파싱 테스트")
    print("=" * 60)
    
    test_cases = [
        "A1",
        "$B$2",
        "Sheet1!A1",
        "Sheet1!$B$2",
        "$A1",
        "A$1",
    ]
    
    for ref_str in test_cases:
        try:
            ref = CellReference.parse(ref_str)
            print(f"  {ref_str:15} → sheet={ref.sheet}, col={ref.column}, row={ref.row}, "
                  f"abs_col={ref.absolute_column}, abs_row={ref.absolute_row}")
        except Exception as e:
            print(f"  {ref_str:15} → ERROR: {e}")


def test_formula_functions():
    """함수 테스트"""
    print("\n" + "=" * 60)
    print("Excel 함수 테스트")
    print("=" * 60)
    
    # 간단한 워크북 생성
    workbook = ExcelWorkbook()
    sheet = ExcelSheet(name="Test", rows=10, cols=10)
    
    # 테스트 데이터
    sheet.set_cell("A1", ExcelCell(coordinate="A1", value=10, data_type=CellType.VALUE))
    sheet.set_cell("A2", ExcelCell(coordinate="A2", value=20, data_type=CellType.VALUE))
    sheet.set_cell("A3", ExcelCell(coordinate="A3", value=30, data_type=CellType.VALUE))
    sheet.set_cell("B1", ExcelCell(coordinate="B1", value="Apple", data_type=CellType.VALUE))
    sheet.set_cell("B2", ExcelCell(coordinate="B2", value="Banana", data_type=CellType.VALUE))
    
    workbook.add_sheet(sheet)
    engine = FormulaEngine(workbook)
    
    # 함수 테스트
    test_formulas = [
        ("=IF(A1>5, \"Yes\", \"No\")", "IF 함수"),
        ("=IFERROR(A1/A2, 0)", "IFERROR 함수"),
        ("=UPPER(\"hello\")", "UPPER 함수"),
        ("=ROW()", "ROW 함수"),
    ]
    
    print("\n함수 평가 테스트:")
    for formula, desc in test_formulas:
        try:
            result = engine.evaluate(formula, "Test", "C1")
            print(f"  {desc:20} {formula:30} → {result}")
        except Exception as e:
            print(f"  {desc:20} {formula:30} → ERROR: {e}")


def test_dependency_graph():
    """의존성 그래프 테스트"""
    print("\n" + "=" * 60)
    print("의존성 그래프 테스트")
    print("=" * 60)
    
    workbook = ExcelWorkbook()
    sheet = ExcelSheet(name="Test", rows=5, cols=5)
    
    # 의존성 있는 셀 생성
    sheet.set_cell("A1", ExcelCell(coordinate="A1", value=10, data_type=CellType.VALUE))
    sheet.set_cell("A2", ExcelCell(coordinate="A2", value=20, data_type=CellType.VALUE))
    sheet.set_cell("B1", ExcelCell(coordinate="B1", formula="=A1*2", data_type=CellType.FORMULA))
    sheet.set_cell("B2", ExcelCell(coordinate="B2", formula="=A2+B1", data_type=CellType.FORMULA))
    sheet.set_cell("C1", ExcelCell(coordinate="C1", formula="=B1+B2", data_type=CellType.FORMULA))
    
    workbook.add_sheet(sheet)
    
    # 의존성 그래프 생성
    graph = workbook._build_dependency_graph()
    print("\n의존성 그래프:")
    for (ref_sheet, ref_coord), deps in graph.items():
        if deps:
            print(f"  {ref_sheet}!{ref_coord} → {[f'{s}!{c}' for s, c in deps]}")
    
    # 계산 순서
    order = workbook._topological_sort(graph)
    print("\n계산 순서:")
    for sheet_name, coord in order:
        print(f"  {sheet_name}!{coord}")


def main():
    """메인 함수"""
    print("\n" + "=" * 60)
    print("Excel Python Engine 테스트")
    print("=" * 60)
    
    # 셀 참조 테스트
    test_cell_reference()
    
    # 함수 테스트
    test_formula_functions()
    
    # 의존성 그래프 테스트
    test_dependency_graph()
    
    # 실제 Excel 파일 테스트
    test_basic_usage()
    
    print("\n" + "=" * 60)
    print("테스트 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

