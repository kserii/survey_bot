from logging import getLogger

from telegram.ext import BaseHandler, CommandHandler, CallbackContext
from telegram import Update

from survey_bot.utils.send_next_message import send_next_message
from survey_bot.utils.mongodb import get_current_survey, select_answer

logger = getLogger(__name__)

DONT_HAVE_ACTIVE_SURVEYS = "Сейчас нет активных опросов"
ALREADY_COMPLETE_SURVEY = "Опрос уже пройден. Ожидайте новых"


def vote_command_handler() -> BaseHandler:
    """Обработка комманды /vote. Участие в опросе"""

    async def handler(update: Update, ctx: CallbackContext):
        # TODO реализовать очитску или сохранение данных
        #  https://github.com/python-telegram-bot/python-telegram-bot/wiki/Storing-bot%2C-user-and-chat-related-data
        current_survey = await get_current_survey()

        if not current_survey:
            await update.message.reply_text(DONT_HAVE_ACTIVE_SURVEYS)
            return

        answer = await select_answer(
            update.effective_user.id,
            current_survey['id']
        )
        if answer:
            await update.message.reply_text(ALREADY_COMPLETE_SURVEY)
            return

        ctx.user_data['survey'] = current_survey
        logger.debug('Current survey: %s', ctx.user_data['survey'])

        # Счетчик текущего вопроса. Когда дойдет до конца - опрос окночен
        ctx.user_data['question_counter'] = iter(
            range(
                len(ctx.user_data['survey']['questions'])
            )
        )

        await send_next_message(ctx, update.message.chat_id, ctx.user_data['survey'], update.effective_user.to_dict())

    return CommandHandler("vote", handler)
