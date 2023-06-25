from flask import Flask
from flask_migrate import init, migrate, upgrade, Migrate
from sqlalchemy_utils import database_exists, create_database

from configuration import Configuration
from models import database

application = Flask(__name__)
application.config.from_object(Configuration)
migration = Migrate(application, database)

if __name__ == '__main__':
    while True:
        try:
            if not database_exists(application.config['SQLALCHEMY_DATABASE_URI']):
                print('Creating database: ' + application.config['SQLALCHEMY_DATABASE_URI'])
                create_database(application.config['SQLALCHEMY_DATABASE_URI'])
                print('Created database.')
            else:
                break

            database.init_app(application)

            with application.app_context() as context:
                print('Performing initial migration.')
                init()
                migrate(message='Initial migration.')
                upgrade()
                print('Initial migration done.')
            break
        except Exception as exception:
            print(exception)

    print('Bootstrap completed.')
