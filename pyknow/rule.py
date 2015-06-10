from functools import wraps, update_wrapper


class Rule:
    def __init__(self):
        self.__fn = None

    def __call__(self, fst=None, *args, **kwargs):
        """
        Decorate or call a function.

        This function is going to be called twice.

        - The first call is when the decorator is been created. At this
          point we assign the función decorated to ``self.__fn`` and
          return ``self`` to be called the second time.

        - The second call is to execute the decorated function, se we
          pass all the arguments along.

        """
        if self.__fn is None:
            if fst is not None:
                self.__fn = fst
                return update_wrapper(self, self.__fn)
            else:
                raise AttributeError("Mandatory function not provided.")
        else:
            args = (tuple() if fst is None else (fst,)) + args
            return self.__fn(*args, **kwargs)
