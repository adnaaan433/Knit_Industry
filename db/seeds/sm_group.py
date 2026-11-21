"""Idempotent seed for S.M. Group / S.M. Knitwears (99 machine sets; cylinders 28G:5, 24G:66, 20G:41, 18G:26, 14G:9)."""

from db.calc import calculate_needle_sinker

# (dia, feeder, mc_type, brand, qty, g28, g24, g20, g18, g14, origin, lycra)
SM_ROWS = [
    (25, 75, "S/J", "Jiunn Long", 1, 0, 1, 0, 0, 0, "Taiwan", ""),
    (26, 84, "S/J", "Lisky", 1, 0, 1, 0, 0, 0, "Taiwan", ""),
    (26, 78, "S/J & Fleece", "Jiunn Long", 2, 0, 2, 2, 0, 0, "Taiwan", ""),
    (27, 81, "S/J", "Jiunn Long", 1, 0, 1, 0, 0, 0, "Taiwan", ""),
    (27, 86, "S/J", "Lisky", 1, 0, 1, 0, 0, 0, "Taiwan", ""),
    (28, 90, "S/J", "Lisky", 2, 0, 2, 0, 0, 0, "Taiwan", ""),
    (38, 114, "S/J", "Lisky", 1, 0, 1, 0, 0, 0, "Taiwan", ""),
    (28, 90, "S/J Open with", "Fukuhara", 1, 1, 1, 0, 0, 0, "Japan", "Yes"),
    (30, 96, "S/J Open with", "Fukuhara", 3, 2, 3, 0, 0, 0, "Japan", "Yes"),
    (30, 90, "S/J & Fleece", "Jiunn Long", 3, 0, 3, 3, 0, 0, "Taiwan", ""),
    (30, 96, "S/J & Fleece", "Lisky", 2, 0, 2, 2, 0, 1, "Taiwan", ""),
    (32, 104, "S/J Open with", "Fukuhara", 2, 2, 2, 0, 0, 0, "Japan", "Yes"),
    (32, 96, "S/J & Fleece", "Jiunn Long", 3, 0, 3, 3, 0, 0, "Taiwan", ""),
    (32, 102, "S/J & Fleece", "Lisky", 2, 0, 2, 2, 0, 1, "Taiwan", ""),
    (34, 108, "S/J Open with", "Fukuhara", 1, 0, 1, 0, 0, 0, "Japan", "Yes"),
    (34, 108, "S/J Open with", "Lisky", 3, 0, 3, 0, 0, 0, "Taiwan", "Yes"),
    (34, 102, "S/J & Fleece", "Jiunn Long", 3, 0, 3, 3, 0, 0, "Taiwan", ""),
    (34, 108, "S/J & Fleece", "Lisky", 2, 0, 2, 2, 0, 1, "Taiwan", ""),
    (36, 116, "S/J Open with", "Fukuhara", 3, 0, 3, 0, 0, 0, "Japan", "Yes"),
    (36, 114, "S/J Open with", "Lisky", 2, 0, 2, 0, 0, 0, "Taiwan", "Yes"),
    (36, 108, "S/J & Fleece", "Jiunn Long", 2, 0, 2, 2, 0, 0, "Taiwan", ""),
    (36, 114, "S/J & Fleece", "Lisky", 2, 0, 2, 2, 0, 1, "Taiwan", ""),
    (38, 120, "S/J Open with", "Fukuhara", 3, 0, 3, 0, 0, 0, "Japan", "Yes"),
    (40, 128, "S/J Open with", "Fukuhara", 1, 0, 1, 0, 0, 0, "Japan", "Yes"),
    (32, 44, "Auto Striper", "Pai Lung", 1, 0, 1, 0, 0, 0, "Taiwan", "Yes"),
    (34, 48, "Auto Striper", "Pai Lung", 2, 0, 2, 0, 0, 0, "Taiwan", "Yes"),
    (36, 50, "Auto Striper", "Pai Lung", 1, 0, 1, 0, 0, 0, "Taiwan", "Yes"),
    (34, 108, "Fleece", "Lisky", 1, 0, 0, 1, 0, 0, "Taiwan", ""),
    (36, 114, "Fleece", "Lisky", 2, 0, 0, 2, 0, 0, "Taiwan", ""),
    (38, 114, "S/J & Fleece", "Jiunn Long", 2, 0, 2, 2, 0, 0, "Taiwan", ""),
    (38, 120, "S/J & Fleece", "Lisky", 2, 0, 2, 2, 0, 0, "Taiwan", ""),
    (38, 120, "S/J & Fleece", "Goanglih", 2, 0, 0, 2, 0, 0, "Taiwan", ""),
    (30, 96, "S/J & Fleece", "Goanglih", 2, 0, 0, 2, 0, 0, "Taiwan", ""),
    (32, 102, "S/J & Fleece", "Goanglih", 3, 0, 0, 3, 0, 1, "Taiwan", ""),
    (34, 108, "S/J & Fleece", "Goanglih", 4, 0, 0, 4, 0, 2, "Taiwan", ""),
    (36, 114, "S/J & Fleece", "Goanglih", 4, 0, 0, 2, 0, 2, "Taiwan", ""),
    (32, 64, "Rib", "Jiunn Long", 1, 0, 0, 0, 1, 0, "Taiwan", "Yes"),
    (38, 77, "Rib", "Jiunn Long", 1, 0, 0, 0, 1, 0, "Taiwan", "Yes"),
    (40, 80, "Rib", "Jiunn Long", 1, 0, 0, 0, 1, 0, "Taiwan", "Yes"),
    (42, 84, "Rib", "Jiunn Long", 1, 0, 0, 0, 1, 0, "Taiwan", "Yes"),
    (44, 88, "Rib", "Jiunn Long", 1, 0, 0, 0, 1, 0, "Taiwan", "Yes"),
    (40, 80, "Rib", "Fukuhara", 1, 0, 0, 0, 1, 0, "Japan", "Yes"),
    (44, 88, "Rib", "Fukuhara", 2, 0, 0, 0, 2, 0, "Japan", "Yes"),
    (44, 88, "Rib", "Pai Lung", 2, 0, 0, 0, 2, 0, "Taiwan", "Yes"),
    (42, 84, "Rib", "Pai Lung", 2, 0, 0, 0, 2, 0, "Taiwan", "Yes"),
    (40, 80, "Rib", "Pai Lung", 2, 0, 0, 0, 2, 0, "Taiwan", "Yes"),
    (36, 68, "Rib/Interlock", "Fukuhara", 1, 0, 1, 0, 1, 0, "Taiwan", "Yes"),
    (34, 72, "Rib/Interlock", "Lisky", 1, 0, 1, 0, 1, 0, "Taiwan", "Yes"),
    (34, 62, "Rib/Interlock", "Fukuhara", 1, 0, 1, 0, 1, 0, "Taiwan", "Yes"),
    (32, 68, "Rib/Interlock", "Lisky", 1, 0, 1, 0, 1, 0, "Taiwan", "Yes"),
    (38, 68, "Rib/Interlock", "Fukuhara", 1, 0, 1, 0, 1, 0, "Japan", "Yes"),
    (38, 76, "Rib/Interlock", "Pai Lung", 1, 0, 1, 0, 1, 0, "Taiwan", "Yes"),
    (36, 72, "Rib/Interlock", "Pai Lung", 2, 0, 2, 0, 2, 0, "Taiwan", "Yes"),
    (34, 68, "Rib/Interlock", "Pai Lung", 3, 0, 2, 0, 3, 0, "Taiwan", "Yes"),
    (32, 64, "Rib/Interlock", "Pai Lung", 1, 0, 1, 0, 1, 0, "Taiwan", "Yes"),
]

FAB_MAP = {
    "S/J": "Single Jersey",
    "S/J Open with": "Single Jersey",
    "S/J & Fleece": "Fleece",
    "Auto Striper": "Single Jersey",
    "Fleece": "Fleece",
    "Rib": "Rib",
    "Rib/Interlock": "Interlock",
}


def seed(conn):
    cur = conn.cursor()
    row = cur.execute("SELECT id FROM industries WHERE name LIKE '%S.M.%' LIMIT 1").fetchone()
    if not row:
        return
    ind_id = row["id"]

    chk = cur.execute(
        "SELECT COUNT(*) as c, COALESCE(SUM(quantity), 0) as q FROM machine_profiles WHERE industry_id = ?",
        (ind_id,),
    ).fetchone()
    if chk["c"] == len(SM_ROWS) and chk["q"] == 99:
        return

    cur.execute("DELETE FROM machine_profiles WHERE industry_id = ?", (ind_id,))
    for idx, (dia, feeder, mtype, brand, qty, g28, g24, g20, g18, g14, origin, lycra) in enumerate(SM_ROWS, 1):
        gauges_present = []
        primary_gauge = 24
        for g_val, g_cnt in [(24, g24), (20, g20), (18, g18), (28, g28), (14, g14)]:
            if g_cnt > 0:
                primary_gauge = g_val
                break
        for g_val, g_cnt in [(28, g28), (24, g24), (20, g20), (18, g18), (14, g14)]:
            if g_cnt > 0:
                gauges_present.append(f"{g_val}G:{g_cnt}")
        g_label_list = "/".join(str(g) for g, c in [(28, g28), (24, g24), (20, g20), (18, g18), (14, g14)] if c > 0)
        lbl = f"{dia}x{g_label_list}"
        rem_parts = [f"Cylinders({', '.join(gauges_present)})"]
        if lycra:
            rem_parts.append("Lycra: Yes")
        rem = " | ".join(rem_parts)

        fab = FAB_MAP.get(mtype, "Single Jersey")
        calc = calculate_needle_sinker(fab, dia, primary_gauge, qty)

        cur.execute(
            """
            INSERT INTO machine_profiles (
                industry_id, fabrication, dia, gauge, dia_gauge_label, brand, quantity,
                needles_per_machine, sinkers_per_machine, remarks,
                unit, machine_category, machine_type, feeders, origin,
                in_operation, sort_order
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '', 'Circular', ?, ?, ?, 1, ?)
            """,
            (
                ind_id,
                fab,
                float(dia),
                float(primary_gauge),
                lbl,
                brand,
                int(qty),
                calc["needles_per_machine"],
                calc["sinkers_per_machine"],
                rem,
                mtype,
                int(feeder),
                origin,
                idx,
            ),
        )
    conn.commit()
