import os
import json
import datetime

# File to store remembered data
REMEMBER_FILE = "remembered_data.json"

def load_remembered_data():
    """Load remembered data from the JSON file."""
    if os.path.exists(REMEMBER_FILE):
        with open(REMEMBER_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}  # Return empty dict if file is corrupted
    return {}

def save_remembered_data(data):
    """Save remembered data to the JSON file."""
    with open(REMEMBER_FILE, "w") as file:
        json.dump(data, file, indent=4)

def remember_data(data):
    """Remember a sentence with a timestamp."""
    if data:
        remembered_data = load_remembered_data()
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y %I:%M %p")
        remembered_data[timestamp] = data
        save_remembered_data(remembered_data)
        return f"I'll remember that: {data}"
    else:
        return "No data to remember."

def retrieve_remembered_data(keyword):
    """Retrieve sentences containing a specific keyword from remembered data."""
    remembered_data = load_remembered_data()
    keyword = keyword.lower()  # Ensure case-insensitive matching
    matching_sentences = [
        sentence for sentence in remembered_data.values() if keyword in sentence.lower()
    ]

    if matching_sentences:
        return matching_sentences
    else:
        return None
