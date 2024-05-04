from logging import getLogger

from telegram.ext import BaseHandler, CommandHandler, CallbackContext
from telegram import Update

from survey_bot.utils.mongodb import get_current_survey

logger = getLogger(__name__)


def vote_command_handler() -> BaseHandler:
    """Обработка комманды /vote. Участие в опросе"""

    async def handler(update: Update, ctx: CallbackContext):
        ctx.user_data['survey'] = await get_current_survey()
        logger.debug(ctx.user_data)
        await update.message.reply_text(text="Ваше слово, товарищ Маузер!")

    return CommandHandler("vote", handler)
