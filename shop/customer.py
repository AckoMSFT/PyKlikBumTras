import csv
import io

from flask import Flask, request, jsonify, Response
from configuration import Configuration
from models import database, Product, ProductCategory, Category, Order, OrderProduct, OrderStatus
from role_check import role_check
from flask_jwt_extended import JWTManager, get_jwt_identity
from sqlalchemy_utils import database_exists, create_database, drop_database
import re

application = Flask(__name__)
application.config.from_object(Configuration)
database.init_app(application)
jwt = JWTManager(application)

@application.route('/search', methods=['GET'])
@role_check(valid_roles=['customer'])
def search():
    product_name = request.args.get('name', '')
    category_name = request.args.get('category', '')

    all_categories = Category.query.filter(Category.name.contains(category_name))
    all_products = Product.query.filter(Product.name.contains(product_name))

    filtered_categories = Category.query.join(ProductCategory, isouter=True)
    filtered_products = Product.query.join(ProductCategory, isouter=True)

    # Apply filters
    if category_name:
        filtered_categories = all_categories
        category_ids = [category.id for category in all_categories]
        filtered_products = filtered_products.filter(ProductCategory.category_id.in_(category_ids))

    if product_name:
        filtered_products = all_products
        product_ids = [product.id for product in all_products]
        filtered_categories = filtered_categories.filter(ProductCategory.product_id.in_(product_ids))

    return jsonify(
        categories=[
            category.name for category in filtered_categories.all()
        ],
        products=[
            product.to_json() for product in filtered_products.all()
        ]
    ), 200

@application.route('/order', methods=['POST'])
@role_check(valid_roles=['customer'])
def order():
    requests = request.json.get('requests', None)

    if not requests:
        return jsonify(
            message='Field requests is missing.'
        ), 400

    for request_id, order_request in enumerate(requests):
        print(request_id)
        print(order_request)

        if 'id' not in order_request:
            return jsonify(
                message='Product id is missing for request number {request_id}.'.format(
                    request_id=request_id
                )
            ), 400

        if 'quantity' not in order_request:
            return jsonify(
                message='Product quantity is missing for request number {request_id}.'.format(
                    request_id=request_id
                )
            ), 400

        product_id = order_request['id']
        if not isinstance(product_id, int) or product_id < 0:
            return jsonify(
                message='Invalid product id for request number {request_id}.'.format(
                    request_id=request_id
                )
            ), 400

        product_quantity = order_request['quantity']
        if not isinstance(product_quantity, int) or product_quantity < 0:
            return jsonify(
                message='Invalid product quantity for request number {request_id}.'.format(
                    request_id=request_id
                )
            ), 400

        product = Product.query.filter_by(id=product_id).first()
        if not product:
            return jsonify(
                message=f'Invalid product for request number {request_id}.'.format(
                    request_id=request_id
                )
            ), 400

    email = get_jwt_identity()

    order = Order(
        price=0,
        status=OrderStatus.CREATED,
        email=email
    )

    database.session.add(order)
    database.session.commit()

    order_price = 0
    for order_request in requests:
        product_id = order_request['id']
        product_quantity = order_request['quantity']

        product = Product.query.filter_by(id=product_id).first()
        product_price = product.price
        product.waiting += product_quantity

        order_price += product_quantity * product_price

        order_product = OrderProduct(
            order_id=order.id,
            product_id=product_id,
            quantity=product_quantity
        )

        database.session.add(order_product)
        database.session.flush()

    order.price = order_price
    database.session.commit()

    return jsonify(
        id=order.id
    ), 200

@application.route('/status', methods=['GET'])
@role_check(valid_roles=['customer'])
def status():
    email = get_jwt_identity()

    orders = Order.query.filter_by(email=email).all()

    return jsonify(
        orders=[
            order.to_json() for order in orders
        ]
    )

@application.route('/delivered', methods=['POST'])
@role_check(valid_roles=['customer'])
def delivered():
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

    if order.status != OrderStatus.PENDING:
        return jsonify(
            message='Invalid order id.'
        ), 400

    order_products = OrderProduct.query.filter_by(order_id=order.id).all()
    for order_product in order_products:
        product = Product.query.filter_by(id=order_product.product_id).first()
        product_quantity = order_product.quantity
        product.sold += product_quantity
        product.waiting -= product_quantity
        database.session.flush()

    order.status = OrderStatus.COMPLETE
    database.session.commit()

    return Response()

if __name__ == '__main__':
    database.init_app(application)

    application.run(debug=True, host='0.0.0.0', port=5002)