import protocol
import representative
import mongo_db

if __name__ == "__main__":
    mongo_db.sync(protocol.get_all_json(), "protokolle")
    mongo_db.sync(representative.get_all(), "mdb_stammdaten")