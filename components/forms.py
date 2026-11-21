"""Shared add/edit forms and st.dialog modals for factories, contacts, and visits."""

from datetime import date, datetime
import streamlit as st
from config.constants import STATUS_OPTIONS, VISIT_TYPES
import db


def factory_form(existing: dict = None):
    """Shared form for adding or editing a factory."""
    is_edit = existing is not None
    with st.form("factory_shared_form", clear_on_submit=not is_edit):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Factory Name *", value=existing["name"] if is_edit else "")
            cluster = st.text_input("Cluster", value=(existing.get("cluster") or "") if is_edit else "")
            location_area = st.text_input("Location Area", value=(existing.get("location_area") or "") if is_edit else "")
        with c2:
            dist_val = float(existing["distance_km"]) if (is_edit and existing.get("distance_km")) else 0.0
            distance_km = st.number_input("Distance (km)", min_value=0.0, step=0.5, value=dist_val)
            map_url = st.text_input("Google Maps Link", value=(existing.get("map_url") or "") if is_edit else "")
            curr_st = existing.get("status", "New") if is_edit else "New"
            st_idx = STATUS_OPTIONS.index(curr_st) if curr_st in STATUS_OPTIONS else 0
            status = st.selectbox("Status", options=STATUS_OPTIONS, index=st_idx)
        general_notes = st.text_area("General Overview Notes", value=(existing.get("general_notes") or "") if is_edit else "")

        submitted = st.form_submit_button("Save Factory", type="primary", use_container_width=True)
        if submitted:
            if not name.strip():
                st.error("Factory name is required.")
            else:
                dist_clean = distance_km if distance_km > 0 else None
                if is_edit:
                    db.update_industry(existing["id"], name, location_area, cluster, dist_clean, map_url, status, general_notes)
                    st.cache_data.clear()
                    st.rerun()
                else:
                    new_id = db.create_industry(name, location_area, cluster, dist_clean, map_url, status, general_notes)
                    st.cache_data.clear()
                    st.query_params["factory"] = str(new_id)
                    st.rerun()


def contact_form(industry_id: int, existing: dict = None):
    """Shared form for adding or editing a contact."""
    is_edit = existing is not None
    with st.form("contact_shared_form", clear_on_submit=not is_edit):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Contact Name *", value=existing["name"] if is_edit else "")
            designation = st.text_input("Designation", value=(existing.get("designation") or "") if is_edit else "")
            phone = st.text_input("Phone", value=(existing.get("phone") or "") if is_edit else "")
        with c2:
            email = st.text_input("Email", value=(existing.get("email") or "") if is_edit else "")
            butex_batch = st.text_input("BUTEX Batch", value=(existing.get("butex_batch") or "") if is_edit else "")
            curr_st = existing.get("status", "New") if is_edit else "New"
            st_idx = STATUS_OPTIONS.index(curr_st) if curr_st in STATUS_OPTIONS else 0
            status = st.selectbox("Status", options=STATUS_OPTIONS, index=st_idx)
        notes = st.text_input("Notes", value=(existing.get("notes") or "") if is_edit else "")

        col_s, col_d = st.columns([3, 1] if is_edit else [1, 0.01])
        with col_s:
            if st.form_submit_button("Save Contact", type="primary", use_container_width=True):
                if not name.strip():
                    st.error("Contact name is required.")
                else:
                    if is_edit:
                        db.update_contact(existing["id"], name, designation, phone, email, butex_batch, status, notes)
                    else:
                        db.add_contact(industry_id, name, designation, phone, email, butex_batch, status, notes)
                    st.cache_data.clear()
                    st.rerun()
        if is_edit:
            with col_d:
                if st.form_submit_button("Delete", use_container_width=True):
                    db.delete_contact(existing["id"])
                    st.cache_data.clear()
                    st.rerun()


def visit_form(industry_id: int, contacts: list = None, existing: dict = None):
    """Shared form for adding or editing a visit log."""
    is_edit = existing is not None
    with st.form("visit_shared_form", clear_on_submit=not is_edit):
        c1, c2, c3 = st.columns(3)
        with c1:
            default_vdate = date.today()
            if is_edit and existing.get("visit_date"):
                try:
                    default_vdate = datetime.strptime(existing["visit_date"], "%Y-%m-%d").date()
                except ValueError:
                    pass
            visit_date = st.date_input("Visit Date *", value=default_vdate)
        with c2:
            curr_vt = existing.get("visit_type", VISIT_TYPES[0]) if is_edit else VISIT_TYPES[0]
            vt_idx = VISIT_TYPES.index(curr_vt) if curr_vt in VISIT_TYPES else 0
            visit_type = st.selectbox("Interaction Type", options=VISIT_TYPES, index=vt_idx)
        with c3:
            default_fdate = None
            if is_edit and existing.get("next_followup_date"):
                try:
                    default_fdate = datetime.strptime(existing["next_followup_date"], "%Y-%m-%d").date()
                except ValueError:
                    pass
            next_followup = st.date_input("Next Follow-up Date", value=default_fdate)

        if not is_edit and contacts:
            c_opts = [f"{c['name']} ({c['designation']})" if c.get("designation") else c["name"] for c in contacts]
            picked = st.multiselect("Contacts Met", options=c_opts)
            extra_att = st.text_input("Other Attendees")
        else:
            picked = []
            extra_att = st.text_input("Attendees", value=(existing.get("attendees") or "") if is_edit else "")

        minutes = st.text_area("Meeting Minutes *", value=(existing.get("meeting_minutes") or "") if is_edit else "", height=140)
        actions = st.text_area("Action Items / Next Steps", value=(existing.get("action_items") or "") if is_edit else "", height=80)
        mark_visited = st.checkbox("Mark factory status as 'Visited'", value=(not is_edit and visit_type == "Factory Visit"))

        col_s, col_d = st.columns([3, 1] if is_edit else [1, 0.01])
        with col_s:
            if st.form_submit_button("Save Visit Log", type="primary", use_container_width=True):
                if not minutes.strip():
                    st.error("Meeting minutes are required.")
                else:
                    att_parts = list(picked)
                    if extra_att.strip():
                        att_parts.append(extra_att.strip())
                    att_str = ", ".join(att_parts)
                    f_str = str(next_followup) if next_followup else ""
                    if is_edit:
                        db.edit_update(existing["id"], visit_date, visit_type, att_str, minutes, actions, f_str)
                    else:
                        db.add_update(industry_id, visit_date, visit_type, att_str, minutes, actions, f_str)
                    if mark_visited:
                        db.update_industry_status(industry_id, "Visited")
                    st.cache_data.clear()
                    st.rerun()
        if is_edit:
            with col_d:
                if st.form_submit_button("Delete", use_container_width=True):
                    db.delete_update(existing["id"])
                    st.cache_data.clear()
                    st.rerun()


@st.dialog("Add Factory", width="large")
def open_add_factory_dialog():
    factory_form(existing=None)


@st.dialog("Edit Factory", width="large")
def open_edit_factory_dialog(industry: dict):
    factory_form(existing=industry)


@st.dialog("Confirm Delete Factory")
def open_delete_factory_dialog(industry: dict):
    st.warning(f"Are you sure you want to permanently delete **{industry['name']}** and all of its machines, contacts, and visits?")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Confirm Delete", type="primary", use_container_width=True):
            db.delete_industry(industry["id"])
            st.cache_data.clear()
            st.query_params.clear()
            st.rerun()
    with c2:
        if st.button("Cancel", use_container_width=True):
            st.rerun()


@st.dialog("Add / Edit Contact", width="large")
def open_contact_dialog(industry_id: int, existing: dict = None):
    contact_form(industry_id, existing=existing)


@st.dialog("Add / Edit Visit Log", width="large")
def open_visit_dialog(industry_id: int, contacts: list = None, existing: dict = None):
    visit_form(industry_id, contacts=contacts, existing=existing)
