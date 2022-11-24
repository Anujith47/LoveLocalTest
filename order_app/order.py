from flask import (
    Blueprint, jsonify, abort
)
from mongoengine.errors import ValidationError

from .schema import Order, OrderItem, Product


bp = Blueprint('order', __name__, url_prefix='/order')


@bp.route('/<order_id>', methods=('GET',))
def order_detail(order_id):
    """
    Returns details of a single order
    """
    try:
        order = Order.objects.get(id=order_id).select_related(2)
    except (ValidationError, Order.DoesNotExist):
        order = None
    if order:
        return jsonify(order.to_json())
    else:
        return abort(404, description='Order Not Found')


@bp.route('/average-product-count', methods=('GET',))
def average_product_count():
    """
    Returns the average of all the product counts of an order in the database
    """
    pipe = [
        {"$group": {"_id": None, "average": {"$avg": "$product_count"}}}]
    try:
        average = round(next(Order.objects().aggregate(pipe))['average'], 2)
    except StopIteration:
        return abort(404, description='No orders with valid values')
    return jsonify({'average_of_products_in_orders': average})


@bp.route('average-product-quantity/<product_id>', methods=('GET',))
def average_product_quantity(product_id):
    """
    Returns the average quantity of all the orded items of a specific product
    """
    try:
        product = Product.objects.get(id=product_id)
    except (ValidationError, Product.DoesNotExist):
        product = None
    if product:
        data = {
            "product": product.name,
            "product_id": str(product.id),
            "average_quantity": []}
        pipe = [
            {"$match": {"product": product.id}},
            {"$group": {
                "_id": "$measurement", "average": {"$avg": "$quantity"}}}]
        results = OrderItem.objects().aggregate(pipe)
        for result in results:
            data["average_quantity"].append(
                {result["_id"]: round(result["average"], 2)})

        return jsonify(data)
    else:
        return abort(404, description='Product Not Found')
