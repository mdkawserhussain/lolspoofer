from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import json
import os
import logging  # Import logging module

app = Flask(__name__)

# Set up logging
log_file = os.path.join(os.path.dirname(__file__), "key_validation_server.log")
logging.basicConfig(filename=log_file, level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Path to store activation keys
KEYS_FILE = "activation_keys.json"

# Load keys from file or initialize an empty dictionary
def load_keys():
    if os.path.exists(KEYS_FILE):
        try:
            with open(KEYS_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            logging.error("Invalid JSON in keys file. Initializing empty keys database.")
            return {}
    return {}

# Save keys to file
def save_keys(keys):
    with open(KEYS_FILE, "w") as f:
        json.dump(keys, f, indent=4)

# Initialize activation keys database
KEYS_DB = load_keys()

@app.route('/validate', methods=['POST'])
def validate_key():
    data = request.get_json()
    key = data.get("key")
    discord_id = data.get("discord_id")  # Optional logging

    if key not in KEYS_DB:
        return jsonify({"valid": False, "message": "Invalid key"})

    key_data = KEYS_DB[key]
    
    # Check key type and conditions
    if key_data["type"] == "single" and key_data.get("used", False):
        return jsonify({"valid": False, "message": "Key already used"})
    elif key_data["type"] == "time-limited":
        expiry_date = datetime.strptime(key_data["expires"], "%Y-%m-%d")
        if expiry_date < datetime.now():
            return jsonify({"valid": False, "message": "Key expired"})

    # Mark single-use keys as used
    if key_data["type"] == "single":
        KEYS_DB[key]["used"] = True
        save_keys(KEYS_DB)

    return jsonify({"valid": True, "message": "Key activated"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))