"""Default Contacts settings."""

import os

PLUGIN_BASE_DIR = os.path.dirname(__file__)

CONTACTS_STATS_FILES = {
    "dev": os.path.join(
        PLUGIN_BASE_DIR, "../frontend/webpack-stats.json"),
    "prod": os.path.join(
        PLUGIN_BASE_DIR, "static/modoboa_contacts/webpack-stats.json")
}


def apply(settings):
    """Modify settings."""
    DEBUG = settings['DEBUG']
    settings["INSTALLED_APPS"] += ("webpack_loader", )
    settings["WEBPACK_LOADER"] = {
        'CONTACTS': {
            'CACHE': not DEBUG,
            'BUNDLE_DIR_NAME': 'modoboa_contacts/',
            'STATS_FILE': CONTACTS_STATS_FILES.get("dev" if DEBUG else "prod"),
            'IGNORE': ['.+\.hot-update.js', '.+\.map']
        }
    }
