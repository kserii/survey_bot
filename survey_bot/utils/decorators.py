import functools
from typing import Callable, Awaitable

from telegram import Update
from telegram.ext import CallbackContext

from survey_bot.utils.mongodb import select_user

NO_HAVE_PERMISSION_TEXT = "Нет доступа!"


def check_permission(access_level: str = 'User'):
    """Декоратор для проверки прав доступа"""

    def decorator(func: Callable[..., Awaitable]):
        @functools.wraps(func)
        async def wrapper(update: Update, ctx: CallbackContext, *args, **kwargs):
            if 'user' not in ctx.user_data:
                ctx.user_data['user'] = await select_user(update.effective_user.id)

            if access_level == 'Admin' and not ctx.user_data['user']['is_admin']:
                await update.message.reply_text(NO_HAVE_PERMISSION_TEXT)
                return

            result = await func(update, ctx, *args, **kwargs)
            return result

        return wrapper
    return decorator
