import datetime
from logging import getLogger
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

from survey_bot.const import MONGO_CONNECTION_URL
from survey_bot.utils.types import BotOptions, Survey, User

logger = getLogger(__name__)

client = AsyncIOMotorClient(MONGO_CONNECTION_URL)
db = client.get_database('survey_bot')

# Collections
SurveysCollection = db.get_collection('surveys')
TelegramUsersCollection = db.get_collection('telegram_users')
AnswersCollection = db.get_collection('answers')
OptionsCollection = db.get_collection('options')


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


async def insert_user(user: User):
    """Добавляет в базу одного уникального пользователя"""
    if not await TelegramUsersCollection.find_one({'id': user['id']}):
        await TelegramUsersCollection.insert_one(user)


async def get_current_survey() -> Optional[Survey]:
    """Получить текущий опрос"""
    options = get_options()
    survey = await SurveysCollection.find_one({
        'id': options['active_survey']
    })
    survey['questions_count'] = len(survey.get('questions', []))
    survey['questions'] = iter(survey.get('questions', []))
    return survey


async def get_options() -> Optional[BotOptions]:
    """Получает состояние и настройки бота"""
    options = await OptionsCollection.find_one()
    return options
