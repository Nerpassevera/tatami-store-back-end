import os
from flask_cors import CORS
from flask import Flask
from .services.auth_services import register_oauth
# Import routes
from .routes.user_routes import bp as user_bp
from .routes.product_routes import bp as product_bp
from .routes.cart_routes import bp as cart_bp
from .routes.order_routes import bp as order_bp
from .routes.category_routes import bp as category_bp
from .routes.address_routes import bp as address_bp
from .routes.auth_routes import bp as auth_bp  # Import auth routes

from .db import db, migrate
from .models import user, order, order_item, product, product_category, category, cart, cart_item, address

def create_app(config=None):
    app = Flask(__name__)
    CORS(app, 
        supports_credentials=True, 
        origins=[os.environ.get("FRONTEND_URL"), "http://localhost:3000", "http://localhost:5173"],
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
    )
    app.secret_key = os.environ.get("FLASK_SECRET_KEY")  

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    global oauth
    oauth = register_oauth(app)

    app.register_blueprint(user_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(address_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    
    return app