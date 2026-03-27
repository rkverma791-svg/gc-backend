from flask import Flask, request, jsonify
import json, time, os

app = Flask(__name__)
CHAIN_FILE = "chain.json"

def load_chain():
    if os.path.exists(CHAIN_FILE):
        with open(CHAIN_FILE) as f:
            return json.load(f)
    return []

def save_chain(chain):
    with open(CHAIN_FILE, "w") as f:
        json.dump(chain, f)

def create_genesis(chain):
    if len(chain) == 0:
        chain.append({
            "index": 0,
            "timestamp": time.time(),
            "transactions": ["Genesis"]
        })

def get_balance(chain, addr):
    bal = 0
    for block in chain:
        for tx in block["transactions"]:
            if isinstance(tx, dict):
                if tx["sender"] == addr:
                    bal -= tx["amount"]
                if tx["receiver"] == addr:
                    bal += tx["amount"]
    return max(bal, 0)

@app.route("/chain")
def chain():
    return jsonify(load_chain())

@app.route("/balance/<addr>")
def balance(addr):
    chain = load_chain()
    return jsonify({"balance": get_balance(chain, addr)})

@app.route("/send", methods=["POST"])
def send():
    data = request.json
    chain = load_chain()
    create_genesis(chain)

    tx = {
        "sender": data["sender"],
        "receiver": data["receiver"],
        "amount": data["amount"]
    }

    if get_balance(chain, tx["sender"]) < tx["amount"]:
        return jsonify({"status": "fail"})

    chain.append({
        "index": len(chain),
        "timestamp": time.time(),
        "transactions": [tx]
    })

    save_chain(chain)
    return jsonify({"status": "success"})

app.run(host="0.0.0.0", port=5000)
