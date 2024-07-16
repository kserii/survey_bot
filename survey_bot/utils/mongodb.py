from logging import getLogger
from typing import Optional, List

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

from survey_bot.const import MONGO_CONNECTION_URL, BOT_OWNER_IDS
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
    """Добавляет в базу пользователя. Если уже есть - не будет добавлен"""
    user_from_db = await TelegramUsersCollection.find_one({'id': user['id']})
    if not user_from_db:
        await TelegramUsersCollection.insert_one({
            **user,
            'is_admin': user['id'] in BOT_OWNER_IDS
        })


async def set_admin_to_user(user: User):
    await TelegramUsersCollection.update_one(
        {'id': user['id']},
        {'$set': {
            'is_admin': True
        }}
    )


async def select_user(telegram_id: int) -> Optional[User]:
    """Получение пользователя из базы данных по telegram id"""
    return await TelegramUsersCollection.find_one({'id': telegram_id})


async def select_all_users() -> Optional[List[User]]:
    """Получение всех пользователей"""
    users_cursor = TelegramUsersCollection.find()
    users = [user async for user in users_cursor]
    return users


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
    """Сохраняет ответы в базу данных"""
    logger.debug('User: %s\n'
                 'Answers: %s', user, answers)
    user_answers = {
        'answers': answers,
        'user_id': user['id'],
        'survey_id': survey['id']
    }
    await AnswersCollection.insert_one(user_answers)


async def select_answers(user_id: int, survey_id: int) -> Optional[UserAnswers]:
    """Получение ответов по id пользователя и id опроса"""
    answer: UserAnswers = await AnswersCollection.find_one({
        'user_id': user_id,
        'survey_id': survey_id
    })
    return answer


async def select_all_answers_by_survey(survey_id: int) -> List[UserAnswers]:
    """Получение ответов по id пользователя и id опроса"""
    pipeline = [
        {
            '$match': {'survey_id': survey_id}
        },
        {
            '$lookup': {
                'from': 'telegram_users',  # The collection to join
                'localField': 'user_id',  # Field from the answers collection
                'foreignField': 'id',  # Field from the telegram_users collection
                'as': 'user_info'  # Output array field
            }
        },
        {
            '$project': {  # Exclude the _id field
                '_id': 0,
                'user_info': {
                    '_id': 0
                }
            }
        }
    ]

    results = []
    async for doc in AnswersCollection.aggregate(pipeline):
        results.append(UserAnswers(**doc))

    return results


async def insert_new_survey_and_update_current(survey: Survey):
    if survey['id'] == -1:
        max_doc = await SurveysCollection.find_one(sort=[('id', -1)])
        survey['id'] = max_doc['id'] + 1
    await SurveysCollection.insert_one(survey)
    result = await update_active_survey(survey['id'])
    return result.modified_count


async def update_active_survey(survey_id: Optional[int]):
    result = await OptionsCollection.update_one(
        {'name': 'options'},
        {"$set": {'active_survey': survey_id}})
    return result
