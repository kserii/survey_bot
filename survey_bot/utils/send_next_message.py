from logging import getLogger
from typing import Optional

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

from survey_bot.utils.mongodb import save_answers
from survey_bot.utils.types import User, Survey, Question

logger = getLogger(__name__)

SURVEY_FINISH_TEXT = 'Опрос окончен. Спасибо за уделенное время!'


async def send_next_message(ctx: CallbackContext, chat_id: int, survey: Survey, user: User):
    try:
        question_id = next(ctx.user_data['question_counter'])
        current_question: Question = survey['questions'][question_id]

        ctx.user_data['current_question_id'] = question_id

        keyboard = make_inline_keyboard(current_question, question_id)
        await ctx.bot.send_message(
            chat_id,
            '[%s/%s]. %s%s' % (
                question_id + 1,
                len(survey['questions']),
                current_question['question_name'],
                '\nНапишите ваш ответ:' if not current_question['question_options'] else ''
            ),
            reply_markup=keyboard
        )
    except StopIteration:
        await save_answers(user, survey, ctx.user_data['answers'])
        ctx.user_data['answers'].clear()
        await ctx.bot.send_message(chat_id, SURVEY_FINISH_TEXT)


def make_inline_keyboard(question: Question, question_id: int) -> Optional[InlineKeyboardMarkup]:
    """
    Возвращает inline клавиатуру с ответами для сообщения.
    Если вопрос преполагает не тест, а письменный ответ - фукнция вернет None
    """
    answers = question['question_options']
    if not answers:
        return None

    # Есть ограничение: max 64 байта в callback_data
    keyboard = [
        [InlineKeyboardButton(
            answer,
            callback_data="%s,%s" % (question_id, answer_id)
        )]
        for answer_id, answer in enumerate(answers)
    ]

    logger.debug('Inline keyboard: %s', keyboard)

    return InlineKeyboardMarkup(keyboard)
