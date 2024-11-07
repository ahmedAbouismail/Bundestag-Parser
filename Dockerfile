# Basis-Image
FROM python:3.9

# Arbeitsverzeichnis setzen
WORKDIR /app

# Kopiere deine Python-Dateien in das Docker-Image
COPY . /app

# Abhängigkeiten installieren
RUN pip install pymongo

# Cron installieren
RUN apt-get update && apt-get install -y cron

# Cronjob hinzufügen
RUN echo "* * * * * /usr/bin/python3 /app/source/main.py >> /var/log/cron.log 2>&1" > /etc/cron.d/mycron

# Die Cron-Job-Datei ausführbar machen
RUN chmod 0644 /etc/cron.d/mycron

# Den Cron-Dienst in den richtigen Pfad hinzufügen
RUN crontab /etc/cron.d/mycron

# Logdatei erstellen
RUN touch /var/log/cron.log

# Cron im Vordergrund laufen lassen
CMD cron && tail -f /var/log/cron.log
