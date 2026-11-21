"""Dashboard page: KPIs, follow-ups due, pipeline, cluster summary, and recent visits."""

from collections import defaultdict
from datetime import date, datetime, timedelta
import html
import streamlit as st
from components.badges import STATUS_COLORS, status_badge
from components.cards import kpi_card, visit_card
from config.constants import STATUS_OPTIONS
import db


@st.cache_data
def _load_dashboard_data():
    return db.get_all_industries(), db.get_all_updates()


industries, all_updates = _load_dashboard_data()

st.title("Dashboard")

total_fac = len(industries)
total_mach = sum(i["machine_count"] for i in industries)
oper_mach = sum(i["operating_machine_count"] for i in industries)
total_con = sum(i["contact_count"] for i in industries)
active_pipe = sum(
    1 for i in industries if i.get("status") in ("Contacted", "Scheduled", "Visited", "Follow-up", "Active Client")
)

k1, k2, k3, k4 = st.columns(4)
with k1:
    kpi_card("Factories", str(total_fac), f"{len({i['cluster'] for i in industries if i.get('cluster')})} clusters")
with k2:
    sub_m = f"{oper_mach:,} operating" if oper_mach != total_mach else "Across profiled plants"
    kpi_card("Machines Logged", f"{total_mach:,}", sub_m)
with k3:
    kpi_card("Contacts", str(total_con), "Verified decision makers")
with k4:
    kpi_card("Active Pipeline", str(active_pipe), "Contacted, Scheduled, Visited, Follow-up")

st.divider()

col_left, col_right = st.columns([1.35, 1])

with col_left:
    st.subheader("Follow-ups Due")
    today = date.today()
    horizon = today + timedelta(days=14)
    due_items = []
    for u in all_updates:
        f_str = (u.get("next_followup_date") or "").strip()
        if not f_str:
            continue
        try:
            f_date = datetime.strptime(f_str, "%Y-%m-%d").date()
        except ValueError:
            continue
        if f_date <= horizon:
            due_items.append((f_date, u))

    due_items.sort(key=lambda x: x[0])

    if not due_items:
        st.info("No follow-ups overdue or due in the next 14 days.")
    else:
        for f_date, u in due_items:
            is_overdue = f_date < today
            tag = "OVERDUE" if is_overdue else ("TODAY" if f_date == today else f"In {(f_date - today).days}d")
            with st.container(border=True):
                r1, r2 = st.columns([3.5, 1.3])
                with r1:
                    st.markdown(f"**{html.escape(u['industry_name'])}** — Due `{f_date}` (**{tag}**)")
                    if u.get("action_items"):
                        st.caption(u["action_items"])
                    else:
                        st.caption(u.get("meeting_minutes") or "")
                with r2:
                    if st.button("Open factory", key=f"dash_fu_{u['id']}", use_container_width=True):
                        st.query_params["factory"] = str(u["industry_id"])
                        st.switch_page("pages/factories.py")

    st.subheader("Recent Visits")
    if not all_updates:
        st.caption("No visit logs recorded yet.")
    else:
        for u in all_updates[:5]:
            visit_card(u, show_factory=True)

with col_right:
    st.subheader("Pipeline Status")
    st_counts = defaultdict(int)
    for i in industries:
        st_counts[i.get("status") or "New"] += 1

    segments = []
    for st_name in STATUS_OPTIONS:
        cnt = st_counts.get(st_name, 0)
        if cnt > 0 and total_fac > 0:
            pct = (cnt / total_fac) * 100
            color = STATUS_COLORS.get(st_name, STATUS_COLORS["New"])["hex"]
            segments.append(f'<div style="width:{pct:.1f}%;background:{color};" title="{st_name}: {cnt}"></div>')
    st.markdown(f'<div class="crm-pipeline-track">{"".join(segments)}</div>', unsafe_allow_html=True)

    with st.container(border=True):
        for st_name in STATUS_OPTIONS:
            cnt = st_counts.get(st_name, 0)
            c_a, c_b = st.columns([3, 1])
            with c_a:
                st.markdown(status_badge(st_name), unsafe_allow_html=True)
            with c_b:
                st.markdown(f"**{cnt}**")

    st.subheader("By Cluster")
    clusters = defaultdict(lambda: {"factories": 0, "machines": 0, "contacts": 0, "visited": 0})
    for i in industries:
        c = i.get("cluster") or "Unassigned"
        clusters[c]["factories"] += 1
        clusters[c]["machines"] += i["machine_count"]
        clusters[c]["contacts"] += i["contact_count"]
        if i.get("status") == "Visited":
            clusters[c]["visited"] += 1

    for c_name, stats in sorted(clusters.items(), key=lambda x: (-x[1]["factories"], x[0])):
        with st.container(border=True):
            r1, r2 = st.columns([2.8, 1.4])
            with r1:
                st.markdown(f"**{html.escape(c_name)}** ({stats['factories']} factories)")
                st.caption(
                    f"{stats['machines']:,} machines • {stats['contacts']} contacts • {stats['visited']} visited"
                )
            with r2:
                if st.button("View", key=f"dash_cl_{c_name}", use_container_width=True):
                    st.query_params["cluster"] = c_name
                    st.switch_page("pages/factories.py")
