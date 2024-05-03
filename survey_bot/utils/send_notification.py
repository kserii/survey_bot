import asyncio

from telegram import Bot
from survey_bot.const import BOT_TOKEN

bot = Bot(BOT_TOKEN)


async def send_notification(user: int):
    print('hi')
    await bot.sendMessage(user, "hello!")


async def send_notifications(message: str, users: list[int]):
    result = [result for result in asyncio.as_completed(map(send_notification, users))]
