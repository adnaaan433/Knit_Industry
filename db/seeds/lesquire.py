"""Idempotent seed for L'Esquire Ltd. (97 machines)."""

from db.calc import calculate_needle_sinker

LESQUIRE_ROWS = [
    # (fabrication, dia, gauge, label, brand, qty)
    ("Fleece", 30, 20, "30x20", "HaanTex", 9),
    ("Fleece", 30, 20, "30x20", "Mayer & Cie", 2),
    ("Fleece", 34, 20, "34x20", "HaanTex", 5),
    ("Fleece", 36, 20, "36x20", "HaanTex", 5),
    ("Fleece", 36, 20, "36x20", "Mayer & Cie", 1),
    ("Fleece", 36, 20, "36x20(F/L)", "Mayer & Cie", 2),
    ("H/Jersey", 30, 20, "30x20", "Pai Long", 2),
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
    ("Interlock", 34, 24, "34x24(I/L)", "Mayer & Cie", 1),
    ("Interlock", 34, 24, "34x24(I/L)", "Orizio", 2),
    ("Interlock", 34, 24, "34x24(I/L)", "Pai Long", 1),
]


def seed(conn):
    cur = conn.cursor()
    row = cur.execute("SELECT id FROM industries WHERE name LIKE '%Esquire%' LIMIT 1").fetchone()
    if not row:
        return
    ind_id = row["id"]

    chk = cur.execute(
        "SELECT COUNT(*) as c, MIN(COALESCE(sort_order, 0)) as min_so FROM machine_profiles WHERE industry_id = ?",
        (ind_id,),
    ).fetchone()
    if chk["c"] == len(LESQUIRE_ROWS) and (chk["min_so"] or 0) > 0:
        return

    cur.execute("DELETE FROM machine_profiles WHERE industry_id = ?", (ind_id,))
    for idx, (fab, dia, gauge, label, brand, qty) in enumerate(LESQUIRE_ROWS, 1):
        calc = calculate_needle_sinker(fab, dia, gauge, qty)
        cur.execute(
            """
            INSERT INTO machine_profiles (
                industry_id, fabrication, dia, gauge, dia_gauge_label, brand, quantity,
                needles_per_machine, sinkers_per_machine, unit, machine_category,
                in_operation, sort_order
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, '', 'Circular', 1, ?)
            """,
            (
                ind_id,
                fab,
                float(dia),
                float(gauge),
                label,
                brand,
                int(qty),
                calc["needles_per_machine"],
                calc["sinkers_per_machine"],
                idx,
            ),
        )
    conn.commit()
