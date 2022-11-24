import os

MONGO_USER = os.environ.get("MONGO_ROOT_USERNAME")
MONGO_PASS = os.environ.get("MONGO_ROOT_PASSWORD")
MONGO_DATABASE = os.environ.get("MONGO_DATABASE")
MONGO_PORT = os.environ.get("MONGO_PORT")
MONGO_HOST = os.environ.get("MONGO_HOST")

ITEMS_PER_PAGE = 10