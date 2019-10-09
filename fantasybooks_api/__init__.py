from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from fantasybooks_api.config import BaseConfig

bcrypt = Bcrypt()
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(BaseConfig())

    from .auth.resources import user_bp

    app.register_blueprint(user_bp)

    CORS(app)
    bcrypt.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    return app
