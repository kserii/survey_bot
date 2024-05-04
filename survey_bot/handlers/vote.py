from logging import getLogger

from telegram.ext import BaseHandler, CommandHandler, CallbackContext
from telegram import Update

from survey_bot.utils.send_next_message import send_next_message
from survey_bot.utils.mongodb import get_current_survey

logger = getLogger(__name__)

DONT_HAVE_ACTIVE_SURVEYS = "Сейчас нет активных опросов"


def vote_command_handler() -> BaseHandler:
    """Обработка комманды /vote. Участие в опросе"""

    async def handler(update: Update, ctx: CallbackContext):
        # TODO реализовать очитску или сохранение данных
        #  https://github.com/python-telegram-bot/python-telegram-bot/wiki/Storing-bot%2C-user-and-chat-related-data
        ctx.user_data['survey'] = await get_current_survey()
        survey = ctx.user_data['survey']
        logger.debug(survey)
        if survey:
            await send_next_message(ctx, update.message.chat_id, survey)
        else:
            await update.message.reply_text(DONT_HAVE_ACTIVE_SURVEYS)

    return CommandHandler("vote", handler)
