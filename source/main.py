import representative
import protocol
import mongo_db
from data_cleaning import clean_parsed_json

if __name__ == "__main__":
    """
    Ausführungsblock des Projekts
    
    Im main Module werden Funktionen aus anderen Modulen aufgerufen, um Daten in MongoDB zu speichern.
    Es werden vier Funktionen verwendet:
    - protocol.get_all_json(): holt alle Protokolldaten, die im 'protocol' Ordner gespeichert sind
    - representative.get_all(): holt alle Zugeordneten-Daten, die im 'representative' Ordner gespeichert sind
    - mongo_db.sync(): um extrahierte Daten in der DB zu speichern
    - clean_parsed_json(): bereinigt alle Daten 
    """

    protocol_data = protocol.get_all_json()

    cleaned_protocol_data = clean_parsed_json(protocol_data)

    representative_data = representative.get_all()

    cleaned_representative_data = clean_parsed_json(representative_data)

    mongo_db.sync(protocol_data, "protokolle")
    mongo_db.sync(representative_data, "mdb_stammdaten")