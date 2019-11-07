from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_redis import FlaskRedis

from fantasybooks_api.config import BaseConfig

bcrypt = Bcrypt()
db = SQLAlchemy()
redis = FlaskRedis()
ma = Marshmallow()
migrate = Migrate()
jwt = JWTManager()


@jwt.token_in_blacklist_loader
def check_if_token_is_revoked(decrypted_token):
    jti = decrypted_token['jti']
    entry = redis.get(jti)
    if entry is None:
        return True
    return entry == b'true'


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(BaseConfig())

    from .resources.auth import user_bp, auth_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)

    CORS(app)
    bcrypt.init_app(app)
    db.init_app(app)
    redis.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from fantasybooks_api.utils import createsuperuser

    app.cli.add_command(createsuperuser)

    return app
