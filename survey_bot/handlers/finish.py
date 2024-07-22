from logging import getLogger

from telegram.ext import BaseHandler, CommandHandler, CallbackContext
from telegram import Update

from survey_bot.utils.decorators import check_permissions
from survey_bot.utils.mongodb import update_active_survey

logger = getLogger(__name__)

SURVEY_IS_FINISH = 'Опрос окончен'


def finish_command_handler() -> BaseHandler:
    """Обработка комманды /finish. Завершение опроса"""

    @check_permissions(access_level='Admin')
    async def handler(update: Update, ctx: CallbackContext):
        result = await update_active_survey(None)
        if result:
            await update.message.reply_text(SURVEY_IS_FINISH)

    return CommandHandler("finish", handler)
