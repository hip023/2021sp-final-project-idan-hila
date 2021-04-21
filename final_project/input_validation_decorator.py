# TODO: add tests for this class

from collections import Callable
from functools import wraps


class NoneStringArgument(ValueError):
    """
    Error which inherits from ValueError to indicate
    that passed argument is not a string
    """
    pass


def validate_string(func: Callable) -> Callable:
    """
    :param func: a method that accepts a string argument
    :raises: NoneStringArgument if object is not a string
    """
    @wraps(func)
    def wrapper(s: str, *args, **kwargs):
        if not isinstance(s, str):
            try:
                s_as_string = str(s)
                func(s_as_string, *args, **kwargs)
            except:
                raise NoneStringArgument(f"argument should be a string. "
                                         f"you sent {s.__class__} argument")
        return func(s, *args, **kwargs)

    return wrapper
