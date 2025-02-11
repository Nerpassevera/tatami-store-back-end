from os import environ
from functools import wraps
from flask import request, jsonify
import requests
from jose import jwt, JWTError
from authlib.integrations.flask_client import OAuth

oauth = OAuth()

def register_oauth(app):
    """Attach OAuth to the app and configure AWS Cognito."""
    oauth.init_app(app)
    app.extensions["oauth"] = oauth

    oauth.register(
        name='cognito',
        authority='https://cognito-idp.us-west-2.amazonaws.com/us-west-2_2z5rG2vjB',
        client_id='7tqidgi3eb03j1i7pt1hsnkf7r',
        client_secret=environ.get("AWS_COGNITO_CLIENT_SECRET"),
        server_metadata_url='https://cognito-idp.us-west-2.amazonaws.com/us-west-2_2z5rG2vjB/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email phone profile'},
        redirect_uri="https://tatami-store-be-4d8522a2c022.herokuapp.com/auth/callback"
    )
    return oauth

COGNITO_POOL_ID = environ.get("AWS_COGNITO_POOL_ID")
COGNITO_REGION = environ.get("AWS_COGNITO_REGION")
COGNITO_ISSUER = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_POOL_ID}"
JWKS_URL = f"{COGNITO_ISSUER}/.well-known/jwks.json"


jwks = requests.get(JWKS_URL).json()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("id_token")
        if not token:
            return jsonify({"error": "ID token missing"}), 401

        try:
            unverified_header = jwt.get_unverified_header(token)
            kid = unverified_header.get("kid")
            key = None
            for jwk in jwks.get("keys", []):
                if jwk.get("kid") == kid:
                    key = jwk
                    break
            if key is None:
                raise JWTError("Public key not found in JWKS")
            
            audience = environ.get("AWS_COGNITO_CLIENT_ID")
            if not audience:
                raise JWTError("AWS_COGNITO_CLIENT_ID environment variable not set")
            
            payload = jwt.decode(
                token,
                key,
                algorithms=["RS256"],
                audience=environ.get("AWS_COGNITO_CLIENT_ID"),
                issuer=COGNITO_ISSUER,
                options={"verify_at_hash": False}
            )
            request.user = payload
        except JWTError as e:
            return jsonify({"error": f"Invalid token: {str(e)}"}), 401

        return f(*args, **kwargs)
    return decorated