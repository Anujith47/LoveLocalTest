import click
from mongoengine.errors import ValidationError

from .order import Order, OrderItem, Product
from .default_data import DEFAULT_DATA


def init_db():  
    # check if there is any existing orders
    existing_orders = Order.objects.all().only('id')
    if existing_orders:
        pass
    else:
        Order.bulk_create(DEFAULT_DATA)


@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    # register the custom command
    app.cli.add_command(init_db_command)