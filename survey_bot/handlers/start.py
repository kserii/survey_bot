from logging import getLogger
from telegram.ext import BaseHandler, CommandHandler, CallbackContext
from telegram import Update

from survey_bot.utils.mongodb import insert_user

logger = getLogger(__name__)


def start_command_handler() -> BaseHandler:
    """Обработка комманды /start или первого сообщения в бота"""

    async def handler(update: Update, ctx: CallbackContext):
        await insert_user(update.effective_user.to_dict())
        await update.message.reply_text(text="I'm a bot, please talk to me!")

    return CommandHandler("start", handler)
