from logging import getLogger
from itertools import cycle

from telegram.ext import BaseHandler, CommandHandler, CallbackContext
from telegram import Update

from survey_bot.utils.mongodb import insert_user, get_current_survey
from survey_bot.utils.send_notification import send_notifications

logger = getLogger(__name__)


def start_command_handler() -> BaseHandler:
    """Обработка комманды /start или первого сообщения в бота"""

    async def handler(update: Update, ctx: CallbackContext):
        await insert_user(update.effective_user.to_dict())
        # current_survey = await get_current_survey()
        # # TODO реализовать очитску или сохранение данных https://github.com/python-telegram-bot/python-telegram-bot/wiki/Storing-bot%2C-user-and-chat-related-data
        # ctx.user_data['survey'] = current_survey.get('id')
        # ctx.user_data['current_question'] = 0
        # ctx.user_data['questions_count'] = len(current_survey.get('questions', []))
        ctx.user_data['iterator'] = cycle(["fisting", "ass", "three", "hundert", "bucks"])
        await send_notifications("hello world!!!", [586274953, 6434347795, 7196168734])
        await update.message.reply_text(text="I'm a bot, please talk to me!")

    return CommandHandler("start", handler)
