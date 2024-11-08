import xml.etree.ElementTree as ET

def parse_mdb(mdb_element):
    # Extrahiere ID und persönliche Angaben
    id = mdb_element.findtext("ID")
    titel = mdb_element.findtext("NAMEN/NAME/ANREDE_TITEL")
    vorname = mdb_element.findtext("NAMEN/NAME/VORNAME")
    nachname = mdb_element.findtext("NAMEN/NAME/NACHNAME")
    fraktion = mdb_element.find("WAHLPERIODEN/WAHLPERIODE/INSTITUTIONEN/INSTITUTION/INS_LANG").text
    
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
            "fraktion": wp.findtext("INSTITUTIONEN/INSTITUTION/INS_LANG"),
            "funktion": wp.findtext("INSTITUTIONEN/INSTITUTION/FKT_LANG", default="")
        }
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
    tree = ET.parse("/data/MDB_STAMMDATEN.XML")
    root = tree.getroot()

    # Extrahiere alle MDB Einträge
    mdb_list = []
    for mdb in root.findall("MDB"):
        mdb_list.append(parse_mdb(mdb))

    return mdb_list