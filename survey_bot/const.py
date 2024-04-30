from os import environ

MONGO_CONNECTION_URL = environ.get("MONGO_CONNECTION_URL") or "mongodb://mongodb:27017"



