"""
Watchers are loggers that log detailed information on
CLIPS, disabled by default and that can be enabled by
the `(watch)` method.

Here, we expose a rule, fact and agenda watchers as
well as a method to enable/disable them both individually
and all of them.

"""
import logging
import os

logging.basicConfig()
RULE_WATCHER = logging.getLogger('rule')
FACT_WATCHER = logging.getLogger('fact')
AGENDA_WATCHER = logging.getLogger('agenda')
MATCH_WATCHER = logging.getLogger('match')

RULE_WATCHER.setLevel(logging.CRITICAL)
FACT_WATCHER.setLevel(logging.CRITICAL)
AGENDA_WATCHER.setLevel(logging.CRITICAL)
MATCH_WATCHER.setLevel(logging.CRITICAL)


def watch(what=False):
    """
    Enable watchers.

    Defaults to enable all watchers, accepts a list of watchers
    to enable.

    """
    if not what:
        what = [RULE_WATCHER, FACT_WATCHER, AGENDA_WATCHER, MATCH_WATCHER]
    for watcher in what:
        watcher.setLevel(logging.DEBUG)


if os.getenv("ENABLE_WATCHERS"):
    watch()
