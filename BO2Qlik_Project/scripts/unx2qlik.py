#!/usr/bin/env python3
"""
Basic parser for .unx files (new generation BO Universe)
Extracts tables, objects, dimensions, measures, joins and prints a summary
"""

import os
import zipfile
import tempfile
import shutil
import xml.etree.ElementTree as ET

class UNX2QlikParser:
    def __init__(self, unx_path):
        self.unx_path = unx_path
        self.extract_dir = tempfile.mkdtemp(prefix="unx_extract_")
        self.tables = []
        self.joins = []
        self.objects = []
        self.dimensions = []
        self.measures = []

    def extract_unx(self):
        print(f"Extracting UNX file: {self.unx_path}")
        with zipfile.ZipFile(self.unx_path, 'r') as zip_ref:
            zip_ref.extractall(self.extract_dir)
        print(f"✅ Extracted to: {self.extract_dir}")

    def parse_datafoundation(self):
        """Parse datafoundation.xml for tables and joins"""
        df_path = os.path.join(self.extract_dir, 'datafoundation', 'datafoundation.xml')
        if not os.path.exists(df_path):
            print(f"❌ File not found: {df_path}")
            return
        tree = ET.parse(df_path)
        root = tree.getroot()
        ns = {'bip': 'http://www.sap.com/rws/bip'}
        # Tables
        for table in root.findall('.//bip:table', ns):
            name = table.get('name') or table.get('id')
            if name:
                self.tables.append(name)
        # Joins
        for join in root.findall('.//bip:join', ns):
            expr = join.get('expression') or join.get('id')
            if expr:
                self.joins.append(expr)
        # If no namespace, try without
        if not self.tables:
            for table in root.findall('.//table'):
                name = table.get('name') or table.get('id')
                if name:
                    self.tables.append(name)
        if not self.joins:
            for join in root.findall('.//join'):
                expr = join.get('expression') or join.get('id')
                if expr:
                    self.joins.append(expr)

    def parse_businesslayer(self):
        """Parse businesslayer.xml for objects, dimensions, measures"""
        bl_path = os.path.join(self.extract_dir, 'businesslayer', 'businesslayer.xml')
        if not os.path.exists(bl_path):
            print(f"❌ File not found: {bl_path}")
            return
        tree = ET.parse(bl_path)
        root = tree.getroot()
        # Objects (dimensions, measures, attributes)
        for obj in root.findall('.//businessObject'):
            name = obj.get('name') or obj.get('id')
            if name:
                self.objects.append(name)
            # Simple categorization
            typ = obj.get('type')
            if typ == 'Dimension':
                self.dimensions.append(name)
            elif typ == 'Measure':
                self.measures.append(name)

    def summary(self):
        print("\n=== UNX SUMMARY ===")
        print(f"Tables found: {len(self.tables)}")
        print(self.tables)
        print(f"Joins found: {len(self.joins)}")
        print(self.joins)
        print(f"Objects found: {len(self.objects)}")
        print(self.objects[:10], '...')
        print(f"Dimensions: {len(self.dimensions)}")
        print(self.dimensions[:10], '...')
        print(f"Measures: {len(self.measures)}")
        print(self.measures[:10], '...')

    def cleanup(self):
        shutil.rmtree(self.extract_dir, ignore_errors=True)

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 unx2qlik.py <file.unx>")
        sys.exit(1)
    unx_file = sys.argv[1]
    if not os.path.exists(unx_file):
        print(f"File not found: {unx_file}")
        sys.exit(1)
    parser = UNX2QlikParser(unx_file)
    try:
        parser.extract_unx()
        parser.parse_datafoundation()
        parser.parse_businesslayer()
        parser.summary()
    finally:
        parser.cleanup() 