from .analytics import analyzed
from .error_reporting import error_reported


def use_case(name):
    """
    Composes the `@analytics.analyzed` and `@error_reporting.error_reported` decorators

    :param name: Name that will be reported in logs and error reporting windows
    """
    def decorator(func):
        return error_reported(name)(analyzed(name)(func))
    return decorator
