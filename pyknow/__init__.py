from functools import wraps, partial
from collections import namedtuple

DynamicFact = namedtuple('DynamicFact', ['is_asserted', 'callable'])


def fact(__fn=None, if_defined=None, **kwargs):
    """
    Returns a ``DynamicFact`` object.

    The object returned has two parameters:

    *is_asserted*: Boolean. The dependencies of this DynamicFact match.
    *callable*: Function. Call without parameters to launch the
                decorated function.

    """
    if __fn is not None:
        @wraps(__fn)
        def wrapper(*args, **kwargs):
            p = partial(__fn, *args, **kwargs)
            return DynamicFact(True, p)
        return wrapper
    else:
        is_asserted = None
        def _fact(fn):
            @wraps(fn)
            def wrapper(__facter=None, *args, **kwargs):
                if if_defined is not None:
                    if __facter is None:
                        is_asserted = False
                    else:
                        is_asserted = if_defined in __facter
                else:
                    is_asserted = True

                if __facter is None:
                    p = partial(fn, *args, **kwargs)
                else:
                    p = partial(fn, __facter, *args, **kwargs)

                return DynamicFact(is_asserted, p)
            return wrapper
        return _fact 
