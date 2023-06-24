from datetime import timedelta

MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = 'root'
MYSQL_HOST = 'localhost' # 'shop_database'
MYSQL_DATABASE_NAME = 'shop'
JWT_SECRET_KEY = 'AckoCar123'
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
