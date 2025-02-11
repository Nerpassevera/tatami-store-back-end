"""
This module provides authentication services for the Tatami Store backend application.
It includes functions to register OAuth with AWS Cognito
and a decorator to require a valid JWT token.

Functions:
    register_oauth(app): Attach OAuth to the app and configure AWS Cognito.
    token_required(f): Decorator to require a valid JWT token.

Constants:
    COGNITO_POOL_ID: AWS Cognito User Pool ID.
    COGNITO_REGION: AWS Cognito Region.
    COGNITO_ISSUER: URL of the AWS Cognito issuer.
    JWKS_URL: URL to fetch the JSON Web Key Set (JWKS).

Dependencies:
    os.environ: To access environment variables.
    functools.wraps: To preserve the original function's metadata.
    flask.request: To access the incoming request.
    flask.jsonify: To create JSON responses.
    requests: To make HTTP requests.
    jose.jwt: To handle JWT operations.
    authlib.integrations.flask_client.OAuth: To handle OAuth integration with Flask.
"""
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
        name="cognito",
        authority=environ.get("AWS_COGNITO_AUTHORITY"),
        client_id=environ.get("AWS_COGNITO_CLIENT_ID"),
        client_secret=environ.get("AWS_COGNITO_CLIENT_SECRET"),
        server_metadata_url=environ.get("AWS_COGNITO_METADATA_URL"),
        client_kwargs={"scope": "openid email phone profile"},
        redirect_uri=f"{environ.get("BACKEND_URL")}/auth/callback"
    )
    return oauth


COGNITO_POOL_ID = environ.get("AWS_COGNITO_POOL_ID")
COGNITO_REGION = environ.get("AWS_COGNITO_REGION")
COGNITO_ISSUER = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_POOL_ID}"
JWKS_URL = f"{COGNITO_ISSUER}/.well-known/jwks.json"

jwks = requests.get(JWKS_URL).json()


def token_required(f):
    """Decorator to require a valid JWT token."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization header missing or invalid"}), 401

        token = auth_header.split(" ")[1]
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
                raise JWTError(
                    "AWS_COGNITO_CLIENT_ID environment variable not set")

            payload = jwt.decode(
                token,
                key,
                algorithms=["RS256"],
                audience=audience,
                issuer=COGNITO_ISSUER,
                options={"verify_at_hash": False}
            )
            request.user = payload
        except JWTError as e:
            return jsonify({"error": f"Invalid token: {str(e)}"}), 401

        return f(*args, **kwargs)
    return decorated
