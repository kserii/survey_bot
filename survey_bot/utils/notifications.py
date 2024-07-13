import asyncio
from logging import getLogger

from telegram.ext import CallbackContext

from survey_bot.utils.mongodb import select_all_users

logger = getLogger(__name__)

API_SEND_REQUEST_PER_MINUTE = 30

api_calls_semaphore = asyncio.Semaphore(API_SEND_REQUEST_PER_MINUTE)


async def send_notification(message: str, user: int, ctx: CallbackContext):
    async with api_calls_semaphore:
        await ctx.bot.sendMessage(user, message)
        await asyncio.sleep(1 / API_SEND_REQUEST_PER_MINUTE)


async def send_notifications(message: str, users: list[int], ctx: CallbackContext):
    """Отправляет сообщение списку пользователей"""
    result = await asyncio.gather(
        *asyncio.as_completed(map(
            lambda user: send_notification(message, user, ctx),
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
        logger.debug('Ошибки %s', fails)


async def send_notifications_all_users(message: str, ctx: CallbackContext):
    users = await select_all_users()
    users = [user['id'] for user in users]
    await send_notifications(message, users, ctx)
