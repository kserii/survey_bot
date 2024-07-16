import functools
from typing import Callable, Awaitable, Literal

from telegram import Update
from telegram.ext import CallbackContext

from survey_bot.utils.mongodb import select_user, get_current_survey, insert_user

NO_HAVE_PERMISSION_TEXT = "Нет доступа!"


def check_permissions(access_level: Literal['User', 'Admin'] = 'User'):
    """Декоратор для проверки прав доступа"""

    def decorator(func: Callable[..., Awaitable]):
        @functools.wraps(func)
        async def wrapper(update: Update, ctx: CallbackContext, *args, **kwargs):
            ctx.user_data['user'] = await select_user(update.effective_user.id)

            if access_level == 'Admin' and not ctx.user_data['user']['is_admin']:
                await update.message.reply_text(NO_HAVE_PERMISSION_TEXT)
                return

            result = await func(update, ctx, *args, **kwargs)
            return result

        return wrapper

    return decorator


def check_context(func: Callable[..., Awaitable]):
    """Декоратор для проверки контекстных переменных"""

    @functools.wraps(func)
    async def wrapper(update: Update, ctx: CallbackContext, *args, **kwargs):
        if 'user' not in ctx.user_data:
            user = await select_user(update.effective_user.id)
            if not user:
                await insert_user(update.effective_user.to_dict())
            ctx.user_data['user'] = user

        if 'survey' not in ctx.user_data:
            ctx.user_data['survey'] = await get_current_survey()

        if 'answers' not in ctx.user_data:
            ctx.user_data['answers'] = []

        if 'question_counter' not in ctx.user_data:
            ctx.user_data['question_counter'] = None

        if 'current_question_id' not in ctx.user_data:
            ctx.user_data['current_question_id'] = None

        result = await func(update, ctx, *args, **kwargs)
        return result

    return wrapper
