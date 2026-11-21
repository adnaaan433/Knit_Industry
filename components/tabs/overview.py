"""Overview tab for a selected factory."""

import streamlit as st
import db


def render_overview_tab(industry: dict, machines: list, contacts: list, updates: list):
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### General Notes")
        with st.form(f"ov_gen_notes_{industry['id']}"):
            g_notes = st.text_area(
                "Factory Overview Notes",
                value=industry.get("general_notes") or "",
                height=110,
                label_visibility="collapsed",
                placeholder="Add general notes about this factory...",
            )
            if st.form_submit_button("Save General Notes"):
                db.update_industry(
                    industry["id"],
                    industry["name"],
                    industry.get("location_area") or "",
                    industry.get("cluster") or "",
                    industry.get("distance_km"),
                    industry.get("map_url") or "",
                    industry.get("status") or "New",
                    g_notes,
                )
                st.cache_data.clear()
                st.success("General notes saved.")
                st.rerun()

    with c2:
        st.markdown("#### Machine Floor Notes")
        with st.form(f"ov_mach_notes_{industry['id']}"):
            m_notes = st.text_area(
                "Machine Floor Notes",
                value=industry.get("machine_profile_notes") or "",
                height=110,
                label_visibility="collapsed",
                placeholder="Spare parts, needle brands, oil, maintenance observations...",
            )
            if st.form_submit_button("Save Machine Notes"):
                db.update_machine_notes(industry["id"], m_notes)
                st.cache_data.clear()
                st.success("Machine floor notes saved.")
                st.rerun()

    st.divider()
    b1, b2 = st.columns(2)
    with b1:
        st.markdown("#### Latest Visit Summary")
        if updates:
            latest = updates[0]
            with st.container(border=True):
                st.markdown(f"**{latest['visit_date']}** • `{latest['visit_type']}`")
                if latest.get("attendees"):
                    st.caption(f"Attendees: {latest['attendees']}")
                st.markdown(latest.get("meeting_minutes") or "")
                if latest.get("action_items"):
                    st.markdown(f"**Action items:** {latest['action_items']}")
        else:
            st.caption("No visits logged yet.")

    with b2:
        st.markdown("#### Next Follow-up")
        followups = [u for u in updates if (u.get("next_followup_date") or "").strip()]
        if followups:
            followups.sort(key=lambda x: x["next_followup_date"])
            nxt = followups[0]
            with st.container(border=True):
                st.markdown(f"📅 **Due Date:** `{nxt['next_followup_date']}`")
                st.caption(f"From {nxt['visit_type']} on {nxt['visit_date']}")
                if nxt.get("action_items"):
                    st.markdown(f"**Action items:**\n{nxt['action_items']}")
        else:
            st.caption("No upcoming follow-up date scheduled.")
