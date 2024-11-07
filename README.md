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

### Was ich probiert habe (Marc)

- Ich habe diese Befehle ausgeführt:

docker build -t bt_extraction .

docker run -d --name bt_extraction_cron -v /var/lib/docker/volumes/def2c69a52761734a603e6be7d22bd4a493b82e011a9f7a8fe7935528f0197b5/_data:/app/data bt_extraction

aber das Problem was ich euch beschrieben habe bekommen.

/var/lib/docker/volumes/def2c69a52761734a603e6be7d22bd4a493b82e011a9f7a8fe7935528f0197b5/_data ist der Pfad von dem Volume von dem Crawler.
den bekommt ihr so: volume inspect name_von dem_volume