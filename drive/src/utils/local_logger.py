import functools
import logging

# TODO il logger non funziona!

def local_logger(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        log = self.log
        self.log = logging.getLogger(f"{func.__module__}.{func.__name__}")
        r = func(self, *args, **kwargs)
        self.log = log
        return r
    return wrapper