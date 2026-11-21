"""Needle and sinker calculation and Dia x Gauge label helpers."""

import re
from config.constants import DOUBLE_BED_FABRICATIONS


def calculate_needle_sinker(fabrication: str, dia: float, gauge: float, quantity: int = 1):
    """
    Calculate needle and sinker requirements based on machine fabrication, diameter, and gauge.
    - Single-bed (Single Jersey, Fleece, H/Jersey):
        needles_per_machine = int(dia * gauge * 3.1416)
        sinkers_per_machine = int(dia * gauge * 3.1416)
    - Double-bed (Rib, Interlock):
        needles_per_machine = int(2 * dia * gauge * 3.1416)
        sinkers_per_machine = 0
    """
    if not dia or not gauge or float(dia) <= 0 or float(gauge) <= 0:
        return {
            "needles_per_machine": 0,
            "sinkers_per_machine": 0,
            "total_needles": 0,
            "total_sinkers": 0,
        }

    fab_norm = (fabrication or "").strip().lower()
    qty = max(int(quantity or 0), 0)

    is_double_bed = (
        fab_norm in DOUBLE_BED_FABRICATIONS
        or "rib" in fab_norm
        or "interlock" in fab_norm
        or "d/j" in fab_norm
        or "double jersey" in fab_norm
    )

    if is_double_bed:
        needles_pm = int(2 * float(dia) * float(gauge) * 3.1416)
        sinkers_pm = 0
    else:
        needles_pm = int(float(dia) * float(gauge) * 3.1416)
        sinkers_pm = int(float(dia) * float(gauge) * 3.1416)

    return {
        "needles_per_machine": needles_pm,
        "sinkers_per_machine": sinkers_pm,
        "total_needles": needles_pm * qty,
        "total_sinkers": sinkers_pm * qty,
    }


def parse_dia_gauge_label(dia_gauge_str: str):
    """Parse strings like '30x20', '36x20(F/L)', '34x24(I/L)' into (dia, gauge, formatted_label)."""
    s = str(dia_gauge_str or "").strip()
    m = re.search(r"(\d+(?:\.\d+)?)\s*[xX×*]\s*(\d+(?:\.\d+)?)", s)
    if m:
        dia = float(m.group(1))
        gauge = float(m.group(2))
        return dia, gauge, s
    return 0.0, 0.0, s


def format_dia_gauge(dia: float, gauge: float, suffix: str = "") -> str:
    if not dia or not gauge or float(dia) <= 0 or float(gauge) <= 0:
        return (suffix or "—").strip()
    d_str = str(int(float(dia))) if float(dia).is_integer() else str(dia)
    g_str = str(int(float(gauge))) if float(gauge).is_integer() else str(gauge)
    suf = (suffix or "").strip()
    if suf and not suf.startswith("("):
        suf = f"({suf})"
    return f"{d_str}x{g_str}{suf}"
