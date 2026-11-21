"""Idempotent seed for Renaissance Apparels Ltd. (79 machines: 67 Circular + 12 Flat Knit)."""

from db.calc import calculate_needle_sinker

# (sl, cat, fab, mtype, dia, gauge, label, feeders, brand, origin, qty, remarks)
RENAISSANCE_ROWS = [
    (1, "Circular", "Single Jersey", "TUBE DIA", 30, 24, "30x24", 90, "Pailung", "Taiwan", 4, "100% LYCRA ATTACHMENT"),
    (2, "Circular", "Single Jersey", "TUBE DIA", 30, 24, "30x24/28", 90, "Pailung", "Taiwan", 4, "100% LYCRA ATTACHMENT"),
    (3, "Circular", "Single Jersey", "TUBE DIA", 30, 24, "30x24/32", 90, "Pailung", "Taiwan", 2, "100% LYCRA ATTACHMENT"),
    (4, "Circular", "Single Jersey", "TUBE DIA", 32, 24, "32x24", 96, "Pailung", "Taiwan", 6, "100% LYCRA ATTACHMENT"),
    (5, "Circular", "Single Jersey", "TUBE DIA", 34, 24, "34x24", 102, "Goang Lih", "Taiwan", 4, "100% LYCRA ATTACHMENT"),
    (6, "Circular", "Single Jersey", "TUBE DIA", 34, 24, "34x24", 102, "Pailung", "Taiwan", 4, "100% LYCRA ATTACHMENT"),
    (7, "Circular", "Single Jersey", "OPEN DIA", 34, 24, "34x24", 102, "Pailung", "Taiwan", 2, "100% LYCRA ATTACHMENT"),
    (8, "Circular", "Single Jersey", "TUBE DIA", 34, 24, "34x24", 204, "Goang Lih", "Taiwan", 2, "MULTI FEEDER (6-FEEDER)"),
    (9, "Circular", "Single Jersey", "TUBE DIA", 36, 24, "36x24", 108, "Pailung", "Taiwan", 7, "100% LYCRA ATTACHMENT"),
    (10, "Circular", "Single Jersey", "OPEN DIA", 36, 24, "36x24/20", 108, "Pailung", "Taiwan", 2, "100% LYCRA ATTACHMENT"),
    (11, "Circular", "Single Jersey", "OPEN DIA", 38, 24, "38x24", 114, "Pailung", "Taiwan", 2, "100% LYCRA ATTACHMENT"),
    (12, "Circular", "Rib", "RIB+INTERLOCK", 36, 18, "36x18/24", 72, "Pailung", "Taiwan", 6, "100% LYCRA ATTACHMENT"),
    (13, "Circular", "Rib", "RIB+INTERLOCK", 38, 16, "38x16/18/24", 76, "Pailung", "Taiwan", 4, "100% LYCRA ATTACHMENT"),
    (14, "Circular", "Rib", "RIB+INTERLOCK", 40, 18, "40x18", 80, "Pailung", "Taiwan", 4, "100% LYCRA ATTACHMENT"),
    (15, "Circular", "Rib", "RIB+INTERLOCK", 42, 18, "42x18", 84, "Pailung", "Taiwan", 4, "100% LYCRA ATTACHMENT"),
    (16, "Circular", "Rib", "RIB+INTERLOCK", 44, 18, "44x18", 88, "Pailung", "Taiwan", 2, "100% LYCRA ATTACHMENT"),
    (17, "Circular", "Fleece", "FLEECE MACHINE", 34, 20, "34x20", 108, "Goang Lih", "Taiwan", 8, "100% LYCRA ATTACHMENT"),
    (18, "Flat", "Rib", "FLAT KNIT MACHINE", 80, 14, "80x14", None, "Matsuya", "China", 12, "100% LYCRA ATTACHMENT"),
]


def seed(conn):
    cur = conn.cursor()
    row = cur.execute("SELECT id FROM industries WHERE name LIKE '%Renaissance%' LIMIT 1").fetchone()
    if not row:
        return
    ind_id = row["id"]

    chk = cur.execute(
        "SELECT COUNT(*) as c, COALESCE(SUM(quantity), 0) as q, MIN(COALESCE(sort_order, 0)) as so FROM machine_profiles WHERE industry_id = ?",
        (ind_id,),
    ).fetchone()
    if chk["c"] == len(RENAISSANCE_ROWS) and chk["q"] == 79 and (chk["so"] or 0) > 0:
        return

    cur.execute("DELETE FROM machine_profiles WHERE industry_id = ?", (ind_id,))
    for sl, cat, fab, mtype, dia, gauge, lbl, feeders, brand, origin, qty, rem in RENAISSANCE_ROWS:
        calc = calculate_needle_sinker(fab, dia, gauge, qty)
        cur.execute(
            """
            INSERT INTO machine_profiles (
                industry_id, fabrication, dia, gauge, dia_gauge_label, brand, quantity,
                needles_per_machine, sinkers_per_machine, remarks,
                unit, machine_category, machine_type, feeders, origin,
                in_operation, sort_order
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '', ?, ?, ?, ?, 1, ?)
            """,
            (
                ind_id,
                fab,
                float(dia),
                float(gauge),
                lbl,
                brand,
                int(qty),
                calc["needles_per_machine"],
                calc["sinkers_per_machine"],
                rem,
                cat,
                mtype,
                feeders,
                origin,
                sl,
            ),
        )
    conn.commit()
