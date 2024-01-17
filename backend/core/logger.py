import logging

from core.settings import Settings

SETTINGS = Settings()


class CustomFormatter(logging.Formatter):
    def format(self, record):
        record.levelname = f"{record.levelname}:"
        return super().format(record)


def get_logger(
    logger_name,
    log_level=SETTINGS.LOG_LEVEL,
):
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    formatter = CustomFormatter(
        "%(levelname)-9s %(asctime)s - [%(name)s] - %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger
