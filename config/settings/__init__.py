import os
from pathlib import Path

from split_settings.tools import include, optional


BASE_DIR = Path(__file__).resolve().parent.parent.parent


LOCAL_SETTINGS_PATH = os.getenv("LOCAL_SETTINGS_PATH", None)

if not LOCAL_SETTINGS_PATH:
    LOCAL_SETTINGS_PATH = BASE_DIR / 'locals/settings.dev.py'

include(
    'base.py',
    optional(LOCAL_SETTINGS_PATH)
)



