from logging import getLogger

from telegram.ext import BaseHandler, CommandHandler, CallbackContext
from telegram import Update

from survey_bot.utils.decorators import check_permissions
from survey_bot.utils.mongodb import set_admin_to_user
from survey_bot.utils.secretkey import get_current_secret

logger = getLogger(__name__)

ADMIN_SUCCESS_TEXT = "Всё верно! Ты получил админку"


def getadmin_command_handler() -> BaseHandler:
    """Обработка комманды /getadmin. Получение прав администратора"""

    @check_permissions(access_level='User')
    async def handler(update: Update, ctx: CallbackContext):
        key = ''.join(ctx.args)
        if get_current_secret() == key:
            await set_admin_to_user(update.effective_user.to_dict())
            await update.message.reply_text(ADMIN_SUCCESS_TEXT)

    return CommandHandler("getadmin", handler)
