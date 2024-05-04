from logging import getLogger

from telegram.ext import BaseHandler, CallbackContext, MessageHandler, filters
from telegram import Update

from survey_bot.utils.mongodb import get_current_survey

logger = getLogger(__name__)

SURVEY_FINISH_TEXT = 'Опрос окончен, спасибо за уделенное время!'


def echo_handler() -> BaseHandler:
    async def handler(update: Update, ctx: CallbackContext):
        logger.debug("%s", ctx.user_data)
        current_survey = ctx.user_data.get("survey") or await get_current_survey()
        try:
            questions = current_survey["questions"]
            await update.message.reply_text(next(questions)["name"])
        except StopIteration:
            await update.message.reply_text(SURVEY_FINISH_TEXT)
        # await update.message.reply_text(update.message.text)

    return MessageHandler(filters.TEXT & ~filters.COMMAND, handler)
