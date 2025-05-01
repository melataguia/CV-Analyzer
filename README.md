# CV Analyzer Backend

Ce projet propose une API Flask permettant de parser des CV (PDF, DOCX) et d’en extraire le texte brut pour traitement NLP via DeepSeek. Un front-end Blazor (optionnel) peut être couplé pour une interface utilisateur.

---

## Prérequis

- **Python** 3.8+  
- **.NET SDK** (optionnel, pour le front-end Blazor)  
- **Tesseract OCR** (pour l’OCR des CV scannés)  

---

## Installation et configuration

1. **Cloner le dépôt**  
   ```bash
   git clone https://votre-repo/CV-Analyzer.git
   cd CV-Analyzer


### Créer et activer un environnement virtuel
# Windows
python -m venv ia_cv
ia_cv\Scripts\activate

#macOS / Linux
python3 -m venv ia_cv
source ia_cv/bin/activate

### Installer les dépendances Python

pip install -r requirements.txt
pip install pdfplumber python-docx pdf2image unidecode groq flask-cors pytesseract

### Installer Tesseract OCR

# macOS
brew install tesseract
brew install tesseract-lang

# Linux (Debian/Ubuntu)
sudo apt update
sudo apt install tesseract-ocr

# Windows
Téléchargez et installez depuis :
https://github.com/tesseract-ocr/tesseract/releases

### (Optionnel) Installer le front-end Blazor

cd frontend-dotnet
dotnet new blazorwasm -n frontend-dotnet
dotnet restore
cd ..

### Lancement de l’application

# Démarrer le serveur Flask
python app/main.py

# Tester l’API
python test_api.py

### Structure du projet

CV-Analyzer/
├── app/
│   ├── main.py         # Point d’entrée Flask
│   └── ...             # Routes & utilitaires
├── tests/
│   └── test_api.py     # Scripts de test de l’API
├── frontend-dotnet/    # (Optionnel) Front-end Blazor
├── requirements.txt    # Liste des dépendances Python
└── README.md           # Ce fichier

