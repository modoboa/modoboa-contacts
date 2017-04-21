"""Default Contacts settings."""

import os

PLUGIN_BASE_DIR = os.path.dirname(__file__)

CONTACTS_STATS_FILES = {
    "dev": os.path.join(
        PLUGIN_BASE_DIR, "../frontend/webpack-stats.json"),
    "prod": os.path.join(
        PLUGIN_BASE_DIR, "static/modoboa_contacts/webpack-stats.json")
}
