import os
import asyncio

from telegram import Update
from telegram.ext import Application
from logging import getLogger

from survey_bot.utils.mongodb import ping_server
from survey_bot.utils.logger import init_logger
from survey_bot.const import BOT_TOKEN
from survey_bot.handlers import __all__ as handlers

logger = getLogger(__name__)


def main():
    init_logger()
    logger.info("Запуск бота")
    logger.debug('\n'.join([f'{k}={v}' for k, v in os.environ.items()]))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(ping_server())

    app = Application.builder().token(BOT_TOKEN).build()

    logger.debug("Загрузка обработчиков:", handlers)
    app.add_handlers([hadler() for hadler in handlers])
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.exception(e)
    except BaseException as be:
        logger.exception(be)
    finally:
        logger.info('Бот выключен')
