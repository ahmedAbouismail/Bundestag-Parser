import re
import html


def sanitize_string(text):
    """
    Bereinigt einen Textstring, um Konsistenz in nachfolgenden Prozessen sicherzustellen
    :param text: Der unbereinigte Textstring.
    :return: Ein bereinigter und standardisierter String.
    """
    if not isinstance(text, str):
        return text

    # Konvertiert HTML-Entities (z. B.  &amp; , &lt;) in ihre Klartextäquivalente (&, <)
    text = html.unescape(text)

    # Normalisiert Zeilenumbrüche, um Konsistenz über Plattformen (z. B. Windows und Mac) hinweg sicherzustellen
    text = text.replace('\r\n', '\n').replace('\r', '\n')

    # Entfernt nicht druckbare Zeichen, die den Text beschädigen können.
    text = re.sub(r'[^\x20-\x7E\xA0-\xFF]', '', text)

    # Ersetzt Anführungszeichen und Bindestriche durch Standardzeichen
    text = text.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
    text = text.replace('–', '-').replace('—', '-')

    # Entfernt HTML-Tags, um den Textinhalt zu behalten
    text = re.sub(r'<[^>]+>', '', text)

    # Schneidet führende und nachfolgende Leerzeichen ab
    text = ' '.join(text.split())

    return text


def sanitize_json(data):
    """
    Bereinigt rekursiv alle Strings innerhalb einer JSON-Struktur
    :param data: Eine JSON-Struktur mit unbereinigten Strings
    :return: Eine bereinigte JSON-Struktur
    """
    if isinstance(data, dict):
        return {key: sanitize_json(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [sanitize_json(element) for element in data]
    elif isinstance(data, str):
        return sanitize_string(data)
    else:
        return data
