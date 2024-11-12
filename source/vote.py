import pandas as pd
import os

def parse_excel(df):
    # Initialisiere das JSON-Format mit aggregierten Werten
    parsed_data = {
        "id": f"{df['Wahlperiode'].iloc[0]}{str(df['Sitzungnr'].iloc[0]).zfill(3)}",
        "wahlperiode": str(df["Wahlperiode"].iloc[0]),
        "sitzungsnummer": str(df["Sitzungnr"].iloc[0]),
        "datum": "",
        "thema": "",
        "stimmen_zählung": {
            "abgegebenen": str(df[["ja", "nein", "Enthaltung", "ungültig"]].sum().sum()),
            "nichtabgegeben": str(df["nichtabgegeben"].sum()),
            "ja": str(df["ja"].sum()),
            "nein": str(df["nein"].sum()),
            "enthaltungen": str(df["Enthaltung"].sum()),
            "ungültige": str(df["ungültig"].sum())
        },
        "stimmen_namentlich": []
    }

    # Gruppierte Stimmabgabe erstellen
    grouped = df.apply(lambda row: {
        "fraktion": str(row["Fraktion/Gruppe"]),
        "stimme": (
            "ja" if row["ja"] == 1 else
            "nein" if row["nein"] == 1 else
            "enthalten" if row["Enthaltung"] == 1 else
            "ungültig" if row["ungültig"] == 1 else
            "nichtabgegeben"
        ),
        "name": ", ".join(filter(pd.notna, [
            str(row.get("Bezeichnung", f"{row['Vorname']} {row['Name']}")),
            str(row.get("xyz", "")),
            str(row.get("xyzy", ""))
        ]))
    }, axis=1).tolist()

    # Votes gruppieren
    grouped_votes = {}
    for vote in grouped:
        key = (vote["fraktion"], vote["stimme"])
        if key not in grouped_votes:
            grouped_votes[key] = {
                "fraktion": vote["fraktion"],
                "stimme": vote["stimme"],
                "name": []
            }
        grouped_votes[key]["name"].append(vote["name"])

    # Gruppierte Votes hinzufügen
    parsed_data["stimmen_namentlich"] = list(grouped_votes.values())

    return parsed_data



def get_all_json():
    all_json = []
    folder_path = "C:\\Users\\ala19\\uni\\parser\\data\\data\\votes"

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            df = pd.read_excel(file_path)
            json_data = parse_excel(df)
            all_json.append(json_data)

    print("Namentliche Stimmen erfolgreich geparst.") 
    return all_json