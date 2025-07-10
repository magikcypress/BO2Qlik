#!/usr/bin/env python3
"""
Automated test for the universal BO2Qlik converter
Validates Qlik script generation from a .unv and a .unx file
"""

import os
import shutil
import sys
import time
import importlib.util

# Dynamically import the universal converter
spec = importlib.util.spec_from_file_location("UniversalBO2QlikConverter", "universal_converter.py")
module = importlib.util.module_from_spec(spec)
sys.modules["UniversalBO2QlikConverter"] = module
spec.loader.exec_module(module)
UniversalBO2QlikConverter = module.UniversalBO2QlikConverter

def run_test_unv():
    print("\n=== UNIVERSAL CONVERTER TEST - UNV MODE ===")
    # Ensure there is a .unv and no .unx
    data_dir = "../data"
    unx_path = os.path.join(data_dir, "test_universe.unx")
    if os.path.exists(unx_path):
        os.remove(unx_path)
    # Run the converter
    converter = UniversalBO2QlikConverter()
    success = converter.run_conversion()
    assert success, "UNV conversion failed"
    # Check output
    output_dir = "../output"
    files = [f for f in os.listdir(output_dir) if f.endswith(".qvs") and "unv" in f]
    assert files, "No Qlik script generated for UNV"
    print(f"✅ Script generated for UNV: {files[-1]}")
    return True

def run_test_unx():
    print("\n=== UNIVERSAL CONVERTER TEST - UNX MODE ===")
    # Generate a test .unx
    from create_test_unx import create_test_unx
    unx_path = create_test_unx()
    # Run the converter
    converter = UniversalBO2QlikConverter()
    success = converter.run_conversion()
    assert success, "UNX conversion failed"
    # Check output
    output_dir = "../output"
    files = [f for f in os.listdir(output_dir) if f.endswith(".qvs") and "unx" in f]
    assert files, "No Qlik script generated for UNX"
    print(f"✅ Script generated for UNX: {files[-1]}")
    return True

def main():
    print("=== AUTOMATED TEST FOR UNIVERSAL CONVERTER ===")
    ok_unv = run_test_unv()
    ok_unx = run_test_unx()
    if ok_unv and ok_unx:
        print("\n🎉 All universal converter tests PASSED!")
        sys.exit(0)
    else:
        print("\n❌ One or more tests failed.")
        sys.exit(1)

if __name__ == "__main__":
    main() 