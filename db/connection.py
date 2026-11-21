"""SQLite connection management."""

import os
import shutil
import sqlite3

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

DB_PATH = os.path.join(DATA_DIR, "crm_data.db")
LEGACY_DB_PATH = os.path.join(ROOT_DIR, "crm_data.db")
BACKUP_DB_PATH = os.path.join(ROOT_DIR, "crm_data.pre_migration.db")


def ensure_db_files():
    """Ensure pre-migration backup exists and data/crm_data.db is seeded from root crm_data.db if needed."""
    if os.path.exists(LEGACY_DB_PATH) and not os.path.exists(BACKUP_DB_PATH):
        shutil.copy2(LEGACY_DB_PATH, BACKUP_DB_PATH)
    if os.path.exists(LEGACY_DB_PATH) and not os.path.exists(DB_PATH):
        shutil.copy2(LEGACY_DB_PATH, DB_PATH)


def get_connection():
    ensure_db_files()
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
