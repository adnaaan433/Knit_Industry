"""CRUD repository for industries, contacts, updates, and machines."""

from config.constants import DEFAULT_BRANDS
from db.calc import calculate_needle_sinker, format_dia_gauge
from db.connection import get_connection


# --- Industries CRUD ---

def get_all_industries():
    conn = get_connection()
    rows = conn.execute("""
        SELECT
            i.*,
            (SELECT COUNT(*) FROM contacts c WHERE c.industry_id = i.id) AS contact_count,
            (SELECT COUNT(*) FROM updates u WHERE u.industry_id = i.id) AS update_count,
            (SELECT COALESCE(SUM(m.quantity), 0) FROM machine_profiles m WHERE m.industry_id = i.id) AS machine_count,
            (SELECT COALESCE(SUM(CASE WHEN COALESCE(m.in_operation, 1) = 1 THEN m.quantity ELSE 0 END), 0)
             FROM machine_profiles m WHERE m.industry_id = i.id) AS operating_machine_count,
            (SELECT MAX(u.visit_date) FROM updates u WHERE u.industry_id = i.id) AS last_visit_date,
            (SELECT MIN(u.next_followup_date) FROM updates u
             WHERE u.industry_id = i.id AND u.next_followup_date IS NOT NULL AND TRIM(u.next_followup_date) != '') AS next_followup_date
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
        "INSERT INTO industries (name, location_area, cluster, distance_km, map_url, status, general_notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (name.strip(), location_area.strip(), cluster.strip(), distance_km, map_url.strip(), status, general_notes.strip()),
    )
    new_id = cur.lastrowid
    conn.commit()
    conn.close()
    return new_id


def update_industry(industry_id, name, location_area, cluster, distance_km, map_url, status, general_notes):
    conn = get_connection()
    conn.execute(
        """UPDATE industries SET name=?, location_area=?, cluster=?, distance_km=?, map_url=?, status=?, general_notes=?, updated_at=CURRENT_TIMESTAMP WHERE id=?""",
        (name.strip(), location_area.strip(), cluster.strip(), distance_km, map_url.strip(), status, general_notes.strip(), industry_id),
    )
    conn.commit()
    conn.close()


def update_industry_status(industry_id, status):
    conn = get_connection()
    conn.execute("UPDATE industries SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (status, industry_id))
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
    rows = conn.execute("SELECT * FROM contacts WHERE industry_id = ? ORDER BY id ASC", (industry_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_contacts():
    conn = get_connection()
    rows = conn.execute("""
        SELECT c.*, i.name AS industry_name, i.cluster AS industry_cluster
        FROM contacts c JOIN industries i ON i.id = c.industry_id
        ORDER BY i.name ASC, c.id ASC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_contact(industry_id, name, designation="", phone="", email="", butex_batch="", status="New", notes=""):
    conn = get_connection()
    conn.execute(
        "INSERT INTO contacts (industry_id, name, designation, phone, email, butex_batch, status, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (industry_id, name.strip(), designation.strip(), phone.strip(), email.strip(), butex_batch.strip(), status, notes.strip()),
    )
    conn.commit()
    conn.close()


def update_contact(contact_id, name, designation, phone, email, butex_batch, status, notes):
    conn = get_connection()
    conn.execute(
        "UPDATE contacts SET name=?, designation=?, phone=?, email=?, butex_batch=?, status=?, notes=? WHERE id=?",
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
    rows = conn.execute("SELECT * FROM updates WHERE industry_id = ? ORDER BY visit_date DESC, id DESC", (industry_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_updates():
    conn = get_connection()
    rows = conn.execute("""
        SELECT u.*, i.name AS industry_name, i.cluster AS industry_cluster, i.status AS industry_status
        FROM updates u JOIN industries i ON i.id = u.industry_id
        ORDER BY u.visit_date DESC, u.id DESC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_update(industry_id, visit_date, visit_type, attendees, meeting_minutes, action_items="", next_followup_date=""):
    conn = get_connection()
    conn.execute(
        "INSERT INTO updates (industry_id, visit_date, visit_type, attendees, meeting_minutes, action_items, next_followup_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (industry_id, str(visit_date), visit_type, attendees.strip(), meeting_minutes.strip(), action_items.strip(), str(next_followup_date) if next_followup_date else ""),
    )
    conn.commit()
    conn.close()


def edit_update(update_id, visit_date, visit_type, attendees, meeting_minutes, action_items="", next_followup_date=""):
    conn = get_connection()
    conn.execute(
        "UPDATE updates SET visit_date=?, visit_type=?, attendees=?, meeting_minutes=?, action_items=?, next_followup_date=? WHERE id=?",
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
    conn.execute("UPDATE industries SET machine_profile_notes = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (notes.strip(), industry_id))
    conn.commit()
    conn.close()


def _enrich_machine_row(r):
    d = dict(r)
    in_op = int(d.get("in_operation") if d.get("in_operation") is not None else 1)
    d["in_operation"] = in_op
    qty = int(d.get("quantity") or 0) if in_op else 0
    calc = calculate_needle_sinker(d.get("fabrication", ""), d.get("dia", 0), d.get("gauge", 0), qty)
    d["needles_per_machine"] = calc["needles_per_machine"] if in_op else 0
    d["sinkers_per_machine"] = calc["sinkers_per_machine"] if in_op else 0
    d["total_needles"] = calc["total_needles"] if in_op else 0
    d["total_sinkers"] = calc["total_sinkers"] if in_op else 0
    return d


def get_machines(industry_id):
    conn = get_connection()
    rows = conn.execute("""
        SELECT * FROM machine_profiles WHERE industry_id = ?
        ORDER BY COALESCE(unit, '') ASC, CASE WHEN COALESCE(sort_order, 0) > 0 THEN 0 ELSE 1 END,
            COALESCE(sort_order, 0) ASC,
            CASE fabrication WHEN 'Fleece' THEN 1 WHEN 'H/Jersey' THEN 2 WHEN 'Single Jersey' THEN 3 WHEN 'Rib' THEN 4 WHEN 'Interlock' THEN 5 ELSE 6 END,
            dia ASC, gauge ASC, dia_gauge_label ASC, brand ASC, id ASC
    """, (industry_id,)).fetchall()
    conn.close()
    return [_enrich_machine_row(r) for r in rows]


def get_all_machines():
    conn = get_connection()
    rows = conn.execute("""
        SELECT m.*, i.name AS industry_name, i.cluster AS industry_cluster
        FROM machine_profiles m JOIN industries i ON i.id = m.industry_id
        ORDER BY i.name ASC, COALESCE(m.unit, '') ASC, COALESCE(m.sort_order, 0) ASC, m.id ASC
    """).fetchall()
    conn.close()
    return [_enrich_machine_row(r) for r in rows]


def _prepare_machine_params(fabrication, dia, gauge, dia_gauge_label, brand, quantity, needle_spec, sinker_spec, remarks, unit, machine_category, machine_type, feeders, origin, model, capacity_kg, machine_no, in_operation, sort_order):
    if not (dia_gauge_label or "").strip():
        dia_gauge_label = format_dia_gauge(dia, gauge)
    in_op = int(in_operation if in_operation is not None else 1)
    calc = calculate_needle_sinker(fabrication, dia, gauge, quantity if in_op else 0)
    return (
        (fabrication or "").strip(), float(dia or 0), float(gauge or 0), (dia_gauge_label or "").strip(),
        (brand or "").strip(), int(quantity or 1), calc["needles_per_machine"], calc["sinkers_per_machine"],
        (needle_spec or "").strip(), (sinker_spec or "").strip(), (remarks or "").strip(),
        (unit or "").strip(), (machine_category or "Circular").strip(), (machine_type or "").strip(),
        int(feeders) if feeders not in (None, "", "—") else None, (origin or "").strip(), (model or "").strip(),
        float(capacity_kg) if capacity_kg not in (None, "", "—") else None, (machine_no or "").strip(),
        in_op, int(sort_order or 0),
    )


def add_machine(industry_id, fabrication, dia, gauge, dia_gauge_label="", brand="", quantity=1, needle_spec="", sinker_spec="", remarks="", unit="", machine_category="Circular", machine_type="", feeders=None, origin="", model="", capacity_kg=None, machine_no="", in_operation=1, sort_order=0):
    params = _prepare_machine_params(fabrication, dia, gauge, dia_gauge_label, brand, quantity, needle_spec, sinker_spec, remarks, unit, machine_category, machine_type, feeders, origin, model, capacity_kg, machine_no, in_operation, sort_order)
    conn = get_connection()
    conn.execute(
        """INSERT INTO machine_profiles (industry_id, fabrication, dia, gauge, dia_gauge_label, brand, quantity, needles_per_machine, sinkers_per_machine, needle_spec, sinker_spec, remarks, unit, machine_category, machine_type, feeders, origin, model, capacity_kg, machine_no, in_operation, sort_order)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (industry_id, *params),
    )
    conn.commit()
    conn.close()


def update_machine(machine_id, fabrication, dia, gauge, dia_gauge_label, brand, quantity, needle_spec="", sinker_spec="", remarks="", unit="", machine_category="Circular", machine_type="", feeders=None, origin="", model="", capacity_kg=None, machine_no="", in_operation=1, sort_order=0):
    params = _prepare_machine_params(fabrication, dia, gauge, dia_gauge_label, brand, quantity, needle_spec, sinker_spec, remarks, unit, machine_category, machine_type, feeders, origin, model, capacity_kg, machine_no, in_operation, sort_order)
    conn = get_connection()
    conn.execute(
        """UPDATE machine_profiles SET fabrication=?, dia=?, gauge=?, dia_gauge_label=?, brand=?, quantity=?, needles_per_machine=?, sinkers_per_machine=?, needle_spec=?, sinker_spec=?, remarks=?, unit=?, machine_category=?, machine_type=?, feeders=?, origin=?, model=?, capacity_kg=?, machine_no=?, in_operation=?, sort_order=? WHERE id=?""",
        (*params, machine_id),
    )
    conn.commit()
    conn.close()


def delete_machine(machine_id):
    conn = get_connection()
    conn.execute("DELETE FROM machine_profiles WHERE id = ?", (machine_id,))
    conn.commit()
    conn.close()


def get_all_brands():
    conn = get_connection()
    rows = conn.execute("SELECT DISTINCT brand FROM machine_profiles WHERE brand IS NOT NULL AND TRIM(brand) != ''").fetchall()
    conn.close()
    seen = set()
    brands = []
    for b in DEFAULT_BRANDS + [r["brand"].strip() for r in rows]:
        if b and b.lower() not in seen:
            seen.add(b.lower())
            brands.append(b)
    return brands
