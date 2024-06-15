from logging import getLogger

from telegram.ext import BaseHandler, CallbackContext, MessageHandler, filters
from telegram import Update

from survey_bot.utils.send_next_message import send_next_message
from survey_bot.utils.types import Answer, Survey, Question

logger = getLogger(__name__)


def user_option_command_handler() -> BaseHandler:
    """Обработка ответов на вопросы без ответа"""

    async def handler(update: Update, ctx: CallbackContext):
        survey: Survey = ctx.user_data['survey']

        question_id = ctx.user_data['current_question_id']
        current_question: Question = survey['questions'][question_id]

        if current_question['question_options'] is not None:
            return

        answer: Answer = {
            'question': current_question['question_name'],
            'answer': update.message.text or ''
        }

        if 'answers' not in ctx.user_data:
            ctx.user_data['answers'] = [answer]
        else:
            ctx.user_data['answers'].append(answer)

        await send_next_message(ctx, update.message.chat.id, survey, update.effective_user.to_dict())

    return MessageHandler(filters.TEXT & ~filters.COMMAND, handler)
