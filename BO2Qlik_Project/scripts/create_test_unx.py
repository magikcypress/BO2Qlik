#!/usr/bin/env python3
"""
Minimal .unx test file generator
Creates a dummy .unx file with some tables, objects, dimensions, and measures
"""

import os
import zipfile
import tempfile
import shutil
from datetime import datetime

def create_test_unx():
    """Creates a minimal .unx test file"""
    # Create a temporary folder for the structure
    temp_dir = tempfile.mkdtemp(prefix="unx_test_")
    try:
        # Create folder structure
        datafoundation_dir = os.path.join(temp_dir, "datafoundation")
        businesslayer_dir = os.path.join(temp_dir, "businesslayer")
        os.makedirs(datafoundation_dir, exist_ok=True)
        os.makedirs(businesslayer_dir, exist_ok=True)
        # Create datafoundation.xml
        datafoundation_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<dataFoundation xmlns="http://www.sap.com/rws/bip">
    <tables>
        <table id="T1" name="Sales_Facts" description="Sales table">
            <columns>
                <column id="C1" name="Shop_id" type="VARCHAR"/>
                <column id="C2" name="Article_id" type="VARCHAR"/>
                <column id="C3" name="Sales_revenue" type="DECIMAL"/>
                <column id="C4" name="Quantity_sold" type="INTEGER"/>
            </columns>
        </table>
        <table id="T2" name="Shop_Lookup" description="Shop table">
            <columns>
                <column id="C5" name="Shop_id" type="VARCHAR"/>
                <column id="C6" name="Shop_name" type="VARCHAR"/>
                <column id="C7" name="City" type="VARCHAR"/>
                <column id="C8" name="Region" type="VARCHAR"/>
            </columns>
        </table>
        <table id="T3" name="Article_Lookup" description="Article table">
            <columns>
                <column id="C9" name="Article_id" type="VARCHAR"/>
                <column id="C10" name="Article_name" type="VARCHAR"/>
                <column id="C11" name="Category" type="VARCHAR"/>
                <column id="C12" name="Price" type="DECIMAL"/>
            </columns>
        </table>
    </tables>
    <joins>
        <join id="J1" name="Sales_Shop_Join">
            <expression>Sales_Facts.Shop_id = Shop_Lookup.Shop_id</expression>
        </join>
        <join id="J2" name="Sales_Article_Join">
            <expression>Sales_Facts.Article_id = Article_Lookup.Article_id</expression>
        </join>
    </joins>
</dataFoundation>'''
        with open(os.path.join(datafoundation_dir, "datafoundation.xml"), "w", encoding="utf-8") as f:
            f.write(datafoundation_xml)
        # Create businesslayer.xml
        businesslayer_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<businessLayer xmlns="http://www.sap.com/rws/bip">
    <businessObjects>
        <!-- Dimensions -->
        <businessObject id="BO1" name="Shop_id" type="Dimension">
            <description>Shop ID</description>
            <dataFoundation>
                <table id="T1" name="Sales_Facts"/>
                <table id="T2" name="Shop_Lookup"/>
            </dataFoundation>
        </businessObject>
        <businessObject id="BO2" name="Shop_name" type="Dimension">
            <description>Shop name</description>
            <dataFoundation>
                <table id="T2" name="Shop_Lookup"/>
            </dataFoundation>
        </businessObject>
        <businessObject id="BO3" name="Article_id" type="Dimension">
            <description>Article ID</description>
            <dataFoundation>
                <table id="T1" name="Sales_Facts"/>
                <table id="T3" name="Article_Lookup"/>
            </dataFoundation>
        </businessObject>
        <businessObject id="BO4" name="Article_name" type="Dimension">
            <description>Article name</description>
            <dataFoundation>
                <table id="T3" name="Article_Lookup"/>
            </dataFoundation>
        </businessObject>
        <businessObject id="BO5" name="City" type="Dimension">
            <description>Shop city</description>
            <dataFoundation>
                <table id="T2" name="Shop_Lookup"/>
            </dataFoundation>
        </businessObject>
        <businessObject id="BO6" name="Region" type="Dimension">
            <description>Shop region</description>
            <dataFoundation>
                <table id="T2" name="Shop_Lookup"/>
            </dataFoundation>
        </businessObject>
        <businessObject id="BO7" name="Category" type="Dimension">
            <description>Article category</description>
            <dataFoundation>
                <table id="T3" name="Article_Lookup"/>
            </dataFoundation>
        </businessObject>
        <!-- Measures -->
        <businessObject id="BO8" name="Sales_revenue" type="Measure">
            <description>Sales revenue</description>
            <dataFoundation>
                <table id="T1" name="Sales_Facts"/>
            </dataFoundation>
        </businessObject>
        <businessObject id="BO9" name="Quantity_sold" type="Measure">
            <description>Quantity sold</description>
            <dataFoundation>
                <table id="T1" name="Sales_Facts"/>
            </dataFoundation>
        </businessObject>
        <businessObject id="BO10" name="Price" type="Measure">
            <description>Article price</description>
            <dataFoundation>
                <table id="T3" name="Article_Lookup"/>
            </dataFoundation>
        </businessObject>
        <!-- Attributes -->
        <businessObject id="BO11" name="Shop_Address" type="Attribute">
            <description>Shop address</description>
            <dataFoundation>
                <table id="T2" name="Shop_Lookup"/>
            </dataFoundation>
        </businessObject>
    </businessObjects>
    <folders>
        <folder id="F1" name="Dimensions">
            <businessObjects>
                <businessObject id="BO1"/>
                <businessObject id="BO2"/>
                <businessObject id="BO3"/>
                <businessObject id="BO4"/>
                <businessObject id="BO5"/>
                <businessObject id="BO6"/>
                <businessObject id="BO7"/>
            </businessObjects>
        </folder>
        <folder id="F2" name="Measures">
            <businessObjects>
                <businessObject id="BO8"/>
                <businessObject id="BO9"/>
                <businessObject id="BO10"/>
            </businessObjects>
        </folder>
        <folder id="F3" name="Attributes">
            <businessObjects>
                <businessObject id="BO11"/>
            </businessObjects>
        </folder>
    </folders>
</businessLayer>'''
        with open(os.path.join(businesslayer_dir, "businesslayer.xml"), "w", encoding="utf-8") as f:
            f.write(businesslayer_xml)
        # Create the .unx file (ZIP)
        output_path = "../data/test_universe.unx"
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_name = os.path.relpath(file_path, temp_dir)
                    zip_file.write(file_path, arc_name)
        print(f"✅ Test .unx file created: {output_path}")
        print(f"📁 Structure created in: {temp_dir}")
        # Show ZIP content
        with zipfile.ZipFile(output_path, 'r') as zip_file:
            print(f"📦 .unx file content:")
            for file_info in zip_file.filelist:
                print(f"   - {file_info.filename}")
        return output_path
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def test_unx_parser():
    """Test the parser with the created .unx file"""
    print("\n=== UNX PARSER TEST ===")
    unx_file = "../data/test_universe.unx"
    if not os.path.exists(unx_file):
        print(f"❌ .unx file not found: {unx_file}")
        return
    from unx2qlik import UNX2QlikParser
    parser = UNX2QlikParser(unx_file)
    try:
        parser.extract_unx()
        parser.parse_datafoundation()
        parser.parse_businesslayer()
        parser.summary()
    finally:
        parser.cleanup()

if __name__ == '__main__':
    print("=== TEST .UNX FILE GENERATOR ===")
    unx_path = create_test_unx()
    test_unx_parser()
    print(f"\n🎉 Test .unx file ready: {unx_path}")
    print("You can now test the parser with this file!") 