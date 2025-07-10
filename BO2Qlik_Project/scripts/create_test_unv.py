#!/usr/bin/env python3
"""
Create Test UNV File
====================

This script creates a minimal test .unv file for testing the UNV parser.
The .unv file is essentially a ZIP archive containing binary metadata files.

Author: BO2Qlik Project
License: MIT
"""

import zipfile
import os
import struct
from pathlib import Path

def create_binary_metadata_file(filename, content):
    """
    Create a binary metadata file with the given content.
    
    Args:
        filename (str): Name of the file to create
        content (bytes): Binary content for the file
    """
    return content

def create_test_unv():
    """
    Create a test .unv file with sample metadata.
    
    Returns:
        str: Path to the created .unv file
    """
    # Define the test data directory
    data_dir = Path("../data")
    data_dir.mkdir(exist_ok=True)
    
    # Test .unv file path
    test_unv_path = data_dir / "test_universe.unv"
    
        # Create sample binary content for different metadata files
    # Note: UNV parser expects files with semicolon suffix
    sample_data = {
        "Tables;": b"Tables\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                   b"Customer\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                   b"Orders\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                   b"Products\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
        
        "Objects;": b"Objects\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                    b"CustomerID\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                    b"CustomerName\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                    b"OrderID\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                    b"OrderDate\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                    b"ProductID\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                    b"ProductName\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                    b"Quantity\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                    b"UnitPrice\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
        
        "Joins;": b"Joins\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                  b"Customer.CustomerID=Orders.CustomerID\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                  b"Orders.ProductID=Products.ProductID\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
        
        "Columns;": "CustomerID CustomerName OrderID OrderDate ProductID ProductName Quantity UnitPrice\n"
                    "CustomerID CustomerName OrderID OrderDate ProductID ProductName Quantity UnitPrice\n"
                    "CustomerID CustomerName OrderID OrderDate ProductID ProductName Quantity UnitPrice\n"
                    "CustomerID CustomerName OrderID OrderDate ProductID ProductName Quantity UnitPrice\n"
                    "CustomerID CustomerName OrderID OrderDate ProductID ProductName Quantity UnitPrice\n"
                    "CustomerID CustomerName OrderID OrderDate ProductID ProductName Quantity UnitPrice\n"
                    "CustomerID CustomerName OrderID OrderDate ProductID ProductName Quantity UnitPrice\n"
                    "CustomerID CustomerName OrderID OrderDate ProductID ProductName Quantity UnitPrice\n"
                    "CustomerID CustomerName OrderID OrderDate ProductID ProductName Quantity UnitPrice\n"
                    "CustomerID CustomerName OrderID OrderDate ProductID ProductName Quantity UnitPrice\n",
        
        "Dimensions;": b"Dimensions\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                       b"CustomerID\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                       b"CustomerName\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                       b"OrderID\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                       b"OrderDate\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                       b"ProductID\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                       b"ProductName\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
        
        "Measures;": b"Measures\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                     b"Quantity\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                     b"UnitPrice\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                     b"TotalAmount\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    }
    
    # Create the .unv file as a ZIP archive
    with zipfile.ZipFile(test_unv_path, 'w', zipfile.ZIP_DEFLATED) as unv_zip:
        for filename, content in sample_data.items():
            # Convert string content to bytes if needed
            if isinstance(content, str):
                content = content.encode('utf-8')
            unv_zip.writestr(filename, content)
    
    print(f"✅ Test .unv file created: {test_unv_path}")
    print(f"📁 File size: {test_unv_path.stat().st_size} bytes")
    print(f"📋 Contains {len(sample_data)} metadata files:")
    for filename in sample_data.keys():
        print(f"   - {filename}")
    
    return str(test_unv_path)

def test_unv_file(unv_path):
    """
    Test the created .unv file by extracting and examining its contents.
    
    Args:
        unv_path (str): Path to the .unv file to test
    """
    print(f"\n🔍 Testing .unv file: {unv_path}")
    
    if not os.path.exists(unv_path):
        print("❌ Error: .unv file not found!")
        return False
    
    try:
        with zipfile.ZipFile(unv_path, 'r') as unv_zip:
            file_list = unv_zip.namelist()
            print(f"✅ Successfully opened .unv file")
            print(f"📋 Found {len(file_list)} files:")
            
            for filename in file_list:
                file_info = unv_zip.getinfo(filename)
                print(f"   - {filename} ({file_info.file_size} bytes)")
            
            # Test reading some content
            if "Tables" in file_list:
                tables_content = unv_zip.read("Tables")
                print(f"\n📊 Sample Tables content (first 100 bytes):")
                print(f"   {tables_content[:100]}")
            
            if "Objects" in file_list:
                objects_content = unv_zip.read("Objects")
                print(f"\n📋 Sample Objects content (first 100 bytes):")
                print(f"   {objects_content[:100]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing .unv file: {e}")
        return False

def main():
    """
    Main function to create and test a .unv file.
    """
    print("🚀 Creating test .unv file...")
    print("=" * 50)
    
    # Create the test .unv file
    unv_path = create_test_unv()
    
    # Test the created file
    print("\n" + "=" * 50)
    success = test_unv_file(unv_path)
    
    if success:
        print(f"\n✅ Test .unv file created and validated successfully!")
        print(f"📁 File location: {unv_path}")
        print(f"💡 You can now use this file to test the UNV parser")
    else:
        print(f"\n❌ Failed to create or validate test .unv file")

if __name__ == "__main__":
    main() 