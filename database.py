import os
import re
import sqlite3
import openpyxl

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "crm_data.db")
EXCEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Knit Industry Contacts.xlsx")
FAKIR_EXCEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Fakir Knitwears Ltd Knitting Section.xlsx")

# Name normalization map to link Contacts sheet names to canonical Factory Locations names
NAME_MAPPING = {
    "Fakir Knitwear Ltd": "Fakir Knitwears Ltd.",
    "Gramtech (Sonali Textile)": "Gram Tech (Sonali Textile)",
    "Nur Group": "Nur Group (Raiyan Knit Composite)",
    "Esquire Knit Composite Ltd.": "L'Esquire Ltd.",
    "Alliance Knit Composit": "Alliance Knit Composite Ltd.",
    "S.M. Knitwears": "S.M. Group",
    "Tosrifa Industries Ltd.": "Tosrifa Industries Ltd",
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

    # Automatically sync any new/updated rows from Excel on startup
    if os.path.exists(EXCEL_PATH):
        sync_from_excel(conn)

    # Seed L'Esquire Knit Composite Ltd. machine profile from example image if empty
    seed_lesquire_machines(conn)

    # Seed Fakir Knitwears Ltd. machine profile from Fakir Knitwears Ltd Knitting Section.xlsx if empty
    seed_fakir_machines(conn)

    # Seed MASCO (Concept Knitting) machine profile if empty
    seed_masco_machines(conn)

    # Seed Renaissance Apparels Ltd. machine profile if empty
    seed_renaissance_machines(conn)

    # Seed Adury Knit Composite machine profile if empty
    seed_adury_machines(conn)

    # Seed Tosrifa Industries Ltd machine profile if empty
    seed_tosrifa_machines(conn)

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


STATUS_RANK = {"New": 0, "Contacted": 1, "Scheduled": 2, "Visited": 3, "Follow-up": 4, "Active Client": 5}


def sync_from_excel(conn=None, excel_path=None):
    """Idempotently sync factories and contacts from Knit Industry Contacts.xlsx into SQLite."""
    close_conn = False
    if conn is None:
        conn = get_connection()
        close_conn = True

    target_excel = excel_path or EXCEL_PATH
    if not os.path.exists(target_excel):
        if close_conn:
            conn.close()
        return

    wb_val = openpyxl.load_workbook(target_excel, data_only=True)
    wb_formula = openpyxl.load_workbook(target_excel, data_only=False)

    cur = conn.cursor()
    industry_ids = {
        r["name"]: r["id"]
        for r in cur.execute("SELECT id, name FROM industries").fetchall()
    }

    if "Factory Locations" in wb_val.sheetnames:
        ws_val = wb_val["Factory Locations"]
        ws_form = wb_formula["Factory Locations"]
        for row_idx in range(2, ws_val.max_row + 1):
            raw_name = _clean_val(ws_val.cell(row_idx, 2).value)
            if not raw_name:
                continue
            name = NAME_MAPPING.get(raw_name, raw_name)
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

            if name not in industry_ids:
                cur.execute(
                    """
                    INSERT INTO industries (name, location_area, cluster, distance_km, map_url, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (name, loc_area, cluster, dist_km, map_url, status),
                )
                industry_ids[name] = cur.lastrowid
            else:
                ind_id = industry_ids[name]
                existing = cur.execute("SELECT * FROM industries WHERE id = ?", (ind_id,)).fetchone()
                new_st = existing["status"]
                if STATUS_RANK.get(status, 0) > STATUS_RANK.get(new_st, 0):
                    new_st = status
                cur.execute(
                    """
                    UPDATE industries
                    SET location_area = COALESCE(NULLIF(?, ''), location_area),
                        cluster = COALESCE(NULLIF(?, ''), cluster),
                        distance_km = COALESCE(?, distance_km),
                        map_url = COALESCE(NULLIF(?, ''), map_url),
                        status = ?
                    WHERE id = ?
                    """,
                    (loc_area, cluster, dist_km, map_url, new_st, ind_id),
                )

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
                    "INSERT INTO industries (name, status) VALUES (?, ?)",
                    (factory_name, c_status),
                )
                industry_ids[factory_name] = cur.lastrowid

            ind_id = industry_ids[factory_name]

            # Upgrade industry status if contact status is higher
            curr_st = cur.execute("SELECT status FROM industries WHERE id = ?", (ind_id,)).fetchone()["status"]
            if STATUS_RANK.get(c_status, 0) > STATUS_RANK.get(curr_st, 0):
                cur.execute("UPDATE industries SET status = ? WHERE id = ?", (c_status, ind_id))

            if person:
                existing_contacts = cur.execute(
                    "SELECT * FROM contacts WHERE industry_id = ?",
                    (ind_id,),
                ).fetchall()

                matched_id = None
                for ec in existing_contacts:
                    ec_phone = (ec["phone"] or "").strip()
                    ec_name = (ec["name"] or "").strip().lower()
                    p_low = person.lower()
                    if phone and ec_phone and phone == ec_phone:
                        matched_id = ec["id"]
                        break
                    if ec_name == p_low or (not ec_phone and ec_name and ec_name in p_low):
                        matched_id = ec["id"]
                        break

                if matched_id is not None:
                    cur.execute(
                        """
                        UPDATE contacts
                        SET name = ?,
                            designation = COALESCE(NULLIF(?, ''), designation),
                            phone = COALESCE(NULLIF(?, ''), phone),
                            butex_batch = COALESCE(NULLIF(?, ''), butex_batch),
                            status = ?
                        WHERE id = ?
                        """,
                        (person, designation, phone, batch, c_status, matched_id),
                    )
                else:
                    cur.execute(
                        """
                        INSERT INTO contacts (industry_id, name, designation, phone, butex_batch, status)
                        VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        (ind_id, person, designation, phone, batch, c_status),
                    )

    # Apply supplemental location details for factories not present in Factory Locations sheet
    supplemental_locations = [
        ("MASCO (Concept Knitting)", "Gazipura Shataish, Tongi", "Gazipur", 28.5, "https://maps.app.goo.gl/6w1qdQMLbkvDyKGt5"),
        ("Renaissance Apparels Ltd.", "Rajendrapur", "Gazipur", 50.2, "https://maps.app.goo.gl/rBiJZQdX3EPDzoaF7"),
    ]
    for s_name, s_loc, s_cluster, s_dist, s_map in supplemental_locations:
        cur.execute(
            """
            UPDATE industries
            SET location_area = COALESCE(NULLIF(location_area, ''), ?),
                cluster = COALESCE(NULLIF(cluster, ''), ?),
                distance_km = COALESCE(distance_km, ?),
                map_url = COALESCE(NULLIF(map_url, ''), ?)
            WHERE name = ?
            """,
            (s_loc, s_cluster, s_dist, s_map, s_name),
        )

    conn.commit()
    if close_conn:
        conn.close()


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


def _parse_fakir_unit_blocks(ws):
    blocks = []
    for r_idx in range(1, ws.max_row + 1):
        for col_start in (1, 11):
            v1 = str(ws.cell(r_idx, col_start).value or "").strip()
            v2 = str(ws.cell(r_idx, col_start + 1).value or "").strip()
            if v1 in ("Serial No.", "SL.") and "M/C" in v2:
                rows = []
                total_val = 0
                curr = r_idx + 1
                while curr <= ws.max_row:
                    sn = ws.cell(curr, col_start).value
                    mc = ws.cell(curr, col_start + 1).value
                    mt = str(ws.cell(curr, col_start + 7).value or "").strip()
                    qty = ws.cell(curr, col_start + 8).value
                    if "Total" in mt:
                        try:
                            total_val = int(float(qty))
                        except (ValueError, TypeError):
                            total_val = len(rows)
                        break
                    if sn is None and mc is None:
                        break
                    if mc is not None and str(mc).strip():
                        raw_feed = ws.cell(curr, col_start + 6).value
                        try:
                            feed_str = str(int(float(raw_feed))) if raw_feed not in (None, "—", "") else "—"
                        except (ValueError, TypeError):
                            feed_str = str(raw_feed)
                        try:
                            sn_val = int(float(sn)) if sn not in (None, " ") else len(rows) + 1
                        except (ValueError, TypeError):
                            sn_val = len(rows) + 1
                        try:
                            qty_val = int(float(qty)) if qty not in (None, "—", "") else 1
                        except (ValueError, TypeError):
                            qty_val = 1
                        rows.append(
                            {
                                "sn": sn_val,
                                "mc_no": str(mc).strip(),
                                "brand": str(ws.cell(curr, col_start + 2).value or "—").strip(),
                                "origin": str(ws.cell(curr, col_start + 3).value or "—").strip(),
                                "dia": str(ws.cell(curr, col_start + 4).value or "—").strip(),
                                "gauge": str(ws.cell(curr, col_start + 5).value or "—").strip(),
                                "feeders": feed_str,
                                "mc_type": mt if mt else "—",
                                "qty": qty_val,
                            }
                        )
                    curr += 1
                if rows:
                    blocks.append(
                        {
                            "row_start": r_idx,
                            "col_start": col_start,
                            "header_sn": v1,
                            "rows": rows,
                            "total": total_val or sum(r["qty"] for r in rows),
                        }
                    )
    return blocks


def get_fakir_knitting_data():
    """Return Fakir Knitwears Ltd. Unit-1, Unit-2, and Overall Summary data (from Excel if present, else saved data)."""
    if not os.path.exists(FAKIR_EXCEL_PATH):
        from fakir_data import FAKIR_SAVED_DATA
        return FAKIR_SAVED_DATA
    wb = openpyxl.load_workbook(FAKIR_EXCEL_PATH, data_only=True)
    u1_blocks = _parse_fakir_unit_blocks(wb["Sheet1"]) if "Sheet1" in wb.sheetnames else []
    u2_blocks = _parse_fakir_unit_blocks(wb["Sheet2"]) if "Sheet2" in wb.sheetnames else []

    unit1_summary = {
        "title": "Unit-1 Summary",
        "brand_wise": [
            ("Jiunn Long:", 77),
            ("U-Masa:", 28),
            ("Fukuhara:", 1),
            ("Samara ENT.:", 1),
            ("NOT IN OPT.:", 2),
            ("TOTAL:", 109),
        ],
        "type_wise": [
            ("S/J:", 78),
            ("D/J:", 28),
            ("Jacquard:", 1),
            ("TOTAL:", 107),
        ],
        "dia_wise": [
            ("20 inch", 1),
            ("26 inch", 1),
            ("28 inch", 3),
            ("30 inch", 3),
            ("32 inch", 12),
            ("34 inch", 10),
            ("36 inch", 23),
            ("38 inch", 23),
            ("40 inch", 19),
            ("42 inch", 7),
            ("44 inch", 2),
            ("46 inch", 3),
            ("TOTAL:", 107),
        ],
        "gauge_wise": [
            ("14 G", 2),
            ("18 G", 18),
            ("20 G", 14),
            ("22 G", 4),
            ("24 G", 67),
            ("26 G", 1),
            ("28 G", 1),
            ("TOTAL:", 107),
        ],
    }

    unit2_summary = {
        "title": "Unit-2 Summary",
        "brand_wise": [
            ("Fukuhara", 40),
            ("Mayer&Cie:", 18),
            ("TOTAL:", 58),
        ],
        "type_wise": [
            ("S/J:", 35),
            ("D/J:", 14),
            ("S/J (AS):", 6),
            ("D/J (AS)", 1),
            ("S/J (3th F)", 2),
            ("TOTAL:", 58),
        ],
        "dia_wise": [
            ("30 inch", 2),
            ("32 inch", 1),
            ("34 inch", 7),
            ("36 inch", 13),
            ("38 inch", 14),
            ("40 inch", 9),
            ("42 inch", 7),
            ("44 inch", 5),
            ("TOTAL:", 58),
        ],
        "gauge_wise": [
            ("18 G", 13),
            ("20 G", 3),
            ("24 G", 37),
            ("28 G", 4),
            ("36 G", 1),
            ("TOTAL:", 58),
        ],
    }

    overall_summary = {
        "title": "Overall Summary",
        "brand_wise": [
            ("Jiunn Long:", 77),
            ("U-Masa:", 28),
            ("Samara ENT.:", 1),
            ("Fukuhara", 41),
            ("Mayer&Cie:", 18),
            ("TOTAL:", 165),
        ],
        "type_wise": [
            ("S/J:", 113),
            ("D/J:", 42),
            ("S/J (AS):", 6),
            ("D/J (AS)", 1),
            ("S/J (3th F)", 2),
            ("Jacquard:", 1),
            ("TOTAL:", 165),
        ],
        "dia_wise": [
            ("20 inch", 1),
            ("26 inch", 1),
            ("28 inch", 3),
            ("30 inch", 5),
            ("32 inch", 13),
            ("34 inch", 17),
            ("36 inch", 36),
            ("38 inch", 37),
            ("40 inch", 28),
            ("42 inch", 14),
            ("44 inch", 7),
            ("46 inch", 3),
            ("TOTAL:", 165),
        ],
        "gauge_wise": [
            ("14 G", 2),
            ("18 G", 31),
            ("20 G", 17),
            ("22 G", 4),
            ("24 G", 104),
            ("26 G", 1),
            ("28 G", 5),
            ("36 G", 1),
            ("TOTAL:", 165),
        ],
    }

    return {
        "unit1_blocks": u1_blocks,
        "unit2_blocks": u2_blocks,
        "unit1_summary": unit1_summary,
        "unit2_summary": unit2_summary,
        "overall_summary": overall_summary,
    }


def seed_fakir_machines(conn):
    """Seed Fakir Knitwears Ltd. consolidated machine rows into machine_profiles so total counts appear across the CRM."""
    cur = conn.cursor()
    row = cur.execute("SELECT id FROM industries WHERE name LIKE '%Fakir Knitwear%' LIMIT 1").fetchone()
    if not row:
        return
    ind_id = row["id"]

    cnt = cur.execute("SELECT COUNT(*) as c FROM machine_profiles WHERE industry_id = ?", (ind_id,)).fetchone()["c"]
    if cnt > 0:
        return

    data = get_fakir_knitting_data()
    if not data:
        return

    grouped_counts = {}
    for unit_name, blocks in [("Unit-1", data["unit1_blocks"]), ("Unit-2", data["unit2_blocks"])]:
        for b in blocks:
            for r in b["rows"]:
                mc_type = r["mc_type"] if r["mc_type"] != "—" else "Not in Operation"
                brand = r["brand"].replace("Mayer&Cie", "Mayer & Cie")
                dia_num = 0.0
                gauge_num = 0.0
                m_d = re.search(r"(\d+)", r["dia"])
                m_g = re.search(r"(\d+)", r["gauge"])
                if m_d:
                    dia_num = float(m_d.group(1))
                if m_g:
                    gauge_num = float(m_g.group(1))
                if dia_num > 0 and gauge_num > 0:
                    label = f"{int(dia_num)}x{int(gauge_num)}"
                else:
                    label = "—"
                key = (mc_type, dia_num, gauge_num, label, brand)
                grouped_counts[key] = grouped_counts.get(key, 0) + int(r["qty"])

    for (mc_type, dia_num, gauge_num, label, brand), qty in sorted(
        grouped_counts.items(), key=lambda x: (x[0][0], x[0][1], x[0][2], x[0][4])
    ):
        cur.execute(
            """
            INSERT INTO machine_profiles (
                industry_id, fabrication, dia, gauge, dia_gauge_label, brand, quantity,
                needles_per_machine, sinkers_per_machine
            ) VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0)
            """,
            (ind_id, mc_type, dia_num, gauge_num, label, brand, qty),
        )
    conn.commit()


def seed_masco_machines(conn):
    """Seed MASCO (Concept Knitting) machine counts into machine_profiles so total machines (197) appear across the CRM."""
    cur = conn.cursor()
    row = cur.execute("SELECT id FROM industries WHERE name LIKE '%MASCO%' LIMIT 1").fetchone()
    if not row:
        return
    ind_id = row["id"]

    cnt = cur.execute("SELECT COUNT(*) as c FROM machine_profiles WHERE industry_id = ?", (ind_id,)).fetchone()["c"]
    if cnt > 0:
        return

    masco_summary_rows = [
        ("Unit-1 Double Jersey", 36, 18, "34\"–40\"", "FUKUHARA", 23),
        ("Unit-1 Single Jersey", 34, 24, "30\"–42\"", "FUKUHARA / KEUM YUNG / LISKY / SANTONI", 98),
        ("Unit-2 Double Jersey", 36, 18, "34\"–40\"", "FUKUHARA / KEUM YUNG", 9),
        ("Unit-2 Single Jersey", 32, 24, "23\"–36\"", "PAI LUNG / FUKUHARA / SANTONI / LISKY / SAN DA", 21),
        ("Unit-2 Eng. Stripe D/J", 35, 24, "34\"–36\"", "FUKUHARA", 2),
        ("Unit-2 Eng. Stripe S/J", 32, 24, "30\"–36\"", "PAI LUNG / FUKUHARA", 8),
        ("Unit-2 Jacquard & Pointal", 32, 18, "30\"–34\"", "HANG XING", 8),
        ("Unit-2 Collar (Flat Knit)", 0, 14, "40\"–80\" Bed", "MATSUYA / KAUO HENG", 28),
    ]
    for fab, dia, gauge, lbl, brand, qty in masco_summary_rows:
        cur.execute(
            """
            INSERT INTO machine_profiles (
                industry_id, fabrication, dia, gauge, dia_gauge_label, brand, quantity,
                needles_per_machine, sinkers_per_machine
            ) VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0)
            """,
            (ind_id, fab, dia, gauge, lbl, brand, qty),
        )
    conn.commit()


def seed_renaissance_machines(conn):
    """Seed Renaissance Apparels Ltd. knitting machines (67 Circular + 12 Flat Knit = 79) into machine_profiles."""
    cur = conn.cursor()
    row = cur.execute("SELECT id FROM industries WHERE name LIKE '%Renaissance%' LIMIT 1").fetchone()
    if not row:
        return
    ind_id = row["id"]

    cnt = cur.execute("SELECT COUNT(*) as c FROM machine_profiles WHERE industry_id = ?", (ind_id,)).fetchone()["c"]
    if cnt > 0:
        return

    renaissance_rows = [
        ("Jersey Machine", 30, 24, "30x24", "PAILUNG", 4),
        ("Jersey Machine", 30, 24, "30x24/28", "PAILUNG", 4),
        ("Jersey Machine", 30, 24, "30x24/32", "PAILUNG", 2),
        ("Jersey Machine", 32, 24, "32x24", "PAILUNG", 6),
        ("Jersey Machine", 34, 24, "34x24", "GOANG LIH", 4),
        ("Jersey Machine", 34, 24, "34x24", "PAILUNG", 4),
        ("Jersey Machine", 34, 24, "34x24 (Open Dia)", "PAILUNG", 2),
        ("Jersey Machine", 34, 24, "34x24 (Multi Feeder)", "GOANG LIH", 2),
        ("Jersey Machine", 36, 24, "36x24", "PAILUNG", 7),
        ("Jersey Machine", 36, 24, "36x24/20 (Open Dia)", "PAILUNG", 2),
        ("Jersey Machine", 38, 24, "38x24 (Open Dia)", "PAILUNG", 2),
        ("Rib+Interlock Machine", 36, 18, "36x18/24", "PAILUNG", 6),
        ("Rib+Interlock Machine", 38, 16, "38x16/18/24", "PAILUNG", 4),
        ("Rib+Interlock Machine", 40, 18, "40x18", "PAILUNG", 4),
        ("Rib+Interlock Machine", 42, 18, "42x18", "PAILUNG", 4),
        ("Rib+Interlock Machine", 44, 18, "44x18", "PAILUNG", 2),
        ("Fleece Machine", 34, 20, "34x20", "GOANG LIH", 8),
        ("Flat Knit Machine", 80, 14, "80x14", "MATSUYA", 12),
    ]
    for fab, dia, gauge, lbl, brand, qty in renaissance_rows:
        cur.execute(
            """
            INSERT INTO machine_profiles (
                industry_id, fabrication, dia, gauge, dia_gauge_label, brand, quantity,
                needles_per_machine, sinkers_per_machine
            ) VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0)
            """,
            (ind_id, fab, dia, gauge, lbl, brand, qty),
        )
    conn.commit()


def seed_adury_machines(conn):
    """Seed Adury Knit Composite knitting machines (63 Circular + 42 Flat Knit = 105) into machine_profiles."""
    cur = conn.cursor()
    row = cur.execute("SELECT id FROM industries WHERE name LIKE '%Adury%' LIMIT 1").fetchone()
    if not row:
        return
    ind_id = row["id"]

    cnt = cur.execute("SELECT COUNT(*) as c FROM machine_profiles WHERE industry_id = ?", (ind_id,)).fetchone()["c"]
    if cnt > 0:
        return

    adury_rows = [
        ("Single Jersey (Open)", 33, 24, "30\"–36\" x 24G", "With FF Lycra Attachments", 4),
        ("Single Jersey (Tube)", 32, 24, "25\"–40\" x 14G–28G", "With FF Lycra Attachments", 29),
        ("Rib & Interlock", 35, 18, "30\"–40\" x 18G–24G", "With Interlock conversion Facilities", 8),
        ("Fleece", 32, 20, "30\"–34\" x 20G", "With Lycra Attachments", 17),
        ("Engineering Stripe S/J", 34, 20, "30\"–38\" x 14G/20G/24G", "6 Finger Auto Stripe", 5),
        ("Collar & Cuff (Flat Knit)", 60, 14, "45\"–80\" x 14G", "Semi Jacquard & Jacquard", 42),
    ]
    for fab, dia, gauge, lbl, brand, qty in adury_rows:
        cur.execute(
            """
            INSERT INTO machine_profiles (
                industry_id, fabrication, dia, gauge, dia_gauge_label, brand, quantity,
                needles_per_machine, sinkers_per_machine
            ) VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0)
            """,
            (ind_id, fab, dia, gauge, lbl, brand, qty),
        )
    conn.commit()


def seed_tosrifa_machines(conn):
    """Seed Tosrifa Industries Ltd knitting machines (45 Circular + 24 Flat Bed = 69) into machine_profiles."""
    cur = conn.cursor()
    row = cur.execute("SELECT id FROM industries WHERE name LIKE '%Tosrifa%' LIMIT 1").fetchone()
    if not row:
        return
    ind_id = row["id"]

    cnt = cur.execute("SELECT COUNT(*) as c FROM machine_profiles WHERE industry_id = ?", (ind_id,)).fetchone()["c"]
    if cnt > 0:
        return

    tosrifa_rows = [
        ("SINGLE JERSEY", 34, 24, "30\"–38\"", "Keum Yong / Mayer & Cie", 10),
        ("Fleece, S/Jersey", 30, 20, "30\" x 20/24/12", "Mayer & Cie / Lisky / Point", 8),
        ("Fleece", 30, 20, "30\" x 20/12", "Lisky / Point", 12),
        ("Rib/Spacer", 42, 18, "42\" x 18G", "Lisky", 6),
        ("Rib", 32, 18, "30\"–34\" x 18G", "Mayer & Cie", 3),
        ("Interlock", 34, 24, "30\"–34\" x 24/28G", "Keum Yong", 4),
        ("Rib/Interlock", 34, 18, "32\"–34\" x 18/24G", "Mayer & Cie", 2),
        ("Flat Bed Knitting Machine", 60, 14, "40\"–80\" Bed", "Shima Seiki / Matsuya", 24),
    ]
    for fab, dia, gauge, lbl, brand, qty in tosrifa_rows:
        cur.execute(
            """
            INSERT INTO machine_profiles (
                industry_id, fabrication, dia, gauge, dia_gauge_label, brand, quantity,
                needles_per_machine, sinkers_per_machine
            ) VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0)
            """,
            (ind_id, fab, dia, gauge, lbl, brand, qty),
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

