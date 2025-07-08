from flask import Flask, request, jsonify, send_from_directory
from flask_dance.contrib.google import make_google_blueprint, google
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

# ✅ Set up Flask with static files from React build
app = Flask(__name__, static_folder='client/build', static_url_path='')
app.secret_key = os.getenv("SECRET_KEY")

# ✅ Allow frontend requests (update URL to your Render app)
CORS(app, origins=[
    "http://localhost:3000",
    "https://app-test-project.onrender.com"
], supports_credentials=True)

# ✅ Google OAuth blueprint setup
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

# ✅ API Route - Unit Conversion
@app.route("/convert", methods=["POST"])
def convert():
    data = request.get_json()
    meters = float(data["value"])
    feet = meters * 3.28084
    return jsonify({"feet": round(feet, 2)})

# ✅ OAuth - Get User Info
@app.route("/me")
def me():
    if not google.authorized:
        return jsonify({"error": "Not logged in"}), 401
    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        return jsonify({"error": "Failed to fetch user info"}), 500
    return jsonify(resp.json())

# ✅ OAuth - Logout
@app.route("/logout")
def logout():
    google_bp.token = None
    return jsonify({"message": "Logged out"}), 200

# ✅ Serve React frontend (fix for Render platform)
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    try:
        return send_from_directory(app.static_folder, path)
    except:
        return send_from_directory(app.static_folder, "index.html")
