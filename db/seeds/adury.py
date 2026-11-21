"""Idempotent seed for Adury Knit Composite (105 machines: 63 Circular + 42 Flat Knit)."""

from db.calc import calculate_needle_sinker

# (cat, fab, mtype, dia, gauge, label, feeders, brand, qty, remarks)
ADURY_ROWS = [
    # Single Jersey (Open) — 4 machines
    ("Circular", "Single Jersey", "Single Jersey (Open)", 30, 24, '30"x24G', 96, "Thermax / Adury", 1, "Cylinders: 24G(1) | With FF Lycra Attachments"),
    ("Circular", "Single Jersey", "Single Jersey (Open)", 32, 24, '32"x24G', 102, "Thermax / Adury", 1, "Cylinders: 24G(1) | With FF Lycra Attachments"),
    ("Circular", "Single Jersey", "Single Jersey (Open)", 34, 24, '34"x24G', 109, "Thermax / Adury", 1, "Cylinders: 24G(1) | With FF Lycra Attachments"),
    ("Circular", "Single Jersey", "Single Jersey (Open)", 36, 24, '36"x24G', 115, "Thermax / Adury", 1, "Cylinders: 24G(1) | With FF Lycra Attachments"),
    # Single Jersey (Tube) — 29 machines
    ("Circular", "Single Jersey", "Single Jersey (Tube)", 25, 24, '25"x24G', 75, "Thermax / Adury", 1, "Cylinders: 24G(1) | With FF Lycra Attachments"),
    ("Circular", "Single Jersey", "Single Jersey (Tube)", 26, 24, '26"x24G/28G', 84, "Thermax / Adury", 1, "Cylinders: 24G(1), 28G(1) | With FF Lycra Attachments"),
    ("Circular", "Single Jersey", "Single Jersey (Tube)", 28, 24, '28"x24G', 84, "Thermax / Adury", 1, "Cylinders: 24G(1) | With FF Lycra Attachments"),
    ("Circular", "Single Jersey", "Single Jersey (Tube)", 30, 24, '30"x20G/24G/28G', 96, "Thermax / Adury", 5, "Cylinders: 20G(2), 24G(5), 28G(3) | With FF Lycra Attachments"),
    ("Circular", "Single Jersey", "Single Jersey (Tube)", 32, 24, '32"x20G/24G/28G', 102, "Thermax / Adury", 5, "Cylinders: 20G(1), 24G(5), 28G(2) | With FF Lycra Attachments"),
    ("Circular", "Single Jersey", "Single Jersey (Tube)", 34, 24, '34"x14G/20G/24G/28G', 108, "Thermax / Adury", 6, "Cylinders: 14G(1), 20G(1), 24G(6), 28G(2) | With FF Lycra Attachments"),
    ("Circular", "Single Jersey", "Single Jersey (Tube)", 36, 24, '36"x14G/20G/24G/28G', 108, "Thermax / Adury", 7, "Cylinders: 14G(2), 20G(3), 24G(7), 28G(1) | With FF Lycra Attachments"),
    ("Circular", "Single Jersey", "Single Jersey (Tube)", 38, 24, '38"x24G', 108, "Thermax / Adury", 1, "Cylinders: 24G(1) | With FF Lycra Attachments"),
    ("Circular", "Single Jersey", "Single Jersey (Tube)", 40, 24, '40"x14G/24G', 128, "Thermax / Adury", 2, "Cylinders: 14G(1), 24G(2) | With FF Lycra Attachments"),
    # Rib & Interlock — 8 machines
    ("Circular", "Rib", "Rib & Interlock", 30, 18, '30"x18G/24G', 60, "Thermax / Adury", 1, "Cylinders: 18G(1), 24G(1) | With Interlock conversion Facilities"),
    ("Circular", "Rib", "Rib & Interlock", 32, 18, '32"x18G/22G/24G', 66, "Thermax / Adury", 1, "Cylinders: 18G(1), 22G(1), 24G(1) | With Interlock conversion Facilities"),
    ("Circular", "Rib", "Rib & Interlock", 34, 18, '34"x18G/24G', 70, "Thermax / Adury", 1, "Cylinders: 18G(1), 24G(1) | With Interlock conversion Facilities"),
    ("Circular", "Rib", "Rib & Interlock", 34, 18, '34"x18G/24G', 62, "Thermax / Adury", 1, "Cylinders: 18G(1), 24G(1) | With Interlock conversion Facilities"),
    ("Circular", "Rib", "Rib & Interlock", 36, 18, '36"x18G/24G', 74, "Thermax / Adury", 1, "Cylinders: 18G(1), 24G(1) | With Interlock conversion Facilities"),
    ("Circular", "Rib", "Rib & Interlock", 36, 18, '36"x18G/24G', 64, "Thermax / Adury", 1, "Cylinders: 18G(1), 24G(1) | With Interlock conversion Facilities"),
    ("Circular", "Rib", "Rib & Interlock", 38, 18, '38"x18G/24G', 78, "Thermax / Adury", 1, "Cylinders: 18G(1), 24G(1) | With Interlock conversion Facilities"),
    ("Circular", "Rib", "Rib & Interlock", 40, 18, '40"x18G/24G', 72, "Thermax / Adury", 1, "Cylinders: 18G(1), 24G(1) | With Interlock conversion Facilities"),
    # Fleece — 17 machines
    ("Circular", "Fleece", "Fleece", 30, 20, '30"x20G', 90, "Thermax / Adury", 5, "Cylinders: 20G(5) | With Lycra Attachments"),
    ("Circular", "Fleece", "Fleece", 32, 20, '32"x20G', 96, "Thermax / Adury", 2, "Cylinders: 20G(2)"),
    ("Circular", "Fleece", "Fleece", 34, 20, '34"x20G', 108, "Thermax / Adury", 10, "Cylinders: 20G(10)"),
    # Engineering Stripe S/J — 5 machines
    ("Circular", "Single Jersey", "Engineering Stripe S/J", 30, 24, '30"x14G/20G/24G', 48, "Thermax / Adury", 1, "6 Finger | Cylinders: 14G(1), 20G(1), 24G(1)"),
    ("Circular", "Single Jersey", "Engineering Stripe S/J", 32, 24, '32"x14G/20G/24G', 54, "Thermax / Adury", 1, "6 Finger | Cylinders: 14G(1), 20G(1), 24G(1)"),
    ("Circular", "Single Jersey", "Engineering Stripe S/J", 34, 24, '34"x14G/20G/24G', 54, "Thermax / Adury", 1, "6 Finger | Cylinders: 14G(1), 20G(1), 24G(1)"),
    ("Circular", "Single Jersey", "Engineering Stripe S/J", 36, 24, '36"x14G/20G/24G', 54, "Thermax / Adury", 1, "6 Finger | Cylinders: 14G(1), 20G(1), 24G(1)"),
    ("Circular", "Single Jersey", "Engineering Stripe S/J", 38, 24, '38"x14G/20G/24G', 54, "Thermax / Adury", 1, "6 Finger | Cylinders: 14G(1), 20G(1), 24G(1)"),
    # Collar & Cuff Flat Knit — 42 machines
    ("Flat", "Rib", "Collar & Cuff (Semi Jacquard)", 60, 14, '60"x14G', None, "Flat Knit", 37, "Color Use: 4 | Needle: 840X2"),
    ("Flat", "Rib", "Collar & Cuff (Jacquard)", 45, 14, '45"x14G', None, "Flat Knit", 2, "Color Use: 4 | Needle: 630X2"),
    ("Flat", "Rib", "Collar & Cuff (Jacquard)", 80, 14, '80"x14G', None, "Flat Knit", 3, "Color Use: 6 | Needle: 1120X2"),
]


def seed(conn):
    cur = conn.cursor()
    row = cur.execute("SELECT id FROM industries WHERE name LIKE '%Adury%' LIMIT 1").fetchone()
    if not row:
        return
    ind_id = row["id"]

    chk = cur.execute(
        "SELECT COUNT(*) as c, COALESCE(SUM(quantity), 0) as q FROM machine_profiles WHERE industry_id = ?",
        (ind_id,),
    ).fetchone()
    if chk["c"] == len(ADURY_ROWS) and chk["q"] == 105:
        return

    cur.execute("DELETE FROM machine_profiles WHERE industry_id = ?", (ind_id,))
    for idx, (cat, fab, mtype, dia, gauge, lbl, feeders, brand, qty, rem) in enumerate(ADURY_ROWS, 1):
        calc = calculate_needle_sinker(fab, dia, gauge, qty)
        unit_name = "Circular Knit" if cat == "Circular" else "Collar & Cuff (Flat Knit)"
        cur.execute(
            """
            INSERT INTO machine_profiles (
                industry_id, fabrication, dia, gauge, dia_gauge_label, brand, quantity,
                needles_per_machine, sinkers_per_machine, remarks,
                unit, machine_category, machine_type, feeders,
                in_operation, sort_order
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?)
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
                unit_name,
                cat,
                mtype,
                feeders,
                idx,
            ),
        )
    conn.commit()
