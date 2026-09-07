from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory store for demo purposes.
todo_items = []


@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "Flask backend running"})


@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    data = request.get_json(silent=True) or request.form

    item_name = data.get("itemName")
    item_description = data.get("itemDescription")

    if not item_name:
        return jsonify({"status": "error", "message": "itemName is required"}), 400

    item = {
        "itemName": item_name,
        "itemDescription": item_description
    }
    todo_items.append(item)

    return jsonify({
        "status": "success",
        "item": item,
        "totalItems": len(todo_items)
    }), 201


@app.route("/items", methods=["GET"])
def get_items():
    return jsonify(todo_items)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
