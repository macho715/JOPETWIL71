# Test imports for jpt71_unified.py
print("Testing imports...")
try:
    import sys
    print("✓ sys")
    from datetime import date
    print("✓ datetime")
    import pandas as pd
    print("✓ pandas")
    from openpyxl import Workbook
    print("✓ openpyxl")
    print("\n✓ All basic imports OK!")
    
    # Excel COM은 scaffold 모드에서 필요 없음
    print("\nTesting Excel COM (optional)...")
    try:
        import win32com.client
        print("✓ pywin32 (Excel COM available)")
    except:
        print("⚠ pywin32 not available (only needed for FINAL sheets)")
        
except ImportError as e:
    print(f"✗ Import error: {e}")

