import click
from mongoengine.errors import ValidationError

from .order import Order, OrderItem, Product

DEFAULT_DATA = [{"order_id":1,"product_count":3,"products":[{"id":1,"measurement":"Kg","name":"Tomato","quantity":2},
                                                      {"id":4,"measurement":"Piece","name":"Eggs","quantity":6},
                                                      {"id":5,"measurement":"Pack","name":"Orange Juice","quantity":1}]},
          {"order_id":2,"product_count":4,"products":[{"id":3,"measurement":"Pack","name":"Bread","quantity":1},
                                                      {"id":7,"measurement":"Pack","name":"Milk","quantity":2},
                                                      {"id":1,"measurement":"Kg","name":"Tomato","quantity":1},
                                                      {"id":2,"measurement":"Kg","name":"Apple","quantity":1}]},
          {"order_id":3,"product_count":3,"products":[{"id":7,"measurement":"Pack","name":"Milk","quantity":2},
                                                      {"id":6,"measurement":"Pack","name":"Chips","quantity":2},
                                                      {"id":5,"measurement":"Pack","name":"Orange Juice","quantity":1}]},
          {"order_id":4,"product_count":2,"products":[{"id":3,"measurement":"Pack","name":"Bread","quantity":1},
                                                      {"id":2,"measurement":"Kg","name":"Apple","quantity":2}]},
          {"order_id":5,"product_count":4,"products":[{"id":5,"measurement":"Pack","name":"Orange Juice","quantity":2},
                                                      {"id":6,"measurement":"Pack","name":"Chips","quantity":2},
                                                      {"id":7,"measurement":"Pack","name":"Milk","quantity":1},
                                                      {"id":8,"measurement":"Pack","name":"Ketchup","quantity":2}]},
          {"order_id":6,"product_count":2,"products":[{"id":6,"measurement":"Pack","name":"Chips","quantity":3},
                                                      {"id":7,"measurement":"Pack","name":"Milk","quantity":1}]},
          {"order_id":7,"product_count":2,"products":[{"id":1,"measurement":"Kg","name":"Tomato","quantity":2},
                                                      {"id":2,"measurement":"Kg","name":"Apple","quantity":1}]}]


def init_db():  
    existing_orders = Order.objects.all().only('id')
    if existing_orders:
        pass
    else:
        for order_data in DEFAULT_DATA:
            items = []
            for item in order_data['products']:
                try:
                    product = Product.objects.get(name=item['name'])
                except (ValidationError, Product.DoesNotExist):
                    product = Product(name=item['name'])
                    product.save()
                item = OrderItem(
                    product=product,
                    measurement=item['measurement'],
                    quantity=item['quantity'])
                item.save()
                items.append(item)
            order = Order(product_count=len(items), order_items=items)
            order.save()


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.cli.add_command(init_db_command)