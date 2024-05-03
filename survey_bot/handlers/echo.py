from logging import getLogger

from telegram.ext import BaseHandler, CallbackContext, MessageHandler, filters
from telegram import Update

logger = getLogger(__name__)


def echo_handler() -> BaseHandler:
    async def handler(update: Update, ctx: CallbackContext):
        logger.debug("%s", ctx.user_data)
        await update.message.reply_text(next(ctx.user_data["iterator"]))
        # await update.message.reply_text(update.message.text)

    return MessageHandler(filters.TEXT & ~filters.COMMAND, handler)
