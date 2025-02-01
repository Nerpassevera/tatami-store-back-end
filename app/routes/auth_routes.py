from flask import Blueprint, redirect, url_for, session, jsonify
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
    user = oauth.cognito.parse_id_token(token)
    session["user"] = user
    return jsonify({"message": "Logged in successfully", "user": user})

# Logout Route
@bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")