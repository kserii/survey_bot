from logging import getLogger

from telegram.ext import BaseHandler, CommandHandler, CallbackContext
from telegram import Update

from survey_bot.utils.decorators import check_permissions

logger = getLogger(__name__)


def finish_command_handler() -> BaseHandler:
    """Обработка комманды /finish. Завершение опроса"""

    @check_permissions(access_level='Admin')
    async def handler(update: Update, ctx: CallbackContext):
        ...

    return CommandHandler("finish", handler)
