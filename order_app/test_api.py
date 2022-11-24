import pytest


@pytest.fixture()
def app():
    from . import app
    app.config.update({
        "TESTING": True
    })

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_order_detail(client):
    response = client.get("/order/637f63fd21e2ab35ed015da5")

    assert response.json["product_count"] == 3

    assert isinstance(response.json["products"], list)

    assert isinstance(response.json["products"][0], dict)    

    assert "id" in response.json["products"][0]

    assert "measurement" in response.json["products"][0]

    assert "name" in response.json["products"][0]

    assert "quantity" in response.json["products"][0]


def test_order_detail_error(client):
    response = client.get("/order/xxxxxxx")

    assert response.status_code == 404


def test_average_product_count(client):
    response = client.get("/order/average-product-count")

    assert response.json["average_of_products_in_orders"] == 2.86


def test_average_product_quantity(client):
    response = client.get("/order/average-product-quantity/637f63fd21e2ab35ed015d9f")

    assert response.json["average_of_products_in_orders"]['product'] == "Tomato"

    assert isinstance(response.json["average_of_products_in_orders"]['average_quantity'], list)


def test_average_product_quantity(client):
    response = client.get("/order/average-product-quantity/xxxxx")

    assert response.status_code == 404
