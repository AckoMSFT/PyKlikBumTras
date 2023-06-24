from datetime import timedelta
from os import environ

MYSQL_USERNAME = environ.get('MYSQL_USERNAME') or 'root'
MYSQL_PASSWORD = environ.get('MYSQL_PASSWORD') or 'root'
MYSQL_HOST = environ.get('MYSQL_HOST') or 'shop_database'
MYSQL_DATABASE_NAME = environ.get('MYSQL_DATABASE_NAME') or 'shop'
JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY') or 'AckoCar123'
JWT_ACCESS_TOKEN_EXPIRY = timedelta(minutes=60)

class Configuration:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{username}:{password}@{host}/{database_name}'.format(
        username = MYSQL_USERNAME,
        password = MYSQL_PASSWORD,
        host = MYSQL_HOST,
        database_name = MYSQL_DATABASE_NAME
    )
    JWT_SECRET_KEY = JWT_SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRY = JWT_ACCESS_TOKEN_EXPIRY
