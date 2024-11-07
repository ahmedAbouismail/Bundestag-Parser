from pymongo import MongoClient
from pymongo.operations import UpdateOne

client = MongoClient("mongodb://localhost:27017")
db = client["bundestag"]

def sync(data, collection_name):
    collection = db[collection_name]

    # Liste von Operationen für bulk_write sammeln
    operations = []
    for record in data:
        if isinstance(record, dict):
            # Verwende UpdateOne für ein Upsert (aktualisieren oder einfügen)
            operations.append(
                UpdateOne(
                    {"id": record["id"]},    # Annahme: "id" ist der eindeutige Schlüssel
                    {"$set": record},
                    upsert=True
                )
            )
        else:
            print(f"Ungültiges Format: {record}")

    # Führt bulk_write nur aus, wenn es Operationen gibt
    if operations:
        result = collection.bulk_write(operations)
        # Verwende bulk_api_result, um auf die Details zuzugreifen
        print(f"Upserts: {result.bulk_api_result.get('nUpserted', 0)}, Modifiziert: {result.modified_count}")
    else:
        print("Keine gültigen Datensätze zu verarbeiten.")