from typing import Optional

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

SURVEY_FINISH_TEXT = 'Опрос окончен. Спасибо за уделенное время!'


async def send_next_message(ctx: CallbackContext, chat_id: int, survey: dict):
    try:
        questions = survey.get('questions')
        current_question = next(questions)
        keyboard = make_inline_keyboard(current_question)
        await ctx.bot.send_message(
            chat_id,
            '[%s/%s]. %s' % (current_question['id'] + 1, survey['questions_count'], current_question['name']),
            reply_markup=keyboard
        )
    except StopIteration:
        await ctx.bot.send_message(chat_id, SURVEY_FINISH_TEXT)


def make_inline_keyboard(question: dict) -> Optional[InlineKeyboardMarkup]:
    """
    Возвращает inline клавиатуру с ответами для сообщения.
    Если вопрос преполагает не тест, а письменный ответ - фукнция вернет None
    """
    answers = question.get('answers')
    if not answers:
        return None

    keyboard = [
        [InlineKeyboardButton(
            answer,
            callback_data="%s,%s" % (question['id'], answer)
        )]
        for answer in answers
    ]

    return InlineKeyboardMarkup(keyboard)
