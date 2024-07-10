import csv
import io
import traceback
import json
from datetime import datetime
from logging import getLogger
from typing import List

from telegram.ext import BaseHandler, CommandHandler, CallbackContext
from telegram import Update, InputFile

from survey_bot.utils.decorators import check_permissions
from survey_bot.utils.mongodb import select_all_answers_by_survey, get_current_survey
from survey_bot.utils.types import UserAnswers

logger = getLogger(__name__)

NO_HAVE_ANSWERS_TEXT = "Пока нет ответов по данному опросу"
ERROR_WHILE_MAKE_CSV = "В процессе создание .CSV произошла ошибка"


def _get_username(user_answers: UserAnswers) -> str:
    user_info = user_answers.get('user_info')
    if not user_info:
        return str(user_answers['user_id'])

    user_info = user_info[0]

    username = user_info.get('username')
    if username:
        return f'@{username}'

    first_name = user_info.get('first_name', '')
    last_name = user_info.get('last_name', '')

    if first_name or last_name:
        return '%s %s' % (first_name, last_name)

    return str(user_answers['user_id'])


async def _export_csv(update: Update, answers: List[UserAnswers], current_survey_id: int):
    """Отправка данных в формате .csv"""
    file = io.StringIO()
    try:
        fieldnames = ['Пользователь', 'Вопрос', 'Ответ']
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for user_answers in answers:
            username = _get_username(user_answers)
            for answer in user_answers['answers']:
                question_text = answer['question']
                answer_text = answer['answer']
                writer.writerow({
                    fieldnames[0]: username,
                    fieldnames[1]: question_text,
                    fieldnames[2]: answer_text
                })
        filename = "report-%s-%s.csv" % (current_survey_id, datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
        doc = InputFile(file.getvalue(), filename=filename)

        await update.effective_sender.send_document(doc)
    except Exception as e:
        await update.message.reply_text("%s\n\n\nОшибка: %s" % (ERROR_WHILE_MAKE_CSV, traceback.format_exc()))
    finally:
        file.close()


async def _export_human_txt(update: Update, users_answers: List[UserAnswers], current_survey_id: int):
    """Отправка данных читаемом формате"""
    txt_rows = []

    for user_answers in users_answers:
        user_rows = ["Ответы пользователя %s:" % _get_username(user_answers)]
        for idx, answer in enumerate(user_answers['answers']):
            user_rows.append("Вопрос #%s '%s': %s" % (idx, answer['question'], answer['answer']))
        txt_rows.append('\n\t'.join(user_rows))

    txt_data = '\n\n'.join(txt_rows)

    filename = "report-%s-%s.txt" % (current_survey_id, datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
    doc = InputFile(txt_data, filename=filename)

    await update.effective_sender.send_document(doc)


async def _export_json(update: Update, answers: List[UserAnswers], current_survey_id: int):
    """Отправка данных об ответах в формате JSON"""

    json_data = json.dumps(answers, ensure_ascii=False, indent=4)
    filename = "report-%s-%s.json" % (current_survey_id, datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))

    doc = InputFile(json_data, filename=filename)

    await update.effective_sender.send_document(doc)


def export_json_command_handler() -> BaseHandler:
    """Обработка комманды /export. Отправляет отчет об ответах на текущий опрос"""

    @check_permissions(access_level='Admin')
    async def handler(update: Update, ctx: CallbackContext):
        current_survey = await get_current_survey()
        answers = await select_all_answers_by_survey(survey_id=current_survey['id'])

        if not answers:
            await update.message.reply_text(NO_HAVE_ANSWERS_TEXT)
            return

        await _export_json(update, answers, current_survey['id'])
        await _export_human_txt(update, answers, current_survey['id'])
        await _export_csv(update, answers, current_survey['id'])

    return CommandHandler("export", handler)
