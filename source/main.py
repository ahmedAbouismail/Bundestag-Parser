import representative
import protocol
import mongo_db

if __name__ == "__main__":
    """
    Ausführungsblock des Projekts
    
    Im main Module werden Funktionen aus anderen Modulen aufgerufen, um Daten in MongoDB zu speichern.
    Es werden zwei Funktionen verwendet:
    - protocol.get_all_json(): holt alle Protokolldaten, die im 'protocol' Ordner gespeichert sind
    - representative.get_all(): holt alle Zugeordneten-Daten, die im 'representative' Ordner gespeichert sind
    """
    mongo_db.sync(protocol.get_all_json(), "protokolle")
    mongo_db.sync(representative.get_all(), "mdb_stammdaten")