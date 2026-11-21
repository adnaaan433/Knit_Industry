"""Idempotent seed for Gram Tech (Sonali Textile) (32 sets: 28 Circular + 4 Flat Knit)."""

import re
from db.calc import calculate_needle_sinker

# (sl, cat, fab, mtype, dia, gauge_str, feeders, brand, origin, qty, remarks)
GRAMTECH_ROWS = [
    (1, "Circular", "Single Jersey", "Open Dia S/J", 32, "24,28", 102, "Pailung", "Taiwan", 3, "S/J, Lycra S/J & Derivatives | 100% Lycra"),
    (2, "Circular", "Single Jersey", "Open Dia S/J", 32, "24", 102, "Jiunn Long", "Taiwan", 2, "S/J, Lycra S/J & Derivatives | 100% Lycra"),
    (3, "Circular", "Single Jersey", "Open Dia S/J", 34, "24,28", 108, "Pailung", "Taiwan", 2, "S/J, Lycra S/J & Derivatives | 100% Lycra"),
    (4, "Circular", "Single Jersey", "Open Dia S/J", 34, "20,24", 108, "Jiunn Long", "Taiwan", 3, "S/J, Lycra S/J & Derivatives | 100% Lycra"),
    (5, "Circular", "Single Jersey", "Open Dia S/J", 36, "24", 116, "Pailung", "Taiwan", 1, "S/J, Lycra S/J & Derivatives | 100% Lycra"),
    (6, "Circular", "Single Jersey", "Open Dia S/J", 36, "24", 116, "Jiunn Long", "Taiwan", 2, "S/J, Lycra S/J & Derivatives | 100% Lycra"),
    (7, "Circular", "Single Jersey", "Open Dia S/J", 38, "24", 120, "Pailung", "Taiwan", 1, "S/J, Lycra S/J & Derivatives | 100% Lycra"),
    (8, "Circular", "Single Jersey", "Tube Dia S/J", 26, "24", 78, "Zentex", "Singapore", 1, "S/J, Lycra S/J & Derivatives | 100% Lycra"),
    (9, "Circular", "Single Jersey", "Tube Dia S/J", 30, "24", 90, "Zentex", "Singapore", 2, "S/J, Lycra S/J & Derivatives | 100% Lycra"),
    (10, "Circular", "Fleece", "Tube Fleece", 34, "20,24", 108, "Goang Lih", "Taiwan", 2, "Fleece, Baby Fleece, Cross Fleece | 100% Lycra"),
    (11, "Circular", "Fleece", "Tube Fleece", 36, "20,24", 116, "Goang Lih", "Taiwan", 2, "Fleece, Baby Fleece, Cross Fleece | 100% Lycra"),
    (12, "Circular", "Rib", "Tube Rib/Interlock", 32, "18", 64, "Zentex", "Singapore", 1, "RIB, Lycra RIB & Derivatives | 100% Lycra"),
    (13, "Circular", "Rib", "Tube Rib/Interlock", 34, "18", 68, "Zentex", "Singapore", 1, "RIB, Lycra RIB & Derivatives | 100% Lycra"),
    (14, "Circular", "Rib", "Tube Rib/Interlock", 36, "18", 72, "Zentex", "Singapore", 1, "RIB, Lycra RIB & Derivatives | 100% Lycra"),
    (15, "Circular", "Rib", "Tube Rib/Interlock", 38, "18", 72, "Zentex", "Singapore", 1, "RIB, Lycra RIB & Derivatives | 100% Lycra"),
    (16, "Circular", "Rib", "Tube Rib/Interlock", 40, "18,24", 80, "Jiunn Long", "Taiwan", 1, "RIB, Lycra RIB & Derivatives | 100% Lycra"),
    (17, "Circular", "Rib", "Tube Rib/Interlock", 42, "18,24,28", 84, "Jiunn Long", "Taiwan", 2, "RIB, Lycra RIB & Derivatives | 100% Lycra"),
    (18, "Flat", "Rib", "Flat Knit", 80, "14", 6, "Kauo Heng Co.", "Taiwan", 4, "Non Jacquard | 100% Lycra"),
]


def seed(conn):
    cur = conn.cursor()
    row = cur.execute("SELECT id FROM industries WHERE name LIKE '%Gram%Tech%' LIMIT 1").fetchone()
    if not row:
        return
    ind_id = row["id"]

    chk = cur.execute(
        "SELECT COUNT(*) as c, COALESCE(SUM(quantity), 0) as q FROM machine_profiles WHERE industry_id = ?",
        (ind_id,),
    ).fetchone()
    if chk["c"] == len(GRAMTECH_ROWS) and chk["q"] == 32:
        return

    cur.execute("DELETE FROM machine_profiles WHERE industry_id = ?", (ind_id,))
    for sl, cat, fab, mtype, dia, gg_str, feeders, brand, origin, qty, rem in GRAMTECH_ROWS:
        m_g = re.search(r"(\d+)", gg_str)
        gauge = float(m_g.group(1)) if m_g else 24.0
        lbl = f"{dia}x{gg_str}"
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
                gauge,
                lbl,
                brand,
                int(qty),
                calc["needles_per_machine"],
                calc["sinkers_per_machine"],
                rem,
                cat,
                mtype,
                int(feeders),
                origin,
                sl,
            ),
        )
    conn.commit()
