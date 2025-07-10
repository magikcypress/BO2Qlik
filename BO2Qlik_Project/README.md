# BO2Qlik - Universal Business Objects Universe to Qlik Cloud Script Converter

## 🇬🇧 English

**BO2Qlik** is a universal converter that extracts metadata from SAP Business Objects Universe files (`.unv` and `.unx`) and generates a ready-to-use Qlik Cloud script. It supports both legacy (`.unv`) and new generation (`.unx`) universes.

### ⚠️ Important Disclaimer

**This project is for educational and demonstration purposes only.**

- **NOT FOR PRODUCTION USE** - This tool is designed as a learning example
- **DEVELOPMENT ENVIRONMENT REQUIRED** - You need a SAP Business Objects development environment to work with these scripts
- **METADATA MIGRATION TOOL** - This is a metadata extraction and conversion tool from BO to Qlik
- **NO DATA TRANSFER** - Only metadata (tables, joins, objects) is extracted, not actual data
- **PROOF OF CONCEPT** - Demonstrates the concept of migrating Business Objects universes to Qlik Cloud

### Features

- Automatic detection and parsing of `.unv` and `.unx` files
- Extraction of tables, joins, dimensions, measures, and attributes
- Generation of a Qlik Cloud script with connection template and data model
- Automated tests for both formats
- **Test file generator**: Easily create a minimal `.unv` test file with `create_test_unv.py`

### Project Structure

```
BO2Qlik_Project/
  scripts/         # All Python scripts (converters, tests, generators)
  data/            # Place your .unv or .unx files here
  output/          # Generated Qlik scripts (.qvs)
  docs/            # Documentation (optional)
```

### Installation

- Python 3.7+
- No external dependencies (uses standard library)

### Usage

1. Place your `.unv` or `.unx` file in the `data/` folder.
2. Run the universal converter:
   ```bash
   cd BO2Qlik_Project/scripts
   python3 universal_converter.py
   ```
3. The generated Qlik script will be in the `output/` folder.

### Generate a Test UNV File

If you don't have a real `.unv` file, you can generate a minimal test file:

```bash
python3 create_test_unv.py
```

This will create `test_universe.unv` in the `data/` folder, ready for testing.

### Automated Tests

To validate both `.unv` and `.unx` support (including the generated test file):

```bash
python3 test_universal_converter.py
```

---

## 🇫🇷 Français

**BO2Qlik** est un convertisseur universel qui extrait les métadonnées des univers SAP Business Objects (`.unv` et `.unx`) et génère un script Qlik Cloud prêt à l'emploi. Il prend en charge les univers anciens (`.unv`) et nouvelle génération (`.unx`).

### ⚠️ Avertissement Important

**Ce projet est uniquement à des fins éducatives et de démonstration.**

- **PAS POUR UNE UTILISATION EN PRODUCTION** - Cet outil est conçu comme un exemple d'apprentissage
- **ENVIRONNEMENT DE DÉVELOPPEMENT REQUIS** - Vous avez besoin d'un environnement SAP Business Objects de développement pour travailler avec ces scripts
- **OUTIL DE MIGRATION DE MÉTADONNÉES** - C'est un outil d'extraction et de conversion de métadonnées de BO vers Qlik
- **AUCUN TRANSFERT DE DONNÉES** - Seules les métadonnées (tables, jointures, objets) sont extraites, pas les données réelles
- **PREUVE DE CONCEPT** - Démontre le concept de migration d'univers Business Objects vers Qlik Cloud

### Fonctionnalités

- Détection et parsing automatique des fichiers `.unv` et `.unx`
- Extraction des tables, jointures, dimensions, mesures et attributs
- Génération d'un script Qlik Cloud avec modèle de connexion et modèle de données
- Tests automatisés pour les deux formats
- **Générateur de fichier de test** : Créez facilement un fichier `.unv` minimal avec `create_test_unv.py`

### Structure du projet

```
BO2Qlik_Project/
  scripts/         # Tous les scripts Python (convertisseurs, tests, générateurs)
  data/            # Placez vos fichiers .unv ou .unx ici
  output/          # Scripts Qlik générés (.qvs)
  docs/            # Documentation (optionnel)
```

### Installation

- Python 3.7+
- Pas de dépendances externes (bibliothèque standard uniquement)

### Utilisation

1. Placez votre fichier `.unv` ou `.unx` dans le dossier `data/`.
2. Lancez le convertisseur universel :
   ```bash
   cd BO2Qlik_Project/scripts
   python3 universal_converter.py
   ```
3. Le script Qlik généré sera dans le dossier `output/`.

### Générer un fichier UNV de test

Si vous n'avez pas de fichier `.unv` réel, vous pouvez générer un fichier de test minimal :

```bash
python3 create_test_unv.py
```

Cela créera `test_universe.unv` dans le dossier `data/`, prêt pour les tests.

### Tests automatisés

Pour valider la prise en charge des deux formats (y compris le fichier de test généré) :

```bash
python3 test_universal_converter.py
```

---

**License:** MIT
