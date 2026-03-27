from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import time

# ---------------- INIT APP ----------------
app = Flask(__name__)
CORS(app)

CHAIN_FILE = "chain.json"


# ---------------- HOME ----------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "GC Backend Running"})


# ---------------- LOAD & SAVE ----------------
def load_chain():
    if not os.path.exists(CHAIN_FILE):
        return []
    try:
        with open(CHAIN_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_chain(chain):
    with open(CHAIN_FILE, "w") as f:
        json.dump(chain, f, indent=4)


# ---------------- INIT GENESIS ----------------
@app.route("/init", methods=["GET"])
def init():
    chain = load_chain()

    if not chain:
        genesis = {
            "index": 0,
            "timestamp": time.time(),
            "transactions": ["Genesis"]
        }
        chain.append(genesis)
        save_chain(chain)

    return jsonify(chain)


# ---------------- GET CHAIN ----------------
@app.route("/chain", methods=["GET"])
def get_chain():
    return jsonify(load_chain())


# ---------------- SEND TRANSACTION ----------------
@app.route("/send", methods=["POST"])
def send():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data received"}), 400

        sender = data.get("sender")
        receiver = data.get("receiver")
        amount = data.get("amount")

        if not sender or not receiver or not amount:
            return jsonify({"error": "Missing fields"}), 400

        chain = load_chain()

        block = {
            "index": len(chain),
            "timestamp": time.time(),
            "transactions": [
                f"{sender} -> {receiver} : {amount}"
            ]
        }

        chain.append(block)
        save_chain(chain)

        return jsonify({
            "message": "Transaction successful",
            "block": block
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
