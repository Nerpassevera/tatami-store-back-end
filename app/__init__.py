import os

from flask_cors import CORS
from flask import Flask

# import routes with alias
from .routes.user_routes import bp as user_bp
from .routes.product_routes import bp as product_bp
from .routes.cart_routes import bp as cart_bp
from .routes.order_routes import bp as order_bp
from .routes.category_routes import bp as category_bp
from .routes.address_routes import bp as address_bp

from .db import db, migrate
from .models import user
from .models import order
from .models import order_item
from .models import product
from .models import product_category
from .models import category
from .models import cart
from .models import cart_item
from .models import address


def create_app(config=None):
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'SQLALCHEMY_DATABASE_URI')

    if config:
        # Merge `config` into the app's configuration
        # to override the app's default settings for testing
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    app.register_blueprint(user_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(address_bp)

    return app
