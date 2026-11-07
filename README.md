# 🏭 Knit Industry CRM

A Streamlit CRM web application built for managing knitting factories, machine profiles, automatic needle & sinker calculations, contacts, and factory visit meeting minutes.

## Features
- **All Industries Directory & Dashboard**: Search and filter factories by name, cluster, and visit status.
- **Dedicated Factory Webpages**:
  - **⚙️ Machine Profile & Needle/Sinker Calculator**:
    - Tracks machines by `Fabrication` (`Single Jersey`, `Fleece`, `H/Jersey`, `Rib`, `Interlock`), `Brand`, `Total Machine`, `Dia`, and `Gauge`.
    - Automatically computes **Needles/M**, **Sinkers/M**, **Total Needles**, and **Total Sinkers**:
      - *Single Jersey, Fleece, H/Jersey*: $\lfloor \text{Dia} \times \text{Gauge} \times 3.1416 \rfloor$
      - *Rib, Interlock*: $\lfloor 2 \times \text{Dia} \times \text{Gauge} \times 3.1416 \rfloor$
  - **👥 Contacts**: Manage factory contact persons, designations, click-to-call phone numbers, BUTEX batch, and statuses.
  - **📝 Updates & Meeting Minutes**: Log chronological factory visits, attendees, meeting minutes, action items, and follow-up dates.
- **💾 Backup & Restore**: Download or restore the SQLite database (`crm_data.db`) directly from the sidebar.

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push this folder to a **GitHub** repository (make sure `app.py`, `database.py`, `requirements.txt`, `.streamlit/config.toml`, `Knit Industry Contacts.xlsx`, and `crm_data.db` are included).
2. Go to [share.streamlit.io](https://share.streamlit.io/) and sign in with GitHub.
3. Click **Create app** -> Select your repository, branch (`main`), and set **Main file path** to `app.py`.
4. Click **Deploy!**

