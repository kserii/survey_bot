from telegram.ext import BaseHandler, CallbackContext, MessageHandler, filters
from telegram import Update


def echo_handler() -> BaseHandler:

    async def handler(update: Update, ctx: CallbackContext):
        await update.message.reply_text(update.message.text)

    return MessageHandler(filters.TEXT & ~filters.COMMAND, handler)
