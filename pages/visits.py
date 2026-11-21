"""Cross-factory visits and follow-ups page."""

from datetime import datetime
import streamlit as st
from components.cards import visit_card
from components.forms import open_visit_dialog
from config.constants import VISIT_TYPES
import db


@st.cache_data
def _load_visits_data():
    return db.get_all_updates(), db.get_all_industries()


all_updates, all_industries = _load_visits_data()

top1, top2 = st.columns([3.5, 1.5])
with top1:
    st.title("Visits & Meeting Minutes")
    st.caption("Chronological log of all factory visits, discussions, action items, and follow-ups.")
with top2:
    fac_map = {i["id"]: i["name"] for i in all_industries}
    pick_fac = st.selectbox(
        "Log visit for factory",
        options=[None] + list(fac_map.keys()),
        format_func=lambda x: "+ Select factory to log visit..." if x is None else fac_map[x],
    )
    if pick_fac is not None:
        open_visit_dialog(pick_fac, contacts=db.get_contacts(pick_fac), existing=None)

f1, f2, f3, f4 = st.columns([2, 1.8, 1.8, 1.2])
with f1:
    factories = sorted(list({u["industry_name"] for u in all_updates}))
    sel_factories = st.multiselect("Factory", options=factories)
with f2:
    sel_types = st.multiselect("Interaction Type", options=VISIT_TYPES)
with f3:
    date_range = st.date_input("Visit Date Range", value=[])
with f4:
    st.write("")
    only_followups = st.toggle("Follow-ups only", value=False)

filtered = []
for u in all_updates:
    if sel_factories and u.get("industry_name") not in sel_factories:
        continue
    if sel_types and u.get("visit_type") not in sel_types:
        continue
    if only_followups and not (u.get("next_followup_date") or "").strip():
        continue
    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        try:
            v_dt = datetime.strptime(u["visit_date"], "%Y-%m-%d").date()
            if not (date_range[0] <= v_dt <= date_range[1]):
                continue
        except ValueError:
            pass
    filtered.append(u)

st.caption(f"Showing **{len(filtered)}** of **{len(all_updates)}** visit records")

if not filtered:
    st.info("No visit records match the current filters.")
else:
    for u in filtered:
        if visit_card(u, on_edit_key=f"all_ed_v_{u['id']}", show_factory=True):
            open_visit_dialog(u["industry_id"], contacts=db.get_contacts(u["industry_id"]), existing=u)
