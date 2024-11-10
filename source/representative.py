import xml.etree.ElementTree as ET
import zipfile

def parse_mdb(mdb_element):
    # Extrahiere ID und persönliche Angaben
    id = mdb_element.findtext("ID")
    titel = mdb_element.findtext("NAMEN/NAME/ANREDE_TITEL")
    vorname = mdb_element.findtext("NAMEN/NAME/VORNAME")
    nachname = mdb_element.findtext("NAMEN/NAME/NACHNAME")
    fraktion = mdb_element.find("BIOGRAFISCHE_ANGABEN/PARTEI_KURZ").text
    
    # Biographie
    biographie = {
        "geburtsdatum": mdb_element.findtext("BIOGRAFISCHE_ANGABEN/GEBURTSDATUM"),
        "sterbedatum": mdb_element.findtext("BIOGRAFISCHE_ANGABEN/STERBEDATUM"),
        "geschlecht": mdb_element.findtext("BIOGRAFISCHE_ANGABEN/GESCHLECHT"),
        "familienstand": mdb_element.findtext("BIOGRAFISCHE_ANGABEN/FAMILIENSTAND"),
        "beruf": mdb_element.findtext("BIOGRAFISCHE_ANGABEN/BERUF"),
        "lebenslauf": mdb_element.findtext("BIOGRAFISCHE_ANGABEN/VITA_KURZ", default="")
    }
    
    # Wahlperioden
    wahlperioden = []
    for wp in mdb_element.findall("WAHLPERIODEN/WAHLPERIODE"):
        wahlperiode = {
            "wahlperiode": wp.findtext("WP"),
            "von": wp.findtext("MDBWP_VON"),
            "bis": wp.findtext("MDBWP_BIS"),
            "institutionen": []
        }

        # Durchlaufe alle Institutionen in der Wahlperiode
        for institution in wp.findall("INSTITUTIONEN/INSTITUTION"):
            institution_data = {
                "institutionsart": institution.findtext("INSART_LANG"),
                "institutionsname": institution.findtext("INS_LANG"),
                "mdb_von": institution.findtext("MDBINS_VON"),
                "mdb_bis": institution.findtext("MDBINS_BIS"),
                "funktion": institution.findtext("FKT_LANG", default=""),
                "funktion_von": institution.findtext("FKTINS_VON", default=""),
                "funktion_bis": institution.findtext("FKTINS_BIS", default="")
            }
            wahlperiode["institutionen"].append(institution_data)

        wahlperioden.append(wahlperiode)

    # Erstelle das JSON-kompatible Dictionary
    result = {
        "id": id,
        "titel": titel,
        "vorname": vorname,
        "nachname": nachname,
        "fraktion": fraktion,
        "biographie": biographie,
        "wahlperiode": wahlperioden
    }
    
    return result

def get_all():

    # Falls wir keine XML-File für die Stammdaten erhalten, dannn einfach hier extracten
    zip_path = "../data/Stammdaten.zip"
    extract_path = "../data/"
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Extrahiere eine bestimmte Datei
        zip_ref.extract("MDB_STAMMDATEN.XML", extract_path)
        print("example.txt wurde extrahiert.")

    tree = ET.parse("../data/MDB_STAMMDATEN.XML")
    root = tree.getroot()

    # Extrahiere alle MDB Einträge
    mdb_list = []
    for mdb in root.findall("MDB"):
        mdb_list.append(parse_mdb(mdb))

    return mdb_list