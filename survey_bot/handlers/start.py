from logging import getLogger

from telegram.ext import BaseHandler, CommandHandler, CallbackContext
from telegram import Update

from survey_bot.utils.mongodb import insert_user, select_user

logger = getLogger(__name__)

WELLCOME_TEXT = "Привет! Чтобы пройти опрос пиши: /vote"


def start_command_handler() -> BaseHandler:
    """Обработка комманды /start или первого сообщения в бота"""

    async def handler(update: Update, ctx: CallbackContext):
        await insert_user(update.effective_user.to_dict())
        ctx.user_data['user'] = await select_user(update.effective_user.id)
        await update.message.reply_text(WELLCOME_TEXT)

    return CommandHandler("start", handler)
