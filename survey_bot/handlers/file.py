import csv
import io
import traceback
from datetime import datetime
from asyncio import Lock
from logging import getLogger

from telegram.ext import BaseHandler, CallbackContext, MessageHandler, filters
from telegram import Update

from survey_bot.utils.decorators import check_permissions
from survey_bot.utils.mongodb import insert_new_survey_and_update_current
from survey_bot.utils.notifications import send_notifications_all_users
from survey_bot.utils.types import Survey

logger = getLogger(__name__)

FILE_IS_INVALID_TEXT = "Данный файл невозможно обработать! Файл должен быть в формате .csv c разделителем ';'"
SUCCESS_ADD_SURVEY_TEXT = "Новый опрос добавлен"
NOTIFICATION_ADD_NEW_SURVEY_TEXT = 'Добавлен новый опрос, пожалуйста, пройдите его:\n/vote'

lock = Lock()


async def _make_survey_from_csv(data: bytearray, update: Update) -> Survey:
    """Обрабатываетм .csv файл и возвращает объект опроса"""
    survey = {
        'id': -1,
        'questions': [],
        'created_at': datetime.now()
    }

    data_str = data.decode('utf-8')
    file = io.StringIO(data_str)
    try:
        csv_reader = csv.DictReader(file, delimiter=';')
        fieldnames = csv_reader.fieldnames
        if fieldnames[0].startswith('\ufeff'):
            fieldnames[0] = fieldnames[0].replace('\ufeff', '')
        csv_reader.fieldnames = fieldnames
        for row in csv_reader:
            question_name = row[fieldnames[0]]
            question_options = list(filter(
                lambda value: value.strip(' .-\t\n'),
                [row[option] for option in fieldnames[1:]]
            ))
            survey['questions'].append({
                'question_name': question_name,
                'question_options': question_options or None  # Варианты
            })
    except Exception as e:
        await update.message.reply_text("%s\n\nОшибка: %s" % (FILE_IS_INVALID_TEXT, traceback.format_exc()))
    finally:
        file.close()
    return survey


def file_processing_handler() -> BaseHandler:
    """Добавление файла с опросом"""

    @check_permissions(access_level='Admin')
    async def handler(update: Update, ctx: CallbackContext):
        async with lock:
            if update.message.document.mime_type != 'text/csv':
                return
            file = await update.message.document.get_file()
            data = await file.download_as_bytearray()
            survey = await _make_survey_from_csv(data, update)
            result = await insert_new_survey_and_update_current(survey)

            if result:
                await update.effective_chat.send_message(SUCCESS_ADD_SURVEY_TEXT)
                await send_notifications_all_users(NOTIFICATION_ADD_NEW_SURVEY_TEXT, ctx)

    return MessageHandler(filters.Document.ALL, handler)
