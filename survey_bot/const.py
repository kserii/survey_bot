from os import environ

MONGO_CONNECTION_URL = environ.get("MONGO_CONNECTION_URL") or "mongodb://mongodb:27017"
BOT_TOKEN = environ.get("BOT_TOKEN") or "INVALID_TOKEN"
LOG_LEVEL = environ.get("LOG_LEVEL") or "DEBUG"
