# Basis-Image
FROM python:3.9-slim

# Arbeitsverzeichnis setzen
WORKDIR /app

# Kopiere deine Python-Dateien in das Docker-Image
COPY . /app

# Abhängigkeiten installieren
RUN pip install --no-cache-dir -r requirements.txt

# Cron installieren
RUN apt-get update && apt-get install -y cron

# Cronjob hinzufügen
RUN echo "30 18 * * * /usr/local/bin/python3 /app/source/main.py >> /var/log/cron.log 2>&1" > /etc/cron.d/mycron

# Die Cron-Job-Datei ausführbar machen
RUN chmod 0644 /etc/cron.d/mycron

# Den Cron-Dienst in den richtigen Pfad hinzufügen
RUN crontab /etc/cron.d/mycron

# Logdatei erstellen
RUN touch /var/log/cron.log

# Exponiere Port 27017 (für MongoDB)
EXPOSE 27017

# Cron im Vordergrund laufen lassen
CMD cron && tail -f /var/log/cron.log
