import time
import logging
import functools


def analyzed(name):
    logging.info('Analytics register[%s]', name)

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
                    'Analytics call[%s](%s)%s',
                    name,
                    time.time() - now,
                    ['', '*'][raised]
                )

        return wrapper

    return decorator
