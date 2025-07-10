#!/usr/bin/env python3
"""
Universal BO2Qlik Converter
Automatically processes .unv and .unx files and generates Qlik Cloud scripts
"""

import os
import sys
import zipfile
import tempfile
import shutil
import xml.etree.ElementTree as ET
from datetime import datetime

class UniversalBO2QlikConverter:
    def __init__(self):
        self.file_path = None
        self.file_type = None  # 'unv' or 'unx'
        self.extract_dir = None
        self.tables = []
        self.joins = []
        self.objects = []
        self.dimensions = []
        self.measures = []
        self.attributes = []
        
    def find_business_objects_file(self):
        """Automatically finds a .unv or .unx file in the data/ folder"""
        data_dir = "../data"
        if not os.path.exists(data_dir):
            print(f"❌ data/ directory not found: {data_dir}")
            return False
        unv_files = []
        unx_files = []
        for file in os.listdir(data_dir):
            if file.endswith('.unv'):
                unv_files.append(file)
            elif file.endswith('.unx'):
                unx_files.append(file)
        # Prefer .unx files (newer)
        if unx_files:
            self.file_path = os.path.join(data_dir, unx_files[0])
            self.file_type = 'unx'
            print(f"📁 UNX file found: {unx_files[0]}")
            return True
        elif unv_files:
            self.file_path = os.path.join(data_dir, unv_files[0])
            self.file_type = 'unv'
            print(f"📁 UNV file found: {unv_files[0]}")
            return True
        else:
            print("❌ No .unv or .unx file found in data/")
            return False
    def extract_file(self):
        """Extracts the file (UNV or UNX)"""
        print(f"Extracting {self.file_type.upper()} file: {self.file_path}")
        self.extract_dir = tempfile.mkdtemp(prefix=f"{self.file_type}_extract_")
        with zipfile.ZipFile(self.file_path, 'r') as zip_ref:
            zip_ref.extractall(self.extract_dir)
        print(f"✅ {self.file_type.upper()} file extracted successfully")
        return True
    def parse_unv_file(self):
        """Parse a UNV file (legacy format)"""
        print("1. Parsing UNV file...")
        # Parse Columns file (readable)
        columns_file = os.path.join(self.extract_dir, 'Columns;')
        if os.path.exists(columns_file):
            with open(columns_file, 'r', encoding='utf-8') as f:
                content = f.read()
                fields = []
                for line in content.split('\n'):
                    if line.strip():
                        fields.extend(line.split())
                self.objects = [field for field in fields if field]
                print(f"   📊 {len(self.objects)} fields found in Columns")
        # Parse binary files for tables and joins
        tables_file = os.path.join(self.extract_dir, 'Tables;')
        if os.path.exists(tables_file):
            with open(tables_file, 'rb') as f:
                data = f.read()
                strings = self.extract_strings(data)
                self.tables = [s for s in strings if len(s) > 3]
                print(f"   📋 {len(self.tables)} tables found")
        joins_file = os.path.join(self.extract_dir, 'Joins;')
        if os.path.exists(joins_file):
            with open(joins_file, 'rb') as f:
                data = f.read()
                strings = self.extract_strings(data)
                self.joins = [s for s in strings if len(s) > 3]
                print(f"   🔗 {len(self.joins)} joins found")
        self.categorize_fields()
        return True
    def parse_unx_file(self):
        """Parse a UNX file (new format)"""
        print("1. Parsing UNX file...")
        # Parse datafoundation.xml
        df_path = os.path.join(self.extract_dir, 'datafoundation', 'datafoundation.xml')
        if os.path.exists(df_path):
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
        # Parse businesslayer.xml
        bl_path = os.path.join(self.extract_dir, 'businesslayer', 'businesslayer.xml')
        if os.path.exists(bl_path):
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
        return True
    def extract_strings(self, data):
        """Extracts readable strings from a binary file"""
        strings = []
        current_string = ""
        for byte in data:
            if 32 <= byte <= 126:
                current_string += chr(byte)
            else:
                if len(current_string) > 3:
                    strings.append(current_string)
                current_string = ""
        if len(current_string) > 3:
            strings.append(current_string)
        return strings
    def categorize_fields(self):
        """Categorizes fields into dimensions and measures"""
        dimension_keywords = ['id', 'name', 'code', 'type', 'category', 'region', 'city', 'country', 'date', 'year', 'month', 'day']
        measure_keywords = ['revenue', 'sales', 'amount', 'quantity', 'count', 'sum', 'total', 'price', 'cost', 'margin', 'profit']
        for field in self.objects:
            field_lower = field.lower()
            is_dimension = any(keyword in field_lower for keyword in dimension_keywords)
            is_measure = any(keyword in field_lower for keyword in measure_keywords)
            if is_dimension and not is_measure:
                self.dimensions.append(field)
            elif is_measure:
                self.measures.append(field)
            else:
                self.dimensions.append(field)
    def generate_qlik_script(self):
        """Generates the Qlik Cloud script"""
        print("2. Generating Qlik Cloud script...")
        script = f"""// Qlik Cloud script generated from {self.file_type.upper()} Business Objects
// Source file: {os.path.basename(self.file_path)}
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
        print("3. Saving script...")
        output_dir = "../output"
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"qlik_script_{self.file_type}_{timestamp}.qvs"
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
        print("=== UNIVERSAL BO2QLIK CONVERTER ===\n")
        try:
            # If no specific file was provided, find one automatically
            if not self.file_path:
                if not self.find_business_objects_file():
                    return False
            
            if not self.extract_file():
                return False
            if self.file_type == 'unx':
                if not self.parse_unx_file():
                    return False
            else:
                if not self.parse_unv_file():
                    return False
            script = self.generate_qlik_script()
            output_file = self.save_script(script)
            print("\n=== CONVERSION SUMMARY ===")
            print(f"📁 {self.file_type.upper()} file processed: {os.path.basename(self.file_path)}")
            print(f"📊 Tables extracted: {len(self.tables)}")
            print(f"🔗 Joins extracted: {len(self.joins)}")
            print(f"📏 Dimensions found: {len(self.dimensions)}")
            print(f"📈 Measures found: {len(self.measures)}")
            print(f"🏷️  Attributes found: {len(self.attributes)}")
            print(f"📄 Script generated: {os.path.basename(output_file)}")
            print(f"\n🎉 {self.file_type.upper()} conversion completed successfully!")
            return True
        except Exception as e:
            print(f"❌ Error during conversion: {e}")
            return False
        finally:
            self.cleanup()
def main():
    converter = UniversalBO2QlikConverter()
    
    # Check if a specific file was provided as argument
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if os.path.exists(file_path):
            converter.file_path = file_path
            if file_path.endswith('.unv'):
                converter.file_type = 'unv'
            elif file_path.endswith('.unx'):
                converter.file_type = 'unx'
            else:
                print(f"❌ Unsupported file format: {file_path}")
                return False
            print(f"📁 Processing specified file: {file_path}")
        else:
            print(f"❌ File not found: {file_path}")
            return False
    
    success = converter.run_conversion()
    return success

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 