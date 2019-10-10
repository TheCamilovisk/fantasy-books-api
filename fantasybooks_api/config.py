from os import getenv


class BaseConfig:
    SECRET_KEY = 'dev'
    
    SQLALCHEMY_DATABASE_URI = 'postgres+psycopg2://{}:{}@{}/{}'.format(
        getenv("POSTGRES_USER"),
        getenv("POSTGRES_PW"),
        getenv("POSTGRES_URL"),
        getenv("POSTGRES_DB"),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BCRYPT_LOG_ROUNDS = 12
