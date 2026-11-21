"""Generic data-driven machine_profile_table() component."""

from collections import defaultdict
import html
import pandas as pd
import streamlit as st
from components.cards import kpi_card
from config.constants import FABRICATION_TYPES
import db


def _build_grouped_html(rows: list) -> str:
    """Build a theme-aware HTML table grouped by Fabrication with subtotals and grand totals."""
    opt_cols = [
        ("machine_no", "M/C No.", False),
        ("machine_type", "Type", False),
        ("model", "Model", False),
        ("origin", "Origin", False),
        ("feeders", "Feeders", True),
        ("capacity_kg", "Cap. (kg)", True),
        ("remarks", "Remarks", False),
    ]
    active_opts = [(key, label, is_num) for key, label, is_num in opt_cols if any(r.get(key) not in (None, "") for r in rows)]

    headers = [("Fabrication", False), ("Dia x Gauge", False), ("Brand", False)] + [(lbl, is_num) for _, lbl, is_num in active_opts]
    meta_col_count = len(headers)
    headers.extend([("Qty", True), ("Needles/M", True), ("Sinkers/M", True), ("Total Needles", True), ("Total Sinkers", True)])

    thead_html = "<thead><tr>" + "".join(
        f'<th{" class=\"num\"" if is_n else ""}>{html.escape(h)}</th>' for h, is_n in headers
    ) + "</tr></thead>"

    fab_order = ["Fleece", "H/Jersey", "Single Jersey", "Rib", "Interlock"]
    grouped = defaultdict(list)
    for r in rows:
        grouped[r.get("fabrication") or "Single Jersey"].append(r)
    ordered_fabs = [f for f in fab_order if f in grouped] + [f for f in grouped if f not in fab_order]

    grand_inst = grand_oper = grand_needles = grand_sinkers = 0
    tbody_rows = []

    for fab in ordered_fabs:
        sub_inst = sub_oper = sub_needles = sub_sinkers = 0
        for item in grouped[fab]:
            in_op = int(item.get("in_operation", 1)) == 1
            qty = int(item.get("quantity") or 0)
            n_pm = int(item.get("needles_per_machine") or 0) if in_op else 0
            s_pm = int(item.get("sinkers_per_machine") or 0) if in_op else 0
            tot_n = int(item.get("total_needles") or 0) if in_op else 0
            tot_s = int(item.get("total_sinkers") or 0) if in_op else 0

            sub_inst += qty
            if in_op:
                sub_oper += qty
                sub_needles += tot_n
                sub_sinkers += tot_s

            cells = [
                f"<td>{html.escape(str(item.get('fabrication') or ''))}</td>",
                f"<td><code>{html.escape(str(item.get('dia_gauge_label') or ''))}</code></td>",
                f"<td><strong>{html.escape(str(item.get('brand') or '—'))}</strong></td>",
            ]
            for key, _, is_num in active_opts:
                val = item.get(key)
                if val in (None, ""):
                    disp = "—"
                elif key == "capacity_kg":
                    disp = str(int(float(val)))
                else:
                    disp = html.escape(str(val))
                cells.append(f'<td{" class=\"num\"" if is_num else ""}>{disp}</td>')

            cells.extend([
                f'<td class="num"><strong>{qty}</strong></td>',
                f'<td class="num">{f"{n_pm:,}" if in_op else "—"}</td>',
                f'<td class="num">{f"{s_pm:,}" if s_pm > 0 else "—"}</td>',
                f'<td class="num">{f"{tot_n:,}" if in_op else "—"}</td>',
                f'<td class="num">{f"{tot_s:,}" if tot_s > 0 else "—"}</td>',
            ])
            tr_cls = "" if in_op else ' class="muted-row"'
            tbody_rows.append(f"<tr{tr_cls}>{''.join(cells)}</tr>")

        grand_inst += sub_inst
        grand_oper += sub_oper
        grand_needles += sub_needles
        grand_sinkers += sub_sinkers

        sub_q = f"{sub_oper}" if sub_inst == sub_oper else f"{sub_oper} ({sub_inst} inst.)"
        tbody_rows.append(
            f'<tr class="subtotal-row"><td colspan="{meta_col_count}">{html.escape(fab)} Subtotal</td>'
            f'<td class="num">{sub_q}</td><td class="num">—</td><td class="num">—</td>'
            f'<td class="num">{sub_needles:,}</td><td class="num">{f"{sub_sinkers:,}" if sub_sinkers > 0 else "—"}</td></tr>'
        )

    grand_q = f"{grand_oper:,}" if grand_inst == grand_oper else f"{grand_oper:,} operating ({grand_inst:,} installed)"
    tbody_rows.append(
        f'<tr class="grandtotal-row"><td colspan="{meta_col_count}">Grand Total</td>'
        f'<td class="num">{grand_q}</td><td class="num">—</td><td class="num">—</td>'
        f'<td class="num">{grand_needles:,}</td><td class="num">{f"{grand_sinkers:,}" if grand_sinkers > 0 else "—"}</td></tr>'
    )
    return f'<div class="crm-table-wrap"><table class="crm-table">{thead_html}<tbody>{"".join(tbody_rows)}</tbody></table></div>'


def _render_machine_editor(industry_id: int, machines: list):
    """Render st.data_editor for adding, editing, and deleting machine rows."""
    cols = ["id", "Unit", "Category", "Fabrication", "Brand", "Dia", "Gauge", "Dia x Gauge", "Quantity", "In Operation", "Type", "Feeders", "Origin", "Model", "Remarks"]
    df_init = pd.DataFrame([
        {
            "id": m["id"], "Unit": m.get("unit") or "", "Category": m.get("machine_category") or "Circular",
            "Fabrication": m.get("fabrication") or "Single Jersey", "Brand": m.get("brand") or "",
            "Dia": float(m.get("dia") or 30), "Gauge": float(m.get("gauge") or 24), "Dia x Gauge": m.get("dia_gauge_label") or "",
            "Quantity": int(m.get("quantity") or 1), "In Operation": bool(int(m.get("in_operation", 1))),
            "Type": m.get("machine_type") or "", "Feeders": int(m["feeders"]) if m.get("feeders") is not None else 0,
            "Origin": m.get("origin") or "", "Model": m.get("model") or "", "Remarks": m.get("remarks") or "",
        }
        for m in machines
    ], columns=cols)

    edited_df = st.data_editor(
        df_init, num_rows="dynamic", use_container_width=True, hide_index=True, key=f"mach_editor_{industry_id}",
        column_config={
            "id": None,
            "Category": st.column_config.SelectboxColumn("Category", options=["Circular", "Flat"], default="Circular"),
            "Fabrication": st.column_config.SelectboxColumn("Fabrication", options=FABRICATION_TYPES, default="Single Jersey"),
            "Quantity": st.column_config.NumberColumn("Qty", min_value=1, default=1),
            "Dia": st.column_config.NumberColumn("Dia", min_value=0.0, default=30.0),
            "Gauge": st.column_config.NumberColumn("Gauge", min_value=0.0, default=24.0),
            "In Operation": st.column_config.CheckboxColumn("In Opt.", default=True),
        },
    )

    if st.button("Save Machine Changes", type="primary", key=f"save_mach_ed_{industry_id}"):
        existing_ids = {m["id"] for m in machines}
        kept_ids = set()
        for idx, row in edited_df.iterrows():
            r_id = row.get("id")
            fab, dia, gauge = str(row.get("Fabrication") or "Single Jersey"), float(row.get("Dia") or 0), float(row.get("Gauge") or 0)
            lbl = str(row.get("Dia x Gauge") or "").strip() or db.format_dia_gauge(dia, gauge)
            kw = dict(
                remarks=str(row.get("Remarks") or "").strip(), unit=str(row.get("Unit") or "").strip(),
                machine_category=str(row.get("Category") or "Circular").strip(), machine_type=str(row.get("Type") or "").strip(),
                feeders=int(row.get("Feeders") or 0) or None, origin=str(row.get("Origin") or "").strip(),
                model=str(row.get("Model") or "").strip(), in_operation=1 if bool(row.get("In Operation", True)) else 0,
                sort_order=idx + 1,
            )
            if pd.notna(r_id) and int(r_id) in existing_ids:
                kept_ids.add(int(r_id))
                db.update_machine(int(r_id), fab, dia, gauge, lbl, str(row.get("Brand") or ""), int(row.get("Quantity") or 1), **kw)
            else:
                db.add_machine(industry_id, fab, dia, gauge, lbl, str(row.get("Brand") or ""), int(row.get("Quantity") or 1), **kw)
        for del_id in existing_ids - kept_ids:
            db.delete_machine(del_id)
        st.cache_data.clear()
        st.success("Machine profile updated.")
        st.rerun()


def machine_profile_table(industry: dict, machines: list):
    """Generic data-driven machine profile component with unit filter, KPIs, grouped table, editor, and CSV export."""
    if st.toggle("Edit machines", value=False, key=f"toggle_edit_m_{industry['id']}"):
        _render_machine_editor(industry["id"], machines)
        return

    if not machines:
        st.info("No machines recorded for this factory yet. Toggle **Edit machines** above to add rows.")
        return

    units = sorted(list({m["unit"] for m in machines if (m.get("unit") or "").strip()}))
    active_rows = machines
    if len(units) > 1:
        unit_totals = {u: sum(m["quantity"] for m in machines if m.get("unit") == u) for u in units}
        unit_choice = st.radio(
            "Unit View", options=["All units"] + units, horizontal=True, key=f"unit_sel_{industry['id']}",
            format_func=lambda u: f"All units ({sum(m['quantity'] for m in machines)})" if u == "All units" else f"{u} ({unit_totals[u]})",
        )
        if unit_choice != "All units":
            active_rows = [m for m in machines if m.get("unit") == unit_choice]

    installed_total = sum(int(m["quantity"] or 0) for m in active_rows)
    operating_total = sum(int(m["quantity"] or 0) for m in active_rows if int(m.get("in_operation", 1)) == 1)
    total_needles = sum(int(m["total_needles"] or 0) for m in active_rows if int(m.get("in_operation", 1)) == 1)
    total_sinkers = sum(int(m["total_sinkers"] or 0) for m in active_rows if int(m.get("in_operation", 1)) == 1)
    brands_cnt = len({m["brand"] for m in active_rows if (m.get("brand") or "").strip() not in ("", "—")})

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        kpi_card("Installed Machines", f"{installed_total:,}", f"{operating_total:,} operating" if installed_total != operating_total else "All in operation")
    with k2:
        kpi_card("Machine Brands", f"{brands_cnt}", f"{len(units) or 1} unit(s)")
    with k3:
        kpi_card("Total Needles", f"{total_needles:,}", "Computed from Dia × Gauge")
    with k4:
        kpi_card("Total Sinkers", f"{total_sinkers:,}", "Single-bed machines")

    st.markdown(_build_grouped_html(active_rows), unsafe_allow_html=True)

    export_df = pd.DataFrame([
        {
            "Unit": m.get("unit") or "", "Category": m.get("machine_category") or "Circular",
            "Fabrication": m["fabrication"], "Dia x Gauge": m["dia_gauge_label"], "Dia": m["dia"], "Gauge": m["gauge"],
            "Brand": m["brand"], "Type": m.get("machine_type") or "", "Model": m.get("model") or "",
            "Origin": m.get("origin") or "", "Feeders": m.get("feeders"), "Capacity (kg)": m.get("capacity_kg"),
            "Quantity": m["quantity"], "In Operation": int(m.get("in_operation", 1)),
            "Needles/M": m["needles_per_machine"], "Sinkers/M": m["sinkers_per_machine"],
            "Total Needles": m["total_needles"], "Total Sinkers": m["total_sinkers"], "Remarks": m.get("remarks") or "",
        }
        for m in active_rows
    ])
    st.download_button(
        "Download CSV", data=export_df.to_csv(index=False).encode("utf-8"),
        file_name=f"{industry['name'].replace(' ', '_')}_machines.csv", mime="text/csv", key=f"dl_csv_m_{industry['id']}",
    )
