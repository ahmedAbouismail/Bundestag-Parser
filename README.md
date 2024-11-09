# Bundestag-Parser

## Projektbeschreibung
Der Bundestag-Parser extrahiert und speichert alle wichtigen Informationen aus den Bundestagsprotokollen und den Stammdaten der Abgeordneten seit 1949. Die extrahierten Daten werden in MongoDB im BSON-Format gespeichert und sind für die Weiterverarbeitung zugänglich.

- **Datenbank**: MongoDB
- **Host**: infosys1.f4.htw-berlin.de:27017
- **Datenformat**: BSON

## Anforderungen

- **Docker**
- **Docker Compose**
- Zugang zur MongoDB-Datenbank

## Workflow

Nach jeder Änderung im Quellcode sind folgende Schritte erforderlich, um den Parser zu aktualisieren und auszuführen:

### 1. Docker-Image erstellen und pushen
Bau das Docker-Image lokal und push es, um den Parser mit den neuesten Änderungen zu aktualisieren.

```bash
.\build.bat
```

### 3. Docker-Container mit Docker Compose erstellen
Starten Sie einen Container für den Parser im Hintergrund. (VM)

```bash
docker compose up -d
```

Der Container wird nun mit den neuesten Änderungen ausgeführt und beginnt, die Bundestagsprotokolle und Stammdaten zu verarbeiten und in die MongoDB zu laden.

## Autoren ##
Ala Al-Khazzan, Ahmed Abouismail, Marc Zimmermann
Projektteam 2 - Bundestag-Parser, HTW Berlin

### ToDo/Notes

- Abstimmungsdaten fehlen
