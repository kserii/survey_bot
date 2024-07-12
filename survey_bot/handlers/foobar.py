from logging import getLogger

from telegram.ext import BaseHandler, CommandHandler, CallbackContext
from telegram import Update

from survey_bot.utils.decorators import check_permissions

logger = getLogger(__name__)


def foobar_command_handler() -> BaseHandler:
    """Обработка комманды /foobar. ДАННЫЙ ОБРАБОТЧИК ДЛЯ РАЗРАБОТКИ И ТЕСТИРОВАНИЯ НЕКОТОРЫХ ФИЧЕЙ"""

    @check_permissions(access_level='Admin')
    async def handler(update: Update, ctx: CallbackContext):
        ...

    return CommandHandler("foobar", handler)
