"""
Permanent Machine Profile data and HTML table renderer for MASCO (Concept Knitting)
Extracted from:
- Machine Profile_10_04_2026.pdf (Unit-1: Kendua, Kanchan, Rupganj, Narayanganj — 121 Machines)
- Machine Profile_04.05_2026 unit-2.pdf (Unit-2: 111/1, Darail, Shataish, Tongi — 48 Circular + 28 Collar = 76 Machines)
"""

import html

# Each circular machine table section has groups by DIA -> BRAND/ORIGIN -> Machine Group -> Gauge/Cylinder rows.
# Structure of each row tuple in `rows`:
#   (dia, dia_span, brand, brand_span, origin, origin_span, num_machines, num_span, gauge, cylinders, feeders, feed_span, remarks, rem_span)
# If a span is 0, that cell is covered by a previous row's rowspan.

MASCO_UNIT1_DOUBLE_JERSEY = [
    # 34" FUKUHARA JAPAN (5 rows)
    ('34"', 5, "FUKUHARA", 5, "JAPAN", 5, 1, 2, "18", "1", "62", 2, "", 1),
    (None, 0, None, 0, None, 0, None, 0, "22", "2", None, 0, "Rib/ INTERLOCK", 1),
    (None, 0, None, 0, None, 0, 4, 3, "18", "4", "70", 3, "", 1),
    (None, 0, None, 0, None, 0, None, 0, "24", "4", None, 0, "INTERLOCK(1 set quilting Device)", 1),
    (None, 0, None, 0, None, 0, None, 0, "28", "2", None, 0, "Rib/ INTERLOCK", 1),
    # 36" FUKUHARA JAPAN (5 rows)
    ('36"', 5, "FUKUHARA", 5, "JAPAN", 5, 2, 2, "18", "2", "64", 2, "", 1),
    (None, 0, None, 0, None, 0, None, 0, "22", "2", None, 0, "Rib/ INTERLOCK", 1),
    (None, 0, None, 0, None, 0, 3, 3, "14", "1", "74", 3, "", 1),
    (None, 0, None, 0, None, 0, None, 0, "18", "3", None, 0, "", 1),
    (None, 0, None, 0, None, 0, None, 0, "24", "3", None, 0, "INTERLOCK(1 set spacer device)", 1),
    # 38" FUKUHARA JAPAN (5 rows)
    ('38"', 5, "FUKUHARA", 5, "JAPAN", 5, 5, 2, "18", "5", "68", 2, "", 1),
    (None, 0, None, 0, None, 0, None, 0, "22", "2", None, 0, "Rib/ INTERLOCK", 1),
    (None, 0, None, 0, None, 0, 2, 3, "14", "1", "78", 3, "", 1),
    (None, 0, None, 0, None, 0, None, 0, "18", "2", None, 0, "", 1),
    (None, 0, None, 0, None, 0, None, 0, "24", "2", None, 0, "Rib/ INTERLOCK", 1),
    # 40" FUKUHARA JAPAN (2 rows)
    ('40"', 2, "FUKUHARA", 2, "JAPAN", 2, 6, 2, "18", "6", "72", 2, "", 2),
    (None, 0, None, 0, None, 0, None, 0, "22", "2", None, 0, None, 0),
]

MASCO_UNIT1_SINGLE_JERSEY = [
    # 30" (9 rows)
    ('30"', 9, "FUKUHARA", 4, "JAPAN", 4, 6, 4, "24", "6", "96", 4, "", 4),
    (None, 0, None, 0, None, 0, None, 0, "28", "5", None, 0, None, 0),
    (None, 0, None, 0, None, 0, None, 0, "32", "2", None, 0, None, 0),
    (None, 0, None, 0, None, 0, None, 0, "36", "1", None, 0, None, 0),
    (None, 0, "KEUM YUNG", 3, "KOREA", 3, 3, 3, "20", "1", "90", 5, "", 1),
    (None, 0, None, 0, None, 0, None, 0, "24", "3", None, 0, "", 1),
    (None, 0, None, 0, None, 0, None, 0, "32", "1", None, 0, "", 1),
    (None, 0, "SANTONI", 2, "ITALY", 2, 3, 2, "20", "3", None, 0, "FLEECE", 1),
    (None, 0, None, 0, None, 0, None, 0, "24", "2", None, 0, "", 1),
    # 32" (15 rows)
    ('32"', 15, "FUKUHARA", 5, "JAPAN", 5, 5, 4, "20", "1", "104", 4, "", 1),
    (None, 0, None, 0, None, 0, None, 0, "22", "2", None, 0, "", 1),
    (None, 0, None, 0, None, 0, None, 0, "24", "5", None, 0, "", 1),
    (None, 0, None, 0, None, 0, None, 0, "28", "4", None, 0, "", 1),
    (None, 0, None, 0, None, 0, 1, 1, "24", "1", "160", 1, "5 FEEDER", 1),
    (None, 0, "KEUM YUNG", 3, "KOREA", 3, 4, 3, "20", "2", "96", 3, "", 1),
    (None, 0, None, 0, None, 0, None, 0, "24", "4", None, 0, "", 1),
    (None, 0, None, 0, None, 0, None, 0, "32", "1", None, 0, "", 1),
    (None, 0, "LISKY", 3, "TAIWAN", 3, 5, 3, "18", "5", "102", 3, "FLEECE", 1),
    (None, 0, None, 0, None, 0, None, 0, "20", "5", None, 0, "FLEECE", 1),
    (None, 0, None, 0, None, 0, None, 0, "24", "5", None, 0, "", 1),
    (None, 0, "SANTONI", 4, "ITALY", 4, 4, 4, "22", "2", "96", 4, "OPEN DIA", 4),
    (None, 0, None, 0, None, 0, None, 0, "24", "4", None, 0, None, 0),
    (None, 0, None, 0, None, 0, None, 0, "28", "2", None, 0, None, 0),
    (None, 0, None, 0, None, 0, None, 0, "36", "4", None, 0, None, 0),
    # 34" (16 rows)
    ('34"', 16, "FUKUHARA", 6, "JAPAN", 6, 5, 5, "14", "2", "108", 5, "", 5),
    (None, 0, None, 0, None, 0, None, 0, "20", "1", None, 0, None, 0),
    (None, 0, None, 0, None, 0, None, 0, "22", "2", None, 0, None, 0),
    (None, 0, None, 0, None, 0, None, 0, "24", "5", None, 0, None, 0),
    (None, 0, None, 0, None, 0, None, 0, "28", "3", None, 0, None, 0),
    (None, 0, None, 0, None, 0, 1, 1, "24", "1", "170", 1, "5 FEEDER", 1),
    (None, 0, "KEUM YUNG", 3, "KOREA", 3, 5, 3, "14", "1", "102", 3, "FLEECE", 3),
    (None, 0, None, 0, None, 0, None, 0, "20", "3", None, 0, None, 0),
    (None, 0, None, 0, None, 0, None, 0, "24", "5", None, 0, None, 0),
    (None, 0, "LISKY", 3, "TAIWAN", 3, 6, 3, "18", "6", "108", 3, "FLEECE", 1),
    (None, 0, None, 0, None, 0, None, 0, "20", "6", None, 0, "FLEECE", 1),
    (None, 0, None, 0, None, 0, None, 0, "24", "6", None, 0, "", 1),
    (None, 0, "SANTONI", 4, "ITALY", 4, 4, 4, "22", "2", "102", 4, "OPEN DIA", 4),
    (None, 0, None, 0, None, 0, None, 0, "24", "4", None, 0, None, 0),
    (None, 0, None, 0, None, 0, None, 0, "28", "2", None, 0, None, 0),
    (None, 0, None, 0, None, 0, None, 0, "36", "4", None, 0, None, 0),
    # 36" (16 rows)
    ('36"', 16, "FUKUHARA", 4, "JAPAN", 4, 6, 4, "14", "3", "114", 4, "", 1),
    (None, 0, None, 0, None, 0, None, 0, "20", "2", None, 0, "", 1),
    (None, 0, None, 0, None, 0, None, 0, "22", "2", None, 0, "", 1),
    (None, 0, None, 0, None, 0, None, 0, "24", "6", None, 0, "", 1),
    (None, 0, "FUKUHARA", 1, "JAPAN", 1, 1, 1, "24", "1", "180", 1, "5 FEEDER", 1),
    (None, 0, "KEUM YUNG", 3, "KOREA", 3, 2, 2, "14", "1", "108", 2, "", 1),
    (None, 0, None, 0, None, 0, None, 0, "24", "2", None, 0, "", 1),
    (None, 0, None, 0, None, 0, 2, 1, "24", "2", "144", 1, "4 FEEDER", 1),
    (None, 0, "LISKY", 4, "TAIWAN", 4, 4, 4, "14", "2", "108", 4, "FLEECE", 1),
    (None, 0, None, 0, None, 0, None, 0, "20", "4", None, 0, "FLEECE", 1),
    (None, 0, None, 0, None, 0, None, 0, "18", "4", None, 0, "FLEECE", 1),
    (None, 0, None, 0, None, 0, None, 0, "24", "4", None, 0, "", 1),
    (None, 0, "SANTONI", 3, "ITALY", 3, 4, 3, "22", "2", "108", 3, "OPEN DIA", 3),
    (None, 0, None, 0, None, 0, None, 0, "24", "4", None, 0, None, 0),
    (None, 0, None, 0, None, 0, None, 0, "28", "2", None, 0, None, 0),
    (None, 0, "SANTONI", 1, "ITALY", 1, 1, 1, "24", "1", "108", 1, "Tubular", 1),
    # 38" (13 rows)
    ('38"', 13, "FUKUHARA", 4, "JAPAN", 4, 5, 4, "14", "3", "120", 4, "", 1),
    (None, 0, None, 0, None, 0, None, 0, "22", "2", None, 0, "", 1),
    (None, 0, None, 0, None, 0, None, 0, "20", "2", None, 0, "", 1),
    (None, 0, None, 0, None, 0, None, 0, "24", "5", None, 0, "", 1),
    (None, 0, "KEUM YUNG", 1, "KOREA", 1, 2, 1, "24", "2", "114", 1, "", 1),
    (None, 0, "LISKY", 4, "TAIWAN", 4, 4, 3, "14", "2", "120", 4, "FLEECE", 1),
    (None, 0, None, 0, None, 0, None, 0, "18", "4", None, 0, "FLEECE", 1),
    (None, 0, None, 0, None, 0, None, 0, "24", "4", None, 0, "", 1),
    (None, 0, None, 0, None, 0, 2, 1, "24", "2", None, 0, "OPEN DIA", 1),
    (None, 0, "SANTONI", 3, "ITALY", 3, 4, 3, "22", "2", "114", 3, "OPEN DIA", 3),
    (None, 0, None, 0, None, 0, None, 0, "24", "4", None, 0, None, 0),
    (None, 0, None, 0, None, 0, None, 0, "28", "2", None, 0, None, 0),
    (None, 0, "SANTONI", 1, "ITALY", 1, 3, 1, "24", "3", "114", 1, "Tubular", 1),
    # 40" (4 rows)
    ('40"', 4, "FUKUHARA", 3, "JAPAN", 3, 4, 3, "14", "2", "128", 3, "", 1),
    (None, 0, None, 0, None, 0, None, 0, "18", "2", None, 0, "", 1),
    (None, 0, None, 0, None, 0, None, 0, "24", "4", None, 0, "", 1),
    (None, 0, "KEUM YUNG", 1, "KOREA", 1, 1, 1, "24", "1", "160", 1, "4 FEEDER", 1),
    # 42" (1 row)
    ('42"', 1, "KEUM YUNG", 1, "KOREA", 1, 1, 1, "24", "1", "126", 1, "", 1),
]

MASCO_UNIT2_DOUBLE_JERSEY = [
    # 34" (4 rows)
    ('34"', 4, "FUKUHARA", 2, "JAPAN", 2, 1, 1, "18", "1", "62", 1, "", 1),
    (None, 0, None, 0, None, 0, 1, 1, "18", "1", "70", 1, "", 1),
    (None, 0, "KEUM YUNG", 2, "KOREA", 2, 1, 2, "18", "1", "68", 2, "", 1),
    (None, 0, None, 0, None, 0, None, 0, "24", "1", None, 0, "Rib/ INTERLOCK", 1),
    # 36 (4 rows)
    ("36", 4, "FUKUHARA", 2, "JAPAN", 2, 2, 2, "18", "2", "74", 2, "", 1),
    (None, 0, None, 0, None, 0, None, 0, "24", "1", None, 0, "", 1),
    (None, 0, "KEUM YUNG", 2, "KOREA", 2, 1, 2, "18", "1", "72", 2, "", 1),
    (None, 0, None, 0, None, 0, None, 0, "24", "1", None, 0, "Rib/ INTERLOCK", 1),
    # 38" (3 rows)
    ('38"', 3, "FUKUHARA", 1, "JAPAN", 1, 1, 1, "18", "1", "68", 1, "", 1),
    (None, 0, "KEUM YUNG", 2, "KOREA", 2, 1, 2, "18", "1", "76", 2, "", 1),
    (None, 0, None, 0, None, 0, None, 0, "24", "1", None, 0, "Rib/ INTERLOCK", 1),
    # 40" (1 row)
    ('40"', 1, "FUKUHARA", 1, "JAPAN", 1, 1, 1, "18", "1", "72", 1, "", 1),
]

MASCO_UNIT2_SINGLE_JERSEY = [
    ('23"', 1, "PAI LUNG", 1, "TAIWAN", 1, 1, 1, "24", "1", "68", 1, "", 1),
    ('25"', 1, "PAI LUNG", 1, "TAIWAN", 1, 1, 1, "24", "1", "74", 1, "", 1),
    ('26"', 1, "KEUM YUNG", 1, "KOREA", 1, 1, 1, "24", "1", "78", 1, "", 1),
    ('28"', 2, "PAI LUNG", 2, "TAIWAN", 2, 2, 2, "24", "2", "84", 2, "", 2),
    (None, 0, None, 0, None, 0, None, 0, "28", "1", None, 0, None, 0),
    # 30" (6 rows)
    ('30"', 6, "FUKUHARA", 1, "JAPAN", 1, 1, 1, "24", "1", "96", 1, "", 1),
    (None, 0, "SANTONI", 3, "ITALY", 3, 4, 3, "20", "1", "90", 3, "Fleece", 1),
    (None, 0, None, 0, None, 0, None, 0, "24", "3", None, 0, "", 1),
    (None, 0, None, 0, None, 0, None, 0, "28", "2", None, 0, "", 1),
    (None, 0, "PAI LUNG", 2, "TAIWAN", 2, 1, 2, "24", "1", "90", 2, "", 1),
    (None, 0, None, 0, None, 0, None, 0, "28", "1", None, 0, "", 1),
    # 32" (6 rows)
    ('32"', 6, "FUKUHARA", 1, "JAPAN", 1, 1, 1, "24", "1", "104", 1, "", 1),
    (None, 0, "SANTONI", 2, "ITALY", 2, 3, 2, "16", "2", "90", 2, "", 2),
    (None, 0, None, 0, None, 0, None, 0, "24", "3", None, 0, None, 0),
    (None, 0, "Lisky", 3, "Thaiwan", 3, 1, 3, "18", "1", "102", 3, "Fleece", 3),
    (None, 0, None, 0, None, 0, None, 0, "20", "1", None, 0, None, 0),
    (None, 0, None, 0, None, 0, None, 0, "24", "1", None, 0, None, 0),
    # 34 (7 rows)
    ("34", 7, "PAI LUNG", 2, "TAIWAN", 2, 1, 2, "24", "1", "102", 2, "", 2),
    (None, 0, None, 0, None, 0, None, 0, "28", "1", None, 0, None, 0),
    (None, 0, "SAN DA", 5, "TAIWAN", 5, 1, 3, "10", "1", "54", 2, "H/J & Fleece", 2),
    (None, 0, None, 0, None, 0, None, 0, "12", "1", None, 0, None, 0),
    (None, 0, None, 0, None, 0, None, 0, "24", "1", "102", 1, "SJ", 1),
    (None, 0, None, 0, None, 0, 1, 2, "19", "1", "68", 1, "Velour", 1),
    (None, 0, None, 0, None, 0, None, 0, "24", "1", "102", 1, "SJ", 1),
    # 36 (4 rows)
    ("36", 4, "PAI LUNG", 2, "TAIWAN", 2, 1, 2, "24", "1", "108", 2, "", 2),
    (None, 0, None, 0, None, 0, None, 0, "28", "1", None, 0, None, 0),
    (None, 0, "SAN DA", 2, "TAIWAN", 2, 1, 2, "19", "1", "72", 1, "Velour", 1),
    (None, 0, None, 0, None, 0, None, 0, "24", "1", "108", 1, "S/J", 1),
]

MASCO_UNIT2_ENG_STRIPE_DJ = [
    ('34"', 3, "FUKUHARA", 3, "JAPAN", 3, 1, 3, "18", "1", "48", 3, "6 COLOR", 1),
    (None, 0, None, 0, None, 0, None, 0, "24", "1", None, 0, "INTERLOCK", 1),
    (None, 0, None, 0, None, 0, None, 0, "7/28", "1", None, 0, "QUARTER GAUGE", 1),
    ('36"', 2, "FUKUHARA", 2, "JAPAN", 2, 1, 2, "18", "1", "50", 2, "6 COLOR", 1),
    (None, 0, None, 0, None, 0, None, 0, "24", "1", None, 0, "INTERLOCK", 1),
]

MASCO_UNIT2_ENG_STRIPE_SJ = [
    ('30"', 3, "PAI LUNG", 3, "TAIWAN", 3, 3, 3, "16", "2", "42", 3, "6 COLOR", 3),
    (None, 0, None, 0, None, 0, None, 0, "20", "3", None, 0, None, 0),
    (None, 0, None, 0, None, 0, None, 0, "24", "3", None, 0, None, 0),
    ('32"', 2, "PAI LUNG", 2, "TAIWAN", 2, 1, 2, "20", "1", "44", 2, "6 COLOR", 2),
    (None, 0, None, 0, None, 0, None, 0, "24", "1", None, 0, None, 0),
    ('34"', 4, "FUKUHARA", 2, "JAPAN", 2, 1, 2, "20", "1", "84", 2, "6 COLOR", 4),
    (None, 0, None, 0, None, 0, None, 0, "24", "1", None, 0, None, 0),
    (None, 0, "PAI LUNG", 2, "TAIWAN", 2, 1, 2, "20", "1", "42", 2, None, 0),
    (None, 0, None, 0, None, 0, None, 0, "24", "1", None, 0, None, 0),
    ('36"', 2, "FUKUHARA", 2, "JAPAN", 2, 2, 2, "20", "2", "84", 2, "6 COLOR", 2),
    (None, 0, None, 0, None, 0, None, 0, "24", "2", None, 0, None, 0),
]

MASCO_UNIT2_JACQUARD_POINTAL = [
    ('34"', 1, "HANG XING", 1, "Chaina", 1, 1, 1, "24", "1", "72", 1, "Jacquard SJ", 1),
    ('30"', 1, "HANG XING", 1, "Chaina", 1, 2, 1, "18", "1", "48", 1, "Pointal Jacquard", 2),
    ('32"', 1, "HANG XING", 1, "Chaina", 1, 2, 1, "18", "1", "51", 1, None, 0),
    ('34"', 1, "HANG XING", 1, "Chaina", 1, 3, 1, "18", "3", "54", 1, "Pointal Jacquard", 1),
]

# Collar table tuples:
# (brand, brand_span, origin, origin_span, num_machines, num_span, gauge, bed_width, num_colors, remarks, rem_span)
MASCO_UNIT2_COLLAR = [
    ("MATSUYA", 6, "JAPAN", 6, 6, 1, "14", '40"', "6", "", 2),
    (None, 0, None, 0, 2, 1, "14", '40"', "4", None, 0),
    (None, 0, None, 0, 9, 2, "16", '80"', "8", "Semi Jacquard", 2),
    (None, 0, None, 0, None, 0, "14", '80"', "8", None, 0),
    (None, 0, None, 0, 6, 1, "16", '80"', "6", "Semi Jacquard", 1),
    (None, 0, None, 0, 3, 1, "16", '60"', "6", "Jacquard", 1),
    ("KAUO HENG", 1, "TAIWAN", 1, 2, 1, "14", '40"', "6", "Semi Jacquard", 1),
]


def _render_circular_section_rows(section_title: str, rows: list, total_footer=None) -> str:
    parts = [
        f'<tr><td colspan="8" style="background-color:#e2efda;color:#0f172a;font-weight:800;text-align:center;font-size:0.98rem;padding:7px;border:1.5px solid #0f172a;">{html.escape(section_title)}</td></tr>',
        "<tr>"
        '<th style="background-color:#ffe699;color:#0f172a;border:1px solid #0f172a;width:9%;">DIA</th>'
        '<th style="background-color:#ffe699;color:#0f172a;border:1px solid #0f172a;width:16%;">BRAND</th>'
        '<th style="background-color:#ffe699;color:#0f172a;border:1px solid #0f172a;width:12%;">ORIGIN</th>'
        '<th style="background-color:#ffe699;color:#0f172a;border:1px solid #0f172a;width:12%;">Number Of Machines</th>'
        '<th style="background-color:#ffe699;color:#0f172a;border:1px solid #0f172a;width:10%;">GAUGES</th>'
        '<th style="background-color:#ffe699;color:#0f172a;border:1px solid #0f172a;width:11%;">CYLINDERS</th>'
        '<th style="background-color:#ffe699;color:#0f172a;border:1px solid #0f172a;width:11%;">FEEDERS</th>'
        '<th style="background-color:#ffe699;color:#0f172a;border:1px solid #0f172a;width:19%;">REMARKS</th>'
        "</tr>",
    ]
    for (
        dia,
        dia_s,
        brand,
        brand_s,
        origin,
        orig_s,
        num_m,
        num_s,
        gauge,
        cyl,
        feed,
        feed_s,
        rem,
        rem_s,
    ) in rows:
        tr = ["<tr>"]
        if dia_s > 0:
            tr.append(f'<td class="total-col" rowspan="{dia_s}"><strong>{html.escape(str(dia))}</strong></td>')
        if brand_s > 0:
            tr.append(f'<td class="total-col" rowspan="{brand_s}">{html.escape(str(brand))}</td>')
        if orig_s > 0:
            tr.append(f'<td class="total-col" rowspan="{orig_s}">{html.escape(str(origin))}</td>')
        if num_s > 0:
            tr.append(f'<td class="total-col" rowspan="{num_s}"><strong>{html.escape(str(num_m))}</strong></td>')
        tr.append(f'<td class="total-col">{html.escape(str(gauge))}</td>')
        tr.append(f'<td class="total-col">{html.escape(str(cyl))}</td>')
        if feed_s > 0:
            tr.append(f'<td class="total-col" rowspan="{feed_s}">{html.escape(str(feed))}</td>')
        if rem_s > 0:
            tr.append(f'<td class="total-col" rowspan="{rem_s}">{html.escape(str(rem))}</td>')
        tr.append("</tr>")
        parts.append("".join(tr))

    if total_footer is not None:
        parts.append(
            f"<tr>"
            f'<td colspan="3" style="background-color:#ffe699;color:#0f172a;font-weight:800;text-align:center;border:1.5px solid #0f172a;padding:7px;">TOTAL MACHINES</td>'
            f'<td class="total-col" style="background-color:#ffe699;color:#0f172a;font-weight:800;border:1.5px solid #0f172a;padding:7px;">{total_footer}</td>'
            f'<td colspan="4" style="background-color:#ffe699;border:1.5px solid #0f172a;"></td>'
            f"</tr>"
        )
    return "".join(parts)


def render_masco_unit1_html() -> str:
    """Render MASCO Unit-1 (Kendua, Kanchan, Rupganj, Narayanganj) Double Jersey & Single Jersey tables (Total: 121)."""
    dj_html = _render_circular_section_rows("DOUBLE JERSEY", MASCO_UNIT1_DOUBLE_JERSEY)
    sj_html = _render_circular_section_rows("SINGLE JERSEY", MASCO_UNIT1_SINGLE_JERSEY, total_footer=121)
    return (
        f'<div class="mp-sheet-container" style="max-width:960px;margin-bottom:1.25rem;">'
        f'<table class="mp-sheet-table" style="font-size:0.88rem;">'
        f"<tbody>{dj_html}{sj_html}</tbody>"
        f"</table>"
        f"</div>"
    )


def render_masco_unit2_circular_html() -> str:
    """Render MASCO Unit-2 (111/1, Darail, Shataish, Tongi) Circular Knitting tables (Total: 48)."""
    s1 = _render_circular_section_rows("DOUBLE JERSEY", MASCO_UNIT2_DOUBLE_JERSEY)
    s2 = _render_circular_section_rows("SINGLE JERSEY", MASCO_UNIT2_SINGLE_JERSEY)
    s3 = _render_circular_section_rows("ENG. STRIPE- Double Jersey (Rib And Interlock)", MASCO_UNIT2_ENG_STRIPE_DJ)
    s4 = _render_circular_section_rows("ENG. STRIPE- Single Jersey", MASCO_UNIT2_ENG_STRIPE_SJ)
    s5 = _render_circular_section_rows("Jacquard & Pointal M/C", MASCO_UNIT2_JACQUARD_POINTAL, total_footer=48)
    return (
        f'<div class="mp-sheet-container" style="max-width:960px;margin-bottom:1.25rem;">'
        f'<table class="mp-sheet-table" style="font-size:0.88rem;">'
        f"<tbody>{s1}{s2}{s3}{s4}{s5}</tbody>"
        f"</table>"
        f"</div>"
    )


def render_masco_unit2_collar_html() -> str:
    """Render MASCO Unit-2 Collar Flat Knitting Machine table (Total: 28)."""
    parts = [
        '<tr><td colspan="7" style="background-color:#e2efda;color:#0f172a;font-weight:800;text-align:center;font-size:0.98rem;padding:7px;border:1.5px solid #0f172a;">Collar</td></tr>',
        "<tr>"
        '<th style="background-color:#ffe699;color:#0f172a;border:1px solid #0f172a;width:16%;">BRAND</th>'
        '<th style="background-color:#ffe699;color:#0f172a;border:1px solid #0f172a;width:13%;">ORIGIN</th>'
        '<th style="background-color:#ffe699;color:#0f172a;border:1px solid #0f172a;width:14%;">Number Of Machines</th>'
        '<th style="background-color:#ffe699;color:#0f172a;border:1px solid #0f172a;width:12%;">GAUGES</th>'
        '<th style="background-color:#ffe699;color:#0f172a;border:1px solid #0f172a;width:13%;">Bed Width</th>'
        '<th style="background-color:#ffe699;color:#0f172a;border:1px solid #0f172a;width:14%;">Number of Colors</th>'
        '<th style="background-color:#ffe699;color:#0f172a;border:1px solid #0f172a;width:18%;">REMARKS</th>'
        "</tr>",
    ]
    for brand, brand_s, origin, orig_s, num_m, num_s, gauge, bed_w, colors, rem, rem_s in MASCO_UNIT2_COLLAR:
        tr = ["<tr>"]
        if brand_s > 0:
            tr.append(f'<td class="total-col" rowspan="{brand_s}"><strong>{html.escape(str(brand))}</strong></td>')
        if orig_s > 0:
            tr.append(f'<td class="total-col" rowspan="{orig_s}">{html.escape(str(origin))}</td>')
        if num_s > 0:
            tr.append(f'<td class="total-col" rowspan="{num_s}"><strong>{html.escape(str(num_m))}</strong></td>')
        tr.append(f'<td class="total-col">{html.escape(str(gauge))}</td>')
        tr.append(f'<td class="total-col">{html.escape(str(bed_w))}</td>')
        tr.append(f'<td class="total-col">{html.escape(str(colors))}</td>')
        if rem_s > 0:
            tr.append(f'<td class="total-col" rowspan="{rem_s}">{html.escape(str(rem))}</td>')
        tr.append("</tr>")
        parts.append("".join(tr))

    parts.append(
        "<tr>"
        '<td colspan="2" style="background-color:#ffe699;color:#0f172a;font-weight:800;text-align:center;border:1.5px solid #0f172a;padding:7px;">TOTAL MACHINES</td>'
        '<td class="total-col" style="background-color:#ffe699;color:#0f172a;font-weight:800;border:1.5px solid #0f172a;padding:7px;">28</td>'
        '<td colspan="4" style="background-color:#ffe699;border:1.5px solid #0f172a;"></td>'
        "</tr>"
    )
    return (
        f'<div class="mp-sheet-container" style="max-width:860px;margin-bottom:1.25rem;">'
        f'<table class="mp-sheet-table" style="font-size:0.88rem;">'
        f'<tbody>{"".join(parts)}</tbody>'
        f"</table>"
        f"</div>"
    )
