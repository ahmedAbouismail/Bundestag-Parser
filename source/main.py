import representative
import protocol
import mongo_db
import vote

if __name__ == "__main__":
    mongo_db.sync(protocol.get_all_json(), "protokolle")
    mongo_db.sync(representative.get_all(), "mdb_stammdaten")
    mongo_db.sync(vote.get_all_json(), "namentliche_abstimmungen")
