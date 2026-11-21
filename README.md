# Knit Industry CRM

A Streamlit + SQLite CRM for managing knitting factories in Bangladesh: factory directory, machine profiles with automatic needle and sinker calculations, contacts, and factory visit meeting minutes.

## Project Structure

```
knit_crm/
├── app.py                      # Entry point: page config, require_login(), CSS loader, st.navigation()
├── auth/
│   ├── __init__.py
│   ├── gate.py                 # require_login() & sign_out()
│   ├── login_page.py           # On-theme login UI, greeting, lockout & rotating textile fact
│   ├── security.py             # PBKDF2-HMAC-SHA256 hash_password() & verify_password()
│   └── facts.py                # Generic circular knitting & textile facts
├── pages/
│   ├── dashboard.py            # KPIs, follow-ups due, pipeline, cluster summary, recent visits
│   ├── factories.py            # Master-detail factory browser (?factory=<id>) with 4 tabs
│   ├── machines.py             # Cross-factory machine explorer (filter by brand/dia/gauge/fabrication)
│   ├── contacts.py             # Searchable contacts directory with click-to-call & CSV export
│   └── visits.py               # All visit logs and follow-ups across factories
├── components/
│   ├── badges.py               # status_badge() and single STATUS_COLORS map
│   ├── cards.py                # kpi_card(), factory_list_item(), contact_card(), visit_card()
│   ├── forms.py                # Shared factory/contact/visit forms & st.dialog modals
│   ├── tables.py               # Generic data-driven machine_profile_table() with st.data_editor
│   └── tabs/
│       ├── overview.py
│       ├── machines.py
│       ├── contacts.py
│       └── visits.py
├── db/
│   ├── connection.py           # get_connection(), DB_PATH (data/crm_data.db)
│   ├── schema.py               # init_db(), additive idempotent schema migrations
│   ├── repo.py                 # CRUD queries for industries, contacts, updates, machines
│   ├── excel_sync.py           # sync_from_excel(), NAME_MAPPING, STATUS_RANK
│   ├── calc.py                 # calculate_needle_sinker(), parse_dia_gauge_label(), format_dia_gauge()
│   └── seeds/                  # Idempotent factory machine profile seeds
│       ├── lesquire.py  fakir.py  masco.py  renaissance.py
│       └── adury.py  tosrifa.py  sm_group.py  gramtech.py
├── config/
│   └── constants.py            # STATUS_OPTIONS, STATUS_RANK, VISIT_TYPES, FABRICATION_TYPES, DEFAULT_BRANDS
├── theme/
│   ├── styles.css              # Light/dark theme-aware CSS variables
│   └── login.css               # Login page animations, knit-stitch pattern & responsive card
├── .streamlit/
│   ├── config.toml             # Streamlit theme and server settings
│   └── secrets.toml.example    # Example secret configuration for app_password_hash
├── data/
│   ├── crm_data.db
│   └── Knit Industry Contacts.xlsx
├── scripts/
│   ├── make_password_hash.py   # CLI tool to generate salted PBKDF2 password hashes
│   └── verify_totals.py        # Automated verification of DB counts, machine totals & needle/sinker math
├── requirements.txt
└── README.md
```

## Login Setup

The app requires a salted PBKDF2-HMAC-SHA256 password hash stored in `app_password_hash` and fails closed if the secret is missing.

### 1. Generate a Password Hash Locally

Run the hash generator script and enter your desired password when prompted:

```bash
python scripts/make_password_hash.py
```

Copy the printed `app_password_hash = "pbkdf2$200000$..."` line into `.streamlit/secrets.toml` (which is gitignored).

### 2. Configure Secrets on Streamlit Community Cloud

1. Open your deployed app dashboard on [share.streamlit.io](https://share.streamlit.io/).
2. Click **⋮ (More options) → Settings → Secrets**.
3. Paste the `app_password_hash = "pbkdf2$200000$..."` line into the Secrets box and click **Save**.

## Design & Data Decisions

- **Multi-cylinder machines (Adury Knit Composite, S.M. Group, MASCO)**: Stored as one row per machine group with `quantity` equal to the physical machine set count (`M/C Qty` / `No of Machine Set`), primary gauge stored in `gauge`, full multi-gauge label in `dia_gauge_label` (e.g., `30x20/24/28`), and cylinder breakdown per gauge preserved in `remarks` (e.g., `Cylinders: 20G(2), 24G(5), 28G(3)`). This guarantees that summing `quantity` always equals the true installed machine total while preserving every cylinder gauge.
- **Needle & Sinker Calculation (`db/calc.py`)**:
  - **Single-bed (`Single Jersey`, `Fleece`, `H/Jersey`)**: `needles_per_machine = int(dia * gauge * 3.1416)`, `sinkers_per_machine = int(dia * gauge * 3.1416)`
  - **Double-bed (`Rib`, `Interlock`)**: `needles_per_machine = int(2 * dia * gauge * 3.1416)`, `sinkers_per_machine = 0`
  - Rows flagged `in_operation = 0` (such as Fakir's 2 non-operational machines) are included in the installed machine count (`167`) and excluded from operating totals (`165`) and needle/sinker totals.

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

To verify all database counts, factory machine totals, and needle/sinker calculations:

```bash
python scripts/verify_totals.py
```

## Deployment on Streamlit Community Cloud

1. Push this repository to GitHub with `app.py` as the main file path.
2. Add `app_password_hash` in the app's **Settings → Secrets** on Streamlit Community Cloud.
3. Keep `data/crm_data.db` and `data/Knit Industry Contacts.xlsx` committed in the repository.
4. **Ephemeral Cloud Storage Note**: Streamlit Community Cloud container storage is ephemeral across restarts. Use the **Data → Download backup (.db)** and **Restore backup (.db)** controls in the sidebar to persist and restore database edits made on the cloud.
