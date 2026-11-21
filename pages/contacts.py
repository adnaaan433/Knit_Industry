"""Cross-factory contacts directory page."""

import pandas as pd
import streamlit as st
from components.cards import contact_card
from components.forms import open_contact_dialog
from config.constants import STATUS_OPTIONS
import db


@st.cache_data
def _load_contacts():
    return db.get_all_contacts()


all_contacts = _load_contacts()

st.title("Contacts Directory")
st.caption("Search and filter key contacts across all knitting factories.")

f1, f2, f3, f4, f5 = st.columns([2.2, 1.8, 1.4, 1.3, 1.1])
with f1:
    search_q = st.text_input("Search name, designation, phone, or factory", placeholder="Search contacts...")
with f2:
    factories = sorted(list({c["industry_name"] for c in all_contacts}))
    sel_factories = st.multiselect("Factory", options=factories)
with f3:
    sel_statuses = st.multiselect("Status", options=STATUS_OPTIONS)
with f4:
    batches = sorted(list({str(c["butex_batch"]) for c in all_contacts if (c.get("butex_batch") or "").strip()}))
    sel_batches = st.multiselect("BUTEX Batch", options=batches)
with f5:
    view_mode = st.radio("View", ["Cards", "Table"], horizontal=True)

filtered = []
for c in all_contacts:
    if search_q:
        q = search_q.lower()
        if (
            q not in (c.get("name") or "").lower()
            and q not in (c.get("designation") or "").lower()
            and q not in (c.get("phone") or "").lower()
            and q not in (c.get("industry_name") or "").lower()
        ):
            continue
    if sel_factories and c.get("industry_name") not in sel_factories:
        continue
    if sel_statuses and c.get("status") not in sel_statuses:
        continue
    if sel_batches and str(c.get("butex_batch") or "") not in sel_batches:
        continue
    filtered.append(c)

df_export = pd.DataFrame(
    [
        {
            "Name": c["name"],
            "Designation": c.get("designation") or "",
            "Factory": c["industry_name"],
            "Cluster": c.get("industry_cluster") or "",
            "Phone": c.get("phone") or "",
            "Email": c.get("email") or "",
            "BUTEX Batch": c.get("butex_batch") or "",
            "Status": c.get("status") or "",
            "Notes": c.get("notes") or "",
        }
        for c in filtered
    ]
)

top1, top2 = st.columns([4, 1.2])
with top1:
    st.caption(f"Showing **{len(filtered)}** of **{len(all_contacts)}** contacts")
with top2:
    st.download_button(
        "Download CSV",
        data=df_export.to_csv(index=False).encode("utf-8"),
        file_name="knit_crm_contacts.csv",
        mime="text/csv",
        use_container_width=True,
    )

if view_mode == "Table":
    st.dataframe(df_export, use_container_width=True, hide_index=True, height=560)
else:
    cols_per_row = 3
    for idx in range(0, len(filtered), cols_per_row):
        cols = st.columns(cols_per_row)
        for c_idx, c in enumerate(filtered[idx : idx + cols_per_row]):
            with cols[c_idx]:
                if contact_card(c, on_edit_key=f"all_ed_c_{c['id']}", show_factory=True):
                    open_contact_dialog(c["industry_id"], existing=c)
