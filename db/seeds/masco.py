"""Idempotent seed for MASCO (Concept Knitting) (197 machines: Unit-1 121, Unit-2 48 Circular + 28 Collar)."""

from db.calc import calculate_needle_sinker

# (unit, machine_category, fabrication, machine_type, dia, gauge, label, brand, origin, qty, feeders, remarks)
MASCO_ROWS = [
    # Unit-1 Double Jersey (23 machines)
    ("Unit-1 (Rupganj)", "Circular", "Rib", "Double Jersey", 34, 18, "34x18/22", "Fukuhara", "Japan", 1, 62, "Cylinders: 18G(1), 22G(2) | Rib/INTERLOCK"),
    ("Unit-1 (Rupganj)", "Circular", "Rib", "Double Jersey", 34, 18, "34x18/24/28", "Fukuhara", "Japan", 4, 70, "Cylinders: 18G(4), 24G(4), 28G(2) | INTERLOCK (1 set quilting)"),
    ("Unit-1 (Rupganj)", "Circular", "Rib", "Double Jersey", 36, 18, "36x18/22", "Fukuhara", "Japan", 2, 64, "Cylinders: 18G(2), 22G(2) | Rib/INTERLOCK"),
    ("Unit-1 (Rupganj)", "Circular", "Rib", "Double Jersey", 36, 18, "36x14/18/24", "Fukuhara", "Japan", 3, 74, "Cylinders: 14G(1), 18G(3), 24G(3) | INTERLOCK (1 set spacer)"),
    ("Unit-1 (Rupganj)", "Circular", "Rib", "Double Jersey", 38, 18, "38x18/22", "Fukuhara", "Japan", 5, 68, "Cylinders: 18G(5), 22G(2) | Rib/INTERLOCK"),
    ("Unit-1 (Rupganj)", "Circular", "Rib", "Double Jersey", 38, 18, "38x14/18/24", "Fukuhara", "Japan", 2, 78, "Cylinders: 14G(1), 18G(2), 24G(2) | Rib/INTERLOCK"),
    ("Unit-1 (Rupganj)", "Circular", "Rib", "Double Jersey", 40, 18, "40x18/22", "Fukuhara", "Japan", 6, 72, "Cylinders: 18G(6), 22G(2)"),
    # Unit-1 Single Jersey (98 machines)
    ("Unit-1 (Rupganj)", "Circular", "Single Jersey", "Single Jersey", 30, 24, "30x24/28/32/36", "Fukuhara", "Japan", 6, 96, "Cylinders: 24G(6), 28G(5), 32G(2), 36G(1)"),
    ("Unit-1 (Rupganj)", "Circular", "Single Jersey", "Single Jersey", 30, 24, "30x20/24/32", "Keum Yung", "Korea", 3, 90, "Cylinders: 20G(1), 24G(3), 32G(1)"),
    ("Unit-1 (Rupganj)", "Circular", "Fleece", "Single Jersey", 30, 20, "30x20/24", "Santoni", "Italy", 3, 90, "Cylinders: 20G(3), 24G(2) | FLEECE"),
    ("Unit-1 (Rupganj)", "Circular", "Single Jersey", "Single Jersey", 32, 24, "32x20/22/24/28", "Fukuhara", "Japan", 5, 104, "Cylinders: 20G(1), 22G(2), 24G(5), 28G(4)"),
    ("Unit-1 (Rupganj)", "Circular", "Single Jersey", "5 Feeder S/J", 32, 24, "32x24", "Fukuhara", "Japan", 1, 160, "5 FEEDER"),
    ("Unit-1 (Rupganj)", "Circular", "Single Jersey", "Single Jersey", 32, 24, "32x20/24/32", "Keum Yung", "Korea", 4, 96, "Cylinders: 20G(2), 24G(4), 32G(1)"),
    ("Unit-1 (Rupganj)", "Circular", "Fleece", "Single Jersey", 32, 20, "32x18/20/24", "Lisky", "Taiwan", 5, 102, "Cylinders: 18G(5), 20G(5), 24G(5) | FLEECE"),
    ("Unit-1 (Rupganj)", "Circular", "Single Jersey", "Open Dia S/J", 32, 24, "32x22/24/28/36", "Santoni", "Italy", 4, 96, "Cylinders: 22G(2), 24G(4), 28G(2), 36G(4) | OPEN DIA"),
    ("Unit-1 (Rupganj)", "Circular", "Single Jersey", "Single Jersey", 34, 24, "34x14/20/22/24/28", "Fukuhara", "Japan", 5, 108, "Cylinders: 14G(2), 20G(1), 22G(2), 24G(5), 28G(3)"),
    ("Unit-1 (Rupganj)", "Circular", "Single Jersey", "5 Feeder S/J", 34, 24, "34x24", "Fukuhara", "Japan", 1, 170, "5 FEEDER"),
    ("Unit-1 (Rupganj)", "Circular", "Fleece", "Single Jersey", 34, 24, "34x14/20/24", "Keum Yung", "Korea", 5, 102, "Cylinders: 14G(1), 20G(3), 24G(5) | FLEECE"),
    ("Unit-1 (Rupganj)", "Circular", "Fleece", "Single Jersey", 34, 20, "34x18/20/24", "Lisky", "Taiwan", 6, 108, "Cylinders: 18G(6), 20G(6), 24G(6) | FLEECE"),
    ("Unit-1 (Rupganj)", "Circular", "Single Jersey", "Open Dia S/J", 34, 24, "34x22/24/28/36", "Santoni", "Italy", 4, 102, "Cylinders: 22G(2), 24G(4), 28G(2), 36G(4) | OPEN DIA"),
    ("Unit-1 (Rupganj)", "Circular", "Single Jersey", "Single Jersey", 36, 24, "36x14/20/22/24", "Fukuhara", "Japan", 6, 114, "Cylinders: 14G(3), 20G(2), 22G(2), 24G(6)"),
    ("Unit-1 (Rupganj)", "Circular", "Single Jersey", "5 Feeder S/J", 36, 24, "36x24", "Fukuhara", "Japan", 1, 180, "5 FEEDER"),
    ("Unit-1 (Rupganj)", "Circular", "Single Jersey", "Single Jersey", 36, 24, "36x14/24", "Keum Yung", "Korea", 2, 108, "Cylinders: 14G(1), 24G(2)"),
    ("Unit-1 (Rupganj)", "Circular", "Single Jersey", "4 Feeder S/J", 36, 24, "36x24", "Keum Yung", "Korea", 2, 144, "4 FEEDER"),
    ("Unit-1 (Rupganj)", "Circular", "Fleece", "Single Jersey", 36, 20, "36x14/18/20/24", "Lisky", "Taiwan", 4, 108, "Cylinders: 14G(2), 20G(4), 18G(4), 24G(4) | FLEECE"),
    ("Unit-1 (Rupganj)", "Circular", "Single Jersey", "Open Dia S/J", 36, 24, "36x22/24/28", "Santoni", "Italy", 4, 108, "Cylinders: 22G(2), 24G(4), 28G(2) | OPEN DIA"),
    ("Unit-1 (Rupganj)", "Circular", "Single Jersey", "Tubular S/J", 36, 24, "36x24", "Santoni", "Italy", 1, 108, "Tubular"),
    ("Unit-1 (Rupganj)", "Circular", "Single Jersey", "Single Jersey", 38, 24, "38x14/20/22/24", "Fukuhara", "Japan", 5, 120, "Cylinders: 14G(3), 22G(2), 20G(2), 24G(5)"),
    ("Unit-1 (Rupganj)", "Circular", "Single Jersey", "Single Jersey", 38, 24, "38x24", "Keum Yung", "Korea", 2, 114, ""),
    ("Unit-1 (Rupganj)", "Circular", "Fleece", "Single Jersey", 38, 18, "38x14/18/24", "Lisky", "Taiwan", 4, 120, "Cylinders: 14G(2), 18G(4), 24G(4) | FLEECE"),
    ("Unit-1 (Rupganj)", "Circular", "Single Jersey", "Open Dia S/J", 38, 24, "38x24", "Lisky", "Taiwan", 2, 120, "OPEN DIA"),
    ("Unit-1 (Rupganj)", "Circular", "Single Jersey", "Open Dia S/J", 38, 24, "38x22/24/28", "Santoni", "Italy", 4, 114, "Cylinders: 22G(2), 24G(4), 28G(2) | OPEN DIA"),
    ("Unit-1 (Rupganj)", "Circular", "Single Jersey", "Tubular S/J", 38, 24, "38x24", "Santoni", "Italy", 3, 114, "Tubular"),
    ("Unit-1 (Rupganj)", "Circular", "Single Jersey", "Single Jersey", 40, 24, "40x14/18/24", "Fukuhara", "Japan", 4, 128, "Cylinders: 14G(2), 18G(2), 24G(4)"),
    ("Unit-1 (Rupganj)", "Circular", "Single Jersey", "4 Feeder S/J", 40, 24, "40x24", "Keum Yung", "Korea", 1, 160, "4 FEEDER"),
    ("Unit-1 (Rupganj)", "Circular", "Single Jersey", "Single Jersey", 42, 24, "42x24", "Keum Yung", "Korea", 1, 126, ""),
    # Unit-2 Double Jersey (9 machines)
    ("Unit-2 (Tongi)", "Circular", "Rib", "Double Jersey", 34, 18, "34x18", "Fukuhara", "Japan", 1, 62, ""),
    ("Unit-2 (Tongi)", "Circular", "Rib", "Double Jersey", 34, 18, "34x18", "Fukuhara", "Japan", 1, 70, ""),
    ("Unit-2 (Tongi)", "Circular", "Rib", "Double Jersey", 34, 18, "34x18/24", "Keum Yung", "Korea", 1, 68, "Cylinders: 18G(1), 24G(1) | Rib/INTERLOCK"),
    ("Unit-2 (Tongi)", "Circular", "Rib", "Double Jersey", 36, 18, "36x18/24", "Fukuhara", "Japan", 2, 74, "Cylinders: 18G(2), 24G(1)"),
    ("Unit-2 (Tongi)", "Circular", "Rib", "Double Jersey", 36, 18, "36x18/24", "Keum Yung", "Korea", 1, 72, "Cylinders: 18G(1), 24G(1) | Rib/INTERLOCK"),
    ("Unit-2 (Tongi)", "Circular", "Rib", "Double Jersey", 38, 18, "38x18", "Fukuhara", "Japan", 1, 68, ""),
    ("Unit-2 (Tongi)", "Circular", "Rib", "Double Jersey", 38, 18, "38x18/24", "Keum Yung", "Korea", 1, 76, "Cylinders: 18G(1), 24G(1) | Rib/INTERLOCK"),
    ("Unit-2 (Tongi)", "Circular", "Rib", "Double Jersey", 40, 18, "40x18", "Fukuhara", "Japan", 1, 72, ""),
    # Unit-2 Single Jersey (21 machines)
    ("Unit-2 (Tongi)", "Circular", "Single Jersey", "Single Jersey", 23, 24, "23x24", "Pai Lung", "Taiwan", 1, 68, ""),
    ("Unit-2 (Tongi)", "Circular", "Single Jersey", "Single Jersey", 25, 24, "25x24", "Pai Lung", "Taiwan", 1, 74, ""),
    ("Unit-2 (Tongi)", "Circular", "Single Jersey", "Single Jersey", 26, 24, "26x24", "Keum Yung", "Korea", 1, 78, ""),
    ("Unit-2 (Tongi)", "Circular", "Single Jersey", "Single Jersey", 28, 24, "28x24/28", "Pai Lung", "Taiwan", 2, 84, "Cylinders: 24G(2), 28G(1)"),
    ("Unit-2 (Tongi)", "Circular", "Single Jersey", "Single Jersey", 30, 24, "30x24", "Fukuhara", "Japan", 1, 96, ""),
    ("Unit-2 (Tongi)", "Circular", "Single Jersey", "Single Jersey", 30, 24, "30x20/24/28", "Santoni", "Italy", 4, 90, "Cylinders: 20G(1), 24G(3), 28G(2) | Fleece"),
    ("Unit-2 (Tongi)", "Circular", "Single Jersey", "Single Jersey", 30, 24, "30x24/28", "Pai Lung", "Taiwan", 1, 90, "Cylinders: 24G(1), 28G(1)"),
    ("Unit-2 (Tongi)", "Circular", "Single Jersey", "Single Jersey", 32, 24, "32x24", "Fukuhara", "Japan", 1, 104, ""),
    ("Unit-2 (Tongi)", "Circular", "Single Jersey", "Single Jersey", 32, 24, "32x16/24", "Santoni", "Italy", 3, 90, "Cylinders: 16G(2), 24G(3)"),
    ("Unit-2 (Tongi)", "Circular", "Fleece", "Single Jersey", 32, 20, "32x18/20/24", "Lisky", "Taiwan", 1, 102, "Cylinders: 18G(1), 20G(1), 24G(1) | Fleece"),
    ("Unit-2 (Tongi)", "Circular", "Single Jersey", "Single Jersey", 34, 24, "34x24/28", "Pai Lung", "Taiwan", 1, 102, "Cylinders: 24G(1), 28G(1)"),
    ("Unit-2 (Tongi)", "Circular", "H/Jersey", "Single Jersey", 34, 24, "34x10/12/24", "San Da", "Taiwan", 1, 54, "Cylinders: 10G(1), 12G(1), 24G(1) | H/J & Fleece / SJ"),
    ("Unit-2 (Tongi)", "Circular", "Single Jersey", "Single Jersey", 34, 24, "34x19/24", "San Da", "Taiwan", 1, 68, "Cylinders: 19G(1), 24G(1) | Velour / SJ"),
    ("Unit-2 (Tongi)", "Circular", "Single Jersey", "Single Jersey", 36, 24, "36x24/28", "Pai Lung", "Taiwan", 1, 108, "Cylinders: 24G(1), 28G(1)"),
    ("Unit-2 (Tongi)", "Circular", "Single Jersey", "Single Jersey", 36, 24, "36x19/24", "San Da", "Taiwan", 1, 72, "Cylinders: 19G(1), 24G(1) | Velour / S/J"),
    # Unit-2 Eng. Stripe Double Jersey (2 machines)
    ("Unit-2 (Tongi)", "Circular", "Rib", "Eng. Stripe D/J", 34, 18, "34x18/24/7-28", "Fukuhara", "Japan", 1, 48, "6 COLOR | INTERLOCK | QUARTER GAUGE"),
    ("Unit-2 (Tongi)", "Circular", "Rib", "Eng. Stripe D/J", 36, 18, "36x18/24", "Fukuhara", "Japan", 1, 50, "6 COLOR | INTERLOCK"),
    # Unit-2 Eng. Stripe Single Jersey (8 machines)
    ("Unit-2 (Tongi)", "Circular", "Single Jersey", "Eng. Stripe S/J", 30, 20, "30x16/20/24", "Pai Lung", "Taiwan", 3, 42, "Cylinders: 16G(2), 20G(3), 24G(3) | 6 COLOR"),
    ("Unit-2 (Tongi)", "Circular", "Single Jersey", "Eng. Stripe S/J", 32, 20, "32x20/24", "Pai Lung", "Taiwan", 1, 44, "Cylinders: 20G(1), 24G(1) | 6 COLOR"),
    ("Unit-2 (Tongi)", "Circular", "Single Jersey", "Eng. Stripe S/J", 34, 20, "34x20/24", "Fukuhara", "Japan", 1, 84, "Cylinders: 20G(1), 24G(1) | 6 COLOR"),
    ("Unit-2 (Tongi)", "Circular", "Single Jersey", "Eng. Stripe S/J", 34, 20, "34x20/24", "Pai Lung", "Taiwan", 1, 42, "Cylinders: 20G(1), 24G(1) | 6 COLOR"),
    ("Unit-2 (Tongi)", "Circular", "Single Jersey", "Eng. Stripe S/J", 36, 20, "36x20/24", "Fukuhara", "Japan", 2, 84, "Cylinders: 20G(2), 24G(2) | 6 COLOR"),
    # Unit-2 Jacquard & Pointal M/C (8 machines)
    ("Unit-2 (Tongi)", "Circular", "Single Jersey", "Jacquard & Pointal", 34, 24, "34x24", "Hangxing", "China", 1, 72, "Jacquard SJ"),
    ("Unit-2 (Tongi)", "Circular", "Rib", "Jacquard & Pointal", 30, 18, "30x18", "Hangxing", "China", 2, 48, "Pointal Jacquard"),
    ("Unit-2 (Tongi)", "Circular", "Rib", "Jacquard & Pointal", 32, 18, "32x18", "Hangxing", "China", 2, 51, "Pointal Jacquard"),
    ("Unit-2 (Tongi)", "Circular", "Rib", "Jacquard & Pointal", 34, 18, "34x18", "Hangxing", "China", 3, 54, "Pointal Jacquard"),
    # Unit-2 Collar Flat Knit (28 machines)
    ("Unit-2 (Collar)", "Flat", "Rib", "Collar Flat Knit", 40, 14, '40"x14G', "Matsuya", "Japan", 6, None, "6 Colors"),
    ("Unit-2 (Collar)", "Flat", "Rib", "Collar Flat Knit", 40, 14, '40"x14G', "Matsuya", "Japan", 2, None, "4 Colors"),
    ("Unit-2 (Collar)", "Flat", "Rib", "Collar Flat Knit", 80, 16, '80"x14G/16G', "Matsuya", "Japan", 9, None, "8 Colors | Semi Jacquard"),
    ("Unit-2 (Collar)", "Flat", "Rib", "Collar Flat Knit", 80, 16, '80"x16G', "Matsuya", "Japan", 6, None, "6 Colors | Semi Jacquard"),
    ("Unit-2 (Collar)", "Flat", "Rib", "Collar Flat Knit", 60, 16, '60"x16G', "Matsuya", "Japan", 3, None, "6 Colors | Jacquard"),
    ("Unit-2 (Collar)", "Flat", "Rib", "Collar Flat Knit", 40, 14, '40"x14G', "Kauo Heng", "Taiwan", 2, None, "6 Colors | Semi Jacquard"),
]


def seed(conn):
    cur = conn.cursor()
    row = cur.execute("SELECT id FROM industries WHERE name LIKE '%MASCO%' LIMIT 1").fetchone()
    if not row:
        return
    ind_id = row["id"]

    chk = cur.execute(
        "SELECT COUNT(*) as c, COALESCE(SUM(quantity), 0) as q FROM machine_profiles WHERE industry_id = ? AND unit != ''",
        (ind_id,),
    ).fetchone()
    if chk["c"] == len(MASCO_ROWS) and chk["q"] == 197:
        return

    cur.execute("DELETE FROM machine_profiles WHERE industry_id = ?", (ind_id,))
    for idx, (unit, cat, fab, mtype, dia, gauge, lbl, brand, origin, qty, feeders, rem) in enumerate(MASCO_ROWS, 1):
        calc = calculate_needle_sinker(fab, dia, gauge, qty)
        cur.execute(
            """
            INSERT INTO machine_profiles (
                industry_id, fabrication, dia, gauge, dia_gauge_label, brand, quantity,
                needles_per_machine, sinkers_per_machine, remarks,
                unit, machine_category, machine_type, feeders, origin,
                in_operation, sort_order
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?)
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
                unit,
                cat,
                mtype,
                feeders,
                origin,
                idx,
            ),
        )
    conn.commit()
