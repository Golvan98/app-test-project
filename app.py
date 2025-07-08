from flask import Flask, request, jsonify, send_from_directory
from flask_dance.contrib.google import make_google_blueprint, google
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, static_folder='client/build', static_url_path='')
app.secret_key = os.getenv("SECRET_KEY")
CORS(app, origins=[
    "http://localhost:3000", 
    "https://your-frontend.onrender.com"  # ⬅️ Update to your deployed frontend URL
], supports_credentials=True)

# ✅ Google OAuth setup
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

# ✅ Serve React frontend
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    if path != "" and os.path.exists(f"client/build/{path}"):
        return send_from_directory("client/build", path)
    else:
        return send_from_directory("client/build", "index.html")
