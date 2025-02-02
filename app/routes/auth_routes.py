from flask import Blueprint, redirect, url_for, session, jsonify, request, current_app
from app.services.user_service import create_user_if_not_exists

bp = Blueprint("auth", __name__)

# User Login Route
@bp.route("/login")
def login():
    oauth = current_app.extensions["oauth"]
    return oauth.cognito.authorize_redirect(redirect_uri=url_for("auth.callback", _external=True))

# Callback to handle Cognito authentication
@bp.route("/callback")
def callback():
    oauth = current_app.extensions["oauth"]
    token = oauth.cognito.authorize_access_token()
    print("TOKEN RECEIVED:", token)
    user_info = oauth.cognito.parse_id_token(token, nonce=None)
    print("USER INFO:", user_info)


    user_data = {
        "cognito_id": user_info.get("sub"),
        "email": user_info.get("email"),
        "phone_number": user_info.get("phone_number"),
        "username": user_info.get("cognito:username"),
        "family_name": user_info.get("family_name"),
        "given_name": user_info.get("given_name"),
    }


    print("USER DATA:", user_data)

    create_user_if_not_exists(user_data)

    user = oauth.cognito.parse_id_token(token, nonce=None)
    session["user"] = user
    return jsonify({"message": "Logged in successfully", "user": user})

# Logout Route
@bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")