"""Default Contacts settings."""

import os

PLUGIN_BASE_DIR = os.path.dirname(os.path.dirname(__file__))

CONTACTS_STATS_FILES = {
    "dev": os.path.join(
        PLUGIN_BASE_DIR, "frontend/webpack-stats.json"),
    "prod": os.path.join(
        PLUGIN_BASE_DIR, "frontend/webpack-stats-prod.json")
}

CONTACTS_STATICFILE_DIR = os.path.join(PLUGIN_BASE_DIR, "frontend", "dist")
