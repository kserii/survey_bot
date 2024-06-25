from logging import getLogger
from typing import Optional

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import CallbackContext

from survey_bot.utils.mongodb import save_answers
from survey_bot.utils.types import Question

logger = getLogger(__name__)

SURVEY_FINISH_TEXT = 'Опрос окончен. Спасибо за уделенное время!'


async def next_message(update: Update, ctx: CallbackContext):
    survey = ctx.user_data['survey']

    try:
        question_id = next(ctx.user_data['question_counter'])
        ctx.user_data['current_question_id'] = question_id

        current_question: Question = survey['questions'][question_id]
        keyboard = make_inline_keyboard(current_question, question_id)

        await update.message.reply_text(
            '[%s/%s]. %s%s' % (
                question_id + 1,
                len(survey['questions']),
                current_question['question_name'],
                '\nНапишите ваш ответ:' if not current_question['question_options'] else ''
            ),
            reply_markup=keyboard
        )
    except StopIteration:
        await save_answers(update.effective_user.to_dict(), survey, ctx.user_data['answers'])
        ctx.user_data['answers'].clear()
        await update.message.reply_text(SURVEY_FINISH_TEXT)


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

    return InlineKeyboardMarkup(keyboard)
