"""Idempotent seed for Tosrifa Industries Ltd (69 machines: 45 Circular + 24 Flat Bed)."""

import re
from db.calc import calculate_needle_sinker

# (sl, mc_no, dia, gauge_str, feeder, mtype, brand, model, origin, cap_kg)
TOSRIFA_CIRCULAR = [
    (1, "6", 30, "24/28", 90, "SINGLE JERSEY", "Keum Yong", "KM-3WVX", "Korea", 250),
    (2, "7", 30, "24/32", 90, "SINGLE JERSEY", "Keum Yong", "KLM-72AV", "Korea", 250),
    (3, "34", 34, "28", 102, "SINGLE JERSEY", "Keum Yong", "KM-3WVX", "Korea", 300),
    (4, "35", 34, "28", 102, "SINGLE JERSEY", "Keum Yong", "KM-3WVX", "Korea", 300),
    (5, "9", 34, "24/28", 102, "SINGLE JERSEY", "Keum Yong", "KM-3WVX", "Korea", 300),
    (6, "8", 30, "24/32", 90, "SINGLE JERSEY", "Keum Yong", "KM-3WVX", "Korea", 250),
    (7, "44", 34, "24/28", 108, "SINGLE JERSEY", "Mayer & Cie", "RELANIT 3.2-II", "Germany", 250),
    (8, "33", 34, "24/28", 108, "SINGLE JERSEY", "Mayer & Cie", "RELANIT 3.2-II", "Germany", 250),
    (9, "11", 38, "24", 123, "SINGLE JERSEY", "Mayer & Cie", "RELANIT 3.2-II", "Germany", 350),
    (10, "22", 36, "24", 114, "SINGLE JERSEY", "Mayer & Cie", "RELANIT 3.2-II", "Germany", 340),
    (11, "10", 30, "20/24", 96, "Fleece, S/Jersey", "Mayer & Cie", "S4-3.2", "Germany", 250),
    (12, "27", 30, "20/24/12", 96, "Fleece, S/Jersey", "Lisky", "4-Tube-2014", "Taiwan", 260),
    (13, "29", 30, "20/24/12", 96, "Fleece, S/Jersey", "Lisky", "4-Tube-2014", "Taiwan", 260),
    (14, "31", 30, "20/24/12", 96, "Fleece, S/Jersey", "Lisky", "4-Tube-2014", "Taiwan", 260),
    (15, "19", 30, "20/24/12", 96, "Fleece, S/Jersey", "Lisky", "Version-Tube-2016", "Taiwan", 280),
    (16, "20", 30, "20/24/12", 96, "Fleece, S/Jersey", "Lisky", "Version-Tube-2016", "Taiwan", 280),
    (17, "40", 30, "20/24", 90, "Fleece, S/Jersey", "Point", "ZD-S", "China", 280),
    (18, "26", 30, "20/28", 90, "Fleece, S/Jersey", "Point", "ZD-S", "China", 280),
    (19, "32", 30, "20/12", 96, "Fleece", "Lisky", "4-Tube-2014", "Taiwan", 280),
    (20, "21", 30, "20/12", 96, "Fleece", "Lisky", "Version-Tube-2016", "Taiwan", 280),
    (21, "30", 30, "20/12", 96, "Fleece", "Lisky", "4-Tube-2014", "Taiwan", 280),
    (22, "28", 30, "20", 96, "Fleece", "Lisky", "4-Tube-2014", "Taiwan", None),
    (23, "25", 30, "20", 90, "Fleece", "Point", "ZD-S", "China", 280),
    (24, "43", 30, "20", 90, "Fleece", "Point", "ZD-S", "China", None),
    (25, "42", 30, "20", 90, "Fleece", "Point", "ZD-S", "China", None),
    (26, "41", 30, "20", 90, "Fleece", "Point", "ZD-S", "China", 280),
    (27, "39", 30, "20", 90, "Fleece", "Point", "ZD-S", "China", 280),
    (28, "38", 30, "20", 90, "Fleece", "Point", "ZD-S", "China", 280),
    (29, "37", 30, "20", 90, "Fleece", "Point", "ZD-S", "China", 280),
    (30, "36", 30, "20", 90, "Fleece", "Point", "ZD-S", "China", 280),
    (31, "24", 42, "18", 84, "Rib/Spacer", "Lisky", "DT/84 A-4", "Taiwan", 300),
    (32, "23", 42, "18/14", 84, "Rib/Spacer", "Lisky", "DT/84 A-4", "Taiwan", 300),
    (33, "1", 42, "18", 84, "Rib/Spacer", "Lisky", "DT/84 A-4", "Taiwan", 300),
    (34, "2", 42, "18", 84, "Rib/Spacer", "Lisky", "DT/84 A-4", "Taiwan", None),
    (35, "12", 42, "18", 84, "Rib/Spacer", "Lisky", "DT/84 A-4", "Taiwan", 300),
    (36, "13", 42, "18", 84, "Rib/Spacer", "Lisky", "DT/84 A-4", "Taiwan", 300),
    (37, "15", 34, "18", 72, "Rib", "Mayer & Cie", "D4-2.2", "Germany", 200),
    (38, "17", 32, "18", 68, "Rib", "Mayer & Cie", "D4-2.2", "Germany", None),
    (39, "18", 30, "18", 62, "Rib", "Mayer & Cie", "F4-2.0", "Germany", 220),
    (40, "4", 34, "24", 82, "Interlock", "Keum Yong", "KLM-72AV", "Korea", None),
    (41, "5", 34, "24/28", 82, "Interlock", "Keum Yong", "KLM-72AV", "Korea", 220),
    (42, "45", 34, "24/28", 82, "Interlock", "Keum Yong", "KLM-72AV", "Korea", 220),
    (43, "3", 30, "24/28", 72, "Interlock", "Keum Yong", "KLM-72AV", "Korea", 210),
    (44, "14", 34, "18/24", 72, "Rib/Interlock", "Mayer & Cie", "D4-2.2", "Germany", 200),
    (45, "16", 32, "18/24", 68, "Rib/Interlock", "Mayer & Cie", "D4-2.2", "Germany", 200),
]

TOSRIFA_FLAT = [
    ("Shima Seiki", "SFF 152", 60, 14, "Japan", 4, "Double Head | 10,000 set/day total"),
    ("Matsuya", "M100", 40, 14, "China", 8, "Single Head | 10,000 set/day total"),
    ("Matsuya", "M 172 SJ", 68, 14, "China", 8, "Double Head | 10,000 set/day total"),
    ("Matsuya", "MC 203 SJ", 80, 14, "China", 2, "Double Head | 10,000 set/day total"),
    ("Matsuya", "Super-NJ 212", 48, 14, "China", 2, "Dual System | 10,000 set/day total"),
]

FAB_MAP = {
    "SINGLE JERSEY": "Single Jersey",
    "Fleece, S/Jersey": "Fleece",
    "Fleece": "Fleece",
    "Rib/Spacer": "Rib",
    "Rib": "Rib",
    "Interlock": "Interlock",
    "Rib/Interlock": "Rib",
}


def seed(conn):
    cur = conn.cursor()
    row = cur.execute("SELECT id FROM industries WHERE name LIKE '%Tosrifa%' LIMIT 1").fetchone()
    if not row:
        return
    ind_id = row["id"]

    chk = cur.execute(
        "SELECT COUNT(*) as c, COALESCE(SUM(quantity), 0) as q FROM machine_profiles WHERE industry_id = ?",
        (ind_id,),
    ).fetchone()
    if chk["c"] == (len(TOSRIFA_CIRCULAR) + len(TOSRIFA_FLAT)) and chk["q"] == 69:
        return

    cur.execute("DELETE FROM machine_profiles WHERE industry_id = ?", (ind_id,))
    for sl, mc_no, dia, gg_str, feeder, mtype, brand, model, origin, cap_kg in TOSRIFA_CIRCULAR:
        m_g = re.search(r"(\d+)", gg_str)
        gauge = float(m_g.group(1)) if m_g else 24.0
        fab = FAB_MAP.get(mtype, "Single Jersey")
        lbl = f"{dia}x{gg_str}"
        calc = calculate_needle_sinker(fab, dia, gauge, 1)
        cur.execute(
            """
            INSERT INTO machine_profiles (
                industry_id, fabrication, dia, gauge, dia_gauge_label, brand, quantity,
                needles_per_machine, sinkers_per_machine,
                unit, machine_category, machine_type, feeders, origin, model,
                capacity_kg, machine_no, in_operation, sort_order
            ) VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?, 'Circular Knitting', 'Circular', ?, ?, ?, ?, ?, ?, 1, ?)
            """,
            (
                ind_id,
                fab,
                float(dia),
                gauge,
                lbl,
                brand,
                calc["needles_per_machine"],
                calc["sinkers_per_machine"],
                mtype,
                int(feeder),
                origin,
                model,
                float(cap_kg) if cap_kg is not None else None,
                mc_no,
                sl,
            ),
        )

    for idx, (brand, model, bed, gauge, origin, qty, rem) in enumerate(TOSRIFA_FLAT, len(TOSRIFA_CIRCULAR) + 1):
        calc = calculate_needle_sinker("Rib", bed, gauge, qty)
        cur.execute(
            """
            INSERT INTO machine_profiles (
                industry_id, fabrication, dia, gauge, dia_gauge_label, brand, quantity,
                needles_per_machine, sinkers_per_machine, remarks,
                unit, machine_category, machine_type, origin, model,
                in_operation, sort_order
            ) VALUES (?, 'Rib', ?, ?, ?, ?, ?, ?, ?, ?, 'Flat Bed Knitting', 'Flat', 'Flat Bed', ?, ?, 1, ?)
            """,
            (
                ind_id,
                float(bed),
                float(gauge),
                f'{bed}"x{gauge}G',
                brand,
                int(qty),
                calc["needles_per_machine"],
                calc["sinkers_per_machine"],
                rem,
                origin,
                model,
                idx,
            ),
        )
    conn.commit()
