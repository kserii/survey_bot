from logging import getLogger

from telegram.ext import BaseHandler, CallbackContext, CallbackQueryHandler
from telegram import Update

from survey_bot.utils.decorators import check_context
from survey_bot.utils.next_message import next_message
from survey_bot.utils.types import Survey

logger = getLogger(__name__)


def question_inline_command_handler() -> BaseHandler:
    """Обработка ответов на вопросы с ответами (inline keyboard)"""

    @check_context
    async def handler(update: Update, ctx: CallbackContext):
        survey: Survey = ctx.user_data['survey']

        query = update.callback_query
        question_id, answer_id = map(int, query.data.split(',', 1))

        question_value: str = survey['questions'][question_id]['question_name']
        answer_value: str = survey['questions'][question_id]['question_options'][answer_id]

        answer = {
            'question': question_value,
            'answer': answer_value
        }

        logger.info('Получен ответ от пользователя %s: %s', update.effective_user.id, answer)

        ctx.user_data['answers'].append(answer)

        await query.answer()
        await query.delete_message()
        await next_message(update, ctx)

    return CallbackQueryHandler(handler)
