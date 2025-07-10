#!/usr/bin/env python3
"""
Full integration test for BO2Qlik
Tests the entire workflow with a real UNV file
"""

import os
import sys
import time
import shutil
import tempfile
from datetime import datetime

def run_integration_test():
    """Runs the full integration test"""
    print("=== BO2Qlik INTEGRATION TEST ===\n")
    start_time = time.time()
    try:
        # Import the main class
        from unv2qlik_final import UNV2QlikConverter
        # Create an instance
        converter = UNV2QlikConverter()
        print("1. 🔍 Checking environment...")
        # Check directory structure
        data_dir = "../data"
        output_dir = "../output"
        if not os.path.exists(data_dir):
            print(f"❌ data/ directory not found: {data_dir}")
            return False
        if not os.path.exists(output_dir):
            print(f"⚠️  output/ directory not found, creating...")
            os.makedirs(output_dir, exist_ok=True)
        print("✅ Environment OK")
        print("\n2. 📁 Checking UNV files...")
        # List UNV files
        unv_files = []
        if os.path.exists(data_dir):
            for file in os.listdir(data_dir):
                if file.endswith('.unv') or file.endswith('.unv.zip'):
                    unv_files.append(file)
        if not unv_files:
            print("❌ No UNV file found in data/")
            return False
        print(f"✅ UNV files found: {unv_files}")
        print("\n3. 🔄 Full workflow test...")
        # Save initial state
        initial_files = set()
        if os.path.exists('.'):
            initial_files = set(os.listdir('.'))
        # Run the full workflow
        print("   - Extracting UNV file...")
        extraction_success = converter.extract_unv_file()
        if not extraction_success:
            print("❌ Extraction failed")
            return False
        print("   ✅ Extraction OK")
        print("   - Parsing files...")
        # Parse files
        columns_result = converter.parse_columns_file()
        tables_result = converter.parse_tables_file()
        joins_result = converter.parse_joins_file()
        print(f"   ✅ Columns: {len(columns_result)} fields found")
        print(f"   ✅ Tables: {len(tables_result)} tables found")
        print(f"   ✅ Joins: {len(joins_result)} joins found")
        print("   - Categorizing fields...")
        converter.categorize_fields()
        print(f"   ✅ Dimensions: {len(converter.dimensions)}")
        print(f"   ✅ Measures: {len(converter.measures)}")
        print("   - Generating Qlik script...")
        script = converter.generate_qlik_script()
        if not script:
            print("❌ Script generation failed")
            return False
        print("   ✅ Script generated")
        print("   - Saving script...")
        # Save script
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        script_filename = f"qlik_script_{timestamp}.qvs"
        script_path = os.path.join(output_dir, script_filename)
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script)
        print(f"   ✅ Script saved: {script_path}")
        print("   - Cleaning up temporary files...")
        converter.cleanup_extracted_files()
        print("   ✅ Cleanup done")
        print("\n4. 📊 Validating results...")
        # Validation
        validation_results = {
            'fields_count': len(converter.fields),
            'tables_count': len(converter.tables),
            'joins_count': len(converter.joins),
            'dimensions_count': len(converter.dimensions),
            'measures_count': len(converter.measures),
            'script_length': len(script),
            'script_contains_tables': any(table in script for table in converter.tables),
            'script_contains_fields': any(field in script for field in converter.fields[:5]),
            'script_contains_joins': any(join in script for join in converter.joins)
        }
        print(f"   📈 Fields extracted: {validation_results['fields_count']}")
        print(f"   📈 Tables extracted: {validation_results['tables_count']}")
        print(f"   📈 Joins extracted: {validation_results['joins_count']}")
        print(f"   📈 Dimensions: {validation_results['dimensions_count']}")
        print(f"   📈 Measures: {validation_results['measures_count']}")
        print(f"   📈 Script size: {validation_results['script_length']} characters")
        # Quality checks
        quality_checks = [
            ('Script contains tables', validation_results['script_contains_tables']),
            ('Script contains fields', validation_results['script_contains_fields']),
            ('Script contains joins', validation_results['script_contains_joins'])
        ]
        for check_name, check_result in quality_checks:
            status = "✅" if check_result else "❌"
            print(f"   {status} {check_name}")
        print("\n5. 🎯 Integration test summary...")
        execution_time = time.time() - start_time
        print(f"   ⏱️  Execution time: {execution_time:.2f} seconds")
        print(f"   📁 UNV file processed: {unv_files[0]}")
        print(f"   📄 Script generated: {script_filename}")
        print(f"   📊 Data extracted: {validation_results['fields_count']} fields, {validation_results['tables_count']} tables")
        # Success criteria
        success_criteria = [
            validation_results['fields_count'] > 0,
            validation_results['tables_count'] > 0,
            validation_results['script_length'] > 1000,
            validation_results['script_contains_tables'],
            validation_results['script_contains_fields']
        ]
        all_success = all(success_criteria)
        if all_success:
            print("\n🎉 INTEGRATION TEST PASSED!")
            print("✅ All success criteria met")
        else:
            print("\n⚠️  PARTIAL INTEGRATION TEST")
            failed_criteria = [i for i, criterion in enumerate(success_criteria) if not criterion]
            print(f"❌ Failed criteria: {len(failed_criteria)}")
        return all_success
    except Exception as e:
        print(f"\n❌ ERROR DURING INTEGRATION TEST: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_performance_test():
    """Performance test"""
    print("\n=== PERFORMANCE TEST ===")
    try:
        from unv2qlik_final import UNV2QlikConverter
        start_time = time.time()
        # Test with a small dataset
        converter = UNV2QlikConverter()
        test_data = b'Test' * 10000  # 40KB of data
        # Measure string extraction time
        start_extract = time.time()
        strings = converter.extract_strings(test_data)
        extract_time = time.time() - start_extract
        # Measure categorization time
        converter.fields = ['Field_' + str(i) for i in range(100)]
        start_categorize = time.time()
        converter.categorize_fields()
        categorize_time = time.time() - start_categorize
        # Measure script generation time
        converter.tables = ['Table_' + str(i) for i in range(10)]
        converter.joins = ['Join_' + str(i) for i in range(5)]
        start_generate = time.time()
        script = converter.generate_qlik_script()
        generate_time = time.time() - start_generate
        total_time = time.time() - start_time
        print(f"⏱️  String extraction time: {extract_time:.4f}s")
        print(f"⏱️  Categorization time: {categorize_time:.4f}s")
        print(f"⏱️  Script generation time: {generate_time:.4f}s")
        print(f"⏱️  Total time: {total_time:.4f}s")
        # Check performance thresholds
        performance_ok = (
            extract_time < 1.0 and
            categorize_time < 0.1 and
            generate_time < 0.5 and
            total_time < 2.0
        )
        if performance_ok:
            print("✅ Performance OK")
        else:
            print("⚠️  Slow performance detected")
        return performance_ok
    except Exception as e:
        print(f"❌ Error during performance test: {e}")
        return False

def main():
    print("🚀 Starting BO2Qlik integration tests\n")
    integration_success = run_integration_test()
    performance_success = run_performance_test()
    print("\n" + "="*60)
    print("FINAL TEST SUMMARY")
    print("="*60)
    print(f"Integration test: {'✅ PASSED' if integration_success else '❌ FAILED'}")
    print(f"Performance test: {'✅ PASSED' if performance_success else '❌ FAILED'}")
    overall_success = integration_success and performance_success
    if overall_success:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ The BO2Qlik converter works correctly")
    else:
        print("\n⚠️  SOME TESTS FAILED")
        print("❌ Issues detected")
    return overall_success

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 