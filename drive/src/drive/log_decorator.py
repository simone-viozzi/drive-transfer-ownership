import functools
import logging


def local_logger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        log = logging.getLogger(f"{func.__module__}.{func.__name__}")
        return func(*args, log=log, **kwargs)
    return wrapper