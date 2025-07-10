#!/usr/bin/env python3
"""
UNX to Qlik Cloud Converter
Extracts data from a .unx file and generates a Qlik Cloud script
"""

import os
import sys
import zipfile
import tempfile
import shutil
import xml.etree.ElementTree as ET
from datetime import datetime

class UNX2QlikConverter:
    def __init__(self, unx_path=None):
        self.unx_path = unx_path
        self.extract_dir = None
        self.tables = []
        self.joins = []
        self.objects = []
        self.dimensions = []
        self.measures = []
        self.attributes = []
        
    def find_unx_file(self):
        """Automatically finds a .unx file in the data/ folder"""
        data_dir = "../data"
        if not os.path.exists(data_dir):
            print(f"❌ data/ directory not found: {data_dir}")
            return False
        unv_files = []
        for file in os.listdir(data_dir):
            if file.endswith('.unx'):
                unv_files.append(file)
        if not unv_files:
            print("❌ No .unx file found in data/")
            return False
        self.unx_path = os.path.join(data_dir, unv_files[0])
        print(f"📁 UNX file found: {self.unx_path}")
        return True
    def extract_unx(self):
        """Extracts the .unx file"""
        if not self.unx_path:
            if not self.find_unx_file():
                return False
        print(f"Extracting UNX file: {self.unx_path}")
        self.extract_dir = tempfile.mkdtemp(prefix="unx_extract_")
        with zipfile.ZipFile(self.unx_path, 'r') as zip_ref:
            zip_ref.extractall(self.extract_dir)
        print(f"✅ UNX file extracted successfully")
        return True
    def parse_datafoundation(self):
        """Parse datafoundation.xml for tables and joins"""
        print("1. Parsing datafoundation.xml...")
        df_path = os.path.join(self.extract_dir, 'datafoundation', 'datafoundation.xml')
        if not os.path.exists(df_path):
            print(f"❌ File not found: {df_path}")
            return False
        tree = ET.parse(df_path)
        root = tree.getroot()
        ns = {'bip': 'http://www.sap.com/rws/bip'}
        for table in root.findall('.//bip:table', ns):
            name = table.get('name') or table.get('id')
            if name:
                self.tables.append(name)
                print(f"   📋 Table found: {name}")
        if not self.tables:
            for table in root.findall('.//table'):
                name = table.get('name') or table.get('id')
                if name:
                    self.tables.append(name)
                    print(f"   📋 Table found (no namespace): {name}")
        for join in root.findall('.//bip:join', ns):
            expr = join.get('expression') or join.get('id')
            if expr:
                self.joins.append(expr)
                print(f"   🔗 Join found: {expr}")
        if not self.joins:
            for join in root.findall('.//join'):
                expr = join.get('expression') or join.get('id')
                if expr:
                    self.joins.append(expr)
                    print(f"   🔗 Join found (no namespace): {expr}")
        print(f"✅ {len(self.tables)} tables and {len(self.joins)} joins found")
        return True
    def parse_businesslayer(self):
        """Parse businesslayer.xml for objects, dimensions, measures"""
        print("2. Parsing businesslayer.xml...")
        bl_path = os.path.join(self.extract_dir, 'businesslayer', 'businesslayer.xml')
        if not os.path.exists(bl_path):
            print(f"❌ File not found: {bl_path}")
            return False
        tree = ET.parse(bl_path)
        root = tree.getroot()
        ns = {'bip': 'http://www.sap.com/rws/bip'}
        for obj in root.findall('.//bip:businessObject', ns):
            name = obj.get('name') or obj.get('id')
            if name:
                self.objects.append(name)
                print(f"   📊 Object found: {name}")
            typ = obj.get('type')
            if typ == 'Dimension':
                self.dimensions.append(name)
                print(f"   📏 Dimension found: {name}")
            elif typ == 'Measure':
                self.measures.append(name)
                print(f"   📈 Measure found: {name}")
            elif typ == 'Attribute':
                self.attributes.append(name)
                print(f"   🏷️  Attribute found: {name}")
        if not self.objects:
            for obj in root.findall('.//businessObject'):
                name = obj.get('name') or obj.get('id')
                if name:
                    self.objects.append(name)
                    print(f"   📊 Object found (no namespace): {name}")
                typ = obj.get('type')
                if typ == 'Dimension':
                    self.dimensions.append(name)
                    print(f"   📏 Dimension found (no namespace): {name}")
                elif typ == 'Measure':
                    self.measures.append(name)
                    print(f"   📈 Measure found (no namespace): {name}")
                elif typ == 'Attribute':
                    self.attributes.append(name)
                    print(f"   🏷️  Attribute found (no namespace): {name}")
        print(f"✅ {len(self.objects)} objects found ({len(self.dimensions)} dimensions, {len(self.measures)} measures, {len(self.attributes)} attributes)")
        return True
    def generate_qlik_script(self):
        """Generates the Qlik Cloud script"""
        print("3. Generating Qlik Cloud script...")
        script = f"""// Qlik Cloud script generated from UNX Business Objects
// Source file: {os.path.basename(self.unx_path)}
// Generation date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
// Extracted tables: {len(self.tables)}
// Extracted objects: {len(self.objects)}

// ========================================
// CONNECTION CONFIGURATION
// ========================================
// Replace these parameters for your environment
LET vServer = 'your_db_server';
LET vDatabase = 'your_database';
LET vUsername = 'your_user';
LET vPassword = 'your_password';

// ========================================
// DATABASE CONNECTION
// ========================================
// Example for SQL Server
// LIB CONNECT TO 'SQL_Server_Connection' (SERVER '$(vServer)', DATABASE '$(vDatabase)', USER '$(vUsername)', PASSWORD '$(vPassword)');

// ========================================
// TABLE LOADING
// ========================================
"""
        for table in self.tables:
            script += f"""
// Loading table {table}
{table}:
LOAD *
FROM [{table}]
;"""
        if self.joins:
            script += f"""

// ========================================
// JOINS
// ========================================
"""
            for join in self.joins:
                script += f"// Join: {join}\n"
        script += f"""

// ========================================
// DIMENSIONS AND MEASURES
// ========================================
// Available dimensions: {', '.join(self.dimensions)}
// Available measures: {', '.join(self.measures)}
// Available attributes: {', '.join(self.attributes)}

// ========================================
// CALCULATION EXAMPLES
// ========================================
"""
        for measure in self.measures:
            script += f"""
// Calculation for {measure}
// Sum({measure}) as Total_{measure}
// Avg({measure}) as Avg_{measure}
// Count({measure}) as Count_{measure}
"""
        script += f"""

// ========================================
// USAGE NOTES
// ========================================
// 1. Adjust connection parameters for your environment
// 2. Edit table names if needed
// 3. Add your own calculations and transformations
// 4. Test joins and optimize performance
// 5. Document your changes

// ========================================
// END OF SCRIPT
// ========================================
"""
        return script
    def save_script(self, script):
        """Saves the generated script"""
        print("4. Saving script...")
        output_dir = "../output"
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"qlik_script_unx_{timestamp}.qvs"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(script)
        print(f"✅ Script saved: {filepath}")
        return filepath
    def cleanup(self):
        """Cleans up temporary files"""
        if self.extract_dir and os.path.exists(self.extract_dir):
            shutil.rmtree(self.extract_dir, ignore_errors=True)
            print("✅ Temporary files cleaned up")
    def run_conversion(self):
        """Runs the full conversion process"""
        print("=== UNX TO QLIK CLOUD CONVERTER ===\n")
        try:
            if not self.extract_unx():
                return False
            if not self.parse_datafoundation():
                return False
            if not self.parse_businesslayer():
                return False
            script = self.generate_qlik_script()
            output_file = self.save_script(script)
            print("\n=== CONVERSION SUMMARY ===")
            print(f"📁 UNX file processed: {os.path.basename(self.unx_path)}")
            print(f"📊 Tables extracted: {len(self.tables)}")
            print(f"🔗 Joins extracted: {len(self.joins)}")
            print(f"📏 Dimensions found: {len(self.dimensions)}")
            print(f"📈 Measures found: {len(self.measures)}")
            print(f"🏷️  Attributes found: {len(self.attributes)}")
            print(f"📄 Script generated: {os.path.basename(output_file)}")
            print("\n🎉 Conversion completed successfully!")
            return True
        except Exception as e:
            print(f"❌ Error during conversion: {e}")
            return False
        finally:
            self.cleanup()
def main():
    converter = UNX2QlikConverter()
    success = converter.run_conversion()
    return success
if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 