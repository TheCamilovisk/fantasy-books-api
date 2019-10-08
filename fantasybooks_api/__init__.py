from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

POSTGRES_URL = '127.0.0.1:5432'
POSTGRES_USER = 'postgres'
POSTGRES_PW = 'postgres'
POSTGRES_DB = 'appwn_dev'


def create_app(config=None):
    app = Flask(__name__)
    app.config[
        'SQLALCHEMY_DATABASE_URI'
    ] = f'postgres+psycopg2://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_URL}/{POSTGRES_DB}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from .auth.resources import user_bp

    app.register_blueprint(user_bp)

    CORS(app)
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    return app
