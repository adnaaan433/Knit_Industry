"""Factories page: Master-detail layout with query-param routing (?factory=<id>)."""

import html
import streamlit as st
from components.badges import status_badge
from components.cards import factory_list_item, kpi_card
from components.forms import (
    open_add_factory_dialog,
    open_delete_factory_dialog,
    open_edit_factory_dialog,
)
from components.tabs.contacts import render_contacts_tab
from components.tabs.machines import render_machines_tab
from components.tabs.overview import render_overview_tab
from components.tabs.visits import render_visits_tab
from config.constants import STATUS_OPTIONS
import db


@st.cache_data
def _load_industries():
    return db.get_all_industries()


@st.cache_data
def _load_factory_details(industry_id: int):
    return (
        db.get_industry(industry_id),
        db.get_machines(industry_id),
        db.get_contacts(industry_id),
        db.get_updates(industry_id),
    )


all_industries = _load_industries()
industry_by_id = {i["id"]: i for i in all_industries}

# Resolve selected factory from ?factory=<id>
qp_fac = st.query_params.get("factory")
selected_id = int(qp_fac) if (qp_fac and str(qp_fac).isdigit() and int(qp_fac) in industry_by_id) else None

col_list, col_detail = st.columns([1, 2.4], gap="medium")

with col_list:
    top_l1, top_l2 = st.columns([2.2, 1.4])
    with top_l1:
        st.subheader("Factories")
    with top_l2:
        if st.button("+ Add Factory", use_container_width=True, type="primary"):
            open_add_factory_dialog()

    search_q = st.text_input("Search factory, location, or cluster", placeholder="Search...")

    all_clusters = sorted(list({i["cluster"] for i in all_industries if i.get("cluster")}))
    qp_cluster = st.query_params.get("cluster")
    default_clusters = [qp_cluster] if qp_cluster in all_clusters else []
    f_clusters = st.multiselect("Cluster", options=all_clusters, default=default_clusters)

    f_statuses = st.multiselect("Status", options=STATUS_OPTIONS)
    sort_by = st.selectbox(
        "Sort by",
        ["Most machines", "Name (A–Z)", "Nearest distance", "Most contacts"],
    )

    filtered = []
    for ind in all_industries:
        if search_q:
            q = search_q.lower()
            if (
                q not in ind["name"].lower()
                and q not in (ind.get("location_area") or "").lower()
                and q not in (ind.get("cluster") or "").lower()
            ):
                continue
        if f_clusters and ind.get("cluster") not in f_clusters:
            continue
        if f_statuses and ind.get("status") not in f_statuses:
            continue
        filtered.append(ind)

    if sort_by == "Most machines":
        filtered.sort(key=lambda x: (-x["machine_count"], -x["contact_count"], x["name"]))
    elif sort_by == "Nearest distance":
        filtered.sort(key=lambda x: (x["distance_km"] if x.get("distance_km") is not None else 9999.0, x["name"]))
    elif sort_by == "Most contacts":
        filtered.sort(key=lambda x: (-x["contact_count"], -x["machine_count"], x["name"]))
    else:
        filtered.sort(key=lambda x: x["name"])

    st.caption(f"Showing **{len(filtered)}** of **{len(all_industries)}** factories")

    if selected_id is None and filtered:
        selected_id = filtered[0]["id"]
        st.query_params["factory"] = str(selected_id)

    # Compact dropdown for quick mobile/narrow selection
    if filtered:
        fac_ids = [i["id"] for i in filtered]
        sel_idx = fac_ids.index(selected_id) if selected_id in fac_ids else 0
        quick_pick = st.selectbox(
            "Quick select factory",
            options=fac_ids,
            index=sel_idx,
            format_func=lambda fid: f"{industry_by_id[fid]['name']} ({industry_by_id[fid]['machine_count']} M)",
            label_visibility="collapsed",
        )
        if quick_pick != selected_id:
            selected_id = quick_pick
            st.query_params["factory"] = str(selected_id)
            st.rerun()

    with st.container(height=620):
        for ind in filtered:
            if factory_list_item(ind, is_selected=(ind["id"] == selected_id)):
                st.query_params["factory"] = str(ind["id"])
                st.rerun()

with col_detail:
    if selected_id is None or selected_id not in industry_by_id:
        st.info("Select a factory from the list on the left.")
    else:
        industry, machines, contacts, updates = _load_factory_details(selected_id)

        # Header block
        with st.container(border=True):
            h1, h2 = st.columns([3.2, 1.8])
            with h1:
                st.markdown(
                    f"### {html.escape(industry['name'])} &nbsp; {status_badge(industry.get('status', 'New'))}",
                    unsafe_allow_html=True,
                )
                loc_parts = [p for p in [industry.get("location_area"), industry.get("cluster")] if p]
                loc_str = ", ".join(loc_parts) if loc_parts else "Location not set"
                dist_str = f" • {industry['distance_km']} km from Dhaka" if industry.get("distance_km") else ""
                st.caption(f"📍 {loc_str}{dist_str}")

            with h2:
                curr_st = industry.get("status") or "New"
                st_opts = STATUS_OPTIONS if curr_st in STATUS_OPTIONS else [curr_st] + STATUS_OPTIONS
                new_st = st.selectbox(
                    "Status",
                    options=st_opts,
                    index=st_opts.index(curr_st),
                    key=f"hdr_st_{selected_id}",
                    label_visibility="collapsed",
                )
                if new_st != curr_st:
                    db.update_industry_status(selected_id, new_st)
                    st.cache_data.clear()
                    st.rerun()

                act1, act2, act3 = st.columns(3)
                with act1:
                    if industry.get("map_url"):
                        st.link_button("Maps", industry["map_url"], use_container_width=True)
                    else:
                        st.button("No Map", disabled=True, use_container_width=True)
                with act2:
                    if st.button("Edit", key=f"edit_fac_{selected_id}", use_container_width=True):
                        open_edit_factory_dialog(industry)
                with act3:
                    if st.button("Delete", key=f"del_fac_{selected_id}", use_container_width=True):
                        open_delete_factory_dialog(industry)

        # KPI Strip
        tot_m = sum(int(m["quantity"] or 0) for m in machines)
        op_m = sum(int(m["quantity"] or 0) for m in machines if int(m.get("in_operation", 1)) == 1)
        next_fu = industry_by_id[selected_id].get("next_followup_date") or "—"

        s1, s2, s3, s4 = st.columns(4)
        with s1:
            sub_m = f"{op_m:,} operating" if tot_m != op_m else "Installed"
            kpi_card("Total Machines", f"{tot_m:,}", sub_m)
        with s2:
            kpi_card("Contacts", str(len(contacts)), "Key personnel")
        with s3:
            kpi_card("Visits", str(len(updates)), industry_by_id[selected_id].get("last_visit_date") or "No visits yet")
        with s4:
            kpi_card("Next Follow-up", next_fu, "Scheduled action")

        tab_ov, tab_mach, tab_con, tab_vis = st.tabs(
            [
                "Overview",
                f"Machines ({tot_m})",
                f"Contacts ({len(contacts)})",
                f"Visits ({len(updates)})",
            ]
        )

        with tab_ov:
            render_overview_tab(industry, machines, contacts, updates)
        with tab_mach:
            render_machines_tab(industry, machines)
        with tab_con:
            render_contacts_tab(industry, contacts)
        with tab_vis:
            render_visits_tab(industry, contacts, updates)
