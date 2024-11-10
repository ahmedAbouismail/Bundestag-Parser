# Bundestag-Parser

## Projektbeschreibung
Der Bundestag-Parser extrahiert und speichert alle wichtigen Informationen aus den Bundestagsprotokollen und den Stammdaten der Abgeordneten seit 1949. Die extrahierten Daten werden in MongoDB im BSON-Format gespeichert und sind für die Weiterverarbeitung zugänglich.

## Entwickler-Informationen
### Anforderungen

- **Docker**
- **Docker Compose**
- Zugang zur MongoDB-Datenbank

### Workflow

Nach jeder Änderung im Quellcode sind folgende Schritte erforderlich, um den Parser zu aktualisieren und auszuführen:

#### 1. Docker-Image erstellen und pushen
Bau das Docker-Image lokal und push es, um den Parser mit den neuesten Änderungen zu aktualisieren.

```bash
.\build.bat
```

#### 2. Docker-Container mit Docker Compose erstellen
Starten Sie einen Container für den Parser im Hintergrund. (VM)

```bash
docker compose up -d
```

Der Container wird nun mit den neuesten Änderungen ausgeführt und beginnt, die Bundestagsprotokolle und Stammdaten zu verarbeiten und in die MongoDB zu laden.

## Nutzeranweisungen

### Täglicher Datenabruf
Jeden Tag um 18:30 Uhr holt unser Parser automatisch die neuen Bundestagsprotokolle, Stammdaten und Abstimmungsdaten vom [Crawler Team1](https://gitlab.com/bachelor8684930/bundestagcrawler). Nach dem Abruf beginnt der Parser sofort mit der Extraktion der relevanten Informationen aus den Protokollen und den Stammdaten der Abgeordneten.

### Datenzugriff
Um auf die extrahierten Daten zuzugreifen, stellen Sie bitte eine Verbindung zur MongoDB-Datenbank her. Verwenden Sie dazu folgende Zugangsdaten:
- **Host**: `infosys1.f4.htw-berlin.de:27017`
  (Der Zugriff ist nur aus dem HTW-Netzwerk oder über VPN möglich.)
- **Datenbankname**: `bundestag`

Die Datenbank enthält drei Hauptkollektionen:
- **Protokolle**: `protokolle`
- **Stammdaten der Abgeordneten**: `mdb_stammdaten`
- **Namentliche Abstimmungen**: `namentliche_abstimmungen` (coming soon)

### Beispielcode für den Datenzugriff (Python)
```python
from pymongo import MongoClient

# Verbindung zur MongoDB
client = MongoClient("mongodb://infosys1.f4.htw-berlin.de:27017")
db = client["bundestag"]

# Daten aus den Kollektionen abfragen
protokolle = db["protokolle"].find({})
abgeordnete = db["mdb_stammdaten"].find({})
abstimmungen = db["namentliche_abstimmungen"].find({})
```

### Datenstruktur

#### Bundestagsprotokolle
Die JSON-Struktur der Bundestagsprotokolle ist wie folgt aufgebaut:
```json
{
  "id": 0001,
  "datum": "string",
  "wahlperiode": "string",
  "sitzungsnummer": "string",
  "sitzungsverlauf": [
    {
      "rede": [
        {
          "redner_id": "string",
          "text": "string"
        }
      ]
    }
  ]
}
```

#### Stammdaten der Abgeordneten
Die JSON-Struktur der Stammdaten der Abgeordneten sieht so aus:
```json
{
  "id": "string",
  "biographie": {
    "geburtsdatum": "string",
    "sterbedatum": "string",
    "geschlecht": "string",
    "familienstand": "string",
    "beruf": "string",
    "lebenslauf": "string"
  },
  "fraktion": "string",
  "nachname": "string",
  "titel": "string",
  "vorname": "string",
  "wahlperiode": [
    {
      "wahlperiode": "string",
      "von": "string",
      "bis": "string",
      "institutionen": [
        {
          "institutionsart": "string",
          "institutionsname": "string",
          "mdb_von": "string",
          "mdb_bis": "string",
          "funktion": "string",
          "funktion_von": "string",
          "funktion_bis": "string"
        }
      ]
    }
  ]
}

```
## Autoren ##
Ala Al-Khazzan, Ahmed Abouismail, Marc Zimmermann<br>
Projektteam 2 - Bundestag-Parser, HTW Berlin

## ToDo/Notes

- Abstimmungsdaten fehlen
- XML für Stammdaten fehlt (Team 1)
