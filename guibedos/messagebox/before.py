import functools

from . import _widget


def info(message, title="Information"):

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            if _widget.make_box(message, title, _widget.INFO):
                return func(*args, **kwargs)

        return wrapper
    return decorator


def warning(message, title="Warning !"):

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            if _widget.make_box(message, title, _widget.WARNING):
                return func(*args, **kwargs)

        return wrapper
    return decorator
