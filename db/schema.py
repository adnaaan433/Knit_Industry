"""Database schema initialization and additive idempotent migrations."""

import os
from db.connection import get_connection
from db.excel_sync import EXCEL_PATH, sync_from_excel
from db.seeds import run_all_seeds

NEW_MACHINE_COLUMNS = [
    ("unit", "TEXT DEFAULT ''"),
    ("machine_category", "TEXT DEFAULT 'Circular'"),
    ("machine_type", "TEXT DEFAULT ''"),
    ("feeders", "INTEGER"),
    ("origin", "TEXT DEFAULT ''"),
    ("model", "TEXT DEFAULT ''"),
    ("capacity_kg", "REAL"),
    ("machine_no", "TEXT DEFAULT ''"),
    ("in_operation", "INTEGER DEFAULT 1"),
    ("sort_order", "INTEGER DEFAULT 0"),
]


def _migrate_machine_profiles(cur):
    cur.execute("PRAGMA table_info(machine_profiles)")
    existing_cols = {row["name"] for row in cur.fetchall()}
    for col_name, col_def in NEW_MACHINE_COLUMNS:
        if col_name not in existing_cols:
            cur.execute(f"ALTER TABLE machine_profiles ADD COLUMN {col_name} {col_def}")


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS industries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            location_area TEXT DEFAULT '',
            cluster TEXT DEFAULT '',
            distance_km REAL,
            map_url TEXT DEFAULT '',
            status TEXT DEFAULT 'New',
            general_notes TEXT DEFAULT '',
            machine_profile_notes TEXT DEFAULT '',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            industry_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            designation TEXT DEFAULT '',
            phone TEXT DEFAULT '',
            email TEXT DEFAULT '',
            butex_batch TEXT DEFAULT '',
            status TEXT DEFAULT 'New',
            notes TEXT DEFAULT '',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (industry_id) REFERENCES industries(id) ON DELETE CASCADE
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            industry_id INTEGER NOT NULL,
            visit_date TEXT NOT NULL,
            visit_type TEXT DEFAULT 'Factory Visit',
            attendees TEXT DEFAULT '',
            meeting_minutes TEXT NOT NULL,
            action_items TEXT DEFAULT '',
            next_followup_date TEXT DEFAULT '',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (industry_id) REFERENCES industries(id) ON DELETE CASCADE
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS machine_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            industry_id INTEGER NOT NULL,
            fabrication TEXT NOT NULL DEFAULT 'Single Jersey',
            dia REAL NOT NULL DEFAULT 30,
            gauge REAL NOT NULL DEFAULT 24,
            dia_gauge_label TEXT DEFAULT '30x24',
            brand TEXT DEFAULT '',
            quantity INTEGER NOT NULL DEFAULT 1,
            needles_per_machine INTEGER NOT NULL DEFAULT 0,
            sinkers_per_machine INTEGER NOT NULL DEFAULT 0,
            needle_spec TEXT DEFAULT '',
            sinker_spec TEXT DEFAULT '',
            remarks TEXT DEFAULT '',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (industry_id) REFERENCES industries(id) ON DELETE CASCADE
        )
    """)

    _migrate_machine_profiles(cur)
    conn.commit()

    if os.path.exists(EXCEL_PATH):
        sync_from_excel(conn)

    run_all_seeds(conn)
    conn.close()
