import csv
import io

from flask import Flask, request, jsonify, Response
from configuration import Configuration
from models import database, Product, ProductCategory, Category
from role_check import role_check
from flask_jwt_extended import JWTManager
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy import and_
import re

application = Flask(__name__)
application.config.from_object(Configuration)
database.init_app(application)
jwt = JWTManager(application)

@application.route('/orders_to_deliver', methods=['GET'])
@role_check(valid_roles=['courier'])
def orders_to_deliver():
    return Response()

if __name__ == '__main__':
    database.init_app(application)

    application.run(debug=True, host='0.0.0.0', port=5003)