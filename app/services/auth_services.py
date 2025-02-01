from os import environ
from authlib.integrations.flask_client import OAuth

oauth = OAuth()  # Create OAuth instance without attaching to Flask app

def register_oauth(app):
    """Attach OAuth to the app and configure AWS Cognito."""
    oauth.init_app(app)  # Now attach it to Flask
    print("AWS_COGNITO_CLIENT_SECRET:", environ.get("AWS_COGNITO_CLIENT_SECRET"))

    oauth.register(
        name='cognito',
        authority='https://cognito-idp.us-west-2.amazonaws.com/us-west-2_2z5rG2vjB',
        client_id='7tqidgi3eb03j1i7pt1hsnkf7r',
        client_secret=environ.get("AWS_COGNITO_CLIENT_SECRET"),
        server_metadata_url='https://cognito-idp.us-west-2.amazonaws.com/us-west-2_2z5rG2vjB/.well-known/openid-configuration',
        client_kwargs={'scope': 'email openid phone'}
)

    return oauth