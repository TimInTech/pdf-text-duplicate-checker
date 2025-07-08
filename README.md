
# PDF Text & Image Duplicate Checker

Dieses Tool erkennt Duplikate unter PDF-Dateien auf Basis von:

- **extrahiertem Textinhalt (via PyMuPDF)**
- **visueller Ähnlichkeit (per pHash über gerenderte Seitenbilder)**

### 📦 Abhängigkeiten

Installiere die Python-Abhängigkeiten über:

```bash
pip install -r requirements.txt
````

Zusätzlich wird `pdftoppm` aus `poppler-utils` benötigt:

```bash
sudo apt install poppler-utils
```

### ▶️ Nutzung

```bash
python src/pdf_dupe_imghash.py    # erkennt visuelle Duplikate
python src/pdf_dupe_text.py       # erkennt Text-Duplikate
```

Duplikate werden geloggt und (optional) verschoben nach:

```
~/Schreibtisch/AllePDF/duplikate/
```

### 📂 Verzeichnisstruktur

```
pdf-text-duplicate-checker/
├── src/
│   ├── pdf_dupe_text.py
│   └── pdf_dupe_imghash.py
├── requirements.txt
├── README.md
└── .gitignore
```

