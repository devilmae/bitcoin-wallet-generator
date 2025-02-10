import json
import os

def save_wallet_to_file(wallet_data, filename="wallets.json"):
    """Save wallet data to a JSON file."""
    os.makedirs("data", exist_ok=True)  # Ensure the directory exists
    filepath = os.path.join("data", filename)

    # Load existing data if available
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            data = json.load(file)
    else:
        data = []

    data.append(wallet_data)

    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)

def load_wallets_from_file(filename="wallets.json"):
    """Load wallet data from a JSON file."""
    filepath = os.path.join("data", filename)
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            return json.load(file)
    return []
