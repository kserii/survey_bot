import json
from datetime import datetime
from logging import getLogger

from telegram.ext import BaseHandler, CommandHandler, CallbackContext
from telegram import Update, InputFile

from survey_bot.const import BOT_OWNER_IDS
from survey_bot.utils.mongodb import select_all_answers_by_survey, get_current_survey

logger = getLogger(__name__)

WELLCOME_TEXT = "Привет! Чтобы пройти опрос пиши: /vote"


def export_json_command_handler() -> BaseHandler:
    """Обработка комманды /export. Вернет json файл с результатом текущего опроса"""

    async def handler(update: Update, ctx: CallbackContext):

        if update.effective_user.id not in BOT_OWNER_IDS or not ctx.user_data['user']['is_admin']:
            return

        current_survey = await get_current_survey()
        answers = await select_all_answers_by_survey(survey_id=current_survey['id'])

        logger.debug('%s', answers)

        if not answers:
            await update.message.reply_text('noo')
            return

        file = InputFile(
            json.dumps(answers, ensure_ascii=False, indent=4),
            filename=f"report-{current_survey['id']}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.json"
        )

        await ctx.bot.send_document(
            chat_id=update.effective_chat.id,
            document=file
        )

    return CommandHandler("export", handler)
