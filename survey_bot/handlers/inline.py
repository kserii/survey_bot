from logging import getLogger

from telegram.ext import BaseHandler, CallbackContext, CallbackQueryHandler
from telegram import Update

from survey_bot.utils.send_next_message import send_next_message
from survey_bot.utils.types import Answer, Survey

logger = getLogger(__name__)


def question_inline_command_handler() -> BaseHandler:
    """Обработка ответов на вопросы с ответами (inline keyboard)"""

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

        ctx.user_data['answers'] = ctx.user_data['answers'] + [answer] if 'answers' in ctx.user_data else [answer]

        logger.info('Answers for %s: %s', update.effective_user.id, ctx.user_data['answers'])
        logger.debug('WHAT IS THIS? %s', query.message)

        await query.answer()
        await query.delete_message()
        await send_next_message(ctx, query.message.chat.id, survey, update.effective_user.to_dict())

    return CallbackQueryHandler(handler)
