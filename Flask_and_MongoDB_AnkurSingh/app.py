from flask import Flask, jsonify, request, render_template, redirect, url_for
from pymongo import MongoClient
from pathlib import Path
import json
import os

app = Flask(__name__)


def load_mongo_uri():
    env_file = Path(__file__).with_name("atlas-credentials.env")
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            key, value = stripped.split("=", 1)
            os.environ[key.strip()] = value.strip().strip('"')
    return os.environ.get("MONGODB_URI")


mongo_uri = load_mongo_uri()
if not mongo_uri:
    raise RuntimeError("MONGODB_URI not found. Add it to atlas-credentials.env or set the environment variable.")

client = MongoClient(mongo_uri)
db = client["student_db"]
collection = db["students"]


# Task 1: JSON API
@app.route("/api")
def api():
    with open("data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return jsonify(data)


# Task 2: Frontend form
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            age = request.form["age"]

            data = {
                "name": name,
                "email": email,
                "age": age,
            }

            collection.insert_one(data)
            return redirect(url_for("success"))

        except Exception as e:
            return render_template("index.html", error=str(e))

    return render_template("index.html")


@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/all")
def all_students():
    students = list(collection.find({}, {"_id": 0}))  # Exclude the MongoDB _id field from the response
    return jsonify(students)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
