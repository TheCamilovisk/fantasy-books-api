from os import getenv

from dateutil import relativedelta


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

    JWT_SECRET_KEY = 'dev'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ('access', 'refresh')
    JWT_ACCESS_TOKEN_EXPIRES = relativedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = relativedelta(days=30)

    REDIS_URL = 'redis://:redis@localhost:6379/0'
