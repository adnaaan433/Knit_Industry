"""Verification script asserting database counts, factory machine totals, and needle/sinker formulas."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.calc import calculate_needle_sinker
from db.connection import get_connection
from db.repo import get_all_industries, get_all_machines
from db.schema import init_db

EXPECTED_MACHINE_TOTALS = {
    "Fakir Knitwears Ltd.": {"installed": 167, "operating": 165},
    "MASCO (Concept Knitting)": {"installed": 197, "operating": 197},
    "Renaissance Apparels Ltd.": {"installed": 79, "operating": 79},
    "Adury Knit Composite": {"installed": 105, "operating": 105},
    "Tosrifa Industries Ltd": {"installed": 69, "operating": 69},
    "Gram Tech (Sonali Textile)": {"installed": 32, "operating": 32},
    "S.M. Group": {"installed": 99, "operating": 99},
    "L'Esquire Ltd.": {"installed": 97, "operating": 97},
}


def main():
    init_db()
    conn = get_connection()
    cur = conn.cursor()

    ind_count = cur.execute("SELECT COUNT(*) as c FROM industries").fetchone()["c"]
    contact_count = cur.execute("SELECT COUNT(*) as c FROM contacts").fetchone()["c"]
    update_count = cur.execute("SELECT COUNT(*) as c FROM updates").fetchone()["c"]
    conn.close()

    errors = []
    print(f"Database counts -> Industries: {ind_count}, Contacts: {contact_count}, Updates: {update_count}")
    if ind_count < 32:
        errors.append(f"Expected at least 32 industries, found {ind_count}")
    if contact_count < 42:
        errors.append(f"Expected at least 42 contacts, found {contact_count}")
    if update_count < 2:
        errors.append(f"Expected at least 2 updates, found {update_count}")

    industries = {i["name"]: i for i in get_all_industries()}
    print("\nFactory Machine Totals:")
    for fac_name, expected in EXPECTED_MACHINE_TOTALS.items():
        ind = industries.get(fac_name)
        if not ind:
            errors.append(f"Missing factory in DB: {fac_name}")
            continue
        inst = ind["machine_count"]
        oper = ind["operating_machine_count"]
        status_str = "PASS" if (inst == expected["installed"] and oper == expected["operating"]) else "FAIL"
        print(
            f"  [{status_str}] {fac_name:<30} installed={inst} (expected {expected['installed']}), "
            f"operating={oper} (expected {expected['operating']})"
        )
        if inst != expected["installed"] or oper != expected["operating"]:
            errors.append(
                f"{fac_name}: got installed={inst}, operating={oper}; "
                f"expected installed={expected['installed']}, operating={expected['operating']}"
            )

    all_machines = get_all_machines()
    formula_mismatches = 0
    for m in all_machines:
        in_op = int(m.get("in_operation", 1))
        qty = int(m["quantity"]) if in_op else 0
        expected_calc = calculate_needle_sinker(m["fabrication"], m["dia"], m["gauge"], qty)
        if (
            m["needles_per_machine"] != expected_calc["needles_per_machine"]
            or m["sinkers_per_machine"] != expected_calc["sinkers_per_machine"]
            or m["total_needles"] != expected_calc["total_needles"]
            or m["total_sinkers"] != expected_calc["total_sinkers"]
        ):
            formula_mismatches += 1
            errors.append(f"Formula mismatch on machine row id={m['id']} ({m['industry_name']})")

    print(f"\nChecked needle/sinker formulas across {len(all_machines)} machine rows: {formula_mismatches} mismatches.")

    if errors:
        print("\nVERIFICATION FAILED:")
        for e in errors:
            print("  -", e)
        sys.exit(1)

    print("\nALL VERIFICATION CHECKS PASSED.")


if __name__ == "__main__":
    main()
