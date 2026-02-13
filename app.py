from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


client = MongoClient("mongodb+srv://<username>:<password>@cluster0.mongodb.net/research?retryWrites=true&w=majority")
db = client["research"]
participants = db["participants"]


# Сохраняем новую анкету + историю
@app.route("/save-anketa", methods=["POST"])
def save_anketa():
    data = request.json
    timestamp = datetime.utcnow().isoformat()

    submission = {
        "timestamp": timestamp,
        "gender": data.get("gender"),
        "age": data.get("age"),
        "job": data.get("job"),
        "alreadyDone": data.get("alreadyDone"),
        "object1Data": {},
        "object2Data": {}
    }

    participants.update_one(
        {"email": data["email"]},
        {"$push": {"submissions": submission}},
        upsert=True
    )
    return jsonify({"status": "ok"})


# Сохраняем объект 1 или 2 для последнего submission
@app.route("/save-object/<object_name>", methods=["POST"])
def save_object(object_name):
    data = request.json
    timestamp = datetime.utcnow().isoformat()

    # Добавляем объект в последний submission
    participants.update_one(
        {"email": data["email"]},
        {"$set": {f"submissions.-1.{object_name}Data": {"answers": data.get("answers"), "timestamp": timestamp}}},
        upsert=False
    )
    return jsonify({"status": "ok"})
