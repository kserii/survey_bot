import datetime
from logging import getLogger
from typing import Optional, List

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

from survey_bot.const import MONGO_CONNECTION_URL
from survey_bot.utils.types import BotOptions, Survey, User, UserAnswers, Answer

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
    options = await get_options()
    survey: Survey = await SurveysCollection.find_one({
        'id': options['active_survey']
    })
    return survey


async def get_options() -> Optional[BotOptions]:
    """Получает состояние и настройки бота"""
    options = await OptionsCollection.find_one({'name': 'options'})
    logger.debug('Bot options: %s', options)
    return options


async def save_answers(user: User, survey: Survey, answers: List[Answer]):
    logger.debug('User: %s\n'
                 'Answers: %s', user, answers)
    user_answers: UserAnswers = {
        'answers': answers,
        'user_id': user['id'],
        'survey_id': survey['id']
    }
    await AnswersCollection.insert_one(user_answers)


async def select_answer(user_id: int, survey_id: int) -> Optional[UserAnswers]:
    answer: UserAnswers = await AnswersCollection.find_one({
        'user_id': user_id,
        'survey_id': survey_id
    })
    return answer
