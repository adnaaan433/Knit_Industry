"""Machines tab for a selected factory."""

import streamlit as st
from components.tables import machine_profile_table
import db


def render_machines_tab(industry: dict, machines: list):
    machine_profile_table(industry, machines)

    with st.expander("Machine Floor Notes", expanded=bool(industry.get("machine_profile_notes"))):
        with st.form(f"tab_mach_notes_{industry['id']}"):
            notes = st.text_area(
                "Spare parts, needle/sinker brands, oil, maintenance",
                value=industry.get("machine_profile_notes") or "",
                height=90,
            )
            if st.form_submit_button("Save Floor Notes"):
                db.update_machine_notes(industry["id"], notes)
                st.cache_data.clear()
                st.success("Notes saved.")
                st.rerun()
