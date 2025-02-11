"""
This module defines the authentication routes for the application using Flask and OAuth.
Routes:
    /login: Initiates the OAuth login process with Cognito.
    /callback: Handles the OAuth callback from Cognito, processes the token,
                and redirects to the frontend with user data.
    /logout: Logs out the user from the session and redirects to the Cognito logout URL.
Functions:
    login(): Initiates the OAuth login process and redirects to the Cognito authorization URL.
    callback(): Handles the OAuth callback, processes the token, creates the user if not exists,
                and redirects to the frontend with user data.
    logout(): Logs out the user from the session and redirects to the Cognito logout URL.
"""
import json
import base64
from os import environ
from flask import Blueprint, redirect, url_for, session, request, current_app
from app.services.user_service import create_user_if_not_exists

bp = Blueprint("auth", __name__)


@bp.route("/login")
def login():
    oauth = current_app.extensions["oauth"]
    next_url = request.args.get("next", "/")
    session["next_url"] = next_url
    return oauth.cognito.authorize_redirect(redirect_uri=url_for("auth.callback", _external=True))


@bp.route("/callback")
def callback():
    oauth = current_app.extensions["oauth"]
    token = oauth.cognito.authorize_access_token()
    next_url = session.pop("next_url", "/")

    id_token = token.get("id_token")

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

    be_user_data = create_user_if_not_exists(user_data).to_dict()
    encoded_user_data = base64.urlsafe_b64encode(
        json.dumps(be_user_data).encode()).decode()

    frontend_url = (
        f"{environ.get('FRONTEND_URL')}{next_url}"
        f"?id_token={id_token}&user_data={encoded_user_data}"
    )
    return redirect(frontend_url)


@bp.route("/logout")
def logout():
    session.pop("user", None)
    cognito_logout_url = (
        f"https://us-west-22z5rg2vjb.auth.us-west-2.amazoncognito.com/logout?"
        f"client_id=7tqidgi3eb03j1i7pt1hsnkf7r&logout_uri={environ.get('FRONTEND_URL')}"
    )
    return redirect(cognito_logout_url)
