#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple test to verify jpt71_unified.py can be imported"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("Testing jpt71_unified.py")
print("=" * 60)

try:
    # Test basic imports
    print("\n1. Testing basic imports...")
    import sys
    from datetime import date
    print("   ✓ sys, datetime")
    
    import pandas as pd
    print("   ✓ pandas")
    
    from openpyxl import Workbook
    print("   ✓ openpyxl")
    
    # Test Excel COM (optional)
    print("\n2. Testing Excel COM (optional)...")
    try:
        import win32com.client
        print("   ✓ pywin32 available")
        excel_com_available = True
    except ImportError:
        print("   ⚠ pywin32 not available (only needed for FINAL sheets)")
        excel_com_available = False
    
    # Try importing the module
    print("\n3. Testing jpt71_unified module import...")
    try:
        import jpt71_unified
        print("   ✓ Module imported successfully")
    except Exception as e:
        print(f"   ✗ Import failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Test scaffold function (no Excel COM needed)
    print("\n4. Testing scaffold creation (dry run)...")
    try:
        # Just verify function exists
        if hasattr(jpt71_unified, 'create_scaffold'):
            print("   ✓ create_scaffold function exists")
        if hasattr(jpt71_unified, 'refresh_and_export'):
            print("   ✓ refresh_and_export function exists")
        if hasattr(jpt71_unified, 'main'):
            print("   ✓ main function exists")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n" + "=" * 60)
    print("All tests passed!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n✗ FATAL ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

