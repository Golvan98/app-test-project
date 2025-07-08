from flask import Flask, request, jsonify
from flask_dance.contrib.google import make_google_blueprint, google
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

# ✅ Updated Google OAuth setup with correct scopes
google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    scope=[
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile"
    ],
    redirect_to="me"
)
app.register_blueprint(google_bp, url_prefix="/login")

@app.route("/convert", methods=["POST"])
def convert():
    data = request.get_json()
    meters = float(data["value"])
    feet = meters * 3.28084
    return jsonify({"feet": round(feet, 2)})

@app.route("/me")
def me():
    if not google.authorized:
        return jsonify({"error": "Not logged in"}), 401
    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        return jsonify({"error": "Failed to fetch user info"}), 500
    return jsonify(resp.json())

@app.route("/logout")
def logout():
    google_bp.token = None
    return jsonify({"message": "Logged out"}), 200

@app.route("/")
def home():
    return jsonify({"message": "Flask API running"})
