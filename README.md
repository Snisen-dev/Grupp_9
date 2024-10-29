# Grupp_9
Perfekt att problemet med .gitignore är löst! Låt oss gå igenom de första stegen för att sätta upp projektet för ert bokningssystem med Flask eller FastAPI och SQLite som databas. Här är en steg-för-steg-plan för att hjälpa er att komma igång.

Projektöversikt och uppdelning
Eftersom ni bygger ett bokningssystem som hanterar rum och tider, kommer vi att börja med att:

Sätta upp projektstrukturen.
Skapa den virtuella miljön och installera nödvändiga paket.
Sätta upp en databas med SQLite.
Skapa grundläggande API-endpoints för att hantera bokningar.
Steg 1: Sätta upp projektstruktur
Börja med att organisera projektet i en struktur som gör det lätt att hantera filer och hålla koden ren.

Exempel på mappstruktur:
bash
Kopiera kod
projektmapp/
│
├── app.py               # Huvudfil för API:et
├── database.py          # Databasinställningar och -anslutning
├── models.py            # (Valfritt) Datamodeller om ni strukturerar större projekt
├── venv/                # Virtuell miljö
├── requirements.txt     # Lista över beroenden
└── .gitignore           # Git ignore-fil
Steg 2: Skapa den virtuella miljön och installera paket
Skapa en virtuell miljö:

bash
Kopiera kod
python -m venv venv
Aktivera miljön:

Git Bash: source venv/Scripts/activate
PowerShell: .\venv\Scripts\Activate
Installera Flask eller FastAPI beroende på vad ni har valt:

För Flask:
bash
Kopiera kod
pip install flask
För FastAPI och Uvicorn (ASGI-server):
bash
Kopiera kod
pip install fastapi uvicorn
Skapa en requirements.txt-fil för att spara beroenden:

bash
Kopiera kod
pip freeze > requirements.txt