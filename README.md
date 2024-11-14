# Bundestag-Parser

## Projektbeschreibung
Der Bundestag-Parser extrahiert und speichert wichtige Informationen aus den Bundestagsprotokollen sowie den Stammdaten der Abgeordneten seit 1949. Die extrahierten Daten werden in MongoDB im BSON-Format gespeichert und sind für die Weiterverarbeitung zugänglich.

## Entwickler-Informationen

### Anforderungen
- **Docker**
- **Docker Compose**
- Zugriff auf die MongoDB-Datenbank (über SSH-Tunnel, siehe unten)

### Workflow

Nach jeder Änderung im Quellcode sind folgende Schritte erforderlich, um den Parser zu aktualisieren und auszuführen:

#### 1. Docker-Image erstellen und pushen
Erstelle das Docker-Image lokal und pushe es, um den Parser mit den neuesten Änderungen zu aktualisieren:

```bash
.\build.bat
```

#### 2. Docker-Container mit Docker Compose starten
Starte den Container im Hintergrund:

```bash
docker compose up -d
```

Der Container verarbeitet nun automatisch die Bundestagsprotokolle und Stammdaten und lädt die Daten in die MongoDB.

## Benutzer-Informationen

### Täglicher Datenabruf
Jeden Tag um 18:30 Uhr ruft unser Parser automatisch die neuesten Bundestagsprotokolle, Stammdaten und Abstimmungsdaten vom [Crawler Team1](https://gitlab.com/bachelor8684930/bundestagcrawler) ab. Nach dem Abruf beginnt der Parser sofort mit der Extraktion und Speicherung der relevanten Informationen.

### Datenzugriff

Um auf die extrahierten Daten zuzugreifen, stellen Sie bitte eine Verbindung zur MongoDB-Datenbank her. Verwenden Sie dazu folgende Zugangsdaten:

- **Host**: `localhost` (Zugriff über SSH-Tunnel)
- **Port**: `27017`
- **Datenbankname**: `bundestag`

Da die Datenbank nur lokal auf dem Server verfügbar ist, benötigen Sie eine Verbindung über das **HTW-Netzwerk oder VPN** und einen **SSH-Tunnel** zur sicheren und verschlüsselten Kommunikation.

#### Verbindung mit SSH-Tunnel herstellen

Richten Sie den SSH-Tunnel in der Kommandozeile wie folgt ein:

```
ssh -L 27017:localhost:27017 local@infosys1.f4.htw-berlin.de
```

- **infosys1.f4.htw-berlin.de**: Die Serveradresse, auf der MongoDB läuft.
- **`-L 27017:localhost:27017`**: Leitet den lokalen Port 27017 auf Port 27017 des Servers weiter.

Solange die SSH-Verbindung aktiv ist, können Sie auf die MongoDB-Datenbank zugreifen, indem Sie `localhost` als Host und `27017` als Port verwenden. Der SSH-Tunnel stellt sicher, dass alle Verbindungen verschlüsselt und sicher übertragen werden. Damit bleibt die Datenbank vor direktem Zugriff aus dem Internet geschützt. Das Passwort für den `local`-User gibt es auf Anfrage per Discord.

### Datenbankstruktur

Die Datenbank `bundestag` enthält drei Hauptkollektionen:

- **Protokolle**: `protokolle`
- **Stammdaten der Abgeordneten**: `mdb_stammdaten`

### Beispielcode für den Datenzugriff (Python)

```python
from pymongo import MongoClient

# Verbindung zur MongoDB
client = MongoClient("mongodb://reader:mongoDB_bundestag-projekt@localhost:27017/bundestag")
db = client["bundestag"]

# Daten aus den Kollektionen abfragen
protokolle = db["protokolle"].find({})
abgeordnete = db["mdb_stammdaten"].find({})
```

### Datenstruktur

#### Bundestagsprotokolle

Die JSON-Struktur der Bundestagsprotokolle sieht wie folgt aus:

```json
{
  "id": 1,
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

Die JSON-Struktur der Stammdaten der Abgeordneten:

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

## Autoren

- Ala Al-Khazzan
- Ahmed Abouismail
- Marc Zimmermann

**Projektteam 2 - Bundestag-Parser, HTW Berlin**

## ToDo / Hinweise

- SSH Tunnel entfernen
- Eventuell noch zu machen, je nach Bedarf
  - Unterscheidung zwischen Haupt- und Nebenredner
  - Kommentare eventuell einbauen

