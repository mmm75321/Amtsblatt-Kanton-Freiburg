Benötigt Pushover von www.pushover.net für Benachrichtigung (Apps für iPhone und Android).<br />
Kann dank Python3 fast überall laufen.<br />
amtsblatt.py herunterladen.<br />
In amtsblatt.py die Variablen definieren (vorab Applikation in Pushover erstellen).<br />
```python
#pushover variables
po_user = "***"
po_token = "***"

#search for string, ideally postal code
search = "3280"
```
Ausführen mittels pyhton3 amtsblatt.py.<br />
Idealerweise wird ein Raspberry Pi und ein Cronjob verwendet. Zum Beispiel (läuft jeden Freitag um 12:00 Uhr):<br />
```console
0 12 * * 5 root  /usr/bin/python3 /<pfad zur datei>/amtsblatt.py
```
Code ist frei verfügbar und ohne Gewähr, mach damit was du willst :)
