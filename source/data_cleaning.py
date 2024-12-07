import os
import re
import json
import logging
import unicodedata
from html import unescape
from logging.handlers import RotatingFileHandler

log_directory = "logs/data_cleaning"
os.makedirs(log_directory, exist_ok=True)

# Configure logging with rotation
log_handler = RotatingFileHandler(
    filename=os.path.join(log_directory, "data_cleaning.log"),  # Log file name
    mode="a",  # Append mode
    maxBytes=5 * 1024 * 1024,  # Maximum log file size (e.g., 5 MB)
    backupCount=10,  # Keep 3 backup files
    encoding="utf-8",  # Ensure special character support
)
log_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

# Set up the root logger
logging.basicConfig(level=logging.INFO, handlers=[log_handler])


def log_change(action, field_name, original, cleaned, change_position):
    """
    Logs details of the cleaning action.

    Parameters:
        action (str): Name of the cleaning action performed.
        field_name (str): Field that was cleaned.
        original (str): Original text before cleaning.
        cleaned (str): Cleaned text after processing.
        change_position (tuple): Start and end indices of the change in the text.
    """
    log_entry = {
        "action": action,
        "field": field_name,
        "original": original[max(0, change_position[0] - 20):change_position[1] + 20],
        "cleaned": cleaned[max(0, change_position[0] - 20):change_position[1] + 20],
        "change_position": change_position
    }
    logging.info(json.dumps(log_entry, ensure_ascii=False))


# Cleaning functions
def remove_non_printable_characters(text, field_name):
    """Removes non-printable and control characters from the text."""
    original = text
    cleaned = re.sub(r'[\x00-\x1F\x7F]', '', text)
    if original != cleaned:
        for match in re.finditer(r'[\x00-\x1F\x7F]', original):
            log_change("Remove Non-Printable Characters", field_name, original, cleaned, (match.start(), match.end()))
    return cleaned


def normalize_whitespace(text, field_name):
    """Standardizes and trims all kinds of whitespace in the text."""
    original = text
    # Normalize all whitespace (including NBSP and NNBSP) to single regular spaces
    cleaned = re.sub(r'\s+', ' ', text).strip()
    if original != cleaned:
        for match in re.finditer(r'\s+', original):
            start, end = match.start(), match.end()
            if original[start:end] != cleaned[start:end]:  # Log only actual changes
                log_change("Normalize Whitespace", field_name, original, cleaned, (start, end))
    return cleaned


def handle_special_symbols(text, field_name):
    """Handles and normalizes special symbols as required."""
    original = text
    # Replace and normalize special symbols
    replacements = {
        '\u2013': '-',  # En dash
        '\u2014': '--',  # Em dash
        '\u2026': '...',  # Ellipsis
        '\u201C': '"',  # Left double quote
        '\u201D': '"',  # Right double quote
        '\u2018': "'",  # Left single quote
        '\u2019': "'",  # Right single quote
        '\u2022': '-',  # Bullet
        '\u00B7': '·',  # Middle dot
        '\u00A7': '§',  # Section sign
        '\u20AC': 'EUR',  # Euro sign
    }
    cleaned = original
    for symbol, replacement in replacements.items():
        if symbol in cleaned:
            cleaned = cleaned.replace(symbol, replacement)

    if original != cleaned:
        for symbol, replacement in replacements.items():
            for match in re.finditer(re.escape(symbol), original):
                log_change("Handle Special Symbols", field_name, original, cleaned, (match.start(), match.end()))
    return cleaned


def escape_html_entities(text, field_name):
    """Converts HTML entities to their readable text form."""
    original = text
    cleaned = unescape(text)
    if original != cleaned:
        for match in re.finditer(r'&[^;]+;', original):
            log_change("Escape HTML Entities", field_name, original, cleaned, (match.start(), match.end()))
    return cleaned


def normalize_encoding(text, field_name):
    """Normalizes text encoding using Unicode NFC normalization."""
    original = text
    cleaned = unicodedata.normalize('NFC', text)
    if original != cleaned:
        for match in re.finditer(r'[\xC3][\xA4\xB6\xBC]', original):  # Detect common encoding issues for Umlauts
            log_change("Normalize Encoding", field_name, original, cleaned, (match.start(), match.end()))
    return cleaned


def clean_text(text, field_name):
    """Applies all cleaning steps to a given text field."""
    text = remove_non_printable_characters(text, field_name)
    text = normalize_whitespace(text, field_name)
    text = handle_special_symbols(text, field_name)
    text = escape_html_entities(text, field_name)
    text = normalize_encoding(text, field_name)
    return text


def clean_json(data):
    """
    Recursively cleans all text fields in a JSON structure.

    Parameters:
        data (dict or list): JSON data to be cleaned.

    Returns:
        Cleaned JSON data.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = clean_text(value, key)
            elif isinstance(value, (dict, list)):
                data[key] = clean_json(value)
    elif isinstance(data, list):
        for i in range(len(data)):
            if isinstance(data[i], str):
                data[i] = clean_text(data[i], f"list_index_{i}")
            elif isinstance(data[i], (dict, list)):
                data[i] = clean_json(data[i])
    return data


def clean_parsed_json(data):
    """
    Cleans the parsed JSON data object.

    Parameters:
        data (dict or list): JSON object parsed from the protocol or representative module.

    Returns:
        dict or list: Cleaned JSON object.
    """
    logging.info("Starting cleaning process for parsed JSON object.")
    cleaned_data = clean_json(data)
    logging.info("Cleaning completed for parsed JSON object.")
    return cleaned_data
