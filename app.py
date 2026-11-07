import os
import streamlit as st
import pandas as pd
from datetime import date, datetime
from collections import defaultdict
import html
import database as db

st.set_page_config(
    page_title="Knit Industry CRM",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize SQLite DB and seed from Excel + L'Esquire example
db.init_db()

# Custom CSS for clean cards, status badges, and Excel-like Machine Profile Table
st.markdown(
    """
    <style>
    .status-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }
    .status-Visited { background-color: #d1fae5; color: #065f46; border: 1px solid #6ee7b7; }
    .status-Scheduled { background-color: #dbeafe; color: #1e40af; border: 1px solid #93c5fd; }
    .status-Contacted { background-color: #fef3c7; color: #92400e; border: 1px solid #fcd34d; }
    .status-Follow-up { background-color: #f3e8ff; color: #6b21a8; border: 1px solid #d8b4fe; }
    .status-Active { background-color: #dcfce7; color: #166534; border: 1px solid #4ade80; }
    .status-New { background-color: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; }
    .industry-header-box {
        padding: 1.2rem 1.5rem;
        border-radius: 10px;
        background: linear-gradient(135deg, rgba(30,64,175,0.06) 0%, rgba(15,23,42,0.03) 100%);
        border: 1px solid rgba(148, 163, 184, 0.25);
        margin-bottom: 1rem;
    }
    .minute-card {
        padding: 1.1rem 1.3rem;
        border-radius: 8px;
        border-left: 4px solid #2563eb;
        background-color: rgba(248, 250, 252, 0.7);
        border-top: 1px solid rgba(148, 163, 184, 0.2);
        border-right: 1px solid rgba(148, 163, 184, 0.2);
        border-bottom: 1px solid rgba(148, 163, 184, 0.2);
        margin-bottom: 0.8rem;
    }
    /* Modern Theme-Adaptive Machine Profile Tables */
    .mp-section-card {
        margin: 0.75rem 0 1.25rem 0;
        border-radius: 10px;
        border: 1px solid rgba(148, 163, 184, 0.22);
        background: rgba(30, 41, 59, 0.25);
        overflow: hidden;
    }
    .mp-section-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.5rem;
        padding: 10px 16px;
        background: rgba(51, 65, 85, 0.38);
        border-bottom: 1px solid rgba(148, 163, 184, 0.2);
    }
    .mp-fab-title {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.02rem;
        font-weight: 700;
    }
    .mp-fab-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        display: inline-block;
    }
    .mp-header-pills {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        font-size: 0.83rem;
    }
    .mp-stat-pill {
        padding: 3px 10px;
        border-radius: 999px;
        background: rgba(148, 163, 184, 0.14);
        border: 1px solid rgba(148, 163, 184, 0.22);
        font-variant-numeric: tabular-nums;
    }
    table.mp-modern-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.88rem;
    }
    table.mp-modern-table th {
        text-align: left;
        padding: 9px 14px;
        font-size: 0.76rem;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        opacity: 0.75;
        border-bottom: 1px solid rgba(148, 163, 184, 0.2);
        background: rgba(15, 23, 42, 0.18);
    }
    table.mp-modern-table th.r-align,
    table.mp-modern-table td.r-align {
        text-align: right;
        font-variant-numeric: tabular-nums;
    }
    table.mp-modern-table th.c-align,
    table.mp-modern-table td.c-align {
        text-align: center;
        font-variant-numeric: tabular-nums;
    }
    table.mp-modern-table td {
        padding: 8px 14px;
        border-bottom: 1px solid rgba(148, 163, 184, 0.12);
        vertical-align: middle;
    }
    table.mp-modern-table tbody tr:hover {
        background: rgba(59, 130, 246, 0.08);
    }
    .diagauge-badge {
        display: inline-block;
        padding: 2px 9px;
        border-radius: 6px;
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 0.84rem;
        font-weight: 600;
        background: rgba(59, 130, 246, 0.14);
        color: #60a5fa;
        border: 1px solid rgba(59, 130, 246, 0.28);
    }
    .qty-badge {
        display: inline-block;
        min-width: 30px;
        padding: 2px 8px;
        border-radius: 6px;
        font-weight: 700;
        background: rgba(148, 163, 184, 0.16);
    }
    table.mp-modern-table tr.mp-subtotal-tr td {
        background: rgba(51, 65, 85, 0.28);
        font-weight: 700;
        border-top: 1px solid rgba(148, 163, 184, 0.25);
        border-bottom: none;
        padding: 9px 14px;
    }
    .mp-grand-banner {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1rem;
        padding: 14px 20px;
        border-radius: 10px;
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.2) 0%, rgba(15, 23, 42, 0.4) 100%);
        border: 1px solid rgba(59, 130, 246, 0.4);
        margin: 0.5rem 0 1rem 0;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

STATUS_OPTIONS = ["New", "Contacted", "Scheduled", "Visited", "Follow-up", "Active Client"]
COMMON_BRANDS = [
    "Mayer & Cie",
    "Orizio",
    "Pai Long",
    "Fukuhara",
    "HaanTex",
    "Hangxing",
    "Santo",
    "Jung Long",
    "Terrot",
    "Jiunn Long",
    "Santoni",
    "Wellknit",
    "Other / Custom",
]


def status_badge_html(status: str) -> str:
    cls_key = status.split()[0] if status else "New"
    if cls_key not in ("Visited", "Scheduled", "Contacted", "Follow-up", "Active", "New"):
        cls_key = "New"
    return f'<span class="status-badge status-{cls_key}">{status}</span>'


FAB_COLORS = {
    "Single Jersey": "#3b82f6",
    "Fleece": "#10b981",
    "H/Jersey": "#f59e0b",
    "Rib": "#a855f7",
    "Interlock": "#ec4899",
}


def render_machine_profile_html(industry: dict, machines: list) -> str:
    """Render modern, theme-adaptive Fabrication section cards and tables with Needle & Sinker calculations."""
    fab_order = ["Fleece", "H/Jersey", "Single Jersey", "Rib", "Interlock"]
    grouped = defaultdict(list)
    for m in machines:
        grouped[m["fabrication"]].append(m)

    ordered_fabs = [f for f in fab_order if f in grouped] + [f for f in grouped if f not in fab_order]

    grand_machines = 0
    grand_needles = 0
    grand_sinkers = 0

    sections_html = []

    for fab in ordered_fabs:
        fab_items = grouped[fab]
        dot_color = FAB_COLORS.get(fab, "#64748b")

        sub_machines = sum(int(i["quantity"] or 0) for i in fab_items)
        sub_needles = sum(int(i["total_needles"] or 0) for i in fab_items)
        sub_sinkers = sum(int(i["total_sinkers"] or 0) for i in fab_items)

        grand_machines += sub_machines
        grand_needles += sub_needles
        grand_sinkers += sub_sinkers

        rows_html = []
        for item in fab_items:
            qty = int(item["quantity"] or 0)
            dia_val = int(item["dia"]) if float(item["dia"]).is_integer() else item["dia"]
            gauge_val = int(item["gauge"]) if float(item["gauge"]).is_integer() else item["gauge"]
            n_pm = int(item["needles_per_machine"] or 0)
            s_pm = int(item["sinkers_per_machine"] or 0)
            tot_n = int(item["total_needles"] or 0)
            tot_s = int(item["total_sinkers"] or 0)

            brand_str = f"<strong>{html.escape(item['brand'] or '—')}</strong>"
            if item.get("needle_spec") or item.get("sinker_spec") or item.get("remarks"):
                meta_bits = [b for b in [item.get("needle_spec"), item.get("sinker_spec"), item.get("remarks")] if b]
                brand_str += f' <span style="opacity:0.68;font-size:0.78rem;">({html.escape(", ".join(meta_bits))})</span>'

            s_pm_str = f"{s_pm:,}" if s_pm > 0 else '<span style="opacity:0.45;">—</span>'
            tot_s_str = f"{tot_s:,}" if tot_s > 0 else '<span style="opacity:0.45;">—</span>'

            rows_html.append(
                f"<tr>"
                f"<td>{brand_str}</td>"
                f'<td class="c-align"><span class="qty-badge">{qty}</span></td>'
                f'<td class="c-align"><span class="diagauge-badge">{dia_val}</span></td>'
                f'<td class="c-align"><span class="diagauge-badge">{gauge_val}</span></td>'
                f'<td class="r-align" style="opacity:0.85;">{n_pm:,}</td>'
                f'<td class="r-align" style="opacity:0.85;">{s_pm_str}</td>'
                f'<td class="r-align"><strong>{tot_n:,}</strong></td>'
                f'<td class="r-align"><strong>{tot_s_str}</strong></td>'
                f"</tr>"
            )

        sub_s_str = f"{sub_sinkers:,}" if sub_sinkers > 0 else "—"
        rows_html.append(
            f'<tr class="mp-subtotal-tr">'
            f"<td>{html.escape(fab)} Subtotal</td>"
            f'<td class="c-align">{sub_machines}</td>'
            f'<td class="c-align" style="opacity:0.5;">—</td>'
            f'<td class="c-align" style="opacity:0.5;">—</td>'
            f'<td class="r-align" style="opacity:0.5;">—</td>'
            f'<td class="r-align" style="opacity:0.5;">—</td>'
            f'<td class="r-align" style="color:#60a5fa;">{sub_needles:,}</td>'
            f'<td class="r-align" style="color:#34d399;">{sub_s_str}</td>'
            f"</tr>"
        )

        sections_html.append(
            f'<div class="mp-section-card">'
            f'<div class="mp-section-header">'
            f'<div class="mp-fab-title">'
            f'<span class="mp-fab-dot" style="background:{dot_color};"></span>'
            f"<span>{html.escape(fab)}</span>"
            f"</div>"
            f'<div class="mp-header-pills">'
            f'<span class="mp-stat-pill">⚙️ <strong>{sub_machines}</strong> Machines</span>'
            f'<span class="mp-stat-pill">🪡 <strong>{sub_needles:,}</strong> Needles</span>'
            f'<span class="mp-stat-pill">🔩 <strong>{sub_s_str}</strong> Sinkers</span>'
            f"</div>"
            f"</div>"
            f'<table class="mp-modern-table">'
            f"<thead><tr>"
            f'<th style="width:22%;">Brand</th>'
            f'<th class="c-align" style="width:12%;">Total Machine</th>'
            f'<th class="c-align" style="width:9%;">Dia</th>'
            f'<th class="c-align" style="width:9%;">Gauge</th>'
            f'<th class="r-align" style="width:12%;">Needles/M</th>'
            f'<th class="r-align" style="width:12%;">Sinkers/M</th>'
            f'<th class="r-align" style="width:12%;">Total Needles</th>'
            f'<th class="r-align" style="width:12%;">Total Sinkers</th>'
            f"</tr></thead>"
            f'<tbody>{"".join(rows_html)}</tbody>'
            f"</table>"
            f"</div>"
        )

    sections_html.append(
        f'<div class="mp-grand-banner">'
        f'<span style="font-size:1.05rem;">🏆 Grand Total Across All Fabrications</span>'
        f'<div class="mp-header-pills" style="font-size:0.92rem;">'
        f'<span class="mp-stat-pill">⚙️ <strong>{grand_machines:,}</strong> Total Machines</span>'
        f'<span class="mp-stat-pill">🪡 <strong>{grand_needles:,}</strong> Total Needles</span>'
        f'<span class="mp-stat-pill">🔩 <strong>{grand_sinkers:,}</strong> Total Sinkers</span>'
        f"</div>"
        f"</div>"
    )

    return "".join(sections_html)


# Session state navigation
if "current_view" not in st.session_state:
    st.session_state.current_view = "directory"
if "selected_industry_id" not in st.session_state:
    st.session_state.selected_industry_id = None
if "sidebar_industry_select" not in st.session_state:
    st.session_state.sidebar_industry_select = None


def navigate_to_industry(industry_id: int):
    st.session_state.selected_industry_id = industry_id
    st.session_state.current_view = "industry_page"
    st.session_state._sync_sidebar = True


def navigate_to_directory():
    st.session_state.current_view = "directory"
    st.session_state._sync_sidebar = True


# Load all industries for navigation & dashboard
all_industries = db.get_all_industries()
industry_map = {ind["id"]: ind for ind in all_industries}

# --- SIDEBAR ---
with st.sidebar:
    st.title("🏭 Knit Industry CRM")
    st.caption("Dedicated Factory Profiles, Machine Profiles, Contacts & Visit Logs")

    if st.button(
        "🏠 All Industries Directory",
        use_container_width=True,
        type="primary" if st.session_state.current_view == "directory" else "secondary",
    ):
        navigate_to_directory()
        st.rerun()

    st.divider()
    st.subheader("🔍 Jump to Industry Webpage")

    industry_options = {
        ind["id"]: f"{ind['name']} ({ind['machine_count']} M | {ind['status']})" for ind in all_industries
    }
    if st.session_state.get("_sync_sidebar"):
        st.session_state.sidebar_industry_select = (
            st.session_state.selected_industry_id
            if st.session_state.current_view == "industry_page"
            and st.session_state.selected_industry_id in industry_options
            else None
        )
        st.session_state._sync_sidebar = False

    selected_jump = st.selectbox(
        "Select an Industry",
        options=[None] + list(industry_options.keys()),
        format_func=lambda x: "— Choose an Industry —" if x is None else industry_options[x],
        key="sidebar_industry_select",
    )

    if selected_jump is not None and (
        selected_jump != st.session_state.selected_industry_id or st.session_state.current_view != "industry_page"
    ):
        navigate_to_industry(selected_jump)
        st.rerun()

    st.divider()
    with st.expander("➕ Add New Industry", expanded=False):
        with st.form("add_industry_sidebar_form", clear_on_submit=True):
            new_name = st.text_input("Factory / Industry Name *")
            new_cluster = st.text_input("Cluster (e.g., Gazipur, Savar, Bhaluka)")
            new_loc = st.text_input("Location Area")
            new_dist = st.number_input("Distance (km)", min_value=0.0, step=0.5, value=0.0)
            new_map = st.text_input("Google Maps Link")
            new_status = st.selectbox("Initial Status", STATUS_OPTIONS, index=0)
            submitted_new = st.form_submit_button("Create Industry Page", use_container_width=True)
            if submitted_new:
                if not new_name.strip():
                    st.error("Industry name is required.")
                else:
                    try:
                        created_id = db.create_industry(
                            name=new_name,
                            location_area=new_loc,
                            cluster=new_cluster,
                            distance_km=new_dist if new_dist > 0 else None,
                            map_url=new_map,
                            status=new_status,
                        )
                        st.success(f"Added {new_name}!")
                        navigate_to_industry(created_id)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Could not create industry: {e}")

    with st.expander("💾 Backup / Restore Database", expanded=False):
        st.caption("Download a backup of your CRM database (`crm_data.db`) or restore from a saved `.db` file.")
        if os.path.exists(db.DB_PATH):
            with open(db.DB_PATH, "rb") as f_db:
                st.download_button(
                    label="📥 Download Database (.db)",
                    data=f_db.read(),
                    file_name=f"crm_data_backup_{date.today()}.db",
                    mime="application/octet-stream",
                    use_container_width=True,
                )
        uploaded_db = st.file_uploader("Upload `.db` backup to restore", type=["db", "sqlite", "sqlite3"])
        if uploaded_db is not None:
            if st.button("🔄 Restore Uploaded Database", use_container_width=True):
                with open(db.DB_PATH, "wb") as out_db:
                    out_db.write(uploaded_db.getvalue())
                db.init_db()
                st.success("Database restored successfully!")
                st.rerun()


# ==============================================================================
# VIEW 1: ALL INDUSTRIES DIRECTORY (DASHBOARD)
# ==============================================================================
if st.session_state.current_view == "directory" or st.session_state.selected_industry_id not in industry_map:
    st.title("🏠 Knit Industry Directory & CRM Dashboard")
    st.markdown(
        "Select any factory below to open its **dedicated webpage** containing its **Machine Profile (with automatic Needle & Sinker calculations)**, **Contacts**, and **Visit Updates / Meeting Minutes**."
    )

    # KPI Row
    total_ind = len(all_industries)
    visited_cnt = sum(1 for i in all_industries if i["status"] == "Visited")
    scheduled_cnt = sum(1 for i in all_industries if i["status"] == "Scheduled")
    total_machines_all = sum(i["machine_count"] for i in all_industries)
    total_contacts = sum(i["contact_count"] for i in all_industries)
    total_updates = sum(i["update_count"] for i in all_industries)

    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("Total Factories", total_ind)
    k2.metric("Visited", visited_cnt)
    k3.metric("Scheduled", scheduled_cnt)
    k4.metric("Logged Machines", total_machines_all)
    k5.metric("Total Contacts", total_contacts)
    k6.metric("Visit Logs / Minutes", total_updates)

    st.divider()

    # Filters
    f_col1, f_col2, f_col3, f_col4 = st.columns([3, 2, 2, 1.5])
    with f_col1:
        search_q = st.text_input(
            "🔎 Search by Factory Name or Location",
            placeholder="e.g. L'Esquire, Fakir, MASCO, Square, Mawna...",
        )
    with f_col2:
        clusters = sorted(list({i["cluster"] for i in all_industries if i["cluster"]}))
        selected_clusters = st.multiselect("📍 Filter by Cluster", options=clusters)
    with f_col3:
        statuses = sorted(list({i["status"] for i in all_industries if i["status"]}))
        selected_statuses = st.multiselect("🏷️ Filter by Status", options=statuses)
    with f_col4:
        view_mode = st.radio("Layout", ["Cards", "Table"], horizontal=True)

    filtered_industries = []
    for ind in all_industries:
        if search_q:
            q = search_q.lower()
            if (
                q not in ind["name"].lower()
                and q not in (ind["location_area"] or "").lower()
                and q not in (ind["cluster"] or "").lower()
            ):
                continue
        if selected_clusters and ind["cluster"] not in selected_clusters:
            continue
        if selected_statuses and ind["status"] not in selected_statuses:
            continue
        filtered_industries.append(ind)

    st.caption(f"Showing **{len(filtered_industries)}** of **{total_ind}** industries")

    if view_mode == "Cards":
        cols_per_row = 3
        for idx in range(0, len(filtered_industries), cols_per_row):
            cols = st.columns(cols_per_row)
            for col_idx, ind in enumerate(filtered_industries[idx : idx + cols_per_row]):
                with cols[col_idx]:
                    with st.container(border=True):
                        top_c1, top_c2 = st.columns([3, 1.3])
                        with top_c1:
                            st.markdown(f"#### {ind['name']}")
                        with top_c2:
                            st.markdown(status_badge_html(ind["status"]), unsafe_allow_html=True)

                        loc_parts = [p for p in [ind["location_area"], ind["cluster"]] if p]
                        loc_str = ", ".join(loc_parts) if loc_parts else "Location not set"
                        dist_str = f" • {ind['distance_km']} km" if ind["distance_km"] else ""
                        st.caption(f"📍 {loc_str}{dist_str}")

                        m1, m2, m3 = st.columns(3)
                        m1.markdown(f"⚙️ **{ind['machine_count']}** Mach.")
                        m2.markdown(f"👥 **{ind['contact_count']}** Contacts")
                        m3.markdown(f"📝 **{ind['update_count']}** Visits")

                        if ind["last_visit_date"]:
                            st.caption(f"🕒 Last Visit: **{ind['last_visit_date']}**")
                        else:
                            st.caption("🕒 No visits logged yet")

                        btn_c1, btn_c2 = st.columns([2, 1])
                        with btn_c1:
                            if st.button(
                                "Open Webpage →",
                                key=f"open_ind_{ind['id']}",
                                use_container_width=True,
                                type="primary",
                            ):
                                navigate_to_industry(ind["id"])
                                st.rerun()
                        with btn_c2:
                            if ind["map_url"]:
                                st.link_button("🗺️ Map", ind["map_url"], use_container_width=True)
    else:
        df_rows = []
        for ind in filtered_industries:
            df_rows.append(
                {
                    "ID": ind["id"],
                    "Factory Name": ind["name"],
                    "Status": ind["status"],
                    "Cluster": ind["cluster"] or "—",
                    "Location Area": ind["location_area"] or "—",
                    "Distance (km)": ind["distance_km"] if ind["distance_km"] else None,
                    "Total Machines": ind["machine_count"],
                    "Contacts": ind["contact_count"],
                    "Updates / Visits": ind["update_count"],
                    "Last Visit": ind["last_visit_date"] or "—",
                    "Map URL": ind["map_url"] or None,
                }
            )
        df_display = pd.DataFrame(df_rows)
        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Map URL": st.column_config.LinkColumn("Google Map", display_text="View Map"),
            },
        )


# ==============================================================================
# VIEW 2: DEDICATED INDUSTRY WEBPAGE
# ==============================================================================
else:
    industry_id = st.session_state.selected_industry_id
    industry = db.get_industry(industry_id)
    contacts = db.get_contacts(industry_id)
    updates = db.get_updates(industry_id)
    machines = db.get_machines(industry_id)
    total_mach_units = sum(m["quantity"] or 0 for m in machines)

    # Top Breadcrumb
    nav_c1, _ = st.columns([1.5, 6])
    with nav_c1:
        if st.button("← Back to Directory", use_container_width=True):
            navigate_to_directory()
            st.rerun()

    # Dedicated Industry Header Box
    st.markdown('<div class="industry-header-box">', unsafe_allow_html=True)
    h_col1, h_col2 = st.columns([3.5, 1.5])
    with h_col1:
        st.markdown(f"# 🏭 {industry['name']}")
        loc_bits = [b for b in [industry["location_area"], industry["cluster"]] if b]
        loc_display = ", ".join(loc_bits) if loc_bits else "Location not specified"
        dist_display = f" • **{industry['distance_km']} km** from Dhaka" if industry["distance_km"] else ""
        st.markdown(f"📍 **Location:** {loc_display}{dist_display}")
        if industry["general_notes"]:
            st.info(f"📌 **Overview Notes:** {industry['general_notes']}")

    with h_col2:
        st.markdown("**Current CRM Status**")
        st.markdown(status_badge_html(industry["status"]), unsafe_allow_html=True)
        new_st = st.selectbox(
            "Update Status",
            options=STATUS_OPTIONS if industry["status"] in STATUS_OPTIONS else [industry["status"]] + STATUS_OPTIONS,
            index=(STATUS_OPTIONS.index(industry["status"]) if industry["status"] in STATUS_OPTIONS else 0),
            key=f"status_sel_{industry_id}",
            label_visibility="collapsed",
        )
        if new_st != industry["status"]:
            db.update_industry_status(industry_id, new_st)
            st.toast(f"Status updated to {new_st}!")
            st.rerun()

        if industry["map_url"]:
            st.link_button("🗺️ Open Location in Google Maps", industry["map_url"], use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Edit Industry Details Expander
    with st.expander("✏️ Edit Factory Details & Overview Notes"):
        with st.form(f"edit_industry_form_{industry_id}"):
            e_c1, e_c2 = st.columns(2)
            with e_c1:
                ed_name = st.text_input("Factory Name *", value=industry["name"])
                ed_cluster = st.text_input("Cluster", value=industry["cluster"] or "")
                ed_loc = st.text_input("Location Area", value=industry["location_area"] or "")
            with e_c2:
                ed_dist = st.number_input(
                    "Distance (km)",
                    min_value=0.0,
                    step=0.5,
                    value=float(industry["distance_km"]) if industry["distance_km"] else 0.0,
                )
                ed_map = st.text_input("Google Maps Link", value=industry["map_url"] or "")
                ed_status = st.selectbox(
                    "Status",
                    options=STATUS_OPTIONS,
                    index=STATUS_OPTIONS.index(industry["status"]) if industry["status"] in STATUS_OPTIONS else 0,
                )
            ed_notes = st.text_area("General Factory Overview / Notes", value=industry["general_notes"] or "")

            b_save, b_del = st.columns([4, 1])
            with b_save:
                if st.form_submit_button("💾 Save Industry Details", type="primary"):
                    db.update_industry(
                        industry_id=industry_id,
                        name=ed_name,
                        location_area=ed_loc,
                        cluster=ed_cluster,
                        distance_km=ed_dist if ed_dist > 0 else None,
                        map_url=ed_map,
                        status=ed_status,
                        general_notes=ed_notes,
                    )
                    st.success("Industry details updated!")
                    st.rerun()
            with b_del:
                if st.form_submit_button("🗑️ Delete Industry"):
                    db.delete_industry(industry_id)
                    navigate_to_directory()
                    st.rerun()

    # Main 3 Sections on Dedicated Industry Webpage
    tab_machines, tab_contacts, tab_updates = st.tabs(
        [
            f"⚙️ Machine Profile ({total_mach_units} Machines)",
            f"👥 Contacts ({len(contacts)})",
            f"📝 Updates & Meeting Minutes ({len(updates)})",
        ]
    )

    # --------------------------------------------------------------------------
    # TAB 1: MACHINE PROFILE & NEEDLE/SINKER CALCULATOR
    # --------------------------------------------------------------------------
    with tab_machines:
        st.subheader(f"⚙️ Machine Profile & Needle/Sinker Requirements — {industry['name']}")

        with st.expander("ℹ️ Needle & Sinker Calculation Formula Reference", expanded=False):
            st.markdown(
                """
                - **Single Jersey, Fleece, H/Jersey**:
                  - **Needles per Machine** = `int(Dia × Gauge × 3.1416)`
                  - **Sinkers per Machine** = `int(Dia × Gauge × 3.1416)`
                - **Rib, Interlock**:
                  - **Needles per Machine** = `int(2 × Dia × Gauge × 3.1416)` *(Cylinder + Dial)*
                  - **Sinkers per Machine** = `0` *(Double-jersey machines)*
                - **Total Needles / Sinkers for Row** = `Per-Machine Requirement × Total Machines`
                """
            )

        # Add Machine Row Form with Live Formula Preview
        with st.container(border=True):
            st.markdown("#### ➕ Add Machine to Profile")
            fc1, fc2, fc3, fc4, fc5 = st.columns([1.5, 1.6, 1.1, 1, 1])
            with fc1:
                in_fab = st.selectbox("Fabrication *", options=db.FABRICATION_TYPES, key=f"mp_fab_{industry_id}")
            with fc2:
                in_brand_choice = st.selectbox("Brand *", options=COMMON_BRANDS, key=f"mp_brand_sel_{industry_id}")
            with fc3:
                in_qty = st.number_input("Total Machine *", min_value=1, max_value=500, value=1, step=1, key=f"mp_qty_{industry_id}")
            with fc4:
                in_dia = st.number_input("Dia *", min_value=1, max_value=100, value=30, step=1, key=f"mp_dia_{industry_id}")
            with fc5:
                in_gauge = st.number_input("Gauge *", min_value=1, max_value=60, value=24, step=1, key=f"mp_gg_{industry_id}")

            opt_c1, opt_c2, opt_c3, opt_c4 = st.columns([1.5, 1.5, 1.5, 1.5])
            with opt_c1:
                if in_brand_choice == "Other / Custom":
                    final_brand = st.text_input("Enter Custom Brand Name *", key=f"mp_custom_brand_{industry_id}")
                else:
                    final_brand = in_brand_choice
                    st.text_input("Selected Brand", value=final_brand, disabled=True, key=f"mp_brand_disp_{industry_id}")
            with opt_c2:
                in_needle_spec = st.text_input("Needle Spec / Part No. (Optional)", placeholder="e.g. Voelker / GB", key=f"mp_nspec_{industry_id}")
            with opt_c3:
                in_sinker_spec = st.text_input("Sinker Spec / Part No. (Optional)", placeholder="e.g. Kern-Liebers", key=f"mp_sspec_{industry_id}")
            with opt_c4:
                in_remarks = st.text_input("Remarks (Optional)", key=f"mp_rem_{industry_id}")

            # Live Preview of Formula Output
            live_calc = db.calculate_needle_sinker(in_fab, in_dia, in_gauge, in_qty)
            live_label = db.format_dia_gauge(in_dia, in_gauge)

            prev_col, btn_col = st.columns([4, 1.4])
            with prev_col:
                sinker_preview = (
                    f"**{live_calc['sinkers_per_machine']:,}** / machine (**{live_calc['total_sinkers']:,}** total)"
                    if live_calc["sinkers_per_machine"] > 0
                    else "**N/A (0)** for Rib/Interlock"
                )
                st.info(
                    f"🧮 **Auto-Calculation ({in_fab} • {final_brand or 'Brand'} • {in_qty} M • Dia {in_dia} • Gauge {in_gauge}):**  "
                    f"Needles = **{live_calc['needles_per_machine']:,}** / M (**{live_calc['total_needles']:,}** total)  |  "
                    f"Sinkers = {sinker_preview}"
                )
            with btn_col:
                if st.button("➕ Add Machine Row", type="primary", use_container_width=True, key=f"btn_add_mp_{industry_id}"):
                    if not final_brand or not final_brand.strip():
                        st.error("Please provide a Brand name.")
                    else:
                        db.add_machine(
                            industry_id=industry_id,
                            fabrication=in_fab,
                            dia=in_dia,
                            gauge=in_gauge,
                            dia_gauge_label=live_label,
                            brand=final_brand,
                            quantity=in_qty,
                            needle_spec=in_needle_spec,
                            sinker_spec=in_sinker_spec,
                            remarks=in_remarks,
                        )
                        st.toast(f"Added {in_qty}x {final_brand} (Dia {in_dia}, Gauge {in_gauge}) to {industry['name']}!")
                        st.rerun()

        if not machines:
            st.info("No machines added to this factory's profile yet. Use the form above to add machines.")
        else:
            # Summary KPIs for this Factory's Machine Profile
            grand_m = sum(m["quantity"] for m in machines)
            grand_n = sum(m["total_needles"] for m in machines)
            grand_s = sum(m["total_sinkers"] for m in machines)
            unique_brands = len({m["brand"] for m in machines if m["brand"]})

            mk1, mk2, mk3, mk4 = st.columns(4)
            mk1.metric("Grand Total Machines", f"{grand_m:,}")
            mk2.metric("Total Needles Required", f"{grand_n:,}")
            mk3.metric("Total Sinkers Required", f"{grand_s:,}")
            mk4.metric("Machine Brands", unique_brands)

            # Sub-tabs inside Machine Profile: Formatted Report View, Brand/Dia Breakdown, Edit/Delete Rows
            mp_view_tab1, mp_view_tab2, mp_view_tab3 = st.tabs(
                [
                    "📊 Formatted Machine Profile Sheet",
                    "📈 Breakdown by Fabrication & Brand",
                    "✏️ Edit / Delete Machine Rows",
                ]
            )

            with mp_view_tab1:
                st.markdown(render_machine_profile_html(industry, machines), unsafe_allow_html=True)

                # CSV Export
                export_df = pd.DataFrame(
                    [
                        {
                            "Fabrication": m["fabrication"],
                            "Brand": m["brand"],
                            "Total Machine": m["quantity"],
                            "Dia": int(m["dia"]) if float(m["dia"]).is_integer() else m["dia"],
                            "Gauge": int(m["gauge"]) if float(m["gauge"]).is_integer() else m["gauge"],
                            "Needles/M": m["needles_per_machine"],
                            "Sinkers/M": m["sinkers_per_machine"],
                            "Total Needles": m["total_needles"],
                            "Total Sinkers": m["total_sinkers"],
                            "Needle Spec": m["needle_spec"],
                            "Sinker Spec": m["sinker_spec"],
                            "Remarks": m["remarks"],
                        }
                        for m in machines
                    ]
                )
                csv_bytes = export_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 Download Machine Profile & Needle/Sinker Sheet (CSV)",
                    data=csv_bytes,
                    file_name=f"{industry['name'].replace(' ', '_')}_Machine_Profile.csv",
                    mime="text/csv",
                )

            with mp_view_tab2:
                b_col1, b_col2 = st.columns(2)
                with b_col1:
                    st.markdown("#### Summary by Fabrication")
                    fab_summary = defaultdict(lambda: {"Machines": 0, "Total Needles": 0, "Total Sinkers": 0})
                    for m in machines:
                        f = m["fabrication"]
                        fab_summary[f]["Machines"] += m["quantity"]
                        fab_summary[f]["Total Needles"] += m["total_needles"]
                        fab_summary[f]["Total Sinkers"] += m["total_sinkers"]
                    df_fab = pd.DataFrame(
                        [
                            {
                                "Fabrication": k,
                                "Total Machines": v["Machines"],
                                "Total Needles": v["Total Needles"],
                                "Total Sinkers": v["Total Sinkers"],
                            }
                            for k, v in fab_summary.items()
                        ]
                    )
                    st.dataframe(df_fab, use_container_width=True, hide_index=True)

                with b_col2:
                    st.markdown("#### Summary by Machine Brand")
                    brand_summary = defaultdict(lambda: {"Machines": 0, "Total Needles": 0, "Total Sinkers": 0})
                    for m in machines:
                        b = m["brand"] or "Unspecified"
                        brand_summary[b]["Machines"] += m["quantity"]
                        brand_summary[b]["Total Needles"] += m["total_needles"]
                        brand_summary[b]["Total Sinkers"] += m["total_sinkers"]
                    df_brand = pd.DataFrame(
                        [
                            {
                                "Brand": k,
                                "Total Machines": v["Machines"],
                                "Total Needles": v["Total Needles"],
                                "Total Sinkers": v["Total Sinkers"],
                            }
                            for k, v in sorted(brand_summary.items(), key=lambda x: -x[1]["Machines"])
                        ]
                    )
                    st.dataframe(df_brand, use_container_width=True, hide_index=True)

            with mp_view_tab3:
                st.caption("Edit or remove individual machine rows below. Any change to Fabrication, Brand, Total Machine, Dia, or Gauge automatically updates the Needle and Sinker counts.")
                for m in machines:
                    d_disp = int(m["dia"]) if float(m["dia"]).is_integer() else m["dia"]
                    g_disp = int(m["gauge"]) if float(m["gauge"]).is_integer() else m["gauge"]
                    with st.expander(
                        f"{m['fabrication']} | {m['brand']} | Total Machine: {m['quantity']} | Dia: {d_disp} | Gauge: {g_disp} "
                        f"(Needles/M: {m['needles_per_machine']:,}, Sinkers/M: {m['sinkers_per_machine']:,})"
                    ):
                        with st.form(f"edit_mach_row_{m['id']}"):
                            em1, em2, em3, em4, em5 = st.columns([1.4, 1.5, 1.1, 1, 1])
                            with em1:
                                e_fab_opts = (
                                    db.FABRICATION_TYPES
                                    if m["fabrication"] in db.FABRICATION_TYPES
                                    else [m["fabrication"]] + db.FABRICATION_TYPES
                                )
                                e_fab = st.selectbox("Fabrication", options=e_fab_opts, index=e_fab_opts.index(m["fabrication"]))
                            with em2:
                                e_brand = st.text_input("Brand", value=m["brand"])
                            with em3:
                                e_qty = st.number_input("Total Machine", min_value=1, max_value=500, value=int(m["quantity"]), step=1)
                            with em4:
                                e_dia = st.number_input("Dia", min_value=1.0, max_value=100.0, value=float(m["dia"]), step=1.0)
                            with em5:
                                e_gg = st.number_input("Gauge", min_value=1.0, max_value=60.0, value=float(m["gauge"]), step=1.0)

                            em7, em8, em9 = st.columns([1.3, 1.3, 1.4])
                            with em7:
                                e_nspec = st.text_input("Needle Spec", value=m["needle_spec"] or "")
                            with em8:
                                e_sspec = st.text_input("Sinker Spec", value=m["sinker_spec"] or "")
                            with em9:
                                e_rem = st.text_input("Remarks", value=m["remarks"] or "")

                            b_col_save, b_col_del = st.columns([3, 1])
                            with b_col_save:
                                if st.form_submit_button("💾 Update Row", use_container_width=True, type="primary"):
                                    final_lbl = db.format_dia_gauge(e_dia, e_gg)
                                    db.update_machine(
                                        machine_id=m["id"],
                                        fabrication=e_fab,
                                        dia=e_dia,
                                        gauge=e_gg,
                                        dia_gauge_label=final_lbl,
                                        brand=e_brand,
                                        quantity=e_qty,
                                        needle_spec=e_nspec,
                                        sinker_spec=e_sspec,
                                        remarks=e_rem,
                                    )
                                    st.rerun()
                            with b_col_del:
                                if st.form_submit_button("🗑️ Delete Row", use_container_width=True):
                                    db.delete_machine(m["id"])
                                    st.rerun()

        st.divider()
        with st.expander("📋 General Machine Floor Notes", expanded=bool(industry["machine_profile_notes"])):
            with st.form(f"machine_notes_form_{industry_id}"):
                mp_notes = st.text_area(
                    "Additional Notes on Factory Machines / Spare Parts / Oil / Maintenance",
                    value=industry["machine_profile_notes"] or "",
                    height=100,
                )
                if st.form_submit_button("💾 Save Notes"):
                    db.update_machine_notes(industry_id, mp_notes)
                    st.success("Notes saved!")
                    st.rerun()

    # --------------------------------------------------------------------------
    # TAB 2: CONTACTS
    # --------------------------------------------------------------------------
    with tab_contacts:
        st.subheader(f"Key Contacts at {industry['name']}")

        with st.expander("➕ Add New Contact Person", expanded=(len(contacts) == 0)):
            with st.form(f"add_contact_form_{industry_id}", clear_on_submit=True):
                ac1, ac2, ac3 = st.columns(3)
                with ac1:
                    c_name = st.text_input("Contact Person Name *")
                    c_desig = st.text_input("Designation (e.g., AGM, Knitting)")
                with ac2:
                    c_phone = st.text_input("Contact Number (e.g., +880 17...)")
                    c_email = st.text_input("Email Address (Optional)")
                with ac3:
                    c_batch = st.text_input("BUTEX Batch (Optional)")
                    c_status = st.selectbox("Contact Status", STATUS_OPTIONS, index=0)
                c_notes = st.text_input("Additional Notes (Optional)")

                if st.form_submit_button("➕ Save Contact", type="primary"):
                    if not c_name.strip():
                        st.error("Please enter the Contact Person's name.")
                    else:
                        db.add_contact(
                            industry_id=industry_id,
                            name=c_name,
                            designation=c_desig,
                            phone=c_phone,
                            email=c_email,
                            butex_batch=c_batch,
                            status=c_status,
                            notes=c_notes,
                        )
                        st.success(f"Added {c_name} to {industry['name']}!")
                        st.rerun()

        if not contacts:
            st.info("No contacts recorded for this factory yet. Use the form above to add the first contact.")
        else:
            c_cols_per_row = 2
            for idx in range(0, len(contacts), c_cols_per_row):
                row_cols = st.columns(c_cols_per_row)
                for c_idx, contact in enumerate(contacts[idx : idx + c_cols_per_row]):
                    with row_cols[c_idx]:
                        with st.container(border=True):
                            ch1, ch2 = st.columns([3, 1.2])
                            with ch1:
                                st.markdown(f"#### 👤 {contact['name']}")
                                st.markdown(f"**{contact['designation'] or 'Designation not specified'}**")
                            with ch2:
                                st.markdown(status_badge_html(contact["status"]), unsafe_allow_html=True)
                                if contact["butex_batch"]:
                                    st.caption(f"🎓 **BUTEX Batch:** {contact['butex_batch']}")

                            info_col1, info_col2 = st.columns(2)
                            with info_col1:
                                if contact["phone"]:
                                    clean_tel = contact["phone"].replace(" ", "").replace("-", "")
                                    st.markdown(f"📞 [{contact['phone']}](tel:{clean_tel})")
                                else:
                                    st.caption("📞 No phone number")
                            with info_col2:
                                if contact["email"]:
                                    st.markdown(f"✉️ [{contact['email']}](mailto:{contact['email']})")

                            if contact["notes"]:
                                st.caption(f"📝 {contact['notes']}")

                            with st.expander("✏️ Edit / Delete Contact"):
                                with st.form(f"edit_contact_{contact['id']}"):
                                    ec1, ec2 = st.columns(2)
                                    with ec1:
                                        u_name = st.text_input("Name", value=contact["name"])
                                        u_desig = st.text_input("Designation", value=contact["designation"] or "")
                                        u_phone = st.text_input("Phone", value=contact["phone"] or "")
                                    with ec2:
                                        u_email = st.text_input("Email", value=contact["email"] or "")
                                        u_batch = st.text_input("BUTEX Batch", value=contact["butex_batch"] or "")
                                        u_st = st.selectbox(
                                            "Status",
                                            options=STATUS_OPTIONS,
                                            index=(
                                                STATUS_OPTIONS.index(contact["status"])
                                                if contact["status"] in STATUS_OPTIONS
                                                else 0
                                            ),
                                        )
                                    u_notes = st.text_input("Notes", value=contact["notes"] or "")
                                    eb1, eb2 = st.columns(2)
                                    with eb1:
                                        if st.form_submit_button("💾 Update", use_container_width=True):
                                            db.update_contact(
                                                contact["id"],
                                                u_name,
                                                u_desig,
                                                u_phone,
                                                u_email,
                                                u_batch,
                                                u_st,
                                                u_notes,
                                            )
                                            st.rerun()
                                    with eb2:
                                        if st.form_submit_button("🗑️ Delete", use_container_width=True):
                                            db.delete_contact(contact["id"])
                                            st.rerun()

    # --------------------------------------------------------------------------
    # TAB 3: UPDATES & VISIT LOGS (MEETING MINUTES)
    # --------------------------------------------------------------------------
    with tab_updates:
        st.subheader(f"📝 Factory Visits, Meeting Minutes & Updates — {industry['name']}")

        with st.expander("➕ Log New Visit / Meeting Minutes", expanded=(len(updates) == 0)):
            with st.form(f"add_update_form_{industry_id}", clear_on_submit=True):
                u_col1, u_col2, u_col3 = st.columns(3)
                with u_col1:
                    v_date = st.date_input("Visit / Meeting Date *", value=date.today())
                with u_col2:
                    v_type = st.selectbox(
                        "Interaction Type",
                        [
                            "Factory Visit",
                            "Phone / WhatsApp Follow-up",
                            "Sample / Technical Trial",
                            "Commercial / Price Discussion",
                            "General Update",
                        ],
                    )
                with u_col3:
                    v_followup = st.date_input("Next Follow-up Date (Optional)", value=None)

                contact_names_list = [
                    f"{c['name']} ({c['designation']})" if c["designation"] else c["name"] for c in contacts
                ]
                selected_attendees = st.multiselect(
                    "Contacts Met / Present (Select from factory contacts)",
                    options=contact_names_list,
                )
                extra_attendees = st.text_input("Other Attendees (if any, comma-separated)")

                v_minutes = st.text_area(
                    "Meeting Minutes & Updated Factory Details *",
                    height=160,
                    placeholder="Write detailed meeting minutes, factory floor observations, current needle/sinker requirements, pricing discussions, or updated details from this visit...",
                )
                v_actions = st.text_area(
                    "Action Items / Next Steps (Optional)",
                    height=80,
                    placeholder="e.g., 1. Send quotation for 24G Mayer & Cie needles\n2. Arrange sample trial next week",
                )
                auto_mark_visited = st.checkbox("Mark factory status as 'Visited'", value=(v_type == "Factory Visit"))

                if st.form_submit_button("💾 Save Visit & Meeting Minutes", type="primary"):
                    if not v_minutes.strip():
                        st.error("Please enter the Meeting Minutes / Update details.")
                    else:
                        all_att = list(selected_attendees)
                        if extra_attendees.strip():
                            all_att.append(extra_attendees.strip())
                        attendees_str = ", ".join(all_att)

                        db.add_update(
                            industry_id=industry_id,
                            visit_date=v_date,
                            visit_type=v_type,
                            attendees=attendees_str,
                            meeting_minutes=v_minutes,
                            action_items=v_actions,
                            next_followup_date=v_followup if v_followup else "",
                        )
                        if auto_mark_visited and industry["status"] != "Visited":
                            db.update_industry_status(industry_id, "Visited")
                        st.success("Visit update and meeting minutes saved!")
                        st.rerun()

        st.divider()

        if not updates:
            st.info(
                "No factory visits or meeting minutes recorded yet for this industry. Use the form above to log your first visit!"
            )
        else:
            st.markdown(f"### 📅 Chronological Visit History ({len(updates)})")
            for upd in updates:
                st.markdown(
                    f'<div class="minute-card">'
                    f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">'
                    f'<span style="font-size:1.08rem; font-weight:700; color:#1e3a8a;">🗓️ {html.escape(str(upd["visit_date"]))} — {html.escape(str(upd["visit_type"]))}</span>'
                    f'<span style="font-size:0.8rem; color:#64748b;">Logged: {html.escape(str(upd["created_at"]))}</span>'
                    f'</div></div>',
                    unsafe_allow_html=True,
                )
                with st.container(border=True):
                    if upd["attendees"]:
                        st.markdown(f"**👥 Attendees / Met With:** {upd['attendees']}")

                    st.markdown("**📝 Meeting Minutes & Visit Details:**")
                    st.markdown(upd["meeting_minutes"])

                    if upd["action_items"]:
                        st.warning(f"**🎯 Action Items / Next Steps:**\n\n{upd['action_items']}")

                    if upd["next_followup_date"]:
                        st.info(f"🔔 **Next Scheduled Follow-up:** `{upd['next_followup_date']}`")

                    with st.expander("✏️ Edit / Delete This Visit Record"):
                        with st.form(f"edit_upd_form_{upd['id']}"):
                            eu1, eu2, eu3 = st.columns(3)
                            with eu1:
                                try:
                                    parsed_vdate = datetime.strptime(upd["visit_date"], "%Y-%m-%d").date()
                                except Exception:
                                    parsed_vdate = date.today()
                                e_vdate = st.date_input("Visit Date", value=parsed_vdate, key=f"evd_{upd['id']}")
                            with eu2:
                                v_types = [
                                    "Factory Visit",
                                    "Phone / WhatsApp Follow-up",
                                    "Sample / Technical Trial",
                                    "Commercial / Price Discussion",
                                    "General Update",
                                ]
                                e_vtype = st.selectbox(
                                    "Interaction Type",
                                    options=v_types,
                                    index=v_types.index(upd["visit_type"]) if upd["visit_type"] in v_types else 0,
                                    key=f"evt_{upd['id']}",
                                )
                            with eu3:
                                parsed_fdate = None
                                if upd["next_followup_date"]:
                                    try:
                                        parsed_fdate = datetime.strptime(upd["next_followup_date"], "%Y-%m-%d").date()
                                    except Exception:
                                        parsed_fdate = None
                                e_fdate = st.date_input("Next Follow-up Date", value=parsed_fdate, key=f"efd_{upd['id']}")

                            e_att = st.text_input("Attendees", value=upd["attendees"] or "", key=f"eat_{upd['id']}")
                            e_min = st.text_area(
                                "Meeting Minutes",
                                value=upd["meeting_minutes"] or "",
                                height=140,
                                key=f"emin_{upd['id']}",
                            )
                            e_act = st.text_area(
                                "Action Items",
                                value=upd["action_items"] or "",
                                height=80,
                                key=f"eact_{upd['id']}",
                            )

                            ub1, ub2 = st.columns(2)
                            with ub1:
                                if st.form_submit_button("💾 Save Changes", use_container_width=True):
                                    db.edit_update(
                                        update_id=upd["id"],
                                        visit_date=e_vdate,
                                        visit_type=e_vtype,
                                        attendees=e_att,
                                        meeting_minutes=e_min,
                                        action_items=e_act,
                                        next_followup_date=e_fdate if e_fdate else "",
                                    )
                                    st.rerun()
                            with ub2:
                                if st.form_submit_button("🗑️ Delete Visit Log", use_container_width=True):
                                    db.delete_update(upd["id"])
                                    st.rerun()
