from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # 프론트가 다른 주소(Origin)에서 접근하면 필요

DATA_FILE = os.path.join(os.path.dirname(__file__), "checklists.json")


def ensure_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({"checklist_rows": [], "checklists": {}}, f, ensure_ascii=False, indent=2)


def read_data():
    ensure_file()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def write_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@app.get("/api/health")
def health():
    return jsonify({"ok": True, "time": datetime.now().isoformat()})


@app.get("/api/checklists")
def get_checklists():
    return jsonify(read_data())


@app.post("/api/checklists")
def save_checklists():
    payload = request.get_json(silent=True) or {}
    checklist_rows = payload.get("checklist_rows")
    checklists = payload.get("checklists")

    if not isinstance(checklist_rows, list) or not isinstance(checklists, dict):
        return jsonify({"ok": False, "message": "Invalid payload"}), 400

    write_data({"checklist_rows": checklist_rows, "checklists": checklists})
    return jsonify({"ok": True})


if __name__ == "__main__":
    # 사내망 다른 PC에서 접속 가능하게 0.0.0.0 바인딩
    app.run(host="0.0.0.0", port=5000)
