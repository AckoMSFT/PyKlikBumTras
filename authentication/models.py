from flask_sqlalchemy import SQLAlchemy

MAX_LENGTH = 256
database = SQLAlchemy()

# TODO (acko): Rewrite me
class User(database.Model):
    __tablename__ = 'users'

    id = database.Column(database.Integer, primary_key=True)
    forename = database.Column(database.String(MAX_LENGTH), nullable=False)
    surname = database.Column(database.String(MAX_LENGTH), nullable=False)
    email = database.Column(database.String(MAX_LENGTH), nullable=False, unique=True)
    password = database.Column(database.String(MAX_LENGTH), nullable=False)
    role = database.Column(database.Integer, database.ForeignKey('roles.id'), nullable=False)


class Role(database.Model):
    __tablename__ = 'roles'

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(MAX_LENGTH), nullable=False)
    users = database.relationship('User', backref='roles')

    def __repr__(self):
        return self.name