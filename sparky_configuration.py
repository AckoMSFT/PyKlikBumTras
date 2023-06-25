from os import environ

MYSQL_USERNAME = environ.get('MYSQL_USERNAME') or 'root'
MYSQL_PASSWORD = environ.get('MYSQL_PASSWORD') or 'root'
MYSQL_HOST = environ.get('MYSQL_HOST') or 'shop_database'
MYSQL_DATABASE_NAME = environ.get('MYSQL_DATABASE_NAME') or 'shop'
MYSQL_DRIVER = 'com.mysql.cj.jdbc.Driver'
JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY') or 'AckoCar123'


class Configuration:
    JDBC_URL = 'jdbc:mysql://{host}:3306/{database_name}'.format(
        host=MYSQL_HOST,
        database_name=MYSQL_DATABASE_NAME
    )
    JDBC_PROPERTIES = {
        'user': MYSQL_USERNAME,
        'password': MYSQL_PASSWORD,
        'driver': MYSQL_DRIVER
    }
    JWT_SECRET_KEY = JWT_SECRET_KEY
