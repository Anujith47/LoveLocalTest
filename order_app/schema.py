from mongoengine.errors import ValidationError

from . import db


class Order(db.Document):
    """
    Schema of an order.
    """
    product_count = db.IntField()
    order_items = db.ListField(db.ReferenceField('OrderItem'))

    def to_json(self):
        return {"order_id": str(self.id),
                "product_count": self.product_count,
                "products": [item.to_json() for item in self.order_items]}

    @classmethod
    def create(cls, data):
        """
        Classmethod can be used to create Orded

        params
        data: dict

        sample data format --> {
                                'products': [{'measurement': 'KG',
                                              'name': 'Apple',
                                              'quantity': 2},
                                             { ......     },
                                             { .....      }]
                                }
        """
        items = []
        for item in data['products']:
            try:
                product = Product.objects.get(name=item['name'])
            except (ValidationError, Product.DoesNotExist):
                product = Product.create(name=item['name'])
            item = OrderItem.create(product, item)
            items.append(item)
        order = cls(product_count=len(items), order_items=items)
        order.save()
        return order

    @classmethod
    def bulk_create(cls, data):
        """
        used to create mmultiple order objects
        params
        data: list

        """
        orders = []
        for order_data in data:
            order = cls.create(order_data)
            orders.append(order)
        return orders


class OrderItem(db.Document):
    """
    Represents a single item in an order
    """
    product = db.ReferenceField('Product')
    measurement = db.StringField()
    quantity = db.FloatField()

    meta = {
        'indexes': [('product', 'measurement', 'quantity')]
    }

    def to_json(self):
        return {"id": str(self.id),
                "name": self.product.name,
                "product_id": str(self.product.id),
                "measurement": self.measurement,
                "quantity": self.quantity}

    @classmethod
    def create(cls, product, data):
        item = cls(
            product=product,
            measurement=data['measurement'],
            quantity=data['quantity'])
        item.save()
        return item


class Product(db.Document):
    """
    Represents a product
    """
    name = db.StringField(unique=True)

    def to_json(self):
        return {"id": str(self.id), "name": self.name}

    @classmethod
    def create(cls, name):
        product = cls(name=name)
        product.save()
        return product
