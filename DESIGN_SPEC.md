# Knit Industry CRM — Redesign and Restructure Spec

A Streamlit + SQLite CRM for managing knitting factories in Bangladesh: factory directory, machine profiles with needle/sinker calculation, contacts, and visit meeting minutes. This document is the single source of truth for the redesign. It describes the current state, the problems, the target structure, the UI design, the data migration, and the build order.

---

## 1. Current state (what exists today)

Files: `app.py` (~2,200 lines), `database.py` (~1,300 lines), `fakir_data.py`, `masco_data.py`, `crm_data.db`, `Knit_Industry_Contacts.xlsx`, `requirements.txt`, `README.md`.

Stack: Python, Streamlit (>=1.38), pandas, openpyxl, sqlite3.

### Database (`crm_data.db`, SQLite, foreign keys ON)

| Table | Columns |
|---|---|
| `industries` | id, name (UNIQUE), location_area, cluster, distance_km, map_url, status, general_notes, machine_profile_notes, created_at, updated_at |
| `contacts` | id, industry_id (FK, cascade), name, designation, phone, email, butex_batch, status, notes, created_at |
| `updates` | id, industry_id (FK, cascade), visit_date, visit_type, attendees, meeting_minutes, action_items, next_followup_date, created_at |
| `machine_profiles` | id, industry_id (FK, cascade), fabrication, dia, gauge, dia_gauge_label, brand, quantity, needles_per_machine, sinkers_per_machine, needle_spec, sinker_spec, remarks, created_at |

Current volume: 32 industries, 42 contacts, 2 updates, 152 machine rows across 8 profiled factories (L'Esquire 41, Gram Tech 5, S.M. Group 7, Fakir Knitwears 59, Tosrifa 8, Adury 6, MASCO 8, Renaissance 18).

Clusters in use: Gazipur, Bhaluka, Rupganj, Narayanganj, Savar, Narshingdi.

### Constants to preserve

- Status options: `New, Contacted, Scheduled, Visited, Follow-up, Active Client`
- Status rank used by Excel sync (never downgrade a status): `New 0, Contacted 1, Scheduled 2, Visited 3, Follow-up 4, Active Client 5`
- Fabrication types: `Single Jersey, Fleece, H/Jersey, Rib, Interlock`
- Visit types: `Factory Visit, Phone / WhatsApp Follow-up, Sample / Technical Trial, Commercial / Price Discussion, General Update`
- Default brands: Mayer & Cie, Orizio, Pai Long, Fukuhara, HaanTex, Hangxing, Santo, Jung Long, Terrot, Jiunn Long, Santoni, Wellknit (plus any brand already in the DB)
- `NAME_MAPPING` in `database.py` (Excel contact-sheet names to canonical factory names). Keep it as-is.

### Needle and sinker calculation (source of truth is the code, not the README)

```
single-bed (Single Jersey, Fleece, H/Jersey):
    needles_per_machine = int(dia * gauge * 3.1416)
    sinkers_per_machine = int(dia * gauge * 3.1416)
double-bed (Rib, Interlock):
    needles_per_machine = int(2 * dia * gauge * 3.1416)
    sinkers_per_machine = 0
total_needles = needles_per_machine * quantity
total_sinkers = sinkers_per_machine * quantity
```

`parse_dia_gauge_label` parses strings like `30x20`, `36x20(F/L)`, `34x24(I/L)` into dia, gauge and label. Keep this behavior.

---

## 2. Problems to fix

1. **One 2,200-line `app.py`** holds CSS, HTML renderers, navigation, all three pages and all forms.
2. **Factory data is hardcoded in the UI layer.** `RENAISSANCE_SECTIONS`, `TOSRIFA_CIRCULAR_ROWS`, `TOSRIFA_FLAT_ROWS`, `SM_KNITWEARS_ROWS`, `GRAMTECH_SECTIONS` and the Adury rows are Python literals. An `if is_fakir / is_masco / is_tosrifa ...` chain picks a renderer by matching the factory name. KPI numbers like `"197"`, `"105"` and `"167 (165 Opt.)"` are typed in by hand and can drift from the data.
3. **Navigation is hand-rolled** (`session_state.current_view`, `_sync_sidebar`, many `st.rerun()` calls). The URL never changes, so there are no bookmarks and the browser back button does nothing useful.
4. **Heavy inline HTML.** Each renderer is 50-150 lines of string concatenation with inline styles. The Excel-style tables are hardcoded white-on-dark and clash with the dark UI.
5. **Copy-pasted UI.** Cards, edit forms, KPI blocks, status colors, `STATUS_OPTIONS` and visit types are repeated in several places.
6. **`database.py` mixes concerns**: schema, Excel import, five factory seeders and CRUD in one file.
7. **Over-decorated look.** Gradient hero banners, glassmorphic cards and a gradient title add noise and no information.

---

## 3. Target structure

```
knit_crm/
├── app.py                      # entry point: page config, load CSS, st.navigation() (~40 lines)
├── pages/
│   ├── dashboard.py            # KPIs, follow-ups due, pipeline, cluster summary
│   ├── factories.py            # master-detail: searchable list + selected factory
│   ├── machines.py             # cross-factory machine explorer (filter by brand/dia/gauge/fabrication)
│   ├── contacts.py             # all contacts, searchable, click-to-call
│   └── visits.py               # all visits and follow-ups across factories
├── components/
│   ├── badges.py               # status_badge(), ONE STATUS_COLORS dict
│   ├── cards.py                # kpi_card(), factory_list_item(), contact_card(), visit_card()
│   ├── forms.py                # factory_form(), contact_form(), visit_form() (add and edit share one function)
│   ├── tables.py               # machine_profile_table() generic grouped table with subtotals
│   └── tabs/
│       ├── overview.py
│       ├── machines.py
│       ├── contacts.py
│       └── visits.py
├── db/
│   ├── connection.py           # get_connection(), DB_PATH
│   ├── schema.py               # init_db(), migrations
│   ├── repo.py                 # CRUD only (industries, contacts, updates, machines)
│   ├── excel_sync.py           # sync_from_excel(), NAME_MAPPING, STATUS_RANK
│   ├── calc.py                 # calculate_needle_sinker(), parse_dia_gauge_label(), format_dia_gauge()
│   └── seeds/                  # one module per factory, run once, idempotent
│       ├── lesquire.py  fakir.py  masco.py  renaissance.py
│       ├── adury.py  tosrifa.py  sm_group.py  gramtech.py
├── config/
│   └── constants.py            # STATUS_OPTIONS, STATUS_RANK, VISIT_TYPES, FABRICATION_TYPES, DEFAULT_BRANDS
├── theme/
│   └── styles.css              # all custom CSS, loaded once; uses CSS variables
├── .streamlit/
│   └── config.toml             # real Streamlit theme (colors, font)
├── data/
│   ├── crm_data.db
│   └── Knit Industry Contacts.xlsx
├── requirements.txt
└── README.md
```

Rules:
- Pages contain layout and wiring only. Reusable UI lives in `components/`. SQL lives only in `db/`.
- No file over about 300 lines. No factory-specific `if` chains anywhere in UI code.
- All constants (statuses, visit types, fabrications, colors) are defined once in `config/constants.py` and `components/badges.py`.
- Use `@st.cache_data` for read queries and clear the cache after writes.

### Routing

Use `st.navigation` / `st.Page` for the five pages. Store the selected factory in `st.query_params["factory"]` so the URL looks like `/factories?factory=12`. That gives bookmarkable links and a working browser back button. Remove `current_view`, `selected_industry_id`, `_sync_sidebar` and `navigate_to_*` helpers.

---

## 4. Design direction

**Layout: app shell with sidebar (Direction A), with a master-detail split (Direction B) inside the Factories page.**

### 4.1 Visual language

- Plain, professional, restrained. Remove gradient hero banners, glass cards, gradient title text and decorative emoji clutter. Keep emoji only where they carry meaning (optional, small).
- One accent color (blue). Status colors carry meaning and nothing else is colorful. Define the palette in `.streamlit/config.toml` so native Streamlit widgets match.
- Font: Plus Jakarta Sans (already in use) or Inter. Two weights.
- Everything must work in both light and dark mode. Use CSS variables (`var(--...)`) and Streamlit theme tokens. No hardcoded `#ffffff` or `#0f172a` table backgrounds.
- Dense, readable tables. Cards only for list items and KPIs.

### 4.2 Status colors (single source of truth)

| Status | Meaning color |
|---|---|
| New | gray |
| Contacted | amber |
| Scheduled | blue |
| Visited | green |
| Follow-up | purple |
| Active Client | teal/dark green |

### 4.3 Sidebar

App name, then navigation: Dashboard, Factories, Machines, Contacts, Visits. Below: an "Add factory" action and a collapsed "Data" section (Sync from Excel, Download backup, Restore backup). Remove the long "quick jump" selectbox; the Factories page list replaces it.

### 4.3.1 Dashboard page

- Row of 4 KPI cards: Factories, Machines logged, Contacts, Active pipeline (Contacted + Scheduled + Visited + Follow-up).
- **Follow-ups due** panel (most important): list of visits with `next_followup_date` today or overdue, then upcoming 14 days. Each row: factory, date, action items, button "Open factory".
- Pipeline: status counts as a horizontal bar or compact stacked bar.
- By cluster: small table or cards (factories, machines, contacts, visited) with a link into the Factories page pre-filtered by cluster.
- Recent visits: last 5 visit logs.

### 4.3.2 Factories page (master-detail)

Two columns, roughly 1:2.4.

**Left (list):**
- Search box (name, location, cluster), cluster multiselect, status multiselect, sort selector (most machines, A-Z, nearest, most contacts).
- Compact selectable list. Each item: factory name, status badge, cluster, machine count. The selected item is highlighted. Selection writes `?factory=<id>`.
- Result count and an "Add factory" button.

**Right (detail):**
- Header: factory name, status badge, location and distance, "Open in Maps" link button, inline status selector, "Edit" popover or dialog (use `st.dialog`), delete with confirmation.
- KPI strip: Total machines, Contacts, Visits, Next follow-up date.
- Tabs: **Overview | Machines | Contacts | Visits**.
  - **Overview:** general notes, machine floor notes, latest visit summary, next follow-up.
  - **Machines:** see section 4.4.
  - **Contacts:** contact cards in a 2-column grid; click-to-call (`tel:`) and `mailto:` links; BUTEX batch; status badge; add and edit through `st.dialog`.
  - **Visits:** chronological timeline; each visit shows date, type, attendees, minutes (markdown), action items and follow-up date; add and edit through `st.dialog`; "Mark factory as Visited" checkbox when logging a Factory Visit.

On narrow screens the list collapses into a selectbox above the detail.

### 4.3.3 Machines page (cross-factory)

A filterable table of all machine rows across factories (factory, unit, fabrication, brand, dia, gauge, quantity, needles/M, sinkers/M, total needles, total sinkers). Filters: factory, brand, fabrication, dia range, gauge. Summary metrics on top (total machines, total needles, total sinkers, brand breakdown chart). CSV export. This page is the main way to find "who runs 34x24 Mayer machines".

### 4.3.4 Contacts page

Searchable table or card list of all contacts across factories: name, designation, factory, phone (click-to-call), email, BUTEX batch, status. Filters: factory, status, BUTEX batch. CSV export.

### 4.3.5 Visits page

All visit logs across factories, newest first, with filters (factory, type, date range) and a "Follow-ups" toggle showing only items that have a next follow-up date.

### 4.4 Machine profile tab (replaces all per-factory HTML renderers)

One generic component, `machine_profile_table()`:

- Input: the factory's machine rows from the DB (grouped by `unit`, then `fabrication`).
- Summary metrics at the top, computed from data: total machines, per-unit totals, number of brands, total needles, total sinkers. No hand-typed totals anywhere.
- If a factory has more than one unit, show a segmented control or sub-tabs per unit plus an "All units" view.
- Grouped table: Fabrication, Dia x Gauge, Brand, (origin, model, feeders, machine type, remarks when present), Quantity, Needles/M, Sinkers/M, Total needles, Total sinkers. Subtotal row per fabrication, grand total row at the bottom. Rows flagged `not_in_operation` are visually muted and excluded from the operating total, but counted in the installed total (Fakir: 167 installed, 165 operating).
- Theme-aware styling via CSS variables. Sticky header. Compact font.
- Optional toggle **"Original sheet view"** for factories that have a faithful replica of their source sheet (Fakir summary blocks: brand-wise, M/C type-wise, dia-wise, gauge-wise). This is a later enhancement and must not block the generic table.
- Editing: an "Edit machines" mode using `st.data_editor` (add, edit, delete rows) with needles and sinkers auto-computed on save via `db/calc.py`.
- Export: CSV download and (optional) Excel download.
- Machine floor notes (spare parts, oil, maintenance) stay as a text area saved to `industries.machine_profile_notes`.

---

## 5. Data migration plan

Goal: all factory machine data lives in the database, and the UI is data-driven.

### 5.1 Schema changes (additive, non-destructive)

Add columns to `machine_profiles` via an idempotent `ALTER TABLE ... ADD COLUMN` migration in `db/schema.py` (check `PRAGMA table_info` first):

| New column | Type | Purpose |
|---|---|---|
| `unit` | TEXT DEFAULT '' | e.g. "Unit-1", "Unit-2", "Collar and Cuff" |
| `machine_category` | TEXT DEFAULT 'Circular' | `Circular` or `Flat` |
| `machine_type` | TEXT DEFAULT '' | e.g. Open Dia, Tube Dia, Auto Striper, Rib/Spacer |
| `feeders` | INTEGER | number of feeders |
| `origin` | TEXT DEFAULT '' | country |
| `model` | TEXT DEFAULT '' | machine model |
| `capacity_kg` | REAL | daily capacity where given (Tosrifa) |
| `machine_no` | TEXT DEFAULT '' | M/C number where given (Fakir, Tosrifa) |
| `in_operation` | INTEGER DEFAULT 1 | 0 for "NOT IN OPERATION" rows |
| `sort_order` | INTEGER DEFAULT 0 | preserves source-sheet row order |

Also add a `data_source` column to `industries` or a small `sheet_summary` table only if needed. Do not drop or rename any existing column.

### 5.2 Move the hardcoded data into seeds

For each hardcoded factory, create `db/seeds/<factory>.py` that inserts rows with the new columns. Seeds must be **idempotent** (skip if the factory already has rows tagged by that seed, or delete-and-reinsert that factory's rows inside one transaction), and must never touch contacts or visit logs.

| Factory | Source today | Notes |
|---|---|---|
| L'Esquire Ltd. | `seed_lesquire_machines` | already in DB (41 rows) |
| Fakir Knitwears Ltd. | `fakir_data.py` + Excel parsing (`get_fakir_knitting_data`) | two units; 109 + 58 machines; includes "NOT IN OPERATION" rows (167 installed, 165 operating); 5 brands |
| MASCO (Concept Knitting) | `masco_data.py` | Unit-1 Rupganj 121 circular; Unit-2 Tongi 48 circular + 28 collar; total 197 |
| Renaissance Apparels Ltd. | `RENAISSANCE_SECTIONS` | 67 circular + 12 flat = 79; brands Pailung, Goang Lih, Matsuya |
| Adury Knit Composite | `render_adury_profile_html` literals | 63 circular + 42 flat (collar and cuff) = 105; cylinder gauges 14G-28G per dia |
| Tosrifa Industries Ltd | `TOSRIFA_CIRCULAR_ROWS`, `TOSRIFA_FLAT_ROWS` | 45 circular + 24 flat = 69; capacity 10,480 kg/day circular and 10,000 sets/day flat |
| S.M. Group (S.M. Knitwears) | `SM_KNITWEARS_ROWS` | 99 machine sets; cylinders 28G:5, 24G:66, 20G:41, 18G:26, 14G:9 |
| Gram Tech (Sonali Textile) | `GRAMTECH_SECTIONS` | 28 circular + 4 flat = 32 sets |

Some sheets use multiple cylinders (gauges) per machine (Adury, S.M.). Model this as one row per machine-and-gauge combination with `quantity` set correctly, or add a `cylinders` text field. Decide one approach and document it. Whatever is chosen, the **totals shown in the UI must match the totals above**; add a verification script (see section 7) that asserts them.

### 5.3 Preserve existing data

The existing `crm_data.db` must keep working. Back it up before migrating (`crm_data.pre_migration.db`). The migration runs automatically at startup and is safe to run repeatedly. Do not reseed contacts or visits.

### 5.4 Excel sync

`sync_from_excel` and `NAME_MAPPING` move to `db/excel_sync.py` unchanged in behavior (never downgrade status using `STATUS_RANK`, hyperlinks extracted as `map_url`, contacts matched by canonical factory name). Expose it as a button in the sidebar Data section. The Excel path becomes `data/Knit Industry Contacts.xlsx` (the repo file is currently uploaded as `Knit_Industry_Contacts.xlsx`; handle both names).

---

## 6. Configuration and deployment

`.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#2563eb"
font = "sans serif"
# provide matching light and dark base settings

[server]
maxUploadSize = 50
```

`requirements.txt`: keep `streamlit>=1.38.0`, `pandas>=2.0.0`, `openpyxl>=3.1.0`. Use only features available in that version (`st.navigation`, `st.Page`, `st.dialog`, `st.query_params`, `st.data_editor`, `st.segmented_control` if the pinned version supports it; otherwise `st.radio(horizontal=True)`). If a newer feature is needed, bump the pin and say so.

Deploy target stays Streamlit Community Cloud with main file `app.py`. Keep `data/crm_data.db` and the Excel file in the repo. Note in the README that Community Cloud storage is ephemeral, so the backup and restore button is the way to persist edits.

`.gitignore`: ignore `__pycache__/`, `.venv/`, `*.pre_migration.db`, `.streamlit/secrets.toml`.

---

## 7. Acceptance criteria

1. `streamlit run app.py` starts with no errors against the existing `crm_data.db`, and all existing industries, contacts and updates are intact (32, 42, 2).
2. Navigation uses `st.navigation`; selecting a factory sets `?factory=<id>`; opening that URL directly loads the factory; browser back works.
3. No file in the project exceeds about 300 lines; `app.py` is under about 60 lines.
4. No factory-name `if` chains and no hardcoded machine totals in UI code. Machine tables are generated from DB rows.
5. Machine totals match the source sheets: Fakir 167 installed (165 operating), MASCO 197, Renaissance 79, Adury 105, Tosrifa 69, Gram Tech 32, S.M. 99. A script `scripts/verify_totals.py` asserts these and exits non-zero on mismatch.
6. Needle/sinker values match `calculate_needle_sinker` for every row (rib/interlock sinkers = 0).
7. Add, edit and delete work for factories, contacts, visits and machine rows. Deleting a factory asks for confirmation. Status updates from the Factories page and from the visit form (auto-mark Visited) still work.
8. Dashboard shows follow-ups due (overdue and next 14 days) from `next_followup_date`.
9. Light and dark mode both look correct, including tables. No hardcoded white table backgrounds.
10. Backup download, restore upload and Excel sync still work from the sidebar Data section.
11. README is updated with the new structure, run instructions and deployment notes.

---

## 8. Build order (milestones)

1. **Scaffold and split.** Create the folder structure. Move `db/` code out of `database.py` with no behavior change. Move constants. Confirm the old UI still runs against the new modules.
2. **Schema migration and seeds.** Add columns, write idempotent seeds, write `scripts/verify_totals.py`, get all totals matching.
3. **Theme and shell.** `config.toml`, `styles.css`, `st.navigation`, sidebar, query-param routing.
4. **Factories page.** Master-detail list, header, KPI strip, Overview tab.
5. **Machines tab.** Generic `machine_profile_table()`, unit sub-tabs, subtotals, editing, CSV export. Delete the old per-factory renderers.
6. **Contacts and Visits tabs** with dialogs for add and edit.
7. **Dashboard, Machines, Contacts and Visits pages.**
8. **Polish and cleanup.** Dark-mode check, empty states, error handling, remove dead code, update README, run the verification script.

Do not remove the old code until its replacement is verified. Keep the app runnable after every milestone.
