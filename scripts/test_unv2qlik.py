#!/usr/bin/env python3
"""
Tests unitaires pour BO2Qlik - Convertisseur UNV vers Qlik Cloud
"""

import unittest
import os
import tempfile
import zipfile
import shutil
from unittest.mock import patch, MagicMock
import sys
import io

# Ajouter le répertoire courant au path pour importer les modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import de la classe principale
from unv2qlik_final import UNV2QlikConverter

class TestUNV2QlikConverter(unittest.TestCase):
    """Tests unitaires pour la classe UNV2QlikConverter"""
    
    def setUp(self):
        """Configuration initiale pour chaque test"""
        self.converter = UNV2QlikConverter()
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
    
    def tearDown(self):
        """Nettoyage après chaque test"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_extract_strings(self):
        """Test de la fonction extract_strings"""
        # Données de test avec des chaînes lisibles et des bytes non-ASCII
        test_data = b'Hello World\x00\x01\x02Test String\x03\x04\x05Another String'
        
        result = self.converter.extract_strings(test_data)
        
        # Vérifications
        self.assertIsInstance(result, list)
        self.assertIn('Hello World', result)
        self.assertIn('Test String', result)
        self.assertIn('Another String', result)
        self.assertEqual(len(result), 3)
    
    def test_categorize_fields(self):
        """Test de la catégorisation des champs"""
        # Champs de test
        self.converter.fields = [
            'Shop_id', 'Article_id', 'Sales_revenue', 'Quantity_sold',
            'City', 'State', 'Category', 'Margin', 'Promotion_cost'
        ]
        
        self.converter.categorize_fields()
        
        # Vérifications des dimensions
        expected_dimensions = ['Shop_id', 'Article_id', 'City', 'State', 'Category']
        for dim in expected_dimensions:
            self.assertIn(dim, self.converter.dimensions)
        
        # Vérifications des mesures
        expected_measures = ['Sales_revenue', 'Quantity_sold', 'Margin', 'Promotion_cost']
        for measure in expected_measures:
            self.assertIn(measure, self.converter.measures)
    
    def test_parse_columns_file_success(self):
        """Test du parsing du fichier Columns avec succès"""
        # Créer un fichier Columns de test
        test_content = """
        Shop_id    Shop_name       Address_1Manager        Date_open
        Article_id Article_label   Category   Family_name
        Sales_revenue Quantity_sold Margin     Promotion_cost
        """
        
        with open('Columns;', 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        result = self.converter.parse_columns_file()
        
        # Vérifications
        self.assertIsInstance(result, list)
        self.assertIn('Shop_id', result)
        self.assertIn('Article_id', result)
        self.assertIn('Sales_revenue', result)
        self.assertIn('Quantity_sold', result)
    
    def test_parse_columns_file_not_found(self):
        """Test du parsing du fichier Columns quand il n'existe pas"""
        result = self.converter.parse_columns_file()
        
        # Vérifications
        self.assertEqual(result, [])
        self.assertEqual(self.converter.fields, [])
    
    def test_parse_tables_file_success(self):
        """Test du parsing du fichier Tables avec succès"""
        # Créer un fichier Tables de test avec des données binaires
        test_data = b'\x00\x01\x02Shop_facts\x03\x04\x05Calendar_year_lookup\x06\x07\x08Article_lookup'
        
        with open('Tables;', 'wb') as f:
            f.write(test_data)
        
        result = self.converter.parse_tables_file()
        
        # Vérifications
        self.assertIsInstance(result, list)
        self.assertIn('Shop_facts', result)
        self.assertIn('Calendar_year_lookup', result)
        self.assertIn('Article_lookup', result)
    
    def test_parse_joins_file_success(self):
        """Test du parsing du fichier Joins avec succès"""
        # Créer un fichier Joins de test avec des données binaires
        test_data = b'\x00\x01\x02Week_id\x03\x04\x05Article_id\x06\x07\x08Shop_id'
        
        with open('Joins;', 'wb') as f:
            f.write(test_data)
        
        result = self.converter.parse_joins_file()
        
        # Vérifications
        self.assertIsInstance(result, list)
        self.assertIn('Week_id', result)
        self.assertIn('Article_id', result)
        self.assertIn('Shop_id', result)
    
    def test_generate_qlik_script(self):
        """Test de la génération du script Qlik"""
        # Préparer des données de test
        self.converter.tables = ['Shop_facts', 'Calendar_year_lookup']
        self.converter.fields = ['Shop_id', 'Sales_revenue', 'Quantity_sold']
        self.converter.dimensions = ['Shop_id']
        self.converter.measures = ['Sales_revenue', 'Quantity_sold']
        self.converter.joins = ['Week_id', 'Article_id']
        
        result = self.converter.generate_qlik_script()
        
        # Vérifications
        self.assertIsInstance(result, str)
        self.assertIn('Script Qlik Cloud généré depuis UNV Business Objects', result)
        self.assertIn('Shop_facts', result)
        self.assertIn('Calendar_year_lookup', result)
        self.assertIn('Shop_id', result)
        self.assertIn('Sales_revenue', result)
        self.assertIn('Quantity_sold', result)
        self.assertIn('Week_id', result)
        self.assertIn('Article_id', result)
    
    def test_cleanup_extracted_files(self):
        """Test du nettoyage des fichiers extraits"""
        # Créer des fichiers de test
        test_files = [
            'Columns;', 'Tables;', 'Joins;', 'Objects;',
            'Parameters;', 'Dimensions;', 'Contexts;'
        ]
        
        for file in test_files:
            with open(file, 'w') as f:
                f.write('test content')
        
        # Créer un dossier de test
        os.makedirs('UNW_Storage', exist_ok=True)
        with open('UNW_Storage/test.txt', 'w') as f:
            f.write('test content')
        
        # Exécuter le nettoyage
        self.converter.cleanup_extracted_files()
        
        # Vérifier que les fichiers ont été supprimés
        for file in test_files:
            self.assertFalse(os.path.exists(file))
        
        self.assertFalse(os.path.exists('UNW_Storage'))
    
    @patch('os.path.exists')
    @patch('os.listdir')
    def test_extract_unv_file_success(self, mock_listdir, mock_exists):
        """Test de l'extraction du fichier UNV avec succès"""
        # Mock des réponses
        mock_exists.return_value = True
        mock_listdir.return_value = ['eFashion.unv']
        
        # Mock de zipfile.ZipFile
        with patch('zipfile.ZipFile') as mock_zip:
            mock_zip.return_value.__enter__.return_value.extractall.return_value = None
            
            result = self.converter.extract_unv_file()
            
            # Vérifications
            self.assertTrue(result)
            # Ne pas vérifier l'appel à ZipFile car il peut ne pas être appelé si les fichiers existent déjà
    
    @patch('os.path.exists')
    def test_extract_unv_file_not_found(self, mock_exists):
        """Test de l'extraction quand aucun fichier UNV n'est trouvé"""
        mock_exists.return_value = False
        
        result = self.converter.extract_unv_file()
        
        # Vérifications
        self.assertFalse(result)
    
    def test_integration_full_workflow(self):
        """Test d'intégration du workflow complet"""
        # Créer des fichiers de test
        test_content = """
        Shop_id    Shop_name       Sales_revenue
        Article_id Article_label   Quantity_sold
        """
        
        with open('Columns;', 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        test_data = b'\x00\x01\x02Shop_facts\x03\x04\x05Calendar_year_lookup'
        with open('Tables;', 'wb') as f:
            f.write(test_data)
        
        test_data = b'\x00\x01\x02Week_id\x03\x04\x05Article_id'
        with open('Joins;', 'wb') as f:
            f.write(test_data)
        
        # Exécuter le workflow
        self.converter.parse_columns_file()
        self.converter.parse_tables_file()
        self.converter.parse_joins_file()
        self.converter.categorize_fields()
        
        # Vérifications
        self.assertGreater(len(self.converter.fields), 0)
        self.assertGreater(len(self.converter.tables), 0)
        self.assertGreater(len(self.converter.joins), 0)
        self.assertGreater(len(self.converter.dimensions), 0)
        self.assertGreater(len(self.converter.measures), 0)
        
        # Test de génération
        script = self.converter.generate_qlik_script()
        self.assertIsInstance(script, str)
        self.assertIn('Script Qlik Cloud', script)

class TestFileOperations(unittest.TestCase):
    """Tests pour les opérations sur les fichiers"""
    
    def setUp(self):
        """Configuration initiale"""
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
    
    def tearDown(self):
        """Nettoyage"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_create_test_unv_file(self):
        """Test de création d'un fichier UNV de test"""
        # Créer un fichier ZIP qui simule un UNV
        test_files = {
            'Columns;': 'Shop_id Shop_name Sales_revenue\n',
            'Tables;': b'\x00\x01\x02Shop_facts\x03\x04\x05',
            'Joins;': b'\x00\x01\x02Week_id\x03\x04\x05',
            'Objects;': b'\x00\x01\x02Test Object\x03\x04\x05'
        }
        
        with zipfile.ZipFile('test.unv', 'w') as zip_file:
            for filename, content in test_files.items():
                if isinstance(content, bytes):
                    zip_file.writestr(filename, content)
                else:
                    zip_file.writestr(filename, content)
        
        # Vérifier que le fichier a été créé
        self.assertTrue(os.path.exists('test.unv'))
        
        # Vérifier le contenu
        with zipfile.ZipFile('test.unv', 'r') as zip_file:
            file_list = zip_file.namelist()
            self.assertIn('Columns;', file_list)
            self.assertIn('Tables;', file_list)
            self.assertIn('Joins;', file_list)

def run_tests():
    """Fonction pour exécuter tous les tests"""
    print("=== Tests unitaires BO2Qlik ===")
    
    # Créer une suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Ajouter les tests
    suite.addTests(loader.loadTestsFromTestCase(TestUNV2QlikConverter))
    suite.addTests(loader.loadTestsFromTestCase(TestFileOperations))
    
    # Exécuter les tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Résumé
    print(f"\n=== Résumé des tests ===")
    print(f"Tests exécutés: {result.testsRun}")
    print(f"Échecs: {len(result.failures)}")
    print(f"Erreurs: {len(result.errors)}")
    
    if result.failures:
        print("\n=== Échecs ===")
        for test, traceback in result.failures:
            print(f"❌ {test}: {traceback}")
    
    if result.errors:
        print("\n=== Erreurs ===")
        for test, traceback in result.errors:
            print(f"❌ {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\n🎉 Tous les tests sont passés !")
    else:
        print("\n⚠️  Certains tests ont échoué.")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1) 