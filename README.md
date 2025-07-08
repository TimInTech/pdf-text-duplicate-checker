
# PDF Text & Image Duplicate Checker

Dieses Tool erkennt Duplikate unter PDF-Dateien auf Basis von:

- **extrahiertem Textinhalt (via PyMuPDF)**
- **visueller Ähnlichkeit (per pHash über gerenderte Seitenbilder)**

---

### 🐍 Voraussetzungen

- Python 3.8 oder höher

---

### 📦 Abhängigkeiten installieren

Installiere die Python-Abhängigkeiten über:

```bash
pip install -r requirements.txt
```

Zusätzlich wird `pdftoppm` aus `poppler-utils` benötigt:

#### Linux:
```bash
sudo apt install poppler-utils
```

#### Windows:
1. Lade Poppler für Windows von [hier](http://blog.alivate.com.au/poppler-windows/) herunter.
2. Entpacke das Archiv, z.B. nach `C:\poppler`.
3. Füge den Pfad zu `C:\poppler\bin` zur Umgebungsvariable `PATH` hinzu:  
   [Anleitung zum Hinzufügen](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/)

---

### ▶️ Nutzung

```bash
python src/pdf_dupe_imghash.py    # erkennt visuelle Duplikate
python src/pdf_dupe_text.py       # erkennt Text-Duplikate
```

Duplikate werden geloggt und (optional) verschoben.

---

### ⚙️ Zielordner für Duplikate anpassen

Standardmäßig werden Duplikate nach  
`~/Schreibtisch/AllePDF/duplikate/`  
verschoben (unter Windows z.B. `C:\Users\<DeinName>\Desktop\AllePDF\duplikate\`).  
Du kannst den Zielordner im jeweiligen Python-Skript (`src/pdf_dupe_text.py` oder `src/pdf_dupe_imghash.py`) anpassen.

---

### 💡 Beispiel (Konsolenausgabe)

```
[2025-07-08 12:00:00] Duplikat gefunden: doc1.pdf == doc2.pdf (Textähnlichkeit: 99%)
[2025-07-08 12:00:01] Duplikat (Bild): doc3.pdf == doc4.pdf (pHash-Abstand: 3)
```

---

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

---

### 📝 Lizenz

MIT License

---


