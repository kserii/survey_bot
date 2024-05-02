from telegram.ext import BaseHandler, CommandHandler, CallbackContext
from telegram import Update


def start_command_handler() -> BaseHandler:
    """Обработка комманды /start или первого сообщения в бота"""

    async def handler(update: Update, ctx: CallbackContext):
        await update.message.reply_text(text="I'm a bot, please talk to me!")

    return CommandHandler("start", handler)
