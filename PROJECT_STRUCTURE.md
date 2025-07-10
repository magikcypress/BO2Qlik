# BO2Qlik Project Structure / Structure du projet BO2Qlik

## Overview / Vue d'ensemble

```
BO2Qlik_Project/
├── 📁 scripts/                      # Main scripts / Scripts principaux
│   ├── universal_converter.py        # Universal converter (.unv & .unx)
│   ├── unx_parser.py                # .unx file parser
│   ├── unv_parser.py                # .unv file parser
│   ├── create_test_unv.py           # Generate a minimal test .unv file / Génère un .unv de test
│   ├── test_universal_converter.py  # Test script
│   └── integration_test.py          # Integration tests
│
├── 📁 data/                         # Source data / Données source
│   ├── eFashion.unv                 # Original UNV file
│   ├── test_universe.unx            # Test UNX file
│   ├── test_universe.unv            # Test UNV file (generated)
│   └── [extracted files]            # Temporary extracted files
│
├── 📁 output/                       # Generated files / Fichiers générés
│   ├── qlik_script_unv.qvs         # Qlik script from .unv
│   ├── qlik_script_unx.qvs         # Qlik script from .unx
│   └── [other generated files]      # Other outputs
│
├── 📁 docs/                         # Documentation / Documentation
│   ├── README.md                    # Main documentation (EN/FR)
│   └── [other docs]                # Additional documentation
│
└── 📁 tests/                        # Test files / Fichiers de test
    └── [test data]                  # Test data and results
```

## Available Scripts / Scripts disponibles

### 1. `universal_converter.py` ⭐ (Recommended / Recommandé)

**Function / Fonction** : Universal converter for both .unv and .unx files
**Fonction** : Convertisseur universel pour les fichiers .unv et .unx

- Automatically detects file format (.unv or .unx)
- Détecte automatiquement le format de fichier (.unv ou .unx)
- Extracts and parses the universe file
- Extrait et analyse le fichier universe
- Generates Qlik Cloud script
- Génère un script Qlik Cloud
- Automatic cleanup after processing
- Nettoyage automatique après traitement

**Usage / Utilisation** :

```bash
python3 universal_converter.py [filename]
```

### 2. `create_test_unv.py`

**Function / Fonction** : Generate a minimal test .unv file for validation
**Fonction** : Génère un fichier .unv de test minimal pour valider le flux

- Creates a valid .unv file with sample metadata
- Crée un fichier .unv valide avec des métadonnées d'exemple
- Useful for testing without a real universe file
- Utile pour tester sans univers réel

**Usage / Utilisation** :

```bash
python3 create_test_unv.py
```

### 3. `unx_parser.py`

**Function / Fonction** : Parser for .unx files (XML-based)
**Fonction** : Parser pour les fichiers .unx (basé sur XML)

- Extracts tables, joins, objects, dimensions, measures
- Extrait les tables, jointures, objets, dimensions, mesures
- Handles XML namespaces
- Gère les espaces de noms XML
- Generates Qlik script from .unx
- Génère un script Qlik à partir du .unx

**Usage / Utilisation** :

```bash
python3 unx_parser.py [filename.unx]
```

### 4. `unv_parser.py`

**Function / Fonction** : Parser for .unv files (binary format)
**Fonction** : Parser pour les fichiers .unv (format binaire)

- Extracts binary data from .unv files
- Extrait les données binaires des fichiers .unv
- Parses metadata and structure
- Analyse les métadonnées et la structure
- Generates Qlik script from .unv
- Génère un script Qlik à partir du .unv

**Usage / Utilisation** :

```bash
python3 unv_parser.py [filename.unv]
```

### 5. `test_universal_converter.py`

**Function / Fonction** : Test script for universal converter
**Fonction** : Script de test pour le convertisseur universel

- Tests both .unv and .unx conversion
- Teste la conversion .unv et .unx
- Validates generated Qlik scripts
- Valide les scripts Qlik générés
- Reports success/failure
- Rapporte succès/échec

**Usage / Utilisation** :

```bash
python3 test_universal_converter.py
```

### 6. `integration_test.py`

**Function / Fonction** : Integration tests
**Fonction** : Tests d'intégration

- Comprehensive testing of all components
- Tests complets de tous les composants
- Validates file processing workflow
- Valide le workflow de traitement des fichiers
- Tests both formats
- Teste les deux formats

**Usage / Utilisation** :

```bash
python3 integration_test.py
```

## Supported Formats / Formats supportés

### .unv Files (Business Objects Universe v4)

- Binary format / Format binaire
- Legacy Business Objects format / Ancien format Business Objects
- Extracted as ZIP archive / Extrait comme archive ZIP
- Contains binary metadata files / Contient des fichiers de métadonnées binaires

### .unx Files (Business Objects Universe v5+)

- XML-based format / Format basé sur XML
- Modern Business Objects format / Format Business Objects moderne
- Extracted as ZIP archive / Extrait comme archive ZIP
- Contains XML metadata files / Contient des fichiers de métadonnées XML

## Generated Files / Fichiers générés

### Qlik Cloud Scripts

- `qlik_script_unv.qvs` : Script from .unv file
- `qlik_script_unx.qvs` : Script from .unx file

### Documentation

- `tables_detected.txt` : List of detected tables
- `fields_detected.txt` : List of detected fields
- `joins_detected.txt` : List of detected joins

## Detected Model (eFashion) / Modèle détecté (eFashion)

### Main Tables / Tables principales

- **Shop_facts** : Facts table (sales) / Table de faits (ventes)
- **Calendar_year_lookup** : Time dimension / Dimension temporelle
- **Article_lookup** : Product dimension / Dimension produits
- **promotion_lookup** : Promotion dimension / Dimension promotions

### Detected Joins / Jointures détectées

- Week_id → Calendar_year_lookup
- Article_id → Article_lookup
- Shop_id → Shop_facts
- Promotion_id → promotion_lookup

### Metrics / Métriques

- **Dimensions** : 29 fields / 29 champs
- **Measures** : 6 fields / 6 champs
- **Tables** : 9 detected tables / 9 tables détectées
- **Joins** : 4 identified relations / 4 relations identifiées

## Recommended Workflow / Workflow recommandé

1. **Preparation / Préparation** :
   - Place your universe file in the data directory
   - Or generate a test file with `python3 create_test_unv.py`
2. **Conversion / Conversion** : Run `python3 universal_converter.py [filename]`
3. **Validation / Validation** : Run `python3 test_universal_converter.py`
4. **Usage / Utilisation** : Open generated .qvs file in Qlik Cloud
5. **Cleanup / Nettoyage** : Automatic cleanup after processing

## Technical Notes / Notes techniques

- **Source format** : UNV/UNX (Business Objects Universe)
- **Target format** : Qlik Cloud (Qlik Sense)
- **Encoding** : UTF-8
- **Delimiter** : Comma (,)
- **Language** : Python 3.6+
- **License** : MIT

## Support / Support

For questions / Pour toute question :

1. Check the main README.md / Consultez le README.md principal
2. Review script logs / Vérifiez les logs des scripts
3. Run test scripts / Lancez les scripts de test
4. Adapt parameters for your environment / Adaptez les paramètres selon votre environnement
