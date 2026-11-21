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
    /* L'Esquire / Factory Custom Machine Profile Table */
    .mp-sheet-container {
        max-width: 760px;
        margin: 0.5rem 0 1.25rem 0;
        border: 1.5px solid #1e293b;
        background: #ffffff;
        color: #0f172a;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    table.mp-sheet-table {
        width: 100%;
        border-collapse: collapse;
        font-family: Calibri, "Segoe UI", Arial, sans-serif;
        font-size: 0.95rem;
        color: #0f172a;
        background: #ffffff;
    }
    table.mp-sheet-table th {
        background-color: #8ea9db;
        color: #0f172a;
        font-weight: 700;
        text-align: center;
        padding: 7px 12px;
        border: 1px solid #334155;
    }
    table.mp-sheet-table td {
        padding: 5px 12px;
        border: 1px solid #64748b;
        vertical-align: middle;
        color: #0f172a;
        background: #ffffff;
    }
    table.mp-sheet-table td.fab-col {
        text-align: center;
        font-weight: 500;
        background: #ffffff;
    }
    table.mp-sheet-table td.diagauge-col {
        text-align: left;
        background: #ffffff;
    }
    table.mp-sheet-table td.brand-col {
        text-align: left;
        background: #ffffff;
    }
    table.mp-sheet-table td.total-col {
        text-align: center;
        font-variant-numeric: tabular-nums;
        background: #ffffff;
    }
    table.mp-sheet-table tr.sheet-subtotal-row td {
        background-color: #8ea9db;
        color: #0f172a;
        font-weight: 700;
        padding: 6px 12px;
        border-top: 1.5px solid #1e293b;
        border-bottom: 1.5px solid #1e293b;
    }
    table.mp-sheet-table tr.sheet-grandtotal-row td {
        background-color: #ffffff;
        color: #0f172a;
        font-weight: 800;
        font-size: 1.05rem;
        padding: 8px 12px;
        border-top: 1.5px solid #1e293b;
        border-bottom: 2px solid #0f172a;
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


def render_machine_profile_html(industry: dict, machines: list) -> str:
    """Render the 4-column grouped Machine Profile table (Fabrication, Dia X Gauge, Brand, Total)."""
    fab_order = ["Fleece", "H/Jersey", "Single Jersey", "Rib", "Interlock"]
    grouped = defaultdict(list)
    for m in machines:
        grouped[m["fabrication"]].append(m)

    ordered_fabs = [f for f in fab_order if f in grouped] + [f for f in grouped if f not in fab_order]

    grand_machines = 0
    rows_html = []

    for fab in ordered_fabs:
        fab_items = grouped[fab]
        fab_rowspan = len(fab_items)

        # Merge consecutive identical Dia X Gauge cells within the same Fabrication
        diagauge_spans = [0] * len(fab_items)
        i = 0
        while i < len(fab_items):
            j = i + 1
            while j < len(fab_items) and fab_items[j]["dia_gauge_label"] == fab_items[i]["dia_gauge_label"]:
                j += 1
            diagauge_spans[i] = j - i
            i = j

        sub_machines = 0
        for idx, item in enumerate(fab_items):
            qty = int(item["quantity"] or 0)
            sub_machines += qty

            tr_parts = ["<tr>"]
            if idx == 0:
                tr_parts.append(f'<td class="fab-col" rowspan="{fab_rowspan}">{html.escape(fab)}</td>')
            if diagauge_spans[idx] > 0:
                tr_parts.append(
                    f'<td class="diagauge-col" rowspan="{diagauge_spans[idx]}">{html.escape(item["dia_gauge_label"])}</td>'
                )
            tr_parts.append(f'<td class="brand-col">{html.escape(item["brand"] or "—")}</td>')
            tr_parts.append(f'<td class="total-col">{qty}</td>')
            tr_parts.append("</tr>")
            rows_html.append("".join(tr_parts))

        grand_machines += sub_machines
        rows_html.append(
            f'<tr class="sheet-subtotal-row">'
            f'<td colspan="3" style="text-align:left;">{html.escape(fab)} Total</td>'
            f'<td class="total-col" style="background-color:#8ea9db;">{sub_machines}</td>'
            f"</tr>"
        )

    rows_html.append(
        f'<tr class="sheet-grandtotal-row">'
        f'<td colspan="3" style="text-align:center;">Grand Total</td>'
        f'<td class="total-col">{grand_machines}</td>'
        f"</tr>"
    )

    return (
        f'<div class="mp-sheet-container">'
        f'<table class="mp-sheet-table">'
        f"<thead><tr>"
        f'<th style="width:24%;">Fabrication</th>'
        f'<th style="width:28%;">Dia X Gauge</th>'
        f'<th style="width:32%;">Brand</th>'
        f'<th style="width:16%;">Total</th>'
        f"</tr></thead>"
        f'<tbody>{"".join(rows_html)}</tbody>'
        f"</table>"
        f"</div>"
    )


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

    with st.expander("💾 Sync Excel & Backup Database", expanded=False):
        if st.button("🔄 Sync from Excel File Now", use_container_width=True):
            db.sync_from_excel()
            st.success("Synced latest data from Knit Industry Contacts.xlsx!")
            st.rerun()
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
    # TAB 1: MACHINE PROFILE
    # --------------------------------------------------------------------------
    with tab_machines:
        st.subheader(f"⚙️ Machine Profile — {industry['name']}")

        if not machines:
            st.info(
                "No machine profile table has been added for this industry yet. "
                "Share the factory's machine profile photo or PDF in the chat to have its exact table format added here."
            )
        else:
            grand_m = sum(m["quantity"] for m in machines)
            unique_brands = len({m["brand"] for m in machines if m["brand"]})
            unique_fabs = len({m["fabrication"] for m in machines if m["fabrication"]})

            mk1, mk2, mk3 = st.columns(3)
            mk1.metric("Grand Total Machines", f"{grand_m:,}")
            mk2.metric("Fabrication Categories", unique_fabs)
            mk3.metric("Machine Brands", unique_brands)

            st.markdown(render_machine_profile_html(industry, machines), unsafe_allow_html=True)

            export_df = pd.DataFrame(
                [
                    {
                        "Fabrication": m["fabrication"],
                        "Dia X Gauge": m["dia_gauge_label"],
                        "Dia": int(m["dia"]) if float(m["dia"]).is_integer() else m["dia"],
                        "Gauge": int(m["gauge"]) if float(m["gauge"]).is_integer() else m["gauge"],
                        "Brand": m["brand"],
                        "Total": m["quantity"],
                    }
                    for m in machines
                ]
            )
            csv_bytes = export_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Machine Profile (CSV)",
                data=csv_bytes,
                file_name=f"{industry['name'].replace(' ', '_')}_Machine_Profile.csv",
                mime="text/csv",
            )

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
