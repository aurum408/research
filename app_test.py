from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client.research

@app.route("/")
def home():
    return "Research server is running"

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    data["timestamp"] = datetime.utcnow()
    db.responses.insert_one(data)
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run()
