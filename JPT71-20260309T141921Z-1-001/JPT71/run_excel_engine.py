#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel Python Engine 실행 스크립트
실제 Excel 파일을 로드하고 계산을 수행합니다.
"""

import sys
import io
from pathlib import Path
from excel_python_engine import ExcelWorkbook
from datetime import datetime

# UTF-8 출력 설정
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

def main():
    """메인 실행 함수"""
    print("=" * 70)
    print("Excel Python Engine 실행")
    print("=" * 70)
    print(f"시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Excel 파일 경로
    script_dir = Path(__file__).parent
    excel_path = script_dir / "content-calendar.xlsx"
    
    if not excel_path.exists():
        print(f"❌ 파일을 찾을 수 없습니다: {excel_path}")
        return
    
    excel_path = str(excel_path)
    
    print(f"📂 Excel 파일 로드: {excel_path}")
    print("-" * 70)
    
    try:
        # 1. Excel 파일 로드
        workbook = ExcelWorkbook.load_from_excel(excel_path)
        
        print(f"✅ 로드 완료!")
        print(f"   - 시트 수: {len(workbook.sheets)}")
        print(f"\n   시트 정보:")
        total_cells = 0
        total_formulas = 0
        
        for sheet_name in workbook.sheets:
            sheet = workbook.sheets[sheet_name]
            formula_count = sum(1 for c in sheet.cells.values() if c.formula)
            total_cells += len(sheet.cells)
            total_formulas += formula_count
            
            print(f"   - {sheet_name:15} | {sheet.rows:3}행 × {sheet.cols:3}열 | "
                  f"{len(sheet.cells):4}개 셀 | {formula_count:4}개 함수")
        
        print(f"\n   총계: {total_cells}개 셀, {total_formulas}개 함수")
        
        # 2. 함수 계산
        print(f"\n🔄 함수 계산 중...")
        print("-" * 70)
        start_time = datetime.now()
        
        workbook.calculate_all()
        
        end_time = datetime.now()
        elapsed = (end_time - start_time).total_seconds()
        
        print(f"✅ 계산 완료! (소요 시간: {elapsed:.2f}초)")
        
        # 3. 계산 결과 통계
        print(f"\n📊 계산 결과 통계:")
        print("-" * 70)
        
        error_count = 0
        success_count = 0
        
        for sheet_name, sheet in workbook.sheets.items():
            sheet_errors = 0
            sheet_success = 0
            
            for cell in sheet.cells.values():
                if cell.formula:
                    if cell.calculated_value and isinstance(cell.calculated_value, str) and cell.calculated_value.startswith("#ERROR"):
                        sheet_errors += 1
                        error_count += 1
                    else:
                        sheet_success += 1
                        success_count += 1
            
            if sheet_errors > 0 or sheet_success > 0:
                total = sheet_errors + sheet_success
                error_rate = (sheet_errors / total * 100) if total > 0 else 0
                print(f"   - {sheet_name:15} | 성공: {sheet_success:4} | 오류: {sheet_errors:4} | 오류율: {error_rate:5.1f}%")
        
        total_calculated = error_count + success_count
        if total_calculated > 0:
            overall_error_rate = (error_count / total_calculated * 100)
            print(f"\n   전체: 성공 {success_count}개, 오류 {error_count}개 (오류율: {overall_error_rate:.1f}%)")
        
        # 4. 샘플 결과 출력
        print(f"\n📋 계산 결과 샘플 (각 시트별 처음 3개):")
        print("-" * 70)
        
        for sheet_name in list(workbook.sheets.keys())[:3]:  # 처음 3개 시트만
            sheet = workbook.sheets[sheet_name]
            formula_cells = [c for c in sheet.cells.values() if c.formula]
            
            if formula_cells:
                print(f"\n   [{sheet_name}]")
                for i, cell in enumerate(formula_cells[:3], 1):
                    formula_preview = cell.formula[:60] + "..." if len(cell.formula) > 60 else cell.formula
                    value_preview = str(cell.calculated_value)[:50] + "..." if cell.calculated_value and len(str(cell.calculated_value)) > 50 else str(cell.calculated_value)
                    
                    status = "❌" if (cell.calculated_value and isinstance(cell.calculated_value, str) and cell.calculated_value.startswith("#ERROR")) else "✅"
                    
                    print(f"   {i}. {status} {cell.coordinate:6} | {formula_preview:60}")
                    print(f"      → {value_preview}")
        
        # 5. 결과 저장 (선택사항)
        output_path = excel_path.replace('.xlsx', '_calculated.xlsx')
        print(f"\n💾 결과 저장: {output_path}")
        print("-" * 70)
        
        try:
            workbook.save_to_excel(output_path)
            print(f"✅ 저장 완료!")
        except Exception as e:
            print(f"❌ 저장 실패: {e}")
        
        print(f"\n" + "=" * 70)
        print(f"완료 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

