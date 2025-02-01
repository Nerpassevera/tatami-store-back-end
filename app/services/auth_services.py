from authlib.integrations.flask_client import OAuth

oauth = OAuth()  # Create OAuth instance without attaching to Flask app

def register_oauth(app):
    """Attach OAuth to the app and configure AWS Cognito."""
    oauth.init_app(app)  # Now attach it to Flask

    oauth.register(
        name="cognito",
        client_id="7tqidgi3eb03ji1pt1hsnkf7r",  # Replace with your Cognito Client ID
        client_secret="<client_secret>",  # Replace with your Cognito Client Secret
        authorize_url="https://cognito-idp.us-west-2.amazonaws.com/us-west-2_2z5rG2vjB/oauth2/authorize",
        access_token_url="https://cognito-idp.us-west-2.amazonaws.com/us-west-2_2z5rG2vjB/oauth2/token",
        server_metadata_url="https://cognito-idp.us-west-2.amazonaws.com/us-west-2_2z5rG2vjB/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email phone"}
    )

    return oauth