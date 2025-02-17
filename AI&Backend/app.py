from flask import Flask, render_template, request, jsonify, session
import json
import os
import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"

USERS_FILE = "users.json"
GALLERY_FILE = "gallery.json"

# Load users from file
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    return {}

# Save users to file
def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file)

# Load gallery from file
def load_gallery():
    if os.path.exists(GALLERY_FILE): 
        with open(GALLERY_FILE, "r") as file:
            return json.load(file)
    return []

# Save gallery to file
def save_gallery(gallery):
    with open(GALLERY_FILE, "w") as file:
        json.dump(gallery, file)

# Function to simulate AI-based jewelry design
def generate_3d_model(prompt, material):
    model_urls = {
        "gold": "msy_qHQN0yNpeUSt0uJAlBfRcA8JCIwW97tjlev0",
        "silver": "msy_bFgAymvHVT5F0JohGgiSbFje0k1eMz4vuY2Y",
        "platinum": "msy_I9Be2zf1iZdJrizbs6TPDH5oRdSvzKPl2Bjk",
    }
    return {"modelUrl": model_urls.get(material, "https://example.com/models/default_ring.glb")}

# Home route
@app.route("/")
def home():
    return render_template("index.html")

# User Registration
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    users = load_users()
    if email in users:
        return jsonify({"error": "Email already registered"}), 400

    users[email] = {"name": name, "password": password}
    save_users(users)

    return jsonify({"message": "Registration successful!"}), 200

# User Login
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    email = data.get("email")
    password = data.get("password")

    users = load_users()
    if email in users and users[email]["password"] == password:
        session["user"] = email
        return jsonify({"message": "Login successful!"}), 200

    return jsonify({"error": "Invalid email or password"}), 401

# Check if user is logged in
@app.route("/check_login", methods=["GET"])
def check_login():
    if "user" in session:
        return jsonify({"loggedIn": True, "user": session["user"]})
    return jsonify({"loggedIn": False})

# Logout
@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return jsonify({"message": "Logged out successfully!"})

# AI Jewelry Generation API
@app.route("/generate", methods=["POST"])
def generate():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    prompt = data.get("prompt", "Elegant gold ring")
    material = data.get("material", "gold")

    model_data = generate_3d_model(prompt, material)

    # Save to gallery
    gallery = load_gallery()
    gallery.append({
        "user": session["user"],
        "prompt": prompt,
        "material": material,
        "modelUrl": model_data["modelUrl"],
        "timestamp": datetime.datetime.now().isoformat()
    })
    save_gallery(gallery)

    return jsonify(model_data)

# Retrieve User Gallery
@app.route("/gallery", methods=["GET"])
def gallery():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user_gallery = [item for item in load_gallery() if item["user"] == session["user"]]
    return jsonify(user_gallery)

# Ensure Flask always returns JSON
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
