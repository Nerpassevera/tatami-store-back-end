import json
import base64
from os import environ
from flask import Blueprint, redirect, url_for, session, request, current_app, jsonify, make_response
from app.services.user_service import create_user_if_not_exists

bp = Blueprint("auth", __name__)

# User Login Route
@bp.route("/login")
def login():
    oauth = current_app.extensions["oauth"]

    print('request.args', request.base_url)
    next_url = request.args.get("next", "/")
    session["next_url"] = next_url
    print("URL:", next_url)
    return oauth.cognito.authorize_redirect(redirect_uri=url_for("auth.callback", _external=True))

# Callback to handle Cognito authentication
@bp.route("/callback")
def callback():
    oauth = current_app.extensions["oauth"]
    token = oauth.cognito.authorize_access_token()
    next_url = session.pop("next_url", "/")
    user = oauth.cognito.parse_id_token(token, nonce=None)
    session["user"] = user

    user_data = {
        "cognito_id": user.get("sub"),
        "email": user.get("email"),
        "phone_number": user.get("phone_number"),
        "username": user.get("cognito:username"),
        "family_name": user.get("family_name"),
        "given_name": user.get("given_name"),
    }

    create_user_if_not_exists(user_data)


    # Convert user_data to JSON and Base64 encode it
    encoded_user_data = base64.b64encode(json.dumps(user_data).encode()).decode()

    response = make_response(redirect('http://localhost:5173'))
    response.set_cookie("user_data", encoded_user_data, httponly=False, samesite="Lax")

    return response

@bp.route("/logout")
def logout():
    session.pop("user", None)

    cognito_logout_url = f"https://us-west-22z5rg2vjb.auth.us-west-2.amazoncognito.com/logout?client_id=7tqidgi3eb03j1i7pt1hsnkf7r&logout_uri={environ.get("FRONTEND_URL")}"
    response = make_response(redirect(cognito_logout_url))
    response.set_cookie("user_data", "", expires=0)
    return response
