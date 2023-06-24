from flask import Flask
from flask_migrate import init, migrate, upgrade, Migrate
from sqlalchemy_utils import database_exists, create_database
from configuration import Configuration
from models import database, User, Role, UserRole

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

                ownerRole = Role(name='owner')
                customerRole = Role(name='customer')
                courierRole = Role(name='courier')

                database.session.add_all([ownerRole, customerRole, courierRole])
                database.session.commit()

                owner_role = Role.query.filter_by(name='owner').first()

                scroogeMcDuck = User(
                    forename='Scrooge',
                    surname='McDuck',
                    email='onlymoney@gmail.com',
                    password='evenmoremoney',
                    roles=[owner_role]
                )

                database.session.add(scroogeMcDuck)
                database.session.commit()

            break
        except Exception as exception:
            print(exception)

    print('Bootstrap completed.')