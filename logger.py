import logging
from logging.handlers import RotatingFileHandler


def add_logger(name):
    """создание логов."""
    logger = logging.basicConfig(
        level=logging.WARNING,
        filename='important.log',
        format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
    )
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = RotatingFileHandler('my_logger.log',
                                  maxBytes=50000000,
                                  backupCount=5)
    logger.addHandler(handler)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    return logger
