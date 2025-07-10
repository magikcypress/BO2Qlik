#!/usr/bin/env python3
"""
Configuration pour les tests BO2Qlik
"""

# Configuration des tests
TEST_CONFIG = {
    'verbose': True,
    'stop_on_failure': False,
    'cleanup_after_tests': True,
    'test_data_dir': 'test_data',
    'output_dir': 'test_output'
}

# Données de test pour les fichiers UNV
TEST_UNV_CONTENT = {
    'Columns;': """
Shop_id    Shop_name       Address_1Manager        Date_open
Article_id Article_label   Category   Family_name
Sales_revenue Quantity_sold Margin     Promotion_cost
Week_id    Year           Month      Day_of_week
City       State          Country    Region
    """,
    
    'Tables;': b'\x00\x01\x02Shop_facts\x03\x04\x05Calendar_year_lookup\x06\x07\x08Article_lookup\x09\x0A\x0BShop_lookup',
    
    'Joins;': b'\x00\x01\x02Week_id\x03\x04\x05Article_id\x06\x07\x08Shop_id\x09\x0A\x0BCity_id',
    
    'Objects;': b'\x00\x01\x02Shop_id\x03\x04\x05Article_id\x06\x07\x08Sales_revenue\x09\x0A\x0BQuantity_sold',
    
    'Parameters;': b'\x00\x01\x02Date_from\x03\x04\x05Date_to\x06\x07\x08Region_filter',
    
    'Dimensions;': b'\x00\x01\x02Shop_id\x03\x04\x05Article_id\x06\x07\x08City\x09\x0A\x0BState',
    
    'Contexts;': b'\x00\x01\x02Sales_Context\x03\x04\x05Inventory_Context\x06\x07\x08Customer_Context'
}

# Champs attendus après parsing
EXPECTED_FIELDS = [
    'Shop_id', 'Shop_name', 'Address_1Manager', 'Date_open',
    'Article_id', 'Article_label', 'Category', 'Family_name',
    'Sales_revenue', 'Quantity_sold', 'Margin', 'Promotion_cost',
    'Week_id', 'Year', 'Month', 'Day_of_week',
    'City', 'State', 'Country', 'Region'
]

# Tables attendues
EXPECTED_TABLES = [
    'Shop_facts', 'Calendar_year_lookup', 'Article_lookup', 'Shop_lookup'
]

# Jointures attendues
EXPECTED_JOINS = [
    'Week_id', 'Article_id', 'Shop_id', 'City_id'
]

# Dimensions attendues (basées sur les règles de catégorisation)
EXPECTED_DIMENSIONS = [
    'Shop_id', 'Article_id', 'Shop_name', 'Article_label', 'Category',
    'Family_name', 'Week_id', 'Year', 'Month', 'Day_of_week',
    'City', 'State', 'Country', 'Region', 'Address_1Manager', 'Date_open'
]

# Mesures attendues
EXPECTED_MEASURES = [
    'Sales_revenue', 'Quantity_sold', 'Margin', 'Promotion_cost'
]

# Script Qlik attendu (fragments)
EXPECTED_SCRIPT_FRAGMENTS = [
    'Script Qlik Cloud généré depuis UNV Business Objects',
    'Shop_facts',
    'Calendar_year_lookup',
    'Article_lookup',
    'Shop_lookup',
    'Shop_id',
    'Sales_revenue',
    'Quantity_sold',
    'Week_id',
    'Article_id'
]

# Messages d'erreur attendus
ERROR_MESSAGES = {
    'file_not_found': 'Fichier non trouvé',
    'extraction_failed': 'Échec de l\'extraction',
    'parsing_failed': 'Échec du parsing',
    'generation_failed': 'Échec de la génération'
}

# Configuration des tests de performance
PERFORMANCE_CONFIG = {
    'max_execution_time': 30,  # secondes
    'max_memory_usage': 100,   # MB
    'large_file_size': 10      # MB
}

# Configuration des tests d'intégration
INTEGRATION_CONFIG = {
    'test_real_unv_file': True,
    'generate_output_files': True,
    'validate_output_format': True,
    'cleanup_test_files': True
}

def get_test_data():
    """Retourne les données de test"""
    return TEST_UNV_CONTENT

def get_expected_results():
    """Retourne les résultats attendus"""
    return {
        'fields': EXPECTED_FIELDS,
        'tables': EXPECTED_TABLES,
        'joins': EXPECTED_JOINS,
        'dimensions': EXPECTED_DIMENSIONS,
        'measures': EXPECTED_MEASURES,
        'script_fragments': EXPECTED_SCRIPT_FRAGMENTS
    }

def get_test_config():
    """Retourne la configuration des tests"""
    return TEST_CONFIG

def get_performance_config():
    """Retourne la configuration des tests de performance"""
    return PERFORMANCE_CONFIG

def get_integration_config():
    """Retourne la configuration des tests d'intégration"""
    return INTEGRATION_CONFIG

def validate_test_results(actual_results, expected_results):
    """Valide les résultats des tests"""
    validation_results = {}
    
    for key, expected in expected_results.items():
        if key in actual_results:
            actual = actual_results[key]
            if isinstance(expected, list):
                # Comparaison de listes
                missing = set(expected) - set(actual)
                extra = set(actual) - set(expected)
                validation_results[key] = {
                    'valid': len(missing) == 0 and len(extra) == 0,
                    'missing': list(missing),
                    'extra': list(extra)
                }
            else:
                # Comparaison simple
                validation_results[key] = {
                    'valid': actual == expected,
                    'expected': expected,
                    'actual': actual
                }
        else:
            validation_results[key] = {
                'valid': False,
                'error': f'Clé "{key}" manquante dans les résultats'
            }
    
    return validation_results

def print_validation_report(validation_results):
    """Affiche un rapport de validation"""
    print("\n=== RAPPORT DE VALIDATION ===")
    
    all_valid = True
    for key, result in validation_results.items():
        if result['valid']:
            print(f"✅ {key}: VALIDE")
        else:
            print(f"❌ {key}: INVALIDE")
            if 'missing' in result:
                print(f"   Manquant: {result['missing']}")
            if 'extra' in result:
                print(f"   En trop: {result['extra']}")
            if 'error' in result:
                print(f"   Erreur: {result['error']}")
            all_valid = False
    
    if all_valid:
        print("\n🎉 Tous les tests de validation sont passés !")
    else:
        print("\n⚠️  Certains tests de validation ont échoué.")
    
    return all_valid 