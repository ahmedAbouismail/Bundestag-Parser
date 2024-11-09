# Parser #

## Parser normal starten ###

Eigenes Volume in Docker erstellen mit zb. dem Namen crawler_data: 

--> Für Instant
```
docker run --name bt_crawler_instant -v crawler_data:/data lajahom/bundestag-crawler:instant
```

oder

--> Für Cron
```
docker run --name bt_crawler_cron -v crawler_data:/data lajahom/bundestag-crawler:cron
```

Anschließend im Projekt-Verzeichnis navigieren und image builden zb. bt_extraction_cron:

```
docker build -t bt_extraction_cron .
```

und dann docker starten

```
docker run --name bt_extraction_cron -v crawler_data:/data bt_extraction_cron
```

## Parser über compose starten ###
```
docker-compose up -d


### ToDo/Notes

- Abstimmungsdaten fehlen
