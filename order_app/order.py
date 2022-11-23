from flask import (
    Blueprint, request, jsonify, abort
)
from mongoengine.errors import ValidationError


from . import db

bp = Blueprint('order', __name__, url_prefix='/order')


class Order(db.Document):
    product_count = db.IntField()
    order_items = db.ListField(db.ReferenceField('OrderItem'))

    def to_json(self):
        return {"order_id": str(self.id),
                "product_count": self.product_count,
                "products": [item.to_json() for item in self.order_items]}


class OrderItem(db.Document):
    product = db.ReferenceField('Product')
    measurement = db.StringField()
    quantity = db.FloatField()

    def to_json(self):
        return {"id": str(self.id),
                "name": self.product.name,
                "product_id": str(self.product.id),
                "measurement": self.measurement,
                "quantity": self.quantity}


class Product(db.Document):
    name = db.StringField(unique=True)


@bp.route('/<order_id>', methods=('GET',))
def order_detail(order_id):
    try:
        order = Order.objects.get(id=order_id).select_related()
    except (ValidationError, Order.DoesNotExist):
        order = None
    if order:
        return jsonify(order.to_json())
    else:
        return abort(404, description='Order Not Found')


@bp.route('/average-product-count', methods=('GET',))
def average_product_count():
    pipe = [
        {"$group": {"_id":None, "average": {"$avg": "$product_count"}}}]
    try:
        average = next(Order.objects().aggregate(pipe))['average']
    except StopIteration:
        return abort(404, description='No orders with valid values')
    return jsonify({'average_of_products_in_orders': average})


@bp.route('average-product-quantity/<product_id>', methods=('GET',))
def average_product_quantity(product_id):
    try:
        product = Product.objects.get(id=product_id)
    except (ValidationError, Order.DoesNotExist):
        order = None
    if product:
        data = {
            "product": product.name,
            "product_id": str(product.id),
            "average_quantity": []}
        pipe = [
            {"$match": {"product": product.id}},
            {"$group": {"_id": "$measurement", "average": {"$avg": "$quantity"}}}]
        results = OrderItem.objects().aggregate(pipe)
        for result in results:
            data["average_quantity"].append({result["_id"]: result["average"]})

        return jsonify(data)
    else:
        return abort(404, description='Product Not Found')