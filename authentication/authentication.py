from flask import Flask, request, jsonify, Response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt
from configuration import Configuration
from models import database, User, Role
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy import and_
import re

application = Flask(__name__)
application.config.from_object(Configuration)
database.init_app(application)
jwt = JWTManager(application)

email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')


@application.route('/register_customer', methods=['POST'])
def register_customer():
    request_json = request.json

    forename = request_json.get('forename', '')
    surname = request_json.get('surname', '')
    email = request_json.get('email', '')
    password = request_json.get('password', '')

    if not forename:
        return jsonify(
            message='Field forename is missing.'
        ), 400

    if not surname:
        return jsonify(
            message='Field surname is missing.'
        ), 400

    if not email:
        return jsonify(
            message='Field email is missing.'
        ), 400

    if not password:
        return jsonify(
            message='Field password is missing.'
        ), 400

    if len(forename) > 256:
        return jsonify(
            message='Invalid forename.'
        ), 400

    if len(surname) > 256:
        return jsonify(
            message='Invalid surname.'
        ), 400

    if len(email) > 256:
        return jsonify(
            message='Invalid email.'
        ), 400

    if not re.fullmatch(email_regex, email):
        return jsonify(
            message='Invalid email.'
        ), 400

    if len(password) < 8:
        return jsonify(
            message='Invalid password.'
        ), 400

    if len(password) > 256:
        return jsonify(
            message='Invalid password.'
        ), 400

    if User.query.filter_by(email=email).first():
        return jsonify(
            message='Email already exists.'
        ), 400

    role = Role.query.filter_by(name='customer').first().id

    user = User(
        forename=forename,
        surname=surname,
        email=email,
        password=password,
        role=role
    )

    database.session.add(user)
    database.session.commit()

    return jsonify(
        forename=forename,
        surname=surname,
        email=email,
        password=password
    ), 200


@application.route('/register_courier', methods=['POST'])
def register_courier():
    request_json = request.json

    forename = request_json.get('forename', '')
    surname = request_json.get('surname', '')
    email = request_json.get('email', '')
    password = request_json.get('password', '')

    if not forename:
        return jsonify(
            message='Field forename is missing.'
        ), 400

    if not surname:
        return jsonify(
            message='Field surname is missing.'
        ), 400

    if not email:
        return jsonify(
            message='Field email is missing.'
        ), 400

    if not password:
        return jsonify(
            message='Field password is missing.'
        ), 400

    if len(forename) > 256:
        return jsonify(
            message='Invalid forename.'
        ), 400

    if len(surname) > 256:
        return jsonify(
            message='Invalid surname.'
        ), 400

    if len(email) > 256:
        return jsonify(
            message='Invalid email.'
        ), 400

    if not re.fullmatch(email_regex, email):
        return jsonify(
            message='Invalid email.'
        ), 400

    if len(password) < 8:
        return jsonify(
            message='Invalid password.'
        ), 400

    if len(password) > 256:
        return jsonify(
            message='Invalid password.'
        ), 400

    if User.query.filter_by(email=email).first():
        return jsonify(
            message='Email already exists.'
        ), 400

    role = Role.query.filter_by(name='courier').first().id

    user = User(
        forename=forename,
        surname=surname,
        email=email,
        password=password,
        role=role
    )

    database.session.add(user)
    database.session.commit()

    return jsonify(
        forename=forename,
        surname=surname,
        email=email,
        password=password
    ), 200


@application.route('/login', methods=['POST'])
def login():
    request_json = request.json

    email = request_json.get('email', '')
    password = request_json.get('password', '')

    if not email:
        return jsonify(
            message='Field email is missing.'
        ), 400

    if not password:
        return jsonify(
            message='Field password is missing.'
        ), 400

    if len(email) > 256:
        return jsonify(
            message='Invalid email.'
        ), 400

    if not re.fullmatch(email_regex, email):
        return jsonify(
            message='Invalid email.'
        ), 400

    user = User.query.filter(
        and_(
            User.email == email,
            User.password == password
        )
    ).first()

    if not user:
        return jsonify(
            message='Invalid credentials.'
        ), 400

    role = Role.query.filter_by(id=user.role).first()

    additional_claims = {
        'forename': user.forename,
        'surname': user.surname,
        'email': user.email,
        'password': user.password,
        'roles': [role.name]
    }

    accessToken = create_access_token(
        identity=email,
        additional_claims=additional_claims,
        expires_delta=Configuration.JWT_ACCESS_TOKEN_EXPIRY
    )

    return jsonify(
        accessToken=accessToken
    ), 200


@application.route('/delete', methods=['POST'])
@jwt_required()
def delete():
    additional_claims = get_jwt()

    email = additional_claims['email']

    user = User.query.filter_by(email=email).first()
    if not User:
        return jsonify(
            message='Unknown user.'
        ), 400

    # Calling delete 2x causes this?
    # File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 2054, in delete
    # 2023-06-21T17:00:31.856818068Z     state = attributes.instance_state(instance)
    # 2023-06-21T17:00:31.856821294Z             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # 2023-06-21T17:00:31.856823889Z AttributeError: 'NoneType' object has no attribute '_sa_instance_state'
    database.session.delete(user)
    database.session.commit()

    return Response()


if __name__ == '__main__':
    # Bootstrap code
    # There is a race condition with connecting to MySQL - so need to retry
    # TODO (acko): Rewrite me

    database.init_app(application)
    with application.app_context() as context:
        if not database_exists(application.config['SQLALCHEMY_DATABASE_URI']):
            create_database(application.config['SQLALCHEMY_DATABASE_URI'])

            ownerRole = Role(name='owner')
            customerRole = Role(name='customer')
            courierRole = Role(name='courier')

            database.session.add_all([ownerRole, customerRole, courierRole])
            database.session.commit()

            scroogeMcDuck = User(
                forename='Scrooge',
                surname='McDuck',
                email='onlymoney@gmail.com',
                password='evenmoremoney',
                role=ownerRole.id
            )

            database.session.add(scroogeMcDuck)
            database.session.commit()
        else:
            print('Database has already been initialized.')

    application.run(debug=True, host='0.0.0.0', port=5000)
