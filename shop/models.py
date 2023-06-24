import datetime
import enum

from flask_sqlalchemy import SQLAlchemy

MAX_LENGTH = 256
database = SQLAlchemy()

class Product(database.Model):
    __tablename__ = 'product'

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(MAX_LENGTH), nullable=False)
    price = database.Column(database.Float, nullable=False)

    categories = database.relationship(
        'Category',
        secondary='product_category',
        lazy='subquery',
        backref=database.backref('product', lazy=True)
    )

    def to_json(self):
        return {
            'categories': [
                category.name for category in self.categories
            ],
            'id': self.id,
            'name': self.name,
            'price': self.price
        }

class Category(database.Model):
    __tablename__ = 'category'

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(MAX_LENGTH), nullable=False)

class ProductCategory(database.Model):
    __tablename__ = 'product_category'

    id = database.Column(database.Integer, primary_key=True)
    product_id = database.Column(database.Integer, database.ForeignKey('product.id'), nullable=False)
    category_id = database.Column(database.Integer, database.ForeignKey('category.id'), nullable=False)

class OrderStatus(enum.Enum):
    CREATED = 0,
    PENDING = 1,
    COMPLETE = 2

class Order(database.Model):
    __tablename__ = 'order'

    id = database.Column(database.Integer, primary_key=True)
    price = database.Column(database.Float, nullable=False, default=0)
    status = database.Column(database.Enum(OrderStatus), nullable=False)
    timestamp = database.Column(database.TIMESTAMP, nullable=False, default=datetime.datetime.now())
    email = database.Column(database.String(MAX_LENGTH), nullable=False)

    products = database.relationship(
        'Product',
        secondary='order_product',
        lazy='subquery',
        backref=database.backref('order', lazy=True)
    )

    def to_json(self):
        order_products = OrderProduct.query.filter_by(order_id=self.id).all()
        return {
            'products': [
                order_product.to_json() for order_product in order_products
            ],
            'price': self.price,
            'status': self.status.name,
            'timestamp': self.timestamp.isoformat()
        }

class OrderProduct(database.Model):
    __tablename__ = 'order_product'

    id = database.Column(database.Integer, primary_key=True)
    order_id = database.Column(database.Integer, database.ForeignKey('order.id'), nullable=False)
    product_id = database.Column(database.Integer, database.ForeignKey('product.id'), nullable=False)
    quantity = database.Column(database.Integer, nullable=False)
    # No need to keep this here...
    price = database.Column(database.Float, nullable=False)

    def to_json(self):
        product = Product.query.filter_by(id=self.product_id).first()
        product_json = product.to_json()

        del product_json['id']
        product_json['quantity'] = self.quantity

        return product_json
