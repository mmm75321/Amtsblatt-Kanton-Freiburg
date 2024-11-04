# import packages
import pypdf
import re
import http.client
import urllib
import wget
import datetime


date = datetime.datetime.now()
date = date + datetime.timedelta(days=-4)
url = "https://abl.fr.ch/system/files/issues/pdfs/FO_" + date.strftime("%G") + "-" + date.strftime("%W") + ".pdf"

try:
    pdffile = wget.download(url)
except:
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json", urllib.parse.urlencode({"token": "***","user": "***","message": "Download failed!",}), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()

# open the pdf file
reader = pypdf.PdfReader(pdffile)

# get number of pages
num_pages = len(reader.pages)

# define key terms
string = "3280"
title = f"Amtsblatt Ausgabe " + date.strftime("%W") + " - " + date.strftime("%G")
message = f"{url}\n"
send = False

# extract text and do the search
for index, page in enumerate(reader.pages):
    text = page.extract_text() 
    # print(text)
    res_search = re.search(string, text)
    if (match := res_search) is not None:
        message = f"{message} Eintrag gefunden auf Seite {index+1}\n" 
        send = True

if send:
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json", urllib.parse.urlencode({"token": "***","user": "***","message": message,"title": title,}), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()
