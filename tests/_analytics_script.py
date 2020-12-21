"""
This script demonstrates the usage of the analytics module of guibedos
"""
import logging
from guibedos.analytics import analyzed


logging.basicConfig(level=logging.INFO)


@analyzed('Never used')
def never_used():
    pass


@analyzed('Used five times')
def used_five_times():
    logging.info('I will be called five times')


@analyzed('Raising exception')
def raising_exception():
    raise RuntimeError('I am raising an exception')


if __name__ == '__main__':
    logging.info("Analytics test script")

    for _ in range(5):
        used_five_times()

    raising_exception()
