from pymongo import MongoClient, errors
from pymongo.operations import UpdateOne

try:
    # client = MongoClient("mongodb://localhost:27017/")
    client = MongoClient("mongodb://infosys1.f4.htw-berlin.de:27017")
    db = client["bundestag"]
except errors.ConnectionFailure as e:
    print(f"Verbindungsfehler: {e}")
except errors.PyMongoError as e:
    print(f"MongoDB-Fehler: {e}")
except Exception as e:
    print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")


def sync(data, collection_name):
    try:
        collection = db[collection_name]

        # Liste von Operationen für bulk_write sammeln
        operations = []
        for record in data:
            if isinstance(record, dict):
                # Verwende UpdateOne für ein Upsert (aktualisieren oder einfügen)
                operations.append(
                    UpdateOne(
                        {"id": record["id"]},  # Annahme: "id" ist der eindeutige Schlüssel
                        {"$set": record},
                        upsert=True
                    )
                )
            else:
                print(f"Ungültiges Format: {record}")

        # Führt bulk_write nur aus, wenn es Operationen gibt
        if operations:
            try:
                result = collection.bulk_write(operations)
                # Verwende bulk_api_result, um auf die Details zuzugreifen
                print(f"Upserts: {result.bulk_api_result.get('nUpserted', 0)}, Modifiziert: {result.modified_count}")
            except errors.BulkWriteError as bwe:
                print(f"Fehler bei Massenoperation: {bwe.details}")
            except errors.PyMongoError as e:
                print(f"MongoDB-Fehler während der Massenoperation: {e}")
            except Exception as e:
                print(f"Ein unerwarteter Fehler ist während der Massenoperation aufgetreten: {e}")

        else:
            print("Keine gültigen Datensätze zu verarbeiten.")

    except errors.CollectionInvalid as e:
        print(f"Ungültige Sammlung: {e}")
    except errors.InvalidOperation as e:
        print(f"Ungültige Operation: {e}")
    except errors.PyMongoError as e:
        print(f"MongoDB-Fehler: {e}")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist in der Sync-Funktion aufgetreten: {e}")
