from pymongo import MongoClient
import json
import os

def confic_db():
    global db_name
    uri = "mongodb+srv://s0573997:mongodb123@bundestag.o75ow.mongodb.net/?retryWrites=true&w=majority&appName=Bundestag"
    client = MongoClient(uri)

    db_name = "Protokolle"
    collection_speak = "Reden" 
    collection_vote = "Abstimmungen"  

    db = client[db_name]
    speak = db[collection_speak]
    vote = db[collection_vote]
    return client, speak, vote


def insert_into_db():
    
    directory_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/documents')
    client, speak, vote = confic_db()

    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)

            # Daten in die neue Sammlung einfügen
            if isinstance(data, list):
                speak.insert_many(data)
                vote.insert_one({ }, {})

            else:
                speak.insert_one(data)
                vote.insert_one({ })

            print(f"Daten von {filename} erfolgreich in der neuen Datenbank '{db_name}' im Cluster gespeichert.")

    client.close()