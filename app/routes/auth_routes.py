from flask import Blueprint, redirect, url_for, session, jsonify, request
from app.services.auth_services import oauth

bp = Blueprint("auth", __name__)

# User Login Route
@bp.route("/login")
def login():
    return oauth.cognito.authorize_redirect(redirect_uri=url_for("auth.callback", _external=True))

# Callback to handle Cognito authentication
@bp.route("/callback")
def callback():
    token = oauth.cognito.authorize_access_token()
    print("TOKEN RECEIVED:", token)
    nonce = session.get("nonce", None)  # Stored in session (best practice)

    if not nonce:
        nonce = request.args.get("nonce")  # Try getting it from request

    if not nonce:
        return jsonify({"error": "Missing nonce"}), 400
    user = oauth.cognito.parse_id_token(token)
    session["user"] = user
    return jsonify({"message": "Logged in successfully", "user": user})

# Logout Route
@bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")