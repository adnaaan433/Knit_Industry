"""Contacts tab for a selected factory."""

import streamlit as st
from components.cards import contact_card
from components.forms import open_contact_dialog


def render_contacts_tab(industry: dict, contacts: list):
    top1, top2 = st.columns([3, 1.2])
    with top1:
        st.markdown(f"#### Contacts ({len(contacts)})")
    with top2:
        if st.button("+ Add Contact", type="primary", use_container_width=True, key=f"add_c_btn_{industry['id']}"):
            open_contact_dialog(industry["id"], existing=None)

    if not contacts:
        st.info("No contacts recorded for this factory yet.")
        return

    cols_per_row = 2
    for idx in range(0, len(contacts), cols_per_row):
        cols = st.columns(cols_per_row)
        for c_idx, c in enumerate(contacts[idx : idx + cols_per_row]):
            with cols[c_idx]:
                if contact_card(c, on_edit_key=f"ed_c_{c['id']}"):
                    open_contact_dialog(industry["id"], existing=c)
