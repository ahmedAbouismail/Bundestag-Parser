import xml.etree.ElementTree as ET
import json
import os

import dbconfig

protokoll_data = {"Tagesordnungspunkte": []}
json_output_file = "/BT-Protokolle.json"
txt_output_file = "/BT-Protokolle.txt"
dataDir = "data"
jsonDirectory = "/documents"

def parse_file():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/protocols/20113.xml')
    tree = ET.parse(file_path)
    root = tree.getroot()
    return root

def create_dir():
    os.makedirs(dataDir, exist_ok=True)
    os.makedirs(dataDir + jsonDirectory, exist_ok=True)

def extract_information():
    root = parse_file()
    redner_id_counter = 0  # Zähler für die automatischen IDs
    with open(dataDir + jsonDirectory+txt_output_file, 'w', encoding='utf-8') as txt_file:
        
        for top in root.findall('.//tagesordnungspunkt'):
            top_data = {
                "TOP-Nummer": top.get("top-id", "Unbekannt"),
                "Beschreibung": top.findtext('kurzbeschreibung', default="Keine Beschreibung"),
                "Reden": []
            }

            for rede in top.findall('.//rede'):
                rede_data = {
                    "Redner": [],
                    "Verlauf": []
                }
                
                # Hauptredner sammeln
                redner_elem = rede.find('.//redner')
                if redner_elem is not None:
                    vorname = redner_elem.findtext('.//vorname')
                    nachname = redner_elem.findtext('.//nachname')
                    name = redner_elem.findtext('name', "").strip()
                    if not name:
                        name = f"{vorname} {nachname}".strip()
                    fraktion = redner_elem.findtext('.//fraktion')
                    rolle_kurz = redner_elem.findtext('.//rolle_kurz')
                    
                    redner_data = {
                        "ID": str(redner_id_counter),  # Automatische ID
                        "Name": name,
                        "Fraktion": fraktion if fraktion else rolle_kurz,
                        "Typ": "Hauptredner"
                    }
                    rede_data["Redner"].append(redner_data)
                    current_speaker_id = str(redner_id_counter)  # ID des aktuellen Redners
                    redner_id_counter += 1 

                    # In die TXT-Datei schreiben
                    txt_file.write(f"Redner: {name if name else 'Unbekannter Redner'}\n")
                    txt_file.write(f"Fraktion: {fraktion if fraktion else rolle_kurz}\n")
                    txt_file.write("Rede:\n")
                    
                    # Sammlung der Redeabsätze und Dictionary zur Sammlung von Text pro RednerID
                    rede_texte = []
                    redner_texts = {} 
                    
                    for absatz in rede:
                        if absatz.tag == 'p' and absatz.text:
                            # Text zum Hauptredner hinzufügen
                            if current_speaker_id not in redner_texts:
                                redner_texts[current_speaker_id] = absatz.text.strip()
                            else:
                                redner_texts[current_speaker_id] += " " + absatz.text.strip()
                            
                            # Absätze zur Rede-TXT-Datei hinzufügen
                            rede_texte.append(f"-> {absatz.text.strip()}")
                        elif absatz.tag == 'name' and absatz.text:
                            # Zwischenruf der Präsidentin
                            zwischenredner_name = absatz.text.strip()
                            zwischenredner_id = str(redner_id_counter)
                            
                            zwischenredner_data = {
                                "ID": zwischenredner_id,
                                "Name": zwischenredner_name,
                                "Fraktion": "Präsidentin",
                                "Typ": "Intervention"
                            }
                            if zwischenredner_data not in rede_data["Redner"]:
                                rede_data["Redner"].append(zwischenredner_data)
                                redner_id_counter += 1
                            
                            # Text des Zwischenredners sammeln
                            if zwischenredner_id not in redner_texts:
                                redner_texts[zwischenredner_id] = f"Zwischenruf von {zwischenredner_name}"
                            else:
                                redner_texts[zwischenredner_id] += f" Zwischenruf von {zwischenredner_name}"
                            rede_texte.append(f"Zwischenredner: {zwischenredner_name}")

                            # Setze den aktuellen Sprecher auf den Zwischenredner
                            current_speaker_id = zwischenredner_id
                    # Übertragen der gesammelten Texte in JSON-Verlauf
                    for rid, text in redner_texts.items():
                        rede_data["Verlauf"].append({
                            "RednerID": rid,
                            "Text": text
                        })
                    
                    # Alle gesammelten Texte als Teil der Rede in die TXT-Datei einfügen
                    for absatz in rede_texte:
                        txt_file.write(f"{absatz}\n")
                    
                    txt_file.write("\n---\n\n")

                    top_data["Reden"].append(rede_data)
            
           
            protokoll_data["Tagesordnungspunkte"].append(top_data)

# Speichern der JSON-Datei
def save_in_json():
    with open(dataDir + jsonDirectory+json_output_file, 'w', encoding='utf-8') as json_file:
        json.dump(protokoll_data, json_file, ensure_ascii=False, indent=4)

    print(f"Die Protokolle wurden erfolgreich in {json_output_file} und {txt_output_file} gespeichert.")


if __name__ == "__main__":
    extract_information()
    save_in_json()
    dbconfig.insert_into_db()