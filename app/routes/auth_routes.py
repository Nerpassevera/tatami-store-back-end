import json
import base64
from urllib.parse import urlencode
from os import environ
from flask import Blueprint, redirect, url_for, session, request, current_app

from app.services.user_service import create_user_if_not_exists

bp = Blueprint("auth", __name__)

# User Login Route
@bp.route("/login")
def login():
    oauth = current_app.extensions["oauth"]
    next_url = request.args.get("next", "/")
    session["next_url"] = next_url
    print("LOGIN >> NEXT URL:", next_url)
    
    return oauth.cognito.authorize_redirect(redirect_uri=url_for("auth.callback", _external=True))

# Callback to handle Cognito authentication
@bp.route("/callback")
def callback():
    oauth = current_app.extensions["oauth"]
    token = oauth.cognito.authorize_access_token()
    next_url = session.pop("next_url", "/")
    print("CALLBACK >> NEXT URL:", next_url)
    
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

    # Convert user data to a Base64 encoded JSON string
    encoded_user_data = base64.urlsafe_b64encode(json.dumps(user_data).encode()).decode()

    # Redirect back to frontend with user data in URL
    frontend_url = f"{environ.get('FRONTEND_URL')}{next_url}?user_data={encoded_user_data}"
    print(f"Redirecting to: {frontend_url}")
    return redirect(frontend_url)

@bp.route("/logout")
def logout():
    session.pop("user", None)

    cognito_logout_url = f"https://us-west-22z5rg2vjb.auth.us-west-2.amazoncognito.com/logout?client_id=7tqidgi3eb03j1i7pt1hsnkf7r&logout_uri={environ.get('FRONTEND_URL')}"
    
    return redirect(cognito_logout_url)