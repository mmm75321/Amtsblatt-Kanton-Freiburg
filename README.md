Benötigt Pushover von www.pushover.net für Benachrichtigungen (Apps für iPhone und Android).<br />
Kann dank Python 3 fast überall laufen.<br />
amtsblatt.py herunterladen.<br />
In amtsblatt.py die Variablen definieren (vorab Applikation in Pushover erstellen).<br />
```python
# Pushover Variablen: User und Token eintragen
po_user = "***"
po_token = "***"

# Suchbegriff eintragen, idealerweise Postleitzahl
# Mehrere Begriffe mit Komma trennen
# Keine Leerschläge
search = "3280"
```
Ausführen mittels python3 amtsblatt.py.<br />
Idealerweise werden ein Raspberry Pi und ein Cronjob verwendet. Zum Beispiel (läuft jeden Freitag um 12:00 Uhr):<br />
```console
0 12 * * 5 <benutzer name> /usr/bin/python3 /<pfad zur datei>/amtsblatt.py
```
Code ist frei verfügbar und ohne Gewähr, mach damit was du willst :)
