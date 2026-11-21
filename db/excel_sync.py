"""Excel synchronization for factories and contacts."""

import os
import re
import openpyxl
from config.constants import STATUS_RANK
from db.connection import DATA_DIR, ROOT_DIR, get_connection

NAME_MAPPING = {
    "Fakir Knitwear Ltd": "Fakir Knitwears Ltd.",
    "Gramtech (Sonali Textile)": "Gram Tech (Sonali Textile)",
    "Nur Group": "Nur Group (Raiyan Knit Composite)",
    "Esquire Knit Composite Ltd.": "L'Esquire Ltd.",
    "Alliance Knit Composit": "Alliance Knit Composite Ltd.",
    "S.M. Knitwears": "S.M. Group",
    "Tosrifa Industries Ltd.": "Tosrifa Industries Ltd",
}

SUPPLEMENTAL_LOCATIONS = [
    ("MASCO (Concept Knitting)", "Gazipura Shataish, Tongi", "Gazipur", 28.5, "https://maps.app.goo.gl/6w1qdQMLbkvDyKGt5"),
    ("Renaissance Apparels Ltd.", "Rajendrapur", "Gazipur", 50.2, "https://maps.app.goo.gl/rBiJZQdX3EPDzoaF7"),
]


def resolve_excel_path(custom_path=None):
    if custom_path and os.path.exists(custom_path):
        return custom_path
    candidates = [
        os.path.join(DATA_DIR, "Knit Industry Contacts.xlsx"),
        os.path.join(DATA_DIR, "Knit_Industry_Contacts.xlsx"),
        os.path.join(ROOT_DIR, "Knit Industry Contacts.xlsx"),
        os.path.join(ROOT_DIR, "Knit_Industry_Contacts.xlsx"),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return candidates[0]


EXCEL_PATH = resolve_excel_path()


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


def sync_from_excel(conn=None, excel_path=None):
    """Idempotently sync factories and contacts from Knit Industry Contacts.xlsx into SQLite."""
    close_conn = False
    if conn is None:
        conn = get_connection()
        close_conn = True

    target_excel = resolve_excel_path(excel_path)
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
            map_url = (
                cell_f.hyperlink.target
                if (cell_f.hyperlink and cell_f.hyperlink.target)
                else _extract_hyperlink(cell_f.value)
            )
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

    for s_name, s_loc, s_cluster, s_dist, s_map in SUPPLEMENTAL_LOCATIONS:
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
