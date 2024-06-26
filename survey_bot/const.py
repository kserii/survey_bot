from os import environ

MONGO_CONNECTION_URL = environ.get("MONGO_CONNECTION_URL") or "mongodb://root:pass@mongodb:27017"
TEST_MONGO_CONNECTION_URL = environ.get("TEST_MONGO_CONNECTION_URL") or "mongodb://root:pass@mongodb:27017"
BOT_TOKEN = environ.get("BOT_TOKEN") or "INVALID_TOKEN"
LOG_LEVEL = environ.get("LOG_LEVEL") or "DEBUG"

# Список telegram id админов бота для отдельных команд.
BOT_OWNER_IDS = list(
    map(lambda owner: int(owner) if owner else -1,
        (environ.get("BOT_OWNER_IDS") or "").split(","))
)
