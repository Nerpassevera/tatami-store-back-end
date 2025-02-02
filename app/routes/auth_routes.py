from flask import Blueprint, redirect, url_for, session, request, current_app
from app.services.user_service import create_user_if_not_exists

bp = Blueprint("auth", __name__)

# User Login Route
@bp.route("/login")
def login():
    oauth = current_app.extensions["oauth"]

    next_url = request.args.get("next", "/")
    session["next_url"] = next_url
    return oauth.cognito.authorize_redirect(redirect_uri=url_for("auth.callback", _external=True))

# Callback to handle Cognito authentication
@bp.route("/callback")
def callback():
    oauth = current_app.extensions["oauth"]
    token = oauth.cognito.authorize_access_token()
    user_info = oauth.cognito.parse_id_token(token, nonce=None)
    session["user"] = user_info
    next_url = session.pop("next_url", "/")

    user_data = {
        "cognito_id": user_info.get("sub"),
        "email": user_info.get("email"),
        "phone_number": user_info.get("phone_number"),
        "username": user_info.get("cognito:username"),
        "family_name": user_info.get("family_name"),
        "given_name": user_info.get("given_name"),
    }


    create_user_if_not_exists(user_data)

    user = oauth.cognito.parse_id_token(token, nonce=None)
    session["user"] = user
    return redirect(next_url)

# Logout Route
@bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")
