from logging import getLogger

from telegram.ext import BaseHandler, CallbackContext, CallbackQueryHandler
from telegram import Update

from survey_bot.utils.send_next_message import send_next_message

logger = getLogger(__name__)


def question_inline_command_handler() -> BaseHandler:
    """Обработка ответов на вопросы с ответами (inline keyboard)"""

    async def handler(update: Update, ctx: CallbackContext):
        survey = ctx.user_data['survey']
        logger.debug(survey)
        query = update.callback_query
        # TODO запись в базу
        question_id, answer = query.data.split(',', 1)
        question_id = int(question_id)
        logger.debug(query.message)

        await query.answer()
        await query.delete_message()
        await send_next_message(ctx, query.message.chat.id, survey)

    return CallbackQueryHandler(handler)
