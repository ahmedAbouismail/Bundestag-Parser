import xml.etree.ElementTree as ET
import os


def parse_xml(xml_file):
    """
    Parst eine XML-Datei und extrahiert daraus Sitzungsdaten
    :param xml_file: Der Pfad zu einer XML-Datei
    :return: Strukturierte Daten in Form eines JSON-Objects
    """
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Extract header data
    header_data = root.find(".//kopfdaten")
    wahlperiode = header_data.find("plenarprotokoll-nummer/wahlperiode").text
    sitzungsnummer = header_data.find("sitzungstitel/sitzungsnr").text
    datum = header_data.find("veranstaltungsdaten/datum").attrib['date']

    # Combine session ID
    sitzungs_id = int(wahlperiode + sitzungsnummer.zfill(3))

    # Parse session course
    sitzungsverlauf_data = []
    for speech in root.findall(".//sitzungsverlauf/tagesordnungspunkt/rede"):

        speech_data = {"rede": []}

        current_speaker = None
        collecting_text = True  # Variable to control text collection based on <name> tag

        for element in speech:
            # Handle speaker start
            if element.tag == "p" and element.attrib.get("klasse") == "redner":
                speaker_element = element.find("redner")
                if speaker_element is not None:
                    speaker_id = speaker_element.attrib.get("id")
                    # Start new speaker dictionary
                    current_speaker = {"redner_id": speaker_id, "text": ""}
                    speech_data["rede"].append(current_speaker)
                    collecting_text = True  # Reset text collection when new speaker starts

            # Handle text collection for speaker's speech
            elif element.tag == "p" and collecting_text:
                if element.attrib.get("klasse") in ["J", "J_1", "O"] and current_speaker:
                    text_content = element.text or ""
                    current_speaker["text"] += text_content

            # Stop collecting text after <name> tag appears
            elif element.tag == "name":
                collecting_text = False

        sitzungsverlauf_data.append(speech_data)

    # Create the JSON object with German keys
    json_data = {
        "id": sitzungs_id,
        "datum": datum,
        "wahlperiode": wahlperiode,
        "sitzungsnummer": sitzungsnummer,
        "sitzungsverlauf": sitzungsverlauf_data
    }

    return json_data


def get_all_json(dir_path='/data/protocols'):
    """
    Durchläuft einen Verzeichnispfad und parst jede XML-Datei darin
    :param dir_path: Verzeichnispfad zu den Protokollen
    :return: Eine Liste von JSON-Objekten zurück, die alle Protokolle enthalten
    """
    all_json = []
    folder_path = dir_path
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):  # Only process files, not subdirectories
            all_json.append(parse_xml(file_path))

    print("Protokolle erfolgreich geparst.")
    return all_json
