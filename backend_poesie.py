
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

POESIE_FILE = "poesie.json"

def carica_poesie():
    if os.path.exists(POESIE_FILE):
        with open(POESIE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salva_poesie(poesie):
    with open(POESIE_FILE, "w", encoding="utf-8") as f:
        json.dump(poesie, f, indent=2, ensure_ascii=False)

@app.route("/api/poesie", methods=["POST"])
def ricevi_poesia():
    testo = request.form.get("testo")
    if not testo:
        return jsonify({"errore": "Testo mancante"}), 400
    poesie = carica_poesie()
    poesie.append({"testo": testo})
    salva_poesie(poesie)
    return jsonify({"messaggio": "Poesia salvata"}), 200

@app.route("/api/poesie", methods=["GET"])
def leggi_poesie():
    poesie = carica_poesie()
    return jsonify(poesie), 200

@app.route("/")
def index():
    return "Backend Poesie attivo."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
