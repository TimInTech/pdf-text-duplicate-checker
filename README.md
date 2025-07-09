# PDF Text & Image Duplicate Checker

Dieses Tool analysiert PDF-Dateien anhand ihres **Textinhalts** und/oder ihrer **Bilder** (pHash-Vergleich) und erkennt Duplikate.

### 🔍 Funktionen

- **Textbasierter Vergleich:** via PyMuPDF (Textextraktion + SHA256)
- **Bildbasierter Vergleich:** via `pdftoppm` + perceptual hash (pHash)
- **Automatisches Verschieben** von Duplikaten in den Unterordner `duplikate/`
- Überspringt defekte oder passwortgeschützte Dateien

---

### 📁 Verzeichnisstruktur

```plaintext
pdf-text-duplicate-checker/
├── .venv/                     # Virtuelle Umgebung
├── src/
│   ├── pdf_text_duplicate_checker.py   # Textbasierter Vergleich
│   ├── pdf_dupe_imghash.py             # Bildbasierter Vergleich (mit Verschieben)
│   └── ...
├── duplikate/                 # Zielordner für gefundene Duplikate
├── requirements.txt           # Python-Abhängigkeiten
├── README.md                  # Diese Datei
```

---

### 🚀 Verwendung

1. **Voraussetzungen**

```bash
sudo apt install poppler-utils python3-venv
```

2. **Projekt initialisieren**

```bash
cd ~/code/pdf-text-duplicate-checker
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. **PDFs vorbereiten**

Lege alle PDFs in folgenden Ordner:

```bash
/home/gummi/Schreibtisch/AllePDF/
```

4. **Duplikate per Bildvergleich erkennen & verschieben**

```bash
python src/pdf_dupe_imghash.py
```

5. **Optional: Nur textbasierter Vergleich (ohne Verschieben)**

```bash
python src/pdf_text_duplicate_checker.py
```

---

### 📦 Abhängigkeiten (`requirements.txt`)

```txt
pillow
imagehash
PyMuPDF
```

---

## 🔐 Hinweis

**Es wird keine Datei gelöscht.**  
Alle erkannten Duplikate werden **nur verschoben** in:  
`/home/gummi/Schreibtisch/AllePDF/duplikate/`
