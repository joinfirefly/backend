import logging
from datetime import datetime

import colorlog


def getLogger(name, level=logging.INFO):
    log_colors = {
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    }
    logger = logging.getLogger(name)
    logger.setLevel(level)
    formatter = colorlog.ColoredFormatter(
        "%(asctime)s %(log_color)s [%(name)s] %(levelname)s: %(message)s",
        log_colors=log_colors,
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    formatter_file = logging.Formatter(
        "%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        handler.setLevel(level)
        logger.addHandler(handler)
    return logger, formatter_file

class logConfig:
    time = datetime.now()