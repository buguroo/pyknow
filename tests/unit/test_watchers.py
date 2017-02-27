"""
Test watchers module
"""


def test_watchers_has_all_watchers():
    """ Test that watchers module contains all watchers """
    # pylint: disable=unused-variable
    from pyknow.watchers import RULE_WATCHER  # NOQA
    from pyknow.watchers import AGENDA_WATCHER  # NOQA
    from pyknow.watchers import FACT_WATCHER  # NOQA


def test_watchers_watch():
    """ Test that watch() method calls setlevel """
    from pyknow.watchers import watch, RULE_WATCHER, FACT_WATCHER
    from pyknow.watchers import AGENDA_WATCHER
    from unittest.mock import MagicMock
    import logging
    RULE_WATCHER.setLevel = MagicMock()
    FACT_WATCHER.setLevel = MagicMock()
    AGENDA_WATCHER.setLevel = MagicMock()
    watch()
    RULE_WATCHER.setLevel.assert_called_with(logging.DEBUG)
    AGENDA_WATCHER.setLevel.assert_called_with(logging.DEBUG)
    FACT_WATCHER.setLevel.assert_called_with(logging.DEBUG)


def test_watchers_watch_once():
    """ Test that watch() method calls setlevel """
    from pyknow.watchers import watch, RULE_WATCHER, FACT_WATCHER
    from pyknow.watchers import AGENDA_WATCHER
    from unittest.mock import MagicMock
    import logging
    for watcher in [RULE_WATCHER, FACT_WATCHER, AGENDA_WATCHER]:
        watcher.setLevel = MagicMock()
        watch([watcher])
        watcher.setLevel.assert_called_with(logging.DEBUG)
