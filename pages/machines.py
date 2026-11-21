"""Cross-factory machine explorer page."""

from collections import defaultdict
import pandas as pd
import streamlit as st
from components.cards import kpi_card
import db


@st.cache_data
def _load_all_machines():
    return db.get_all_machines()


all_machines = _load_all_machines()

st.title("Machines Explorer")
st.caption("Search and filter knitting machines, needle counts, and sinker requirements across all factories.")

f1, f2, f3, f4, f5 = st.columns([2, 1.6, 1.5, 1.5, 1.4])
with f1:
    factories = sorted(list({m["industry_name"] for m in all_machines}))
    sel_factories = st.multiselect("Factory", options=factories)
with f2:
    brands = sorted(list({m["brand"] for m in all_machines if (m.get("brand") or "").strip() not in ("", "—")}))
    sel_brands = st.multiselect("Brand", options=brands)
with f3:
    fabs = sorted(list({m["fabrication"] for m in all_machines if m.get("fabrication")}))
    sel_fabs = st.multiselect("Fabrication", options=fabs)
with f4:
    dias = [float(m["dia"]) for m in all_machines if float(m.get("dia") or 0) > 0]
    min_d, max_d = (int(min(dias)), int(max(dias))) if dias else (10, 80)
    dia_range = st.slider("Dia Range (inch)", min_value=0, max_value=max(max_d, 80), value=(0, max(max_d, 80)))
with f5:
    gauges = sorted(list({int(m["gauge"]) for m in all_machines if float(m.get("gauge") or 0) > 0}))
    sel_gauges = st.multiselect("Gauge", options=gauges)

filtered = []
for m in all_machines:
    if sel_factories and m["industry_name"] not in sel_factories:
        continue
    if sel_brands and m.get("brand") not in sel_brands:
        continue
    if sel_fabs and m.get("fabrication") not in sel_fabs:
        continue
    d_val = float(m.get("dia") or 0)
    if not (dia_range[0] <= d_val <= dia_range[1]):
        continue
    if sel_gauges and int(m.get("gauge") or 0) not in sel_gauges:
        continue
    filtered.append(m)

tot_inst = sum(int(m["quantity"] or 0) for m in filtered)
tot_oper = sum(int(m["quantity"] or 0) for m in filtered if int(m.get("in_operation", 1)) == 1)
tot_needles = sum(int(m["total_needles"] or 0) for m in filtered if int(m.get("in_operation", 1)) == 1)
tot_sinkers = sum(int(m["total_sinkers"] or 0) for m in filtered if int(m.get("in_operation", 1)) == 1)

k1, k2, k3, k4 = st.columns(4)
with k1:
    kpi_card("Matching Machines", f"{tot_inst:,}", f"{tot_oper:,} operating")
with k2:
    kpi_card("Factories Matched", str(len({m["industry_id"] for m in filtered})), f"{len(filtered)} rows")
with k3:
    kpi_card("Total Needles", f"{tot_needles:,}", "Operating machines")
with k4:
    kpi_card("Total Sinkers", f"{tot_sinkers:,}", "Single-bed operating")

df_rows = pd.DataFrame(
    [
        {
            "Factory": m["industry_name"],
            "Unit": m.get("unit") or "—",
            "Category": m.get("machine_category") or "Circular",
            "Fabrication": m["fabrication"],
            "Brand": m["brand"],
            "Dia x Gauge": m["dia_gauge_label"],
            "Dia": int(m["dia"]) if float(m["dia"]).is_integer() else m["dia"],
            "Gauge": int(m["gauge"]) if float(m["gauge"]).is_integer() else m["gauge"],
            "Quantity": m["quantity"],
            "In Operation": bool(int(m.get("in_operation", 1))),
            "Needles/M": m["needles_per_machine"],
            "Sinkers/M": m["sinkers_per_machine"],
            "Total Needles": m["total_needles"],
            "Total Sinkers": m["total_sinkers"],
            "Type": m.get("machine_type") or "",
            "Origin": m.get("origin") or "",
            "Feeders": m.get("feeders"),
            "Remarks": m.get("remarks") or "",
        }
        for m in filtered
    ]
)

c_table, c_chart = st.columns([2.5, 1])
with c_table:
    st.dataframe(df_rows, use_container_width=True, hide_index=True, height=520)
    st.download_button(
        "Download Filtered Machines (CSV)",
        data=df_rows.to_csv(index=False).encode("utf-8"),
        file_name="knit_crm_machines.csv",
        mime="text/csv",
    )

with c_chart:
    st.markdown("#### Brand Breakdown")
    brand_totals = defaultdict(int)
    for m in filtered:
        b = (m.get("brand") or "Unspecified").strip()
        if b and b != "—":
            brand_totals[b] += int(m["quantity"] or 0)
    if brand_totals:
        df_b = pd.DataFrame(
            [{"Brand": k, "Machines": v} for k, v in sorted(brand_totals.items(), key=lambda x: -x[1])]
        )
        st.bar_chart(df_b.set_index("Brand")["Machines"])
        st.dataframe(df_b, use_container_width=True, hide_index=True)
