import functools

from logging import Logger


def log_handler(logger: Logger):
    def log_(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            logger.info("Accept request in handler: %s", func.__name__)
            res = await func(*args, **kwargs)
            return res

        return wrapper

    return log_
