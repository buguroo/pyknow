"""
Global configuration

"""

import os
from pyknow.watchers import watch

PYKNOW_STRICT = os.getenv("PYKNOW_STRICT")
if os.getenv("ENABLE_WATCHERS"):
    watch()
