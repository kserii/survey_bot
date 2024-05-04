import asyncio
from logging import getLogger

from telegram import Bot

from survey_bot.const import BOT_TOKEN

logger = getLogger(__name__)

bot = Bot(BOT_TOKEN)


async def send_notification(message: str, user: int):
    await bot.sendMessage(user, message)


async def send_notifications(message: str, users: list[int]):
    """Отправляет сообщение списку пользователей"""
    result = await asyncio.gather(
        *asyncio.as_completed(map(
            lambda user: send_notification(message, user),
            users
        )),
        return_exceptions=True
    )
    fails = tuple(filter(
        lambda x: isinstance(x, Exception),
        result
    ))

    logger.info('Сообщения отправлены %s пользователям', len(result) - len(fails))
    if len(fails):
        logger.warning('%s сообщений не были доставлены', len(fails))
        logger.debug(fails)
