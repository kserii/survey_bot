import logging

from survey_bot.const import LOG_LEVEL

def init_logger(logfile: str = 'survey_bot/logs/bot.log'):
    """Инициализация логирования"""
    log_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVEL)

    file_handler = logging.FileHandler(logfile)
    file_handler.setFormatter(log_formatter)
    root_logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    root_logger.addHandler(console_handler)
