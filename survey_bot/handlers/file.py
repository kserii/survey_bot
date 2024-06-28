import csv
import io
from datetime import datetime
from asyncio import Lock
from logging import getLogger

from telegram.ext import BaseHandler, CallbackContext, MessageHandler, filters
from telegram import Update

from survey_bot.utils.decorators import check_permissions
from survey_bot.utils.mongodb import insert_new_survey_and_update_current
from survey_bot.utils.types import Survey

logger = getLogger(__name__)

FILE_IS_INVALID = "Данный файл невозможно обработать! Файл должен быть в формате .csv c разделителем ';'"

lock = Lock()


async def make_survey_from_csv(data: bytearray, update: Update) -> Survey:
    """Возвращает опрос"""
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
            survey['questions'].append({
                'question_name': row[fieldnames[0]],  # Вопрос
                'question_options': list(filter(
                    lambda value: value.strip(' .-\t\n'),
                    [row[option] for option in fieldnames[1:]]
                ))  # Варианты
            })
    except Exception as e:
        await update.message.reply_text("%s\n\n\nОшибка: %s" % (FILE_IS_INVALID, e))
    finally:
        file.close()
    return survey


def file_processing_handler() -> BaseHandler:
    """Обработка файла"""

    @check_permissions(access_level='Admin')
    async def handler(update: Update, ctx: CallbackContext):
        async with lock:
            logger.debug('file is: %s', update.message.document)
            if update.message.document.mime_type != 'text/csv':
                return
            file = await update.message.document.get_file()
            data = await file.download_as_bytearray()
            survey = await make_survey_from_csv(data, update)
            await insert_new_survey_and_update_current(survey)

    return MessageHandler(filters.Document.ALL, handler)


def downloader(update, context):
    context.bot.get_file(update.message.document).download()

    # writing to a custom file
    with open("custom/file.doc", 'wb') as f:
        context.bot.get_file(update.message.document).download(out=f)