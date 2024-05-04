from logging import getLogger
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

from survey_bot.const import MONGO_CONNECTION_URL

logger = getLogger(__name__)

client = AsyncIOMotorClient(MONGO_CONNECTION_URL)
db = client.get_database('survey_bot')


async def ping_server():
    # Replace the placeholder with your Atlas connection string
    uri = MONGO_CONNECTION_URL
    # Set the Stable API version when creating a new client
    test_client = AsyncIOMotorClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        await test_client.admin.command('ping')
        logger.debug("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        logger.exception(e)
    finally:
        test_client.close()


async def insert_user(user: dict):
    """Добавляет в базу одного уникального пользователя"""
    telegram_users_collection = db.get_collection('telegram_users')
    if not await telegram_users_collection.find_one({'id': user['id']}):
        await telegram_users_collection.insert_one(user)


async def get_current_survey() -> Optional[dict]:
    """Получить текущий опрос"""
    surveys_collection = db.get_collection('surveys')
    survey = await surveys_collection.find_one({
        "is_active": True
    })
    survey["questions"] = iter(survey["questions"])
    return survey
