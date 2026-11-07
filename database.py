import os
import re
import sqlite3
import openpyxl

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "crm_data.db")
EXCEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Knit Industry Contacts.xlsx")

# Name normalization map to link Contacts sheet names to canonical Factory Locations names
NAME_MAPPING = {
    "Fakir Knitwear Ltd": "Fakir Knitwears Ltd.",
    "Gramtech (Sonali Textile)": "Gram Tech (Sonali Textile)",
    "Nur Group": "Nur Group (Raiyan Knit Composite)",
    "Esquire Knit Composite Ltd.": "L'Esquire Ltd.",
    "Alliance Knit Composit": "Alliance Knit Composite Ltd.",
}

FABRICATION_TYPES = [
    "Single Jersey",
    "Fleece",
    "H/Jersey",
    "Rib",
    "Interlock",
]

DOUBLE_BED_FABRICATIONS = {"rib", "interlock"}


def calculate_needle_sinker(fabrication: str, dia: float, gauge: float, quantity: int = 1):
    """
    Calculate needle and sinker requirements based on machine fabrication, diameter, and gauge.
    - For Single Jersey, Fleece, H/Jersey:
        Needles per machine = int(dia * gauge * 3.1416)
        Sinkers per machine = int(dia * gauge * 3.1416)
    - For Rib, Interlock:
        Needles per machine = int(2 * dia * gauge * 3.1416)
        Sinkers per machine = 0 (Double-jersey cylinder + dial machines do not use sinkers)
    """
    if not dia or not gauge or dia <= 0 or gauge <= 0:
        return {
            "needles_per_machine": 0,
            "sinkers_per_machine": 0,
            "total_needles": 0,
            "total_sinkers": 0,
        }

    fab_norm = (fabrication or "").strip().lower()
    qty = max(int(quantity or 0), 0)

    if fab_norm in DOUBLE_BED_FABRICATIONS or "rib" in fab_norm or "interlock" in fab_norm:
        needles_pm = int(2 * float(dia) * float(gauge) * 3.1416)
        sinkers_pm = 0
    else:
        needles_pm = int(float(dia) * float(gauge) * 3.1416)
        sinkers_pm = int(float(dia) * float(gauge) * 3.1416)

    return {
        "needles_per_machine": needles_pm,
        "sinkers_per_machine": sinkers_pm,
        "total_needles": needles_pm * qty,
        "total_sinkers": sinkers_pm * qty,
    }


def parse_dia_gauge_label(dia_gauge_str: str):
    """
    Parse strings like '30x20', '36x20(F/L)', '30x20(S/J)', '34x24(I/L)' into (dia, gauge, formatted_label).
    """
    s = str(dia_gauge_str or "").strip()
    m = re.search(r"(\d+(?:\.\d+)?)\s*[xX×*]\s*(\d+(?:\.\d+)?)", s)
    if m:
        dia = float(m.group(1))
        gauge = float(m.group(2))
        return dia, gauge, s
    return 0.0, 0.0, s


def format_dia_gauge(dia: float, gauge: float, suffix: str = "") -> str:
    d_str = str(int(dia)) if float(dia).is_integer() else str(dia)
    g_str = str(int(gauge)) if float(gauge).is_integer() else str(gauge)
    suf = (suffix or "").strip()
    if suf and not suf.startswith("("):
        suf = f"({suf})"
    return f"{d_str}x{g_str}{suf}"


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


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

    # Migrate old machine_profiles table if it was created with the previous placeholder schema
    cur.execute("PRAGMA table_info(machine_profiles)")
    existing_cols = {row["name"] for row in cur.fetchall()}
    if "fabrication" not in existing_cols:
        cur.execute("DROP TABLE machine_profiles")
        cur.execute("""
            CREATE TABLE machine_profiles (
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

    conn.commit()

    # Seed from Excel if industries table is empty
    cur.execute("SELECT COUNT(*) as cnt FROM industries")
    if cur.fetchone()["cnt"] == 0 and os.path.exists(EXCEL_PATH):
        seed_from_excel(conn)

    # Seed L'Esquire Knit Composite Ltd. machine profile from example image if empty
    seed_lesquire_machines(conn)

    conn.close()


def _clean_val(val):
    if val is None:
        return ""
    s = str(val).strip()
    if s in ("—", "-", "None", "nan"):
        return ""
    if re.match(r"^\d+\.0$", s):
        return s[:-2]
    return s


def _extract_hyperlink(cell_val):
    if not cell_val:
        return ""
    s = str(cell_val)
    m = re.search(r'HYPERLINK\(\s*"([^"]+)"', s, re.IGNORECASE)
    if m:
        return m.group(1)
    if s.startswith("http"):
        return s
    return ""


def seed_from_excel(conn):
    wb_val = openpyxl.load_workbook(EXCEL_PATH, data_only=True)
    wb_formula = openpyxl.load_workbook(EXCEL_PATH, data_only=False)

    cur = conn.cursor()
    industry_ids = {}

    if "Factory Locations" in wb_val.sheetnames:
        ws_val = wb_val["Factory Locations"]
        ws_form = wb_formula["Factory Locations"]
        for row_idx in range(2, ws_val.max_row + 1):
            name = _clean_val(ws_val.cell(row_idx, 2).value)
            if not name:
                continue
            loc_area = _clean_val(ws_val.cell(row_idx, 3).value)
            cluster = _clean_val(ws_val.cell(row_idx, 4).value)
            dist_raw = ws_val.cell(row_idx, 5).value
            try:
                dist_km = float(dist_raw) if dist_raw not in (None, "—", "-") else None
            except (ValueError, TypeError):
                dist_km = None

            cell_f = ws_form.cell(row_idx, 6)
            map_url = ""
            if cell_f.hyperlink and cell_f.hyperlink.target:
                map_url = cell_f.hyperlink.target
            else:
                map_url = _extract_hyperlink(cell_f.value)

            status = _clean_val(ws_val.cell(row_idx, 7).value) or "New"

            cur.execute(
                """
                INSERT OR IGNORE INTO industries (name, location_area, cluster, distance_km, map_url, status)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (name, loc_area, cluster, dist_km, map_url, status),
            )
            cur.execute("SELECT id FROM industries WHERE name = ?", (name,))
            industry_ids[name] = cur.fetchone()["id"]

    if "Contacts" in wb_val.sheetnames:
        ws_c = wb_val["Contacts"]
        for row_idx in range(2, ws_c.max_row + 1):
            raw_factory = _clean_val(ws_c.cell(row_idx, 2).value)
            if not raw_factory:
                continue
            factory_name = NAME_MAPPING.get(raw_factory, raw_factory)

            person = _clean_val(ws_c.cell(row_idx, 3).value)
            designation = _clean_val(ws_c.cell(row_idx, 4).value)
            phone = _clean_val(ws_c.cell(row_idx, 5).value)
            batch = _clean_val(ws_c.cell(row_idx, 6).value)
            c_status = _clean_val(ws_c.cell(row_idx, 7).value) or "New"

            if factory_name not in industry_ids:
                cur.execute(
                    "INSERT OR IGNORE INTO industries (name, status) VALUES (?, ?)",
                    (factory_name, c_status),
                )
                cur.execute("SELECT id FROM industries WHERE name = ?", (factory_name,))
                industry_ids[factory_name] = cur.fetchone()["id"]

            ind_id = industry_ids[factory_name]

            if c_status in ("Visited", "Contacted"):
                cur.execute("SELECT status FROM industries WHERE id = ?", (ind_id,))
                curr_st = cur.fetchone()["status"]
                if curr_st == "New" or (curr_st == "Contacted" and c_status == "Visited"):
                    cur.execute("UPDATE industries SET status = ? WHERE id = ?", (c_status, ind_id))

            if person:
                cur.execute(
                    """
                    INSERT INTO contacts (industry_id, name, designation, phone, butex_batch, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (ind_id, person, designation, phone, batch, c_status),
                )

    conn.commit()


def seed_lesquire_machines(conn):
    """Seed L'Esquire Ltd. with the exact Machine Profile from the user's reference sheet."""
    cur = conn.cursor()
    row = cur.execute("SELECT id FROM industries WHERE name LIKE '%Esquire%' LIMIT 1").fetchone()
    if not row:
        return
    ind_id = row["id"]

    cnt = cur.execute("SELECT COUNT(*) as c FROM machine_profiles WHERE industry_id = ?", (ind_id,)).fetchone()["c"]
    if cnt > 0:
        return

    lesquire_data = [
        # Fleece (24)
        ("Fleece", 30, 20, "30x20", "HaanTex", 9),
        ("Fleece", 30, 20, "30x20", "Mayer & Cie", 2),
        ("Fleece", 34, 20, "34x20", "HaanTex", 5),
        ("Fleece", 36, 20, "36x20", "HaanTex", 5),
        ("Fleece", 36, 20, "36x20", "Mayer & Cie", 1),
        ("Fleece", 36, 20, "36x20(F/L)", "Mayer & Cie", 2),
        # H/Jersey (2)
        ("H/Jersey", 30, 20, "30x20", "Pai Long", 2),
        # Single Jersey (48)
        ("Single Jersey", 24, 24, "24x24", "Orizio", 2),
        ("Single Jersey", 26, 24, "26x24", "Orizio", 2),
        ("Single Jersey", 26, 24, "26x24", "Santo", 1),
        ("Single Jersey", 28, 24, "28x24", "Orizio", 2),
        ("Single Jersey", 30, 20, "30x20(S/J)", "Pai Long", 1),
        ("Single Jersey", 30, 24, "30x24", "Hangxing", 5),
        ("Single Jersey", 30, 24, "30x24", "Mayer & Cie", 6),
        ("Single Jersey", 30, 24, "30x24", "Orizio", 3),
        ("Single Jersey", 30, 24, "30x24", "Santo", 2),
        ("Single Jersey", 30, 24, "30x24(S/J)", "Pai Long", 2),
        ("Single Jersey", 32, 24, "32x24", "Orizio", 2),
        ("Single Jersey", 34, 24, "34x24", "Hangxing", 5),
        ("Single Jersey", 34, 24, "34x24", "Mayer & Cie", 2),
        ("Single Jersey", 34, 24, "34x24(S/J)", "Mayer & Cie", 1),
        ("Single Jersey", 36, 24, "36x24", "Hangxing", 4),
        ("Single Jersey", 36, 24, "36x24", "Mayer & Cie", 4),
        ("Single Jersey", 38, 24, "38x24", "Hangxing", 4),
        # Rib (19)
        ("Rib", 30, 18, "30x18", "Orizio", 3),
        ("Rib", 30, 20, "30x20(Rib)", "Fukuhara", 1),
        ("Rib", 30, 20, "30x20(Rib)", "Pai Long", 1),
        ("Rib", 32, 20, "32x20(Rib)", "Mayer & Cie", 2),
        ("Rib", 34, 20, "34x20(Rib)", "Mayer & Cie", 1),
        ("Rib", 34, 20, "34x20(Rib)", "Orizio", 1),
        ("Rib", 34, 20, "34x20(Rib)", "Pai Long", 1),
        ("Rib", 36, 18, "36x18", "Hangxing", 1),
        ("Rib", 36, 18, "36x18", "Orizio", 1),
        ("Rib", 36, 20, "36x20(Rib)", "Pai Long", 1),
        ("Rib", 40, 18, "40x18", "Fukuhara", 2),
        ("Rib", 40, 18, "40x18", "Jung Long", 2),
        ("Rib", 42, 18, "42x18", "Fukuhara", 1),
        ("Rib", 42, 18, "42x18", "Jung Long", 1),
        # Interlock (4)
        ("Interlock", 34, 24, "34x24(I/L)", "Mayer & Cie", 1),
        ("Interlock", 34, 24, "34x24(I/L)", "Orizio", 2),
        ("Interlock", 34, 24, "34x24(I/L)", "Pai Long", 1),
    ]

    for fab, dia, gauge, label, brand, qty in lesquire_data:
        calc = calculate_needle_sinker(fab, dia, gauge, qty)
        cur.execute(
            """
            INSERT INTO machine_profiles (
                industry_id, fabrication, dia, gauge, dia_gauge_label, brand, quantity,
                needles_per_machine, sinkers_per_machine
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                ind_id,
                fab,
                dia,
                gauge,
                label,
                brand,
                qty,
                calc["needles_per_machine"],
                calc["sinkers_per_machine"],
            ),
        )
    conn.commit()


# --- CRUD Helpers ---

def get_all_industries():
    conn = get_connection()
    rows = conn.execute("""
        SELECT
            i.*,
            (SELECT COUNT(*) FROM contacts c WHERE c.industry_id = i.id) AS contact_count,
            (SELECT COUNT(*) FROM updates u WHERE u.industry_id = i.id) AS update_count,
            (SELECT COALESCE(SUM(m.quantity), 0) FROM machine_profiles m WHERE m.industry_id = i.id) AS machine_count,
            (SELECT MAX(u.visit_date) FROM updates u WHERE u.industry_id = i.id) AS last_visit_date
        FROM industries i
        ORDER BY i.name ASC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_industry(industry_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM industries WHERE id = ?", (industry_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def create_industry(name, location_area="", cluster="", distance_km=None, map_url="", status="New", general_notes=""):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO industries (name, location_area, cluster, distance_km, map_url, status, general_notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (name.strip(), location_area.strip(), cluster.strip(), distance_km, map_url.strip(), status, general_notes.strip()),
    )
    new_id = cur.lastrowid
    conn.commit()
    conn.close()
    return new_id


def update_industry(industry_id, name, location_area, cluster, distance_km, map_url, status, general_notes):
    conn = get_connection()
    conn.execute(
        """
        UPDATE industries
        SET name = ?, location_area = ?, cluster = ?, distance_km = ?, map_url = ?, status = ?, general_notes = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (name.strip(), location_area.strip(), cluster.strip(), distance_km, map_url.strip(), status, general_notes.strip(), industry_id),
    )
    conn.commit()
    conn.close()


def update_industry_status(industry_id, status):
    conn = get_connection()
    conn.execute(
        "UPDATE industries SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (status, industry_id),
    )
    conn.commit()
    conn.close()


def delete_industry(industry_id):
    conn = get_connection()
    conn.execute("DELETE FROM industries WHERE id = ?", (industry_id,))
    conn.commit()
    conn.close()


# --- Contacts CRUD ---

def get_contacts(industry_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM contacts WHERE industry_id = ? ORDER BY id ASC",
        (industry_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_contact(industry_id, name, designation="", phone="", email="", butex_batch="", status="New", notes=""):
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO contacts (industry_id, name, designation, phone, email, butex_batch, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (industry_id, name.strip(), designation.strip(), phone.strip(), email.strip(), butex_batch.strip(), status, notes.strip()),
    )
    conn.commit()
    conn.close()


def update_contact(contact_id, name, designation, phone, email, butex_batch, status, notes):
    conn = get_connection()
    conn.execute(
        """
        UPDATE contacts
        SET name = ?, designation = ?, phone = ?, email = ?, butex_batch = ?, status = ?, notes = ?
        WHERE id = ?
        """,
        (name.strip(), designation.strip(), phone.strip(), email.strip(), butex_batch.strip(), status, notes.strip(), contact_id),
    )
    conn.commit()
    conn.close()


def delete_contact(contact_id):
    conn = get_connection()
    conn.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    conn.commit()
    conn.close()


# --- Updates / Visit Logs CRUD ---

def get_updates(industry_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM updates WHERE industry_id = ? ORDER BY visit_date DESC, id DESC",
        (industry_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_update(industry_id, visit_date, visit_type, attendees, meeting_minutes, action_items="", next_followup_date=""):
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO updates (industry_id, visit_date, visit_type, attendees, meeting_minutes, action_items, next_followup_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (industry_id, str(visit_date), visit_type, attendees.strip(), meeting_minutes.strip(), action_items.strip(), str(next_followup_date) if next_followup_date else ""),
    )
    conn.commit()
    conn.close()


def edit_update(update_id, visit_date, visit_type, attendees, meeting_minutes, action_items="", next_followup_date=""):
    conn = get_connection()
    conn.execute(
        """
        UPDATE updates
        SET visit_date = ?, visit_type = ?, attendees = ?, meeting_minutes = ?, action_items = ?, next_followup_date = ?
        WHERE id = ?
        """,
        (str(visit_date), visit_type, attendees.strip(), meeting_minutes.strip(), action_items.strip(), str(next_followup_date) if next_followup_date else "", update_id),
    )
    conn.commit()
    conn.close()


def delete_update(update_id):
    conn = get_connection()
    conn.execute("DELETE FROM updates WHERE id = ?", (update_id,))
    conn.commit()
    conn.close()


# --- Machine Profile CRUD ---

def update_machine_notes(industry_id, notes):
    conn = get_connection()
    conn.execute(
        "UPDATE industries SET machine_profile_notes = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (notes.strip(), industry_id),
    )
    conn.commit()
    conn.close()


def get_machines(industry_id):
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT * FROM machine_profiles
        WHERE industry_id = ?
        ORDER BY
            CASE fabrication
                WHEN 'Fleece' THEN 1
                WHEN 'H/Jersey' THEN 2
                WHEN 'Single Jersey' THEN 3
                WHEN 'Rib' THEN 4
                WHEN 'Interlock' THEN 5
                ELSE 6
            END,
            dia ASC,
            gauge ASC,
            dia_gauge_label ASC,
            brand ASC,
            id ASC
        """,
        (industry_id,),
    ).fetchall()
    conn.close()
    result = []
    for r in rows:
        d = dict(r)
        calc = calculate_needle_sinker(d["fabrication"], d["dia"], d["gauge"], d["quantity"])
        d["needles_per_machine"] = calc["needles_per_machine"]
        d["sinkers_per_machine"] = calc["sinkers_per_machine"]
        d["total_needles"] = calc["total_needles"]
        d["total_sinkers"] = calc["total_sinkers"]
        result.append(d)
    return result


def add_machine(
    industry_id,
    fabrication,
    dia,
    gauge,
    dia_gauge_label="",
    brand="",
    quantity=1,
    needle_spec="",
    sinker_spec="",
    remarks="",
):
    if not dia_gauge_label.strip():
        dia_gauge_label = format_dia_gauge(dia, gauge)
    calc = calculate_needle_sinker(fabrication, dia, gauge, quantity)
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO machine_profiles (
            industry_id, fabrication, dia, gauge, dia_gauge_label, brand, quantity,
            needles_per_machine, sinkers_per_machine, needle_spec, sinker_spec, remarks
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            industry_id,
            fabrication.strip(),
            float(dia),
            float(gauge),
            dia_gauge_label.strip(),
            brand.strip(),
            int(quantity),
            calc["needles_per_machine"],
            calc["sinkers_per_machine"],
            needle_spec.strip(),
            sinker_spec.strip(),
            remarks.strip(),
        ),
    )
    conn.commit()
    conn.close()


def update_machine(
    machine_id,
    fabrication,
    dia,
    gauge,
    dia_gauge_label,
    brand,
    quantity,
    needle_spec="",
    sinker_spec="",
    remarks="",
):
    if not dia_gauge_label.strip():
        dia_gauge_label = format_dia_gauge(dia, gauge)
    calc = calculate_needle_sinker(fabrication, dia, gauge, quantity)
    conn = get_connection()
    conn.execute(
        """
        UPDATE machine_profiles
        SET fabrication = ?, dia = ?, gauge = ?, dia_gauge_label = ?, brand = ?, quantity = ?,
            needles_per_machine = ?, sinkers_per_machine = ?, needle_spec = ?, sinker_spec = ?, remarks = ?
        WHERE id = ?
        """,
        (
            fabrication.strip(),
            float(dia),
            float(gauge),
            dia_gauge_label.strip(),
            brand.strip(),
            int(quantity),
            calc["needles_per_machine"],
            calc["sinkers_per_machine"],
            needle_spec.strip(),
            sinker_spec.strip(),
            remarks.strip(),
            machine_id,
        ),
    )
    conn.commit()
    conn.close()


def delete_machine(machine_id):
    conn = get_connection()
    conn.execute("DELETE FROM machine_profiles WHERE id = ?", (machine_id,))
    conn.commit()
    conn.close()


DEFAULT_BRANDS = [
    "Mayer & Cie",
    "Orizio",
    "Pai Long",
    "Fukuhara",
    "HaanTex",
    "Hangxing",
    "Santo",
    "Jung Long",
    "Terrot",
    "Jiunn Long",
    "Santoni",
    "Wellknit",
]


def get_all_brands():
    conn = get_connection()
    rows = conn.execute(
        "SELECT DISTINCT brand FROM machine_profiles WHERE brand IS NOT NULL AND TRIM(brand) != ''"
    ).fetchall()
    conn.close()
    seen = set()
    brands = []
    for b in DEFAULT_BRANDS + [r["brand"].strip() for r in rows]:
        if b and b.lower() not in seen:
            seen.add(b.lower())
            brands.append(b)
    return brands

