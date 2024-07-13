from logging import getLogger

from telegram.ext import BaseHandler, CommandHandler, CallbackContext
from telegram import Update

from survey_bot.utils.decorators import check_permissions
from survey_bot.utils.secretkey import get_current_secret

logger = getLogger(__name__)


def getkey_command_handler() -> BaseHandler:
    """Обработка комманды /getkey. Получение секретного ключа"""

    @check_permissions(access_level='Admin')
    async def handler(update: Update, ctx: CallbackContext):
        key = get_current_secret()
        await update.message.reply_text('%s' % key)

    return CommandHandler("getkey", handler)
