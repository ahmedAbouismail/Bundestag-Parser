# Parser #


## Wie startet  man den Parser ###
Entweder in VS Code manuell starten oder über die CLI
```
python main.py
```

Oder über Docker (eher für den späteren verlauf)
```
docker compose -f docker-compose.yml up -d
```

### Wie startet man den Crawler bzw. holt man sich die Datein ###
Hier werden die Daten aus dem shared Volume erstmal lokal im Projekt kopiert um damit weiter zu arbeiten.

README von https://gitlab.com/bachelor8684930/bundestagcrawler anschauen:

Teil vom Crawler
```
git clone https://gitlab.com/bachelor8684930/bundestagcrawler.git
```
```
docker compose -f docker-compose.yml up -d
```

Teil vom Parser:
``` 
docker cp bundestag-crawler:/data ./data 
```

- Falls der obere Befehl erneut ausgeführt wird (Um die aktuellsten Protokolle zu erhalten), dann wird erneut ein unterordner erstellt daher bei Bedarf vorher den Ordner löschen: ``` rm -r ./data```


Die "Testergebnisse" werden nach ``` python main.py ```  unter data/documents lokal gespeichert und dann auch in den shared Volume kopiert. 

``` 
docker cp data/documents  bundestag-crawler:/data 
```


### ToDo/Notes

- Schema für die extraktion bzw. welche Teile geparst werden sollen

- MongoDB in VM? Gerade ist es noch lokal bzw auf Cluster in der cloud

- Alles was bei uns mit Docker zu tun hat, ist wahrscheinlich nur für den späteren verlauf wichtig ``` docker compose -f docker-compose.yml up -d ```