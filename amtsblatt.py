# Pakete importieren
import pypdf
import re
import http.client
import urllib
import wget
import datetime
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
date = datetime.datetime.now() + datetime.timedelta(days=-4)
url = "https://abl.fr.ch/system/files/issues/pdfs/FO_" + date.strftime("%G") + "-" + date.strftime("%W") + ".pdf"
title = f"Amtsblatt Ausgabe " + date.strftime("%W") + " - " + date.strftime("%G")
message = f"Suche nach «{search}» in \n{url}\n\n"
send = False

# Funktion um Pushovernachricht zu senden
def send_pushover(title, message):
    conn = http.client.HTTPSConnection("api.pushover.net", 443)
    conn.request("POST", "/1/messages.json", urllib.parse.urlencode({"token": po_token,"user": po_user,"message": message,"title": title})
        , { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()

# PDF Datei herunterladen
try:
    pdffile = wget.download(url)
    print("")
except:
    send_pushover(title, f"Download von {url} ist fehlgeschlagen.")
    raise

# PDF Datei öffnen
try:
    reader = pypdf.PdfReader(pdffile)
except:
    send_pushover(title, f"Verarbeitung der PDF Datei {url} ist fehlgeschlagen.")
    os.remove(pdffile)
    raise

# Anzahl Seiten der PDF Datei ermitteln
num_pages = len(reader.pages)

# Suchbegriff nach Kommas trennen
splitsearch = [split.strip() for split in search.split(',')]

# Suche durchführen (Seite für Seite, Suchbegriff für Suchbegriff)
for pindex, page in enumerate(reader.pages):
    text = page.extract_text() 
    for svalue in splitsearch:
        res_search = re.search(svalue, text)
        if (match := res_search) is not None:
            message = f"{message}Eintrag «{svalue}» gefunden auf Seite {pindex+1}\n" 
            send = True

# PDF Datei löschen
os.remove(pdffile)

# Pushover Nachricht senden
if send:
    send_pushover(title, message)
else:
    send_pushover(title,f"{message}Keine Einträge gefunden.")
