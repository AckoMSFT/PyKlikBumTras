import csv
import io

from flask import Flask, request, jsonify, Response
from configuration import Configuration
from models import database, Product, ProductCategory, Category, Order, OrderProduct, OrderStatus
from role_check import role_check
from flask_jwt_extended import JWTManager
from sqlalchemy import func

application = Flask(__name__)
application.config.from_object(Configuration)
database.init_app(application)
jwt = JWTManager(application)

@application.route('/update', methods=['POST'])
@role_check(valid_roles=['owner'])
def update():
    try:
        file = request.files['file']

        if not file:
            return jsonify(
                message='Field file is missing'
            ), 400

        bytes = file.stream.read().decode('UTF-8')
        stream = io.StringIO(bytes)
        csv_reader = csv.reader(stream)
    except:
        return jsonify(
            message='Field file is missing.'
        ), 400

    for line_number, line in enumerate(csv_reader):
        # print(line_number, line)

        cnt = len(line)
        if cnt != 3:
            return jsonify(
                message='Incorrect number of values on line {line_number}.'.format(
                    line_number=line_number
                )
            ), 400

    stream.seek(0)
    csv_reader = csv.reader(stream)

    for line_number, line in enumerate(csv_reader):
        # print(line_number, line)

        product_price = line[2]

        try:
            if float(product_price) <= 0:
                raise ValueError()
        except ValueError:
            return jsonify(
                message='Incorrect price on line {line_number}.'.format(
                    line_number=line_number
                )
            ), 400

    stream.seek(0)
    csv_reader = csv.reader(stream)

    for line_number, line in enumerate(csv_reader):
        # print(line_number, line)

        product_name = line[1]

        if Product.query.filter_by(name=product_name).first():
            return jsonify(
                message='Product {product_name} already exists.'.format(
                    product_name=product_name
                )
            ), 400

    stream.seek(0)
    csv_reader = csv.reader(stream)

    for line_number, line in enumerate(csv_reader):
        # print(line_number, line)

        product_categories = line[0].split('|')
        product_name = line[1]
        product_price = float(line[2])

        print(product_categories)
        print(product_name)
        print(product_price)

        # flush vs commit, flush can give you rollback, commit calls flush

        product = Product(
            name=product_name,
            price=product_price
        )

        database.session.add(product)
        database.session.commit()

        for category_name in product_categories:
            category = Category.query.filter_by(name=category_name).first()

            if not category:
                category = Category(
                    name=category_name
                )

                database.session.add(category)
                database.session.commit()

            product_category = ProductCategory(
                product_id=product.id,
                category_id=category.id
            )

            database.session.add(product_category)
            database.session.commit()

    return Response()

@application.route('/product_statistics', methods=['GET'])
@role_check(valid_roles=['owner'])
def product_statistics():
    statistics = []

    query_sold = database.session.query(Product.name, func.sum(OrderProduct.quantity)).join(OrderProduct)\
        .filter(OrderProduct.product_id == Product.id).filter(OrderProduct.quantity > 0).join(Order)\
        .filter(OrderProduct.order_id == Order.id)\
        .filter(Order.status == OrderStatus.COMPLETE).group_by(Product.id).all()

    query_waiting = database.session.query(Product.name, func.sum(OrderProduct.quantity)).join(OrderProduct)\
        .filter(OrderProduct.product_id == Product.id).filter(OrderProduct.quantity > 0).join(Order)\
        .filter(OrderProduct.order_id == Order.id)\
        .filter(Order.status != OrderStatus.COMPLETE).group_by(Product.id).all()

    product_stats = {
    }

    for sold in query_sold:
        product_name = sold[0]
        product_sold = int(sold[1])

        if product_name not in product_stats:
            product_stats[product_name] = {
                'sold': product_sold,
                'waiting': 0,
            }
        else:
            product_stats[product_name]['sold'] += product_sold

    for waiting in query_waiting:
        product_name = waiting[0]
        product_waiting = int(waiting[1])

        if product_name not in product_stats:
            product_stats[product_name] = {
                'sold': 0,
                'waiting': product_waiting,
            }
        else:
            product_stats[product_name]['waiting'] += product_waiting

    for key, value in product_stats.items():
        product_name = key
        statistic = value
        statistic['name'] = product_name
        statistics.append(statistic)

    return jsonify(
        statistics=statistics,
    ), 200

@application.route('/category_statistics', methods=['GET'])
@role_check(valid_roles=['owner'])
def category_statistics():
    categories = database.session.query(Category.name).all()

    category_statistics = []
    for category_name in categories:
        name = category_name[0]
        print(name)

        count = database.session.query(func.sum(OrderProduct.quantity)).join(Product, Product.id == OrderProduct.product_id)\
        .filter(OrderProduct.quantity > 0).join(Order, Order.id == OrderProduct.order_id)\
        .join(ProductCategory, ProductCategory.product_id == Product.id)\
            .join(Category, Category.id == ProductCategory.category_id)\
            .filter(Category.name == name)\
        .filter(Order.status == OrderStatus.COMPLETE).group_by(Category.name)\
            .first()

        if count:
            category_statistics.append([name, int(count[0])])
        else:
            category_statistics.append([name, 0])

    category_statistics = sorted(category_statistics, key=lambda x: (-x[1], x[0]))

    return jsonify(
        statistics=[x[0] for x in category_statistics]
    ), 200


if __name__ == '__main__':
    database.init_app(application)

    application.run(debug=True, host='0.0.0.0', port=5001)
