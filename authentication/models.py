from flask_sqlalchemy import SQLAlchemy

MAX_LENGTH = 256
database = SQLAlchemy()

class User(database.Model):
    __tablename__ = 'user'

    id = database.Column(database.Integer, primary_key=True)
    forename = database.Column(database.String(MAX_LENGTH), nullable=False)
    surname = database.Column(database.String(MAX_LENGTH), nullable=False)
    email = database.Column(database.String(MAX_LENGTH), nullable=False, unique=True)
    password = database.Column(database.String(MAX_LENGTH), nullable=False)

    roles = database.relationship(
        'Role',
        secondary='user_role',
        backref=database.backref('user', lazy='dynamic')
    )

class Role(database.Model):
    __tablename__ = 'role'

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(MAX_LENGTH), nullable=False, unique=True)

class UserRole(database.Model):
    __tablename__ = 'user_role'

    id = database.Column(database.Integer, primary_key=True)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = database.Column(database.Integer, database.ForeignKey('role.id', ondelete='CASCADE'))