#!/usr/bin/env python3
"""
Tests rapides pour BO2Qlik - Vérification des fonctionnalités principales
"""

import os
import sys
import tempfile
import zipfile
import shutil

def test_basic_functionality():
    """Test des fonctionnalités de base"""
    print("🧪 Test des fonctionnalités de base...")
    
    try:
        # Import de la classe principale
        from unv2qlik_final import UNV2QlikConverter
        
        # Créer une instance
        converter = UNV2QlikConverter()
        
        # Test de la fonction extract_strings
        test_data = b'Hello World\x00\x01\x02Test String\x03\x04\x05'
        strings = converter.extract_strings(test_data)
        
        if 'Hello World' in strings and 'Test String' in strings:
            print("✅ extract_strings: OK")
        else:
            print("❌ extract_strings: ÉCHEC")
            return False
        
        # Test de la catégorisation
        converter.fields = ['Shop_id', 'Sales_revenue', 'City', 'Margin']
        converter.categorize_fields()
        
        if 'Shop_id' in converter.dimensions and 'Sales_revenue' in converter.measures:
            print("✅ categorize_fields: OK")
        else:
            print("❌ categorize_fields: ÉCHEC")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur dans les tests de base: {e}")
        return False

def test_file_parsing():
    """Test du parsing de fichiers"""
    print("🧪 Test du parsing de fichiers...")
    
    try:
        from unv2qlik_final import UNV2QlikConverter
        
        # Créer un répertoire temporaire
        temp_dir = tempfile.mkdtemp()
        original_cwd = os.getcwd()
        os.chdir(temp_dir)
        
        # Créer des fichiers de test
        test_content = """
        Shop_id    Shop_name       Sales_revenue
        Article_id Article_label   Quantity_sold
        """
        
        with open('Columns;', 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        # Tester le parsing
        converter = UNV2QlikConverter()
        result = converter.parse_columns_file()
        
        if 'Shop_id' in result and 'Sales_revenue' in result:
            print("✅ parse_columns_file: OK")
        else:
            print("❌ parse_columns_file: ÉCHEC")
            return False
        
        # Nettoyer
        os.chdir(original_cwd)
        shutil.rmtree(temp_dir)
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur dans le parsing de fichiers: {e}")
        return False

def test_script_generation():
    """Test de la génération de script"""
    print("🧪 Test de la génération de script...")
    
    try:
        from unv2qlik_final import UNV2QlikConverter
        
        converter = UNV2QlikConverter()
        
        # Préparer des données de test
        converter.tables = ['Shop_facts', 'Calendar_year_lookup']
        converter.fields = ['Shop_id', 'Sales_revenue', 'Quantity_sold']
        converter.dimensions = ['Shop_id']
        converter.measures = ['Sales_revenue', 'Quantity_sold']
        converter.joins = ['Week_id', 'Article_id']
        
        # Générer le script
        script = converter.generate_qlik_script()
        
        # Vérifications
        checks = [
            ('Script Qlik Cloud généré', 'Titre du script'),
            ('Shop_facts', 'Table principale'),
            ('Shop_id', 'Champ dimension'),
            ('Sales_revenue', 'Champ mesure'),
            ('Week_id', 'Jointure')
        ]
        
        all_ok = True
        for check_text, description in checks:
            if check_text in script:
                print(f"✅ {description}: OK")
            else:
                print(f"❌ {description}: ÉCHEC")
                all_ok = False
        
        return all_ok
        
    except Exception as e:
        print(f"❌ Erreur dans la génération de script: {e}")
        return False

def test_cleanup_functionality():
    """Test de la fonctionnalité de nettoyage"""
    print("🧪 Test de la fonctionnalité de nettoyage...")
    
    try:
        from unv2qlik_final import UNV2QlikConverter
        
        # Créer un répertoire temporaire
        temp_dir = tempfile.mkdtemp()
        original_cwd = os.getcwd()
        os.chdir(temp_dir)
        
        # Créer des fichiers de test
        test_files = ['Columns;', 'Tables;', 'Joins;', 'Objects;']
        for file in test_files:
            with open(file, 'w') as f:
                f.write('test content')
        
        # Créer un dossier de test
        os.makedirs('UNW_Storage', exist_ok=True)
        with open('UNW_Storage/test.txt', 'w') as f:
            f.write('test content')
        
        # Tester le nettoyage
        converter = UNV2QlikConverter()
        converter.cleanup_extracted_files()
        
        # Vérifier que les fichiers ont été supprimés
        files_exist = [os.path.exists(file) for file in test_files]
        dir_exists = os.path.exists('UNW_Storage')
        
        if not any(files_exist) and not dir_exists:
            print("✅ cleanup_extracted_files: OK")
        else:
            print("❌ cleanup_extracted_files: ÉCHEC")
            return False
        
        # Nettoyer
        os.chdir(original_cwd)
        shutil.rmtree(temp_dir)
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur dans le nettoyage: {e}")
        return False

def test_unv_file_detection():
    """Test de la détection de fichiers UNV"""
    print("🧪 Test de la détection de fichiers UNV...")
    
    try:
        # Vérifier si le fichier UNV existe dans data/
        data_dir = "../data"
        if os.path.exists(data_dir):
            unv_files = [f for f in os.listdir(data_dir) if f.endswith('.unv') or f.endswith('.unv.zip')]
            
            if unv_files:
                print(f"✅ Fichiers UNV trouvés: {unv_files}")
                return True
            else:
                print("⚠️  Aucun fichier UNV trouvé dans data/")
                return True  # Pas d'erreur, juste un avertissement
        else:
            print("⚠️  Répertoire data/ non trouvé")
            return True  # Pas d'erreur, juste un avertissement
            
    except Exception as e:
        print(f"❌ Erreur dans la détection de fichiers UNV: {e}")
        return False

def run_quick_tests():
    """Exécuter tous les tests rapides"""
    print("=== Tests rapides BO2Qlik ===\n")
    
    tests = [
        ("Fonctionnalités de base", test_basic_functionality),
        ("Parsing de fichiers", test_file_parsing),
        ("Génération de script", test_script_generation),
        ("Fonctionnalité de nettoyage", test_cleanup_functionality),
        ("Détection de fichiers UNV", test_unv_file_detection)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erreur inattendue: {e}")
            results.append((test_name, False))
    
    # Résumé
    print("\n" + "="*50)
    print("RÉSUMÉ DES TESTS RAPIDES")
    print("="*50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nTests réussis: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 Tous les tests rapides sont passés !")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) ont échoué.")
        return False

if __name__ == '__main__':
    success = run_quick_tests()
    sys.exit(0 if success else 1) 