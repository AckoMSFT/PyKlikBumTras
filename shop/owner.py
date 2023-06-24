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

if __name__ == '__main__':
    database.init_app(application)

    application.run(debug=True, host='0.0.0.0', port=5001)
