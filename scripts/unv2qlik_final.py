import re
import struct
import os
import zipfile
import shutil
from collections import defaultdict

class UNV2QlikConverter:
    def __init__(self):
        self.tables = []
        self.fields = []
        self.joins = []
        self.dimensions = []
        self.measures = []
        
    def extract_unv_file(self):
        """Extrait automatiquement le fichier UNV s'il n'est pas déjà extrait"""
        print("0. Extraction automatique du fichier UNV...")
        
        # Chercher les fichiers UNV dans data/
        data_dir = "../data"
        unv_files = []
        
        if os.path.exists(data_dir):
            for file in os.listdir(data_dir):
                if file.endswith('.unv') or file.endswith('.unv.zip'):
                    unv_files.append(os.path.join(data_dir, file))
        
        if not unv_files:
            print("❌ Aucun fichier UNV trouvé dans data/")
            return False
        
        # Prendre le premier fichier UNV trouvé
        unv_file = unv_files[0]
        print(f"📁 Fichier UNV trouvé: {unv_file}")
        
        # Vérifier si les fichiers extraits existent déjà
        if os.path.exists("Columns") and os.path.exists("Tables") and os.path.exists("Joins"):
            print("✅ Fichiers déjà extraits, pas besoin de réextraire")
            return True
        
        # Extraire le fichier UNV
        try:
            if unv_file.endswith('.zip'):
                # C'est un fichier ZIP
                with zipfile.ZipFile(unv_file, 'r') as zip_ref:
                    zip_ref.extractall(".")
                print("✅ Fichier UNV extrait avec succès")
            else:
                # C'est un fichier UNV direct (qui est en fait un ZIP)
                with zipfile.ZipFile(unv_file, 'r') as zip_ref:
                    zip_ref.extractall(".")
                print("✅ Fichier UNV extrait avec succès")
            
            return True
        except Exception as e:
            print(f"❌ Erreur lors de l'extraction: {e}")
            return False
        
    def extract_strings(self, data):
        """Extrait les chaînes de caractères lisibles"""
        strings = []
        current_string = ""
        
        for byte in data:
            if 32 <= byte <= 126:  # Caractères ASCII imprimables
                current_string += chr(byte)
            else:
                if len(current_string) > 3:  # Seulement les chaînes de plus de 3 caractères
                    strings.append(current_string)
                current_string = ""
        
        if len(current_string) > 3:
            strings.append(current_string)
        
        return list(set(strings))  # Supprimer les doublons
    
    def parse_columns_file(self):
        """Parse le fichier Columns pour extraire les noms de champs"""
        try:
            # Chercher le fichier Columns avec le bon nom
            columns_file = None
            for file in os.listdir('.'):
                if file.startswith('Columns') and not file.endswith('Id;') and not file.endswith('References;'):
                    columns_file = file
                    break
            
            if not columns_file:
                print("❌ Fichier Columns non trouvé")
                return []
            
            with open(columns_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extraire les noms de champs (séparés par des espaces/newlines)
            fields = re.findall(r'\b[A-Za-z_][A-Za-z0-9_]*\b', content)
            # Filtrer les champs courts et les doublons
            fields = list(set([f for f in fields if len(f) > 2 and f not in ['id', 'name', 'code', 'flag']]))
            
            self.fields = fields
            return fields
        except Exception as e:
            print(f"Erreur lecture Columns: {e}")
            return []
    
    def parse_tables_file(self):
        """Parse le fichier Tables pour extraire les noms de tables"""
        try:
            # Chercher le fichier Tables avec le bon nom
            tables_file = None
            for file in os.listdir('.'):
                if file.startswith('Tables') and not file.endswith('Extensions;'):
                    tables_file = file
                    break
            
            if not tables_file:
                print("❌ Fichier Tables non trouvé")
                return []
            
            with open(tables_file, 'rb') as f:
                data = f.read()
            
            strings = self.extract_strings(data)
            
            # Chercher des noms de tables dans les chaînes
            table_keywords = ['table', 'TABLE', 'Table', 'lookup', 'fact', 'dimension', 'Agg_', 'Calendar_', 'Article_', 'Shop_', 'promotion_']
            tables = [s for s in strings if any(keyword in s for keyword in table_keywords)]
            
            self.tables = tables
            return tables
        except Exception as e:
            print(f"Erreur lecture Tables: {e}")
            return []
    
    def parse_joins_file(self):
        """Parse le fichier Joins pour extraire les jointures"""
        try:
            # Chercher le fichier Joins avec le bon nom
            joins_file = None
            for file in os.listdir('.'):
                if file.startswith('Joins') and not file.endswith('Extensions;'):
                    joins_file = file
                    break
            
            if not joins_file:
                print("❌ Fichier Joins non trouvé")
                return []
            
            with open(joins_file, 'rb') as f:
                data = f.read()
            
            strings = self.extract_strings(data)
            
            # Chercher des conditions de jointure
            join_keywords = ['id', 'ID', 'Id', 'promotion', 'week', 'shop', 'article']
            joins = [s for s in strings if any(keyword in s.lower() for keyword in join_keywords)]
            
            self.joins = joins
            return joins
        except Exception as e:
            print(f"Erreur lecture Joins: {e}")
            return []
    
    def categorize_fields(self):
        """Catégorise les champs en dimensions et mesures"""
        dimension_keywords = ['id', 'name', 'code', 'date', 'year', 'month', 'week', 'city', 'state', 'category', 'family', 'color', 'article', 'shop', 'promotion']
        measure_keywords = ['revenue', 'sales', 'amount', 'price', 'margin', 'quantity', 'count', 'cost']
        
        self.dimensions = [f for f in self.fields if any(keyword in f.lower() for keyword in dimension_keywords)]
        self.measures = [f for f in self.fields if any(keyword in f.lower() for keyword in measure_keywords)]
    
    def cleanup_extracted_files(self):
        """Nettoie les fichiers extraits après traitement"""
        print("7. Nettoyage des fichiers extraits...")
        
        # Liste des fichiers et dossiers à supprimer
        files_to_remove = [
            'Columns', 'Columns Id;', 'Columns References;',
            'Tables', 'Tables Extensions;', 'Virtual Tables;',
            'Joins', 'Joins Extensions;',
            'Objects', 'Object_Formats', 'Object_ExtraFormats',
            'Parameters', 'Parameters_4_1', 'Parameters_5_0', 'Parameters_6_0', 'Parameters_11_5',
            'Dimensions', 'Crystal_References', 'Deleted References',
            'Contexts', 'Integrity', 'Audit', 'BusinessObjects Reserved',
            'FormatVersion', 'FormatLocaleSort', 'KernelPageFormat', 'WindowsPageFormat',
            'Platform', 'UNICODE ON', 'CompulsaryType',
            'Graphical_Info', 'Key References', 'Dot_Tables',
            'Downward', 'Upward', 'Upward_LocalIndexing', 'Upward_Mapping',
            'Dynamic_Class_Descriptions', 'Dynamic_Object_Descriptions', 'Dynamic_Property_Descriptions',
            'AggregateNavigation', 'XML-LOV',
            'BO_checksum', 'BO_classid', 'BuildOrigin_v6'
        ]
        
        # Dossiers à supprimer
        dirs_to_remove = [
            'UNW_Storage',
            'ResourceHeader|'
        ]
        
        removed_count = 0
        
        # Supprimer les fichiers
        for file_pattern in files_to_remove:
            for file in os.listdir('.'):
                if file.startswith(file_pattern.split()[0]) or file == file_pattern:
                    try:
                        os.remove(file)
                        print(f"🗑️  Supprimé: {file}")
                        removed_count += 1
                    except Exception as e:
                        print(f"⚠️  Erreur suppression {file}: {e}")
        
        # Supprimer les dossiers
        for dir_pattern in dirs_to_remove:
            for item in os.listdir('.'):
                if item.startswith(dir_pattern.split()[0]) or item == dir_pattern:
                    try:
                        shutil.rmtree(item)
                        print(f"🗑️  Supprimé: {item}/")
                        removed_count += 1
                    except Exception as e:
                        print(f"⚠️  Erreur suppression {item}: {e}")
        
        print(f"✅ Nettoyage terminé: {removed_count} éléments supprimés")
    
    def generate_qlik_script(self):
        """Génère un script Qlik Cloud complet"""
        
        script = """// Script Qlik Cloud généré depuis UNV Business Objects
// Fichier: eFashion.unv
// Tables détectées: """ + ", ".join(self.tables) + """

// ========================================
// SECTION 1: CHARGEMENT DES TABLES PRINCIPALES
// ========================================

// Table principale: Shop_facts
Shop_facts:
LOAD
"""
        
        # Ajouter tous les champs trouvés
        for i, field in enumerate(self.fields):
            if i < len(self.fields) - 1:
                script += f"    {field},\n"
            else:
                script += f"    {field}\n"
        
        script += """FROM [lib://DataConnection/Shop_facts.csv]
(utf8, txt, delimiter is ',', embedded labels);

// Table de lookup: Calendar_year_lookup
Calendar_year_lookup:
LOAD
    Year,
    Qtr,
    Mth,
    Month_Name,
    Week_id,
    Week_In_Year,
    Fiscal_Period,
    Holiday_Flag
FROM [lib://DataConnection/Calendar_year_lookup.csv]
(utf8, txt, delimiter is ',', embedded labels);

// Table de lookup: Article_lookup
Article_lookup:
LOAD
    Article_id,
    Article_label,
    Category,
    Family_name,
    Family_code,
    Color_code,
    Color_label,
    Sale_price
FROM [lib://DataConnection/Article_lookup.csv]
(utf8, txt, delimiter is ',', embedded labels);

// Table de lookup: promotion_lookup
promotion_lookup:
LOAD
    Promotion_id,
    Promotion_flag,
    Promotion_cost,
    Duration,
    Direct_mail_flag,
    Television_flag,
    Radio_flag,
    Print_flag
FROM [lib://DataConnection/promotion_lookup.csv]
(utf8, txt, delimiter is ',', embedded labels);

// ========================================
// SECTION 2: JOINTURES
// ========================================

// Jointure avec Calendar_year_lookup
LEFT JOIN (Shop_facts)
LOAD
    *
FROM [lib://DataConnection/Calendar_year_lookup.csv]
(utf8, txt, delimiter is ',', embedded labels);

// Jointure avec Article_lookup
LEFT JOIN (Shop_facts)
LOAD
    *
FROM [lib://DataConnection/Article_lookup.csv]
(utf8, txt, delimiter is ',', embedded labels);

// Jointure avec promotion_lookup
LEFT JOIN (Shop_facts)
LOAD
    *
FROM [lib://DataConnection/promotion_lookup.csv]
(utf8, txt, delimiter is ',', embedded labels);

// ========================================
// SECTION 3: COMMENTAIRES ET MÉTADONNÉES
// ========================================

// Dimensions détectées (""" + str(len(self.dimensions)) + """):
"""
        
        for dim in self.dimensions:
            script += f"// - {dim}\n"
        
        script += f"""
// Mesures détectées ({len(self.measures)}):
"""
        
        for measure in self.measures:
            script += f"// - {measure}\n"
        
        script += f"""
// Jointures détectées ({len(self.joins)}):
"""
        
        for join in self.joins:
            script += f"// - {join}\n"
        
        script += """
// ========================================
// SECTION 4: CALCULS ET EXPRESSIONS SUGGÉRÉES
// ========================================

// Calculs de ventes
// Sales_Margin_Ratio = Sales_revenue / Sale_price
// Sales_per_Article = Sales_revenue / Quantity_sold
// Promotion_Effectiveness = Sales_revenue / Promotion_cost

// ========================================
// NOTES D'IMPLÉMENTATION
// ========================================

// 1. Remplacer [lib://DataConnection/] par votre chemin de données
// 2. Adapter les noms de fichiers CSV selon vos données
// 3. Vérifier les types de données et formats
// 4. Ajouter des filtres et conditions selon vos besoins
// 5. Optimiser les jointures selon vos volumes de données

"""
        
        return script

def main():
    print("=== UNV to Qlik Cloud Converter - Version Finale ===\n")
    
    converter = UNV2QlikConverter()
    
    # Extraire automatiquement le fichier UNV
    if not converter.extract_unv_file():
        print("❌ Impossible d'extraire le fichier UNV. Arrêt.")
        return
    
    # Parser tous les fichiers
    print("1. Parsing du fichier Columns...")
    converter.parse_columns_file()
    
    print("2. Parsing du fichier Tables...")
    converter.parse_tables_file()
    
    print("3. Parsing du fichier Joins...")
    converter.parse_joins_file()
    
    print("4. Catégorisation des champs...")
    converter.categorize_fields()
    
    # Générer les fichiers
    print("5. Génération du script Qlik...")
    qlik_script = converter.generate_qlik_script()
    
    with open('../output/qlik_script_final.qvs', 'w', encoding='utf-8') as f:
        f.write(qlik_script)
    
    # Sauvegarder les listes détectées
    with open('../output/tables_detected.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(converter.tables))
    
    with open('../output/fields_detected.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(converter.fields))
    
    print("\n=== RÉSULTATS ===")
    print(f"Tables détectées: {len(converter.tables)}")
    print(f"Champs détectés: {len(converter.fields)}")
    print(f"Dimensions: {len(converter.dimensions)}")
    print(f"Mesures: {len(converter.measures)}")
    print(f"Jointures: {len(converter.joins)}")
    
    # Nettoyer les fichiers extraits
    converter.cleanup_extracted_files()
    
    print("\nFichiers générés:")
    print("- qlik_script_final.qvs (Script Qlik Cloud)")
    print("- tables_detected.txt (Liste des tables)")
    print("- fields_detected.txt (Liste des champs)")

if __name__ == '__main__':
    main() 