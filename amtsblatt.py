# import packages
import pypdf
import re
import http.client
import urllib
import wget
import datetime

#pushover variables
po_user = "***"
po_token = "***"

#search for string, ideally postal code
search = "3280"

#end of sections which needs to be modified
#other variables
date = datetime.datetime.now() + datetime.timedelta(days=-4)
url = "https://abl.fr.ch/system/files/issues/pdfs/FO_" + date.strftime("%G") + "-" + date.strftime("%W") + ".pdf"
title = f"Amtsblatt Ausgabe " + date.strftime("%W") + " - " + date.strftime("%G")
message = f"{url}\n"
send = False

def send_pushover(title, message):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json", urllib.parse.urlencode({"token": po_token,"user": po_user,"message": message,"title": title})
        , { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()

try:
    pdffile = wget.download(url)
except:
    send_pushover(title, f"Download von {url} fehlgeschlagen.")

# open the pdf file
reader = pypdf.PdfReader(pdffile)

# get number of pages
num_pages = len(reader.pages)

# extract text and do the search
for index, page in enumerate(reader.pages):
    text = page.extract_text()
    res_search = re.search(search, text)
    if (match := res_search) is not None:
        message = f"{message} Eintrag gefunden auf Seite {index+1}\n"
        send = True

if send:
    send_pushover(title, message)
else:
    send_pushover(title,f"Wert {search} in {url} nicht gefunden.")
