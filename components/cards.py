"""Reusable cards for KPIs, factory list items, contacts, and visits."""

import html
import streamlit as st
from components.badges import status_badge


def kpi_card(label: str, value: str, sub: str = ""):
    sub_html = f'<div class="crm-kpi-sub">{html.escape(sub)}</div>' if sub else ""
    st.markdown(
        f'<div class="crm-kpi">'
        f'<div class="crm-kpi-label">{html.escape(label)}</div>'
        f'<div class="crm-kpi-value">{html.escape(str(value))}</div>'
        f"{sub_html}"
        f"</div>",
        unsafe_allow_html=True,
    )


def factory_list_item(ind: dict, is_selected: bool) -> bool:
    """Render a compact selectable factory card in the master list. Returns True if clicked."""
    cluster_txt = ind.get("cluster") or "—"
    mach_cnt = ind.get("machine_count", 0)
    op_cnt = ind.get("operating_machine_count", mach_cnt)
    mach_str = f"{mach_cnt} M" if mach_cnt == op_cnt else f"{op_cnt}/{mach_cnt} M"

    with st.container(border=True):
        c1, c2 = st.columns([3.2, 1.3])
        with c1:
            prefix = "▸ " if is_selected else ""
            st.markdown(f"**{prefix}{html.escape(ind['name'])}**")
            st.caption(f"{cluster_txt} • {mach_str} • {ind.get('contact_count', 0)} contacts")
        with c2:
            st.markdown(status_badge(ind.get("status", "New")), unsafe_allow_html=True)
            btn_type = "primary" if is_selected else "secondary"
            if st.button("Select", key=f"sel_fac_{ind['id']}", use_container_width=True, type=btn_type):
                return True
    return False


def contact_card(contact: dict, on_edit_key: str = "", show_factory: bool = False):
    """Render a contact card with click-to-call and mailto links."""
    with st.container(border=True):
        top1, top2 = st.columns([3, 1.2])
        with top1:
            st.markdown(f"**{html.escape(contact['name'])}**")
            desig = contact.get("designation") or "Designation not set"
            fac_part = f" • *{html.escape(contact.get('industry_name', ''))}*" if show_factory else ""
            st.caption(f"{desig}{fac_part}")
        with top2:
            st.markdown(status_badge(contact.get("status", "New")), unsafe_allow_html=True)
            if contact.get("butex_batch"):
                st.caption(f"BUTEX: **{html.escape(str(contact['butex_batch']))}**")

        ic1, ic2 = st.columns(2)
        with ic1:
            phone = (contact.get("phone") or "").strip()
            if phone:
                clean_tel = phone.replace(" ", "").replace("-", "")
                st.markdown(f"📞 [{html.escape(phone)}](tel:{html.escape(clean_tel)})")
            else:
                st.caption("No phone")
        with ic2:
            email = (contact.get("email") or "").strip()
            if email:
                st.markdown(f"✉️ [{html.escape(email)}](mailto:{html.escape(email)})")

        if contact.get("notes"):
            st.caption(contact["notes"])

        if on_edit_key:
            if st.button("Edit", key=on_edit_key, use_container_width=True):
                return True
    return False


def visit_card(upd: dict, on_edit_key: str = "", show_factory: bool = False):
    """Render a chronological visit log card."""
    with st.container(border=True):
        h1, h2 = st.columns([3.5, 1.2])
        with h1:
            fac_prefix = f"**{html.escape(upd.get('industry_name', ''))}** — " if show_factory else ""
            st.markdown(f"{fac_prefix}**{html.escape(str(upd['visit_date']))}** • `{html.escape(upd['visit_type'])}`")
            if upd.get("attendees"):
                st.caption(f"Attendees: {upd['attendees']}")
        with h2:
            if upd.get("next_followup_date"):
                st.caption(f"Follow-up: **{upd['next_followup_date']}**")
            if on_edit_key:
                if st.button("Edit", key=on_edit_key, use_container_width=True):
                    return True

        st.markdown(upd.get("meeting_minutes") or "")
        if upd.get("action_items"):
            st.markdown(f"**Action items:**\n{upd['action_items']}")
    return False
