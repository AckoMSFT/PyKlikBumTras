import csv
import io

from flask import Flask, request, jsonify, Response
from configuration import Configuration
from models import database, Product, ProductCategory, Category, Order, OrderStatus
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
    orders = Order.query.filter_by(status=OrderStatus.CREATED).all()

    return jsonify(
        orders=[
            order.to_json_delivery() for order in orders
        ]
    )

@application.route('/pick_up_order', methods=['POST'])
@role_check(valid_roles=['courier'])
def pick_up_order():
    request_json = request.json

    id = request_json.get('id', '')
    if not id:
        return jsonify(
            message='Missing order id.'
        ), 400

    if not isinstance(id, int) or id < 0:
        return jsonify(
            message='Invalid order id.'
        ), 400

    order = Order.query.filter_by(id=id).first()
    if not order:
        return jsonify(
            message='Invalid order id.'
        ), 400

    if order.status != OrderStatus.CREATED:
        return jsonify(
            message='Invalid order id.'
        ), 400

    order.status = OrderStatus.PENDING
    database.session.commit()

    return Response()

if __name__ == '__main__':
    database.init_app(application)

    application.run(debug=True, host='0.0.0.0', port=5003)