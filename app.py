"""Knit Industry CRM — Entry point."""

from datetime import date
import os
import streamlit as st
from components.forms import open_add_factory_dialog
import db

st.set_page_config(page_title="Knit Industry CRM", page_icon="🏭", layout="wide")
db.init_db()

css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "theme", "styles.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f_css:
        st.markdown(f"<style>{f_css.read()}</style>", unsafe_allow_html=True)

pg = st.navigation([
    st.Page("pages/dashboard.py", title="Dashboard", icon="📊", default=True),
    st.Page("pages/factories.py", title="Factories", icon="🏭"),
    st.Page("pages/machines.py", title="Machines", icon="⚙️"),
    st.Page("pages/contacts.py", title="Contacts", icon="👥"),
    st.Page("pages/visits.py", title="Visits", icon="📝"),
])

with st.sidebar:
    if st.button("+ Add Factory", use_container_width=True, type="primary"):
        open_add_factory_dialog()
    with st.expander("Data", expanded=False):
        if st.button("Sync from Excel", use_container_width=True):
            db.sync_from_excel()
            st.cache_data.clear()
            st.success("Synced with Excel.")
            st.rerun()
        if os.path.exists(db.DB_PATH):
            with open(db.DB_PATH, "rb") as f_db:
                st.download_button(
                    "Download backup (.db)",
                    data=f_db.read(),
                    file_name=f"crm_data_backup_{date.today()}.db",
                    mime="application/octet-stream",
                    use_container_width=True,
                )
        uploaded_db = st.file_uploader("Restore backup (.db)", type=["db", "sqlite", "sqlite3"])
        if uploaded_db is not None and st.button("Restore backup", use_container_width=True):
            with open(db.DB_PATH, "wb") as out_db:
                out_db.write(uploaded_db.getvalue())
            db.init_db()
            st.cache_data.clear()
            st.success("Database restored.")
            st.rerun()

pg.run()
