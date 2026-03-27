from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import hashlib
import json
import os

app = Flask(__name__)
CORS(app)

# ---------------- BLOCKCHAIN STORAGE ----------------
CHAIN_FILE = "chain.json"

# Create genesis block if not exists
def create_genesis():
    if not os.path.exists(CHAIN_FILE):
        genesis_block = [{
            "index": 0,
            "timestamp": time.time(),
            "data": "Genesis Block",
            "prev_hash": "0",
            "hash": "0"
        }]
        with open(CHAIN_FILE, "w") as f:
            json.dump(genesis_block, f, indent=4)

# Load chain
def load_chain():
    with open(CHAIN_FILE, "r") as f:
        return json.load(f)

# Save chain
def save_chain(chain):
    with open(CHAIN_FILE, "w") as f:
        json.dump(chain, f, indent=4)

# Hash block
def hash_block(block):
    block_string = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()

# Add new block
def add_block(data):
    chain = load_chain()
    prev_block = chain[-1]

    new_block = {
        "index": len(chain),
        "timestamp": time.time(),
        "data": data,
        "prev_hash": prev_block["hash"]
    }

    new_block["hash"] = hash_block(new_block)
    chain.append(new_block)
    save_chain(chain)

    return new_block

# Initialize
create_genesis()

# ---------------- ROUTES ----------------

@app.route('/')
def home():
    return "✅ GC Backend Running"

@app.route('/send', methods=['POST'])
def send():
    try:
        data = request.json

        receiver = data.get("to")
        amount = data.get("amount")

        if not receiver or not amount:
            return jsonify({"error": "Missing data"}), 400

        tx_data = {
            "to": receiver,
            "amount": amount
        }

        block = add_block(tx_data)

        return jsonify({
            "status": "success",
            "block": block
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/chain')
def get_chain():
    chain = load_chain()
    return jsonify(chain)

# ---------------- RUN ----------------

if __name__ == '__main__':
    app.run()
