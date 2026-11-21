"""Visits tab for a selected factory."""

import streamlit as st
from components.cards import visit_card
from components.forms import open_visit_dialog


def render_visits_tab(industry: dict, contacts: list, updates: list):
    top1, top2 = st.columns([3, 1.2])
    with top1:
        st.markdown(f"#### Visit Logs & Meeting Minutes ({len(updates)})")
    with top2:
        if st.button("+ Log Visit", type="primary", use_container_width=True, key=f"add_v_btn_{industry['id']}"):
            open_visit_dialog(industry["id"], contacts=contacts, existing=None)

    if not updates:
        st.info("No visits or meeting minutes logged for this factory yet.")
        return

    for upd in updates:
        if visit_card(upd, on_edit_key=f"ed_v_{upd['id']}"):
            open_visit_dialog(industry["id"], contacts=contacts, existing=upd)
