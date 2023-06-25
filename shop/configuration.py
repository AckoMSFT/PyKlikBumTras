from datetime import timedelta
from os import environ

MYSQL_USERNAME = environ.get('MYSQL_USERNAME') or 'root'
MYSQL_PASSWORD = environ.get('MYSQL_PASSWORD') or 'root'
MYSQL_HOST = environ.get('MYSQL_HOST') or 'shop_database'
MYSQL_DATABASE_NAME = environ.get('MYSQL_DATABASE_NAME') or 'shop'
JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY') or 'AckoCar123'
JWT_ACCESS_TOKEN_EXPIRY = timedelta(minutes=60)
SPARKY_IP = environ.get('SPARKY_IP') or 'sparky'
SPARKY_PORT = environ.get('SPARKY_PORT') or 5431
SPARKY_PORT = int(SPARKY_PORT)
SPARKY_PRODUCT_STATISTICS = environ.get('SPARKY_PRODUCT_STATISTICS') or 'product_statistics'
SPARKY_CATEGORY_STATISTICS = environ.get('SPARKY_CATEGORY_STATISTICS') or 'category_statistics'


class Configuration:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{username}:{password}@{host}/{database_name}'.format(
        username=MYSQL_USERNAME,
        password=MYSQL_PASSWORD,
        host=MYSQL_HOST,
        database_name=MYSQL_DATABASE_NAME
    )
    JWT_SECRET_KEY = JWT_SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRY = JWT_ACCESS_TOKEN_EXPIRY
    SPARKY_IP = SPARKY_IP
    SPARKY_PORT = SPARKY_PORT
    SPARKY_PRODUCT_STATISTICS = SPARKY_PRODUCT_STATISTICS
    SPARKY_CATEGORY_STATISTICS = SPARKY_CATEGORY_STATISTICS
