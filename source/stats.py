TOTAL_PROTOCOL_COUNT = 0
TOTAL_REPRESENTATIVE_COUNT = 0
TOTAL_SPEECHES = 0

def get_stats():
    # Create the JSON object with German keys
    json_data = [{
        "id": "statistics",
        "Protokolle": TOTAL_PROTOCOL_COUNT,
        "Abgeordnete seit 1949": TOTAL_REPRESENTATIVE_COUNT,
        "Reden": TOTAL_SPEECHES,
    }]

    return json_data