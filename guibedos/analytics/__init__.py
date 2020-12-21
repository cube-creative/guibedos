import time
import logging
import functools

from .constants import *


def analyzed(name):
    logging.info(REGISTER_MESSAGE, name)

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            raised = False

            try:
                return func(*args, **kwargs)

            except Exception as e:
                raised = True
                raise

            finally:
                logging.info(
                    CALL_MESSAGE,
                    name,
                    time.time() - now,
                    ['', '*'][raised]
                )

        return wrapper

    return decorator
