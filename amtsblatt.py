# Pakete importieren
import pypdf
import re
import http.client
import urllib
import wget
from datetime import datetime, timedelta
import os

# Pushover Variablen: User und Token eintragen
po_user = "***"
po_token = "***"

# Suchbegriff eintragen, idealerweise Postleitzahl
# Mehrere Begriffe mit Komma trennen
# Keine Leerschläge
search = "3280"

# Änderungen unterhalb von hier nicht notwendig
# Weitere Variablen (zur Laufzeit gesetzt)
heute = datetime.today()
offset = (heute.weekday() + 3) % 7
datum = heute - timedelta(days=offset)
jahr = str(datum.year)
ausgabe = f"0{str(round(datum.timetuple().tm_yday/7+0.5))}"[-2:]
url = f"https://abl.fr.ch/system/files/issues/pdfs/FO_{jahr}-{ausgabe}.pdf"
titel = f"Amtsblatt Ausgabe {ausgabe} - {jahr}"
message = f"Suche nach «{search}» in \n{url}\n\n"
send = False

# Funktion um Pushovernachricht zu senden
def send_pushover(titel, message):
    conn = http.client.HTTPSConnection("api.pushover.net", 443)
    conn.request("POST", "/1/messages.json", urllib.parse.urlencode({"token": po_token,"user": po_user,"message": message,"title": titel})
        , { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()

# PDF Datei herunterladen
try:
    pdffile = wget.download(url)
    print("")
except Exception as e:
    send_pushover(titel, f"Download von {url} ist fehlgeschlagen. Fehlermeldung: {e}")
    raise

# PDF Datei öffnen
try:
    reader = pypdf.PdfReader(pdffile)
except Exception as e:
    send_pushover(titel, f"Verarbeitung der PDF Datei {url} ist fehlgeschlagen. Fehlermeldung: {e}")
    os.remove(pdffile)
    raise

# Suchbegriff nach Kommas trennen
search_terms = [split.strip() for split in search.split(',')]

# Suche durchführen (Seite für Seite, Suchbegriff für Suchbegriff)
for pindex, page in enumerate(reader.pages):
    text = page.extract_text() 
    for term in search_terms:
        res_search = re.search(rf"\b{term}\b", text)
        if (match := res_search) is not None:
            message += f"Eintrag «{term}» gefunden auf Seite {pindex+1}\n" 
            send = True

# PDF Datei löschen
os.remove(pdffile)

# Pushover Nachricht senden
if not send:
    message += f"Keine Einträge gefunden."

send_pushover(titel, message)
