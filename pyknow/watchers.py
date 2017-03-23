"""
Watchers are loggers that log detailed information on
CLIPS, disabled by default and that can be enabled by
the `(watch)` method.

Here, we expose a rule, fact and agenda watchers as
well as a method to enable/disable them both individually
and all of them.

"""
import logging

logging.basicConfig()


def define_watcher(name):
    watcher = logging.getLogger('.'.join((__name__, name)))
    watcher.setLevel(logging.CRITICAL)
    return watcher


def watch(*what, level=logging.DEBUG):
    """
    Enable watchers.

    Defaults to enable all watchers, accepts a list of watchers
    to enable.

    """
    if not what:
        what = ALL

    for watcher in what:
        watcher.setLevel(level)


RULES = define_watcher('RULES')
ACTIVATIONS = define_watcher('ACTIVATIONS')
FACTS = define_watcher('FACTS')
AGENDA = define_watcher('AGENDA')

ALL = tuple(v for k, v in globals().items() if k.isupper())
__all__ = (tuple(k for k, v in globals().items() if k.isupper())
           + ('ALL', 'watch'))
