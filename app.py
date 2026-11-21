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

# Custom CSS for modern SaaS look, Landing Page, Industry Cards, and Custom Machine Profile Tables
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .block-container {
        padding-top: 1.6rem !important;
        padding-bottom: 3rem !important;
        max-width: 1380px !important;
    }

    /* Status Badges */
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.74rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }
    .status-Visited { background: rgba(16, 185, 129, 0.18); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); }
    .status-Scheduled { background: rgba(59, 130, 246, 0.18); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.4); }
    .status-Contacted { background: rgba(245, 158, 11, 0.18); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); }
    .status-Follow-up { background: rgba(168, 85, 247, 0.18); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.4); }
    .status-Active { background: rgba(34, 197, 94, 0.22); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.5); }
    .status-New { background: rgba(148, 163, 184, 0.15); color: #94a3b8; border: 1px solid rgba(148, 163, 184, 0.3); }

    /* Landing Page Hero */
    .landing-hero {
        position: relative;
        padding: 2.6rem 2.8rem;
        border-radius: 20px;
        background: radial-gradient(circle at 85% 15%, rgba(59, 130, 246, 0.25) 0%, rgba(17, 24, 39, 0.92) 55%, rgba(10, 14, 26, 0.98) 100%);
        border: 1px solid rgba(59, 130, 246, 0.32);
        box-shadow: 0 20px 45px -15px rgba(0, 0, 0, 0.6), inset 0 1px 0 0 rgba(255, 255, 255, 0.1);
        margin-bottom: 1.5rem;
    }
    .hero-eyebrow {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 999px;
        background: rgba(59, 130, 246, 0.16);
        border: 1px solid rgba(96, 165, 250, 0.35);
        color: #60a5fa;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 1.1px;
        text-transform: uppercase;
        margin-bottom: 0.9rem;
    }
    .hero-title {
        font-size: 2.55rem;
        font-weight: 800;
        line-height: 1.18;
        margin: 0 0 0.75rem 0;
        background: linear-gradient(90deg, #ffffff 0%, #93c5fd 55%, #38bdf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #94a3b8;
        max-width: 760px;
        line-height: 1.6;
        margin: 0;
    }

    /* Glassmorphic KPI Cards */
    .kpi-card {
        padding: 1.35rem 1.4rem;
        border-radius: 16px;
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.65) 0%, rgba(15, 23, 42, 0.85) 100%);
        border: 1px solid rgba(148, 163, 184, 0.18);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
        margin-bottom: 0.8rem;
    }
    .kpi-icon {
        font-size: 1.35rem;
        margin-bottom: 0.4rem;
    }
    .kpi-value {
        font-size: 2.05rem;
        font-weight: 800;
        color: #f8fafc;
        line-height: 1.15;
        font-variant-numeric: tabular-nums;
    }
    .kpi-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #94a3b8;
        margin-top: 0.25rem;
    }
    .kpi-sub {
        font-size: 0.75rem;
        color: #60a5fa;
        margin-top: 0.35rem;
        font-weight: 500;
    }

    /* Factory Directory Card */
    .factory-card-box {
        padding: 1.15rem 1.25rem 0.85rem 1.25rem;
        border-radius: 14px;
        background: linear-gradient(160deg, rgba(30, 41, 59, 0.55) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(148, 163, 184, 0.18);
        margin-bottom: 0.4rem;
    }
    .factory-card-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #f8fafc;
        margin: 0;
        line-height: 1.3;
    }
    .factory-card-loc {
        font-size: 0.82rem;
        color: #94a3b8;
        margin: 0.35rem 0 0.75rem 0;
    }
    .stat-chip-row {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        margin-bottom: 0.35rem;
    }
    .stat-chip {
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.78rem;
        font-weight: 600;
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(148, 163, 184, 0.18);
        color: #e2e8f0;
    }
    .stat-chip-highlight {
        background: rgba(59, 130, 246, 0.16);
        border: 1px solid rgba(59, 130, 246, 0.38);
        color: #93c5fd;
    }

    /* Section Headers */
    .section-banner {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.85rem 1.25rem;
        border-radius: 12px;
        background: rgba(30, 41, 59, 0.45);
        border-left: 4px solid #3b82f6;
        border-top: 1px solid rgba(148, 163, 184, 0.15);
        border-right: 1px solid rgba(148, 163, 184, 0.15);
        border-bottom: 1px solid rgba(148, 163, 184, 0.15);
        margin: 1.2rem 0 1rem 0;
    }

    .industry-header-box {
        padding: 1.6rem 1.9rem;
        border-radius: 16px;
        background: radial-gradient(circle at 90% 20%, rgba(59, 130, 246, 0.18) 0%, rgba(17, 24, 39, 0.9) 70%);
        border: 1px solid rgba(59, 130, 246, 0.3);
        box-shadow: 0 12px 30px -10px rgba(0, 0, 0, 0.45);
        margin-bottom: 1.2rem;
    }
    .minute-card {
        padding: 1.1rem 1.3rem;
        border-radius: 10px;
        border-left: 4px solid #3b82f6;
        background-color: rgba(30, 41, 59, 0.65);
        border-top: 1px solid rgba(148, 163, 184, 0.2);
        border-right: 1px solid rgba(148, 163, 184, 0.2);
        border-bottom: 1px solid rgba(148, 163, 184, 0.2);
        margin-bottom: 0.6rem;
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


def render_fakir_block_html(block: dict) -> str:
    """Render one Fakir Knitwears machine block (Serial No., M/C NO., BRAND, ORIGIN, M/C Dia, M/C Gauge, Feeders, M/C Type, QTY.)."""
    rows_html = []
    for r in block["rows"]:
        is_not_opt = "NOT IN OPERATION" in r["brand"].upper()
        row_style = ' style="background-color:#fee2e2;color:#991b1b;font-weight:600;"' if is_not_opt else ""
        rows_html.append(
            f"<tr{row_style}>"
            f'<td class="total-col">{r["sn"]}</td>'
            f'<td class="total-col"><strong>{html.escape(r["mc_no"])}</strong></td>'
            f'<td class="brand-col">{html.escape(r["brand"])}</td>'
            f'<td class="total-col">{html.escape(r["origin"])}</td>'
            f'<td class="total-col">{html.escape(r["dia"])}</td>'
            f'<td class="total-col">{html.escape(r["gauge"])}</td>'
            f'<td class="total-col">{html.escape(str(r["feeders"]))}</td>'
            f'<td class="total-col">{html.escape(r["mc_type"])}</td>'
            f'<td class="total-col">{r["qty"]}</td>'
            f"</tr>"
        )

    rows_html.append(
        f'<tr class="sheet-subtotal-row">'
        f'<td colspan="8" style="text-align:right;">Total=</td>'
        f'<td class="total-col" style="background-color:#8ea9db;">{block["total"]}</td>'
        f"</tr>"
    )

    sn_head = html.escape(block.get("header_sn", "Serial No."))
    return (
        f'<div class="mp-sheet-container" style="max-width:100%;margin-bottom:1rem;">'
        f'<table class="mp-sheet-table" style="font-size:0.84rem;">'
        f"<thead><tr>"
        f"<th>{sn_head}</th>"
        f"<th>M/C NO.</th>"
        f"<th>BRAND</th>"
        f"<th>ORIGIN</th>"
        f"<th>M/C Dia</th>"
        f"<th>M/C Gauge</th>"
        f"<th>Feeders</th>"
        f"<th>M/C Type</th>"
        f"<th>QTY.</th>"
        f"</tr></thead>"
        f'<tbody>{"".join(rows_html)}</tbody>'
        f"</table>"
        f"</div>"
    )


def render_fakir_summary_card_html(summary: dict) -> str:
    """Render the 4-part summary table (Brand wise, M/C typewise, Dia wise, Gauge wise) matching Fakir's Excel sheet."""
    def _subtable(header_label: str, pairs: list) -> str:
        trs = []
        for k, v in pairs:
            is_tot = "TOTAL" in str(k).upper()
            cls = ' class="sheet-subtotal-row"' if is_tot else ""
            bg = ' style="background-color:#8ea9db;"' if is_tot else ""
            trs.append(
                f"<tr{cls}>"
                f"<td{bg}>{html.escape(str(k))}</td>"
                f'<td class="total-col"{bg}><strong>{v}</strong></td>'
                f"</tr>"
            )
        return (
            f'<table class="mp-sheet-table" style="font-size:0.86rem;">'
            f'<thead><tr><th colspan="2">{html.escape(header_label)}</th></tr></thead>'
            f'<tbody>{"".join(trs)}</tbody>'
            f"</table>"
        )

    return (
        f'<div style="margin:0.75rem 0 1.25rem 0;padding:12px 14px;border:1.5px solid #334155;background:#f8fafc;color:#0f172a;border-radius:6px;">'
        f'<div style="font-weight:800;font-size:1.05rem;margin-bottom:10px;color:#0f172a;text-decoration:underline;">'
        f'{html.escape(summary["title"])}'
        f"</div>"
        f'<div style="display:grid;grid-template-columns:repeat(4, 1fr);gap:12px;align-items:start;">'
        f'<div>{_subtable("Brand wise:", summary["brand_wise"])}</div>'
        f'<div>{_subtable("M/C typewise:", summary["type_wise"])}</div>'
        f'<div>{_subtable("Dia wise:", summary["dia_wise"])}</div>'
        f'<div>{_subtable("Gauge wise:", summary["gauge_wise"])}</div>'
        f"</div>"
        f"</div>"
    )


RENAISSANCE_SECTIONS = [
    {
        "title": "JERSEY MACHINE",
        "show_col_headers": True,
        "rows": [
            (1, "30", "24", "90", "TUBE DIA", "PAILUNG", "TAIWAN", 4, "100% LYCRA ATTACHMENT"),
            (2, "30", "24/28", "90", "TUBE DIA", "PAILUNG", "TAIWAN", 4, "100% LYCRA ATTACHMENT"),
            (3, "30", "24/32", "90", "TUBE DIA", "PAILUNG", "TAIWAN", 2, "100% LYCRA ATTACHMENT"),
            (4, "32", "24", "96", "TUBE DIA", "PAILUNG", "TAIWAN", 6, "100% LYCRA ATTACHMENT"),
            (5, "34", "24", "102", "TUBE DIA", "GOANG LIH", "TAIWAN", 4, "100% LYCRA ATTACHMENT"),
            (6, "34", "24", "102", "TUBE DIA", "PAILUNG", "TAIWAN", 4, "100% LYCRA ATTACHMENT"),
            (7, "34", "24", "102", "OPEN DIA", "PAILUNG", "TAIWAN", 2, "100% LYCRA ATTACHMENT"),
            (8, "34", "24", "204", "TUBE DIA", "GOANG LIH", "TAIWAN", 2, "MULTI FEEDER (6-FEEDER)"),
            (9, "36", "24", "108", "TUBE DIA", "PAILUNG", "TAIWAN", 7, "100% LYCRA ATTACHMENT"),
            (10, "36", "24/20", "108", "OPEN DIA", "PAILUNG", "TAIWAN", 2, "100% LYCRA ATTACHMENT"),
            (11, "38", "24", "114", "OPEN DIA", "PAILUNG", "TAIWAN", 2, "100% LYCRA ATTACHMENT"),
        ],
        "footers": [("TOTAL", 39)],
    },
    {
        "title": "RIB+INTERLOCK MACHINE",
        "show_col_headers": False,
        "rows": [
            (12, "36", "18/24", "72", "", "PAILUNG", "TAIWAN", 6, "100% LYCRA ATTACHMENT"),
            (13, "38", "16/18/24", "76", "", "PAILUNG", "TAIWAN", 4, "100% LYCRA ATTACHMENT"),
            (14, "40", "18", "80", "", "PAILUNG", "TAIWAN", 4, "100% LYCRA ATTACHMENT"),
            (15, "42", "18", "84", "", "PAILUNG", "TAIWAN", 4, "100% LYCRA ATTACHMENT"),
            (16, "44", "18", "88", "", "PAILUNG", "TAIWAN", 2, "100% LYCRA ATTACHMENT"),
        ],
        "footers": [("TOTAL", 20)],
    },
    {
        "title": "FLEECE MACHINE",
        "show_col_headers": False,
        "rows": [
            (17, "34", "20", "108", "", "GOANG LIH", "TAIWAN", 8, "100% LYCRA ATTACHMENT"),
        ],
        "footers": [
            ("TOTAL", 8),
            ("TOTAL NO OF CIRCULAR KNITTING MACHINE", 67),
        ],
    },
    {
        "title": "FLAT KNIT MACHINE",
        "show_col_headers": False,
        "rows": [
            (18, "80", "14", "", "", "MATSUYA", "CHINA", 12, "100% LYCRA ATTACHMENT"),
        ],
        "footers": [
            ("TOTAL NO OF FLAT KNITTING MACHINE", 12),
        ],
    },
]


def render_renaissance_profile_html() -> str:
    """Render Renaissance Apparels Ltd. Knitting Machine Profile (Jersey, Rib+Interlock, Fleece, Flat Knit; excluding Utility)."""
    blocks_html = []
    for sec in RENAISSANCE_SECTIONS:
        trs = [
            f'<tr><td colspan="9" style="background-color:#bdd7ee;color:#0f172a;font-weight:800;text-align:center;padding:6px;border:1px solid #0f172a;">{html.escape(sec["title"])}</td></tr>'
        ]
        if sec["show_col_headers"]:
            trs.append(
                "<tr>"
                '<th style="background-color:#c6e0b4;color:#0f172a;border:1px solid #0f172a;width:7%;">SL.NO.</th>'
                '<th style="background-color:#c6e0b4;color:#0f172a;border:1px solid #0f172a;width:9%;">M/C DIA</th>'
                '<th style="background-color:#c6e0b4;color:#0f172a;border:1px solid #0f172a;width:11%;">M/C GAUGE</th>'
                '<th style="background-color:#c6e0b4;color:#0f172a;border:1px solid #0f172a;width:9%;">FEEDER</th>'
                '<th style="background-color:#c6e0b4;color:#0f172a;border:1px solid #0f172a;width:13%;">TYPES OF DIA</th>'
                '<th style="background-color:#c6e0b4;color:#0f172a;border:1px solid #0f172a;width:13%;">BRAND</th>'
                '<th style="background-color:#c6e0b4;color:#0f172a;border:1px solid #0f172a;width:10%;">ORIGIN</th>'
                '<th style="background-color:#c6e0b4;color:#0f172a;border:1px solid #0f172a;width:10%;">QUANTITY</th>'
                '<th style="background-color:#c6e0b4;color:#0f172a;border:1px solid #0f172a;width:18%;">REMARKS</th>'
                "</tr>"
            )
        for sl, dia, gg, feeder, dtype, brand, origin, qty, rem in sec["rows"]:
            trs.append(
                f"<tr>"
                f'<td class="total-col" style="width:7%;">{sl}</td>'
                f'<td class="total-col" style="width:9%;">{html.escape(dia)}</td>'
                f'<td class="total-col" style="width:11%;">{html.escape(gg)}</td>'
                f'<td class="total-col" style="width:9%;">{html.escape(feeder)}</td>'
                f'<td class="total-col" style="width:13%;">{html.escape(dtype)}</td>'
                f'<td class="total-col" style="width:13%;">{html.escape(brand)}</td>'
                f'<td class="total-col" style="width:10%;">{html.escape(origin)}</td>'
                f'<td class="total-col" style="width:10%;"><strong>{qty}</strong></td>'
                f'<td class="total-col" style="width:18%;">{html.escape(rem)}</td>'
                f"</tr>"
            )
        for f_label, f_val in sec["footers"]:
            trs.append(
                f"<tr>"
                f'<td colspan="7" style="text-align:center;font-weight:800;border:1px solid #0f172a;padding:6px;">{html.escape(f_label)}</td>'
                f'<td class="total-col" style="font-weight:800;border:1px solid #0f172a;padding:6px;">{f_val}</td>'
                f'<td style="border:1px solid #0f172a;"></td>'
                f"</tr>"
            )
        blocks_html.append(
            f'<div class="mp-sheet-container" style="max-width:960px;margin-bottom:0.85rem;">'
            f'<table class="mp-sheet-table" style="font-size:0.86rem;">'
            f'<tbody>{"".join(trs)}</tbody>'
            f"</table>"
            f"</div>"
        )
    return "".join(blocks_html)


def render_adury_profile_html() -> str:
    """Render Adury Knit Composite Ltd. Knitting Machine Profile matching AKCL MC Profile.pdf."""
    def _std_section(title: str, rows: list, total_row: list) -> str:
        parts = [
            f'<tr><td colspan="11" style="background-color:#f8cbad;color:#0f172a;font-weight:800;text-align:left;font-size:0.95rem;padding:6px 10px;border:1px solid #0f172a;">{html.escape(title)}</td></tr>',
            "<tr>"
            '<th rowspan="2" style="background-color:#8ea9db;border:1px solid #0f172a;width:8%;">Dia</th>'
            '<th rowspan="2" style="background-color:#8ea9db;border:1px solid #0f172a;width:8%;">Feeder</th>'
            '<th rowspan="2" style="background-color:#8ea9db;border:1px solid #0f172a;width:9%;">M/C Qty</th>'
            '<th colspan="7" style="background-color:#8ea9db;border:1px solid #0f172a;width:45%;">Cylinder</th>'
            '<th rowspan="2" style="background-color:#8ea9db;border:1px solid #0f172a;width:30%;">Remarks</th>'
            "</tr>",
            "<tr>"
            '<th style="background-color:#8ea9db;border:1px solid #0f172a;">14G</th>'
            '<th style="background-color:#8ea9db;border:1px solid #0f172a;">18G</th>'
            '<th style="background-color:#8ea9db;border:1px solid #0f172a;">20G</th>'
            '<th style="background-color:#8ea9db;border:1px solid #0f172a;">22G</th>'
            '<th style="background-color:#8ea9db;border:1px solid #0f172a;">24G</th>'
            '<th style="background-color:#8ea9db;border:1px solid #0f172a;">25G</th>'
            '<th style="background-color:#8ea9db;border:1px solid #0f172a;">28G</th>'
            "</tr>",
        ]
        for r in rows:
            dia, dia_span, feeder, qty, g14, g18, g20, g22, g24, g25, g28, rem = r
            tr = ["<tr>"]
            if dia_span > 0:
                tr.append(f'<td class="total-col" rowspan="{dia_span}"><strong>{html.escape(str(dia))}</strong></td>')
            tr.append(f'<td class="total-col">{html.escape(str(feeder))}</td>')
            tr.append(f'<td class="total-col"><strong>{html.escape(str(qty))}</strong></td>')
            for gval in (g14, g18, g20, g22, g24, g25, g28):
                tr.append(f'<td class="total-col">{html.escape(str(gval))}</td>')
            tr.append(f'<td class="total-col">{html.escape(str(rem))}</td>')
            tr.append("</tr>")
            parts.append("".join(tr))

        t_cells = "".join(
            f'<td class="total-col" style="background-color:#8ea9db;font-weight:800;">{v}</td>' for v in total_row
        )
        parts.append(
            f'<tr class="sheet-subtotal-row">'
            f'<td colspan="2" style="text-align:right;background-color:#8ea9db;font-weight:800;">Total =</td>'
            f"{t_cells}"
            f'<td style="background-color:#8ea9db;"></td>'
            f"</tr>"
        )
        return "".join(parts)

    sj_open_rows = [
        ('30"', 1, 96, 1, "", "", "", "", 1, "", "", "With FF Lycra Attachments"),
        ('32"', 1, 102, 1, "", "", "", "", 1, "", "", "With FF Lycra Attachments"),
        ('34"', 1, 109, 1, "", "", "", "", 1, "", "", "With FF Lycra Attachments"),
        ('36"', 1, 115, 1, "", "", "", "", 1, "", "", "With FF Lycra Attachments"),
    ]
    sj_tube_rows = [
        ('25"', 1, 75, 1, "", "", "", "", 1, "", "", "With FF Lycra Attachments"),
        ('26"', 1, 84, 1, "", "", "", "", 1, "", 1, "With FF Lycra Attachments"),
        ('28"', 1, 84, 1, "", "", "", "", 1, "", "", "With FF Lycra Attachments"),
        ('30"', 1, 96, 5, "", "", 2, "", 5, "", 3, "With FF Lycra Attachments"),
        ('32"', 1, 102, 5, "", "", 1, "", 5, "", 2, "With FF Lycra Attachments"),
        ('34"', 1, 108, 6, 1, "", 1, "", 6, "", 2, "With FF Lycra Attachments"),
        ('36"', 1, 108, 7, 2, "", 3, "", 7, "", 1, "With FF Lycra Attachments"),
        ('38"', 1, 108, 1, "", "", "", "", 1, "", "", "With FF Lycra Attachments"),
        ('40"', 1, 128, 2, 1, "", "", "", 2, "", "", "With FF Lycra Attachments"),
    ]
    rib_il_rows = [
        ('30"', 1, 60, 1, "", 1, "", "", 1, "", "", "With Interlock conversion Facilities"),
        ('32"', 1, 66, 1, "", 1, "", 1, 1, "", "", "With Interlock conversion Facilities"),
        ('34"', 2, 70, 1, "", 1, "", "", 1, "", "", "With Interlock conversion Facilities"),
        (None, 0, 62, 1, "", 1, "", "", 1, "", "", "With Interlock conversion Facilities"),
        ('36"', 2, 74, 1, "", 1, "", "", 1, "", "", "With Interlock conversion Facilities"),
        (None, 0, 64, 1, "", 1, "", "", 1, "", "", "With Interlock conversion Facilities"),
        ('38"', 1, 78, 1, "", 1, "", "", 1, "", "", "With Interlock conversion Facilities"),
        ('40"', 1, 72, 1, "", 1, "", "", 1, "", "", "With Interlock conversion Facilities"),
    ]
    fleece_rows = [
        ("30", 1, 90, 5, "", "", 5, "", "", "", "", "With Lycra Attachments"),
        ("32", 1, 96, 2, "", "", 2, "", "", "", "", ""),
        ("34", 1, 108, 10, "", "", 10, "", "", "", "", ""),
    ]

    sec1 = _std_section("Single Jersey (Open)", sj_open_rows, [4, 0, 0, 0, 0, 4, 0, 0])
    sec2 = _std_section("Single Jersey (Tube)", sj_tube_rows, [29, 4, 0, 7, 0, 29, 0, 9])
    sec3 = _std_section("Rib & Interlock", rib_il_rows, [8, 0, 8, 0, 1, 8, 0, 0])
    sec4 = _std_section("Fleece", fleece_rows, [17, 0, 0, 17, 0, 0, 0, 0])

    # Engineering Stripe S/J section (has 'Finger' column and 6 Cylinder columns: 14G..25G)
    eng_rows_data = [
        ("30", 48, 6, 1, 1, "", 1, "", 1, "", ""),
        ("32", 54, 6, 1, 1, "", 1, "", 1, "", ""),
        ("34", 54, 6, 1, 1, "", 1, "", 1, "", ""),
        ("36", 54, 6, 1, 1, "", 1, "", 1, "", ""),
        ("38", 54, 6, 1, 1, "", 1, "", 1, "", ""),
    ]
    eng_parts = [
        '<tr><td colspan="11" style="background-color:#f8cbad;color:#0f172a;font-weight:800;text-align:left;font-size:0.95rem;padding:6px 10px;border:1px solid #0f172a;">Engineering Stripe S/J</td></tr>',
        "<tr>"
        '<th rowspan="2" style="background-color:#8ea9db;border:1px solid #0f172a;">Dia</th>'
        '<th rowspan="2" style="background-color:#8ea9db;border:1px solid #0f172a;">Feeder</th>'
        '<th rowspan="2" style="background-color:#8ea9db;border:1px solid #0f172a;">Finger</th>'
        '<th rowspan="2" style="background-color:#8ea9db;border:1px solid #0f172a;">M/C Qty</th>'
        '<th colspan="6" style="background-color:#8ea9db;border:1px solid #0f172a;">Cylinder</th>'
        '<th rowspan="2" style="background-color:#8ea9db;border:1px solid #0f172a;">Remarks</th>'
        "</tr>",
        "<tr>"
        '<th style="background-color:#8ea9db;border:1px solid #0f172a;">14G</th>'
        '<th style="background-color:#8ea9db;border:1px solid #0f172a;">18G</th>'
        '<th style="background-color:#8ea9db;border:1px solid #0f172a;">20G</th>'
        '<th style="background-color:#8ea9db;border:1px solid #0f172a;">22G</th>'
        '<th style="background-color:#8ea9db;border:1px solid #0f172a;">24G</th>'
        '<th style="background-color:#8ea9db;border:1px solid #0f172a;">25G</th>'
        "</tr>",
    ]
    for dia, fd, fg, mq, c14, c18, c20, c22, c24, c25, rem in eng_rows_data:
        eng_parts.append(
            f"<tr>"
            f'<td class="total-col"><strong>{dia}</strong></td>'
            f'<td class="total-col">{fd}</td>'
            f'<td class="total-col"><strong>{fg}</strong></td>'
            f'<td class="total-col"><strong>{mq}</strong></td>'
            f'<td class="total-col">{c14}</td>'
            f'<td class="total-col">{c18}</td>'
            f'<td class="total-col">{c20}</td>'
            f'<td class="total-col">{c22}</td>'
            f'<td class="total-col">{c24}</td>'
            f'<td class="total-col">{c25}</td>'
            f'<td class="total-col">{rem}</td>'
            f"</tr>"
        )
    eng_t_cells = "".join(
        f'<td class="total-col" style="background-color:#8ea9db;font-weight:800;">{v}</td>' for v in [5, 5, 0, 5, 0, 5, 0]
    )
    eng_parts.append(
        f'<tr class="sheet-subtotal-row">'
        f'<td colspan="3" style="text-align:right;background-color:#8ea9db;font-weight:800;">Total =</td>'
        f"{eng_t_cells}"
        f'<td style="background-color:#8ea9db;"></td>'
        f"</tr>"
    )
    sec5 = "".join(eng_parts)

    # Collar & Cuff + Total M/C Summary Box
    collar_table = (
        '<table class="mp-sheet-table" style="font-size:0.86rem;">'
        "<tbody>"
        '<tr><td colspan="6" style="background-color:#f8cbad;color:#0f172a;font-weight:800;text-align:left;font-size:0.95rem;padding:6px 10px;border:1px solid #0f172a;">Collar &amp; Cuff</td></tr>'
        "<tr>"
        '<th style="background-color:#8ea9db;border:1px solid #0f172a;">Bed</th>'
        '<th style="background-color:#8ea9db;border:1px solid #0f172a;">Qty</th>'
        '<th style="background-color:#8ea9db;border:1px solid #0f172a;">Color Use</th>'
        '<th style="background-color:#8ea9db;border:1px solid #0f172a;">GG</th>'
        '<th style="background-color:#8ea9db;border:1px solid #0f172a;">Needle</th>'
        '<th style="background-color:#8ea9db;border:1px solid #0f172a;">Remark\'s</th>'
        "</tr>"
        '<tr><td colspan="6" style="background-color:#f8cbad;color:#0f172a;font-weight:800;text-align:center;padding:4px;border:1px solid #0f172a;">Semi Jacquard</td></tr>'
        '<tr><td class="total-col">60"</td><td class="total-col"><strong>37</strong></td><td class="total-col">4</td><td class="total-col">14</td><td class="total-col"><strong>840X2</strong></td><td class="total-col"></td></tr>'
        '<tr><td colspan="6" style="background-color:#f8cbad;color:#0f172a;font-weight:800;text-align:center;padding:4px;border:1px solid #0f172a;">Jacquard</td></tr>'
        '<tr><td class="total-col">45"</td><td class="total-col"><strong>2</strong></td><td class="total-col">4</td><td class="total-col">14</td><td class="total-col"><strong>630X2</strong></td><td class="total-col"></td></tr>'
        '<tr><td class="total-col">80"</td><td class="total-col"><strong>3</strong></td><td class="total-col">6</td><td class="total-col">14</td><td class="total-col"><strong>1120X2</strong></td><td class="total-col"></td></tr>'
        '<tr class="sheet-subtotal-row">'
        '<td style="background-color:#8ea9db;font-weight:800;text-align:center;">Total =</td>'
        '<td class="total-col" style="background-color:#8ea9db;font-weight:800;">42</td>'
        '<td colspan="4" style="background-color:#8ea9db;"></td>'
        "</tr>"
        "</tbody></table>"
    )

    summary_box = (
        '<div style="display:flex;flex-direction:column;justify-content:center;align-items:center;height:100%;padding:24px;border:1.5px solid #1e293b;background:#ffffff;color:#0f172a;text-align:center;">'
        '<div style="font-size:1.6rem;font-weight:800;margin-bottom:10px;font-family:Georgia,serif;">Total M/C</div>'
        '<div style="font-size:1.25rem;font-weight:700;margin-bottom:8px;font-family:Georgia,serif;">Circular Knit : 63</div>'
        '<div style="font-size:1.25rem;font-weight:700;font-family:Georgia,serif;">Flat Knit : 42</div>'
        "</div>"
    )

    return (
        f'<div class="mp-sheet-container" style="max-width:980px;margin-bottom:0.85rem;">'
        f'<table class="mp-sheet-table" style="font-size:0.85rem;">'
        f"<tbody>{sec1}{sec2}{sec3}{sec4}{sec5}</tbody>"
        f"</table>"
        f'<div style="display:grid;grid-template-columns:1.8fr 1.2fr;border-top:1px solid #0f172a;">'
        f"<div>{collar_table}</div>"
        f"<div>{summary_box}</div>"
        f"</div>"
        f"</div>"
    )


TOSRIFA_CIRCULAR_ROWS = [
    # (sl, mc_no, dia, gauge, feeder, mc_type, type_span, brand, model, origin, cap_kg)
    (1, 6, 30, "24/28", 90, "SINGLE JERSEY", 10, "Keum Yong", "KM-3WVX", "Korea", "250"),
    (2, 7, 30, "24/32", 90, None, 0, "Keum Yong", "KLM-72AV", "Korea", "250"),
    (3, 34, 34, "28", 102, None, 0, "Keum Yong", "KM-3WVX", "Korea", "300"),
    (4, 35, 34, "28", 102, None, 0, "Keum Yong", "KM-3WVX", "Korea", "300"),
    (5, 9, 34, "24/28", 102, None, 0, "Keum Yong", "KM-3WVX", "Korea", "300"),
    (6, 8, 30, "24/32", 90, None, 0, "Keum Yong", "KM-3WVX", "Korea", "250"),
    (7, 44, 34, "24/28", 108, None, 0, "Mayer & Cie", "RELANIT 3.2-II", "Germany", "250"),
    (8, 33, 34, "24/28", 108, None, 0, "Mayer & Cie", "RELANIT 3.2-II", "Germany", "250"),
    (9, 11, 38, "24", 123, None, 0, "Mayer & Cie", "RELANIT 3.2-II", "Germany", "350"),
    (10, 22, 36, "24", 114, None, 0, "Mayer & Cie", "RELANIT 3.2-II", "Germany", "340"),
    (11, 10, 30, "20/24", 96, "Fleece, S/Jersey", 8, "Mayer & Cie", "S4-3.2", "Germany", "250"),
    (12, 27, 30, "20/24/12", 96, None, 0, "Lisky", "4-Tube-2014", "Taiwan", "260"),
    (13, 29, 30, "20/24/12", 96, None, 0, "Lisky", "4-Tube-2014", "Taiwan", "260"),
    (14, 31, 30, "20/24/12", 96, None, 0, "Lisky", "4-Tube-2014", "Taiwan", "260"),
    (15, 19, 30, "20/24/12", 96, None, 0, "Lisky", "Version-Tube-2016", "Taiwan", "280"),
    (16, 20, 30, "20/24/12", 96, None, 0, "Lisky", "Version-Tube-2016", "Taiwan", "280"),
    (17, 40, 30, "20/24", 90, None, 0, "Point", "ZD-S", "China", "280"),
    (18, 26, 30, "20/28", 90, None, 0, "Point", "ZD-S", "China", "280"),
    (19, 32, 30, "20/12", 96, "Fleece", 12, "Lisky", "4-Tube-2014", "Taiwan", "280"),
    (20, 21, 30, "20/12", 96, None, 0, "Lisky", "Version-Tube-2016", "Taiwan", "280"),
    (21, 30, 30, "20/12", 96, None, 0, "Lisky", "4-Tube-2014", "Taiwan", "280"),
    (22, 28, 30, "20", 96, None, 0, "Lisky", "4-Tube-2014", "Taiwan", ""),
    (23, 25, 30, "20", 90, None, 0, "Point", "ZD-S", "China", "280"),
    (24, 43, 30, "20", 90, None, 0, "Point", "ZD-S", "China", ""),
    (25, 42, 30, "20", 90, None, 0, "Point", "ZD-S", "China", ""),
    (26, 41, 30, "20", 90, None, 0, "Point", "ZD-S", "China", "280"),
    (27, 39, 30, "20", 90, None, 0, "Point", "ZD-S", "China", "280"),
    (28, 38, 30, "20", 90, None, 0, "Point", "ZD-S", "China", "280"),
    (29, 37, 30, "20", 90, None, 0, "Point", "ZD-S", "China", "280"),
    (30, 36, 30, "20", 90, None, 0, "Point", "ZD-S", "China", "280"),
    (31, 24, 42, "18", 84, "Rib/Spacer", 6, "Lisky", "DT/84 A-4", "Taiwan", "300"),
    (32, 23, 42, "18/14", 84, None, 0, "Lisky", "DT/84 A-4", "Taiwan", "300"),
    (33, 1, 42, "18", 84, None, 0, "Lisky", "DT/84 A-4", "Taiwan", "300"),
    (34, 2, 42, "18", 84, None, 0, "Lisky", "DT/84 A-4", "Taiwan", ""),
    (35, 12, 42, "18", 84, None, 0, "Lisky", "DT/84 A-4", "Taiwan", "300"),
    (36, 13, 42, "18", 84, None, 0, "Lisky", "DT/84 A-4", "Taiwan", "300"),
    (37, 15, 34, "18", 72, "Rib", 3, "Mayer & Cie", "D4-2.2", "Germany", "200"),
    (38, 17, 32, "18", 68, None, 0, "Mayer & Cie", "D4-2.2", "Germany", ""),
    (39, 18, 30, "18", 62, None, 0, "Mayer & Cie", "F4-2.0", "Germany", "220"),
    (40, 4, 34, "24", 82, "Interlock", 4, "Keum Yong", "KLM-72AV", "Korea", ""),
    (41, 5, 34, "24/28", 82, None, 0, "Keum Yong", "KLM-72AV", "Korea", "220"),
    (42, 45, 34, "24/28", 82, None, 0, "Keum Yong", "KLM-72AV", "Korea", "220"),
    (43, 3, 30, "24/28", 72, None, 0, "Keum Yong", "KLM-72AV", "Korea", "210"),
    (44, 14, 34, "18/24", 72, "Rib/Interlock", 2, "Mayer & Cie", "D4-2.2", "Germany", "200"),
    (45, 16, 32, "18/24", 68, None, 0, "Mayer & Cie", "D4-2.2", "Germany", "200"),
]

TOSRIFA_FLAT_ROWS = [
    ("Shima Seiki", "SFF 152", '60"', "Japan", 4, "Double Head"),
    ("Matsuya", "M100", '40"', "China", 8, "Single Head"),
    ("Matsuya", "M 172 SJ", '68"', "China", 8, "Double Head"),
    ("Matsuya", "MC 203 SJ", '80"', "China", 2, "Double Head"),
    ("Matsuya", "Super-NJ 212", '48"', "China", 2, "Duel System"),
]


def render_tosrifa_profile_html() -> str:
    """Render Tosrifa Industries Ltd. Circular & Flat Bed Knitting Machine Profile table."""
    circ_trs = [
        "<tr>"
        '<th style="background-color:#ffffff;color:#0f172a;border:1.5px solid #0f172a;width:7%;">SL No</th>'
        '<th style="background-color:#ffffff;color:#0f172a;border:1.5px solid #0f172a;width:8%;">M/C no</th>'
        '<th style="background-color:#ffffff;color:#0f172a;border:1.5px solid #0f172a;width:8%;">Mc Dia</th>'
        '<th style="background-color:#ffffff;color:#0f172a;border:1.5px solid #0f172a;width:10%;">Gauge</th>'
        '<th style="background-color:#ffffff;color:#0f172a;border:1.5px solid #0f172a;width:9%;">No.of Feeder</th>'
        '<th style="background-color:#ffffff;color:#0f172a;border:1.5px solid #0f172a;width:13%;">Mc Type</th>'
        '<th style="background-color:#ffffff;color:#0f172a;border:1.5px solid #0f172a;width:13%;">Mc Brand</th>'
        '<th style="background-color:#ffffff;color:#0f172a;border:1.5px solid #0f172a;width:14%;">Model</th>'
        '<th style="background-color:#ffffff;color:#0f172a;border:1.5px solid #0f172a;width:9%;">Origin</th>'
        '<th style="background-color:#ffffff;color:#0f172a;border:1.5px solid #0f172a;width:9%;">Capacity /kg</th>'
        "</tr>"
    ]
    for sl, mc_no, dia, gg, feeder, mtype, t_span, brand, model, origin, cap in TOSRIFA_CIRCULAR_ROWS:
        is_shaded = cap == ""
        cell_bg = "background-color:#e2e8f0;" if is_shaded else ""
        tr = ["<tr>"]
        tr.append(f'<td class="total-col" style="{cell_bg}"><strong>{sl}</strong></td>')
        tr.append(f'<td class="total-col" style="{cell_bg}"><strong>{mc_no}</strong></td>')
        tr.append(f'<td class="total-col" style="{cell_bg}"><strong>{dia}</strong></td>')
        tr.append(f'<td class="total-col" style="{cell_bg}"><strong>{html.escape(gg)}</strong></td>')
        tr.append(f'<td class="total-col" style="{cell_bg}"><strong>{feeder}</strong></td>')
        if t_span > 0:
            tr.append(
                f'<td class="total-col" rowspan="{t_span}" style="background-color:#ffffff;font-weight:800;">{html.escape(mtype)}</td>'
            )
        tr.append(f'<td class="total-col" style="{cell_bg}"><strong>{html.escape(brand)}</strong></td>')
        tr.append(f'<td class="total-col" style="{cell_bg}"><strong>{html.escape(model)}</strong></td>')
        tr.append(f'<td class="total-col" style="{cell_bg}"><strong>{html.escape(origin)}</strong></td>')
        tr.append(f'<td class="total-col" style="{cell_bg}"><strong>{html.escape(cap)}</strong></td>')
        tr.append("</tr>")
        circ_trs.append("".join(tr))

    circ_trs.append(
        "<tr>"
        '<td colspan="9" style="background-color:#ffffff;color:#0f172a;font-weight:800;text-align:left;padding:6px 16px;border:1.5px solid #0f172a;">Flat Bed Knitting Machine:</td>'
        '<td class="total-col" style="background-color:#e2e8f0;color:#0f172a;font-weight:800;border:1.5px solid #0f172a;">10480</td>'
        "</tr>"
    )

    flat_trs = [
        "<tr>"
        '<th style="background-color:#ffffff;color:#0f172a;border:1.5px solid #0f172a;width:19%;">M/c Brand</th>'
        '<th style="background-color:#ffffff;color:#0f172a;border:1.5px solid #0f172a;width:19%;">Model No.</th>'
        '<th style="background-color:#ffffff;color:#0f172a;border:1.5px solid #0f172a;width:10%;">Bed</th>'
        '<th style="background-color:#ffffff;color:#0f172a;border:1.5px solid #0f172a;width:15%;">Origin</th>'
        '<th style="background-color:#ffffff;color:#0f172a;border:1.5px solid #0f172a;width:13%;">No.of Qty</th>'
        '<th style="background-color:#ffffff;color:#0f172a;border:1.5px solid #0f172a;width:15%;">No of Head Per M/C</th>'
        '<th style="background-color:#ffffff;color:#0f172a;border:1.5px solid #0f172a;width:9%;"></th>'
        "</tr>"
    ]
    for idx, (f_brand, f_model, f_bed, f_orig, f_qty, f_head) in enumerate(TOSRIFA_FLAT_ROWS):
        tr = [
            "<tr>",
            f'<td class="total-col"><strong>{html.escape(f_brand)}</strong></td>',
            f'<td class="total-col"><strong>{html.escape(f_model)}</strong></td>',
            f'<td class="total-col"><strong>{html.escape(f_bed)}</strong></td>',
            f'<td class="total-col"><strong>{html.escape(f_orig)}</strong></td>',
            f'<td class="total-col"><strong>{f_qty}</strong></td>',
            f'<td class="total-col"><strong>{html.escape(f_head)}</strong></td>',
        ]
        if idx == 0:
            tr.append(
                f'<td class="total-col" rowspan="{len(TOSRIFA_FLAT_ROWS)}" style="font-weight:800;">10000 set/day</td>'
            )
        tr.append("</tr>")
        flat_trs.append("".join(tr))

    return (
        f'<div class="mp-sheet-container" style="max-width:980px;margin-bottom:1rem;">'
        f'<table class="mp-sheet-table" style="font-size:0.84rem;">'
        f'<tbody>{"".join(circ_trs)}</tbody>'
        f"</table>"
        f'<table class="mp-sheet-table" style="font-size:0.84rem;border-top:none;">'
        f'<tbody>{"".join(flat_trs)}</tbody>'
        f"</table>"
        f"</div>"
    )


SM_KNITWEARS_ROWS = [
    # (dia, feeder, mc_type, brand, qty, g28, g24, g20, g18, g14, origin, lycra)
    ('25"', 75, "S/J", "Jiunn Long", 1, "", 1, "", "", "", "Taiwan", ""),
    ('26"', 84, "S/J", "Lisky", 1, "", 1, "", "", "", "Taiwan", ""),
    ('26"', 78, "S/J & Fleece", "Jiunn Long", 2, "", 2, 2, "", "", "Taiwan", ""),
    ('27"', 81, "S/J", "Jiunn Long", 1, "", 1, "", "", "", "Taiwan", ""),
    ('27"', 86, "S/J", "Lisky", 1, "", 1, "", "", "", "Taiwan", ""),
    ('28"', 90, "S/J", "Lisky", 2, "", 2, "", "", "", "Taiwan", ""),
    ('38"', 114, "S/J", "Lisky", 1, "", 1, "", "", "", "Taiwan", ""),
    ('28"', 90, "S/J Open with", "Fukuhara", 1, 1, 1, "", "", "", "Japan", "Yes"),
    ('30"', 96, "S/J Open with", "Fukuhara", 3, 2, 3, "", "", "", "Japan", "Yes"),
    ('30"', 90, "S/J & Fleece", "Jiunn Long", 3, "", 3, 3, "", "", "Taiwan", ""),
    ('30"', 96, "S/J & Fleece", "Lisky", 2, "", 2, 2, "", 1, "Taiwan", ""),
    ('32"', 104, "S/J Open with", "Fukuhara", 2, 2, 2, "", "", "", "Japan", "Yes"),
    ('32"', 96, "S/J & Fleece", "Jiunn Long", 3, "", 3, 3, "", "", "Taiwan", ""),
    ('32"', 102, "S/J & Fleece", "Lisky", 2, "", 2, 2, "", 1, "Taiwan", ""),
    ('34"', 108, "S/J Open with", "Fukuhara", 1, "", 1, "", "", "", "Japan", "Yes"),
    ('34"', 108, "S/J Open with", "Lisky", 3, "", 3, "", "", "", "Taiwan", "Yes"),
    ('34"', 102, "S/J & Fleece", "Jiunn Long", 3, "", 3, 3, "", "", "Taiwan", ""),
    ('34"', 108, "S/J & Fleece", "Lisky", 2, "", 2, 2, "", 1, "Taiwan", ""),
    ('36"', 116, "S/J Open with", "Fukuhara", 3, "", 3, "", "", "", "Japan", "Yes"),
    ('36"', 114, "S/J Open with", "Lisky", 2, "", 2, "", "", "", "Taiwan", "Yes"),
    ('36"', 108, "S/J & Fleece", "Jiunn Long", 2, "", 2, 2, "", "", "Taiwan", ""),
    ('36"', 114, "S/J & Fleece", "Lisky", 2, "", 2, 2, "", 1, "Taiwan", ""),
    ('38"', 120, "S/J Open with", "Fukuhara", 3, "", 3, "", "", "", "Japan", "Yes"),
    ('40"', 128, "S/J Open with", "Fukuhara", 1, "", 1, "", "", "", "Japan", "Yes"),
    ('32"', 44, "Auto Striper", "Pai Lung", 1, "", 1, "", "", "", "Taiwan", "Yes"),
    ('34"', 48, "Auto Striper", "Pai Lung", 2, "", 2, "", "", "", "Taiwan", "Yes"),
    ('36"', 50, "Auto Striper", "Pai Lung", 1, "", 1, "", "", "", "Taiwan", "Yes"),
    ('34"', 108, "Fleece", "Lisky", 1, "", "", 1, "", "", "Taiwan", ""),
    ('36"', 114, "Fleece", "Lisky", 2, "", "", 2, "", "", "Taiwan", ""),
    ('38"', 114, "S/J & Fleece", "Jiunn Long", 2, "", 2, 2, "", "", "Taiwan", ""),
    ('38"', 120, "S/J & Fleece", "Lisky", 2, "", 2, 2, "", "", "Taiwan", ""),
    ('38"', 120, "S/J & Fleece", "Goanglih", 2, "", "", 2, "", "", "Taiwan", ""),
    ('30"', 96, "S/J & Fleece", "Goanglih", 2, "", "", 2, "", "", "Taiwan", ""),
    ('32"', 102, "S/J & Fleece", "Goanglih", 3, "", "", 3, "", 1, "Taiwan", ""),
    ('34"', 108, "S/J & Fleece", "Goanglih", 4, "", "", 4, "", 2, "Taiwan", ""),
    ('36"', 114, "S/J & Fleece", "Goanglih", 4, "", "", 2, "", 2, "Taiwan", ""),
    ('32"', 64, "Rib", "Jiunn Long", 1, "", "", "", 1, "", "Taiwan", "Yes"),
    ('38"', 77, "Rib", "Jiunn Long", 1, "", "", "", 1, "", "Taiwan", "Yes"),
    ('40"', 80, "Rib", "Jiunn Long", 1, "", "", "", 1, "", "Taiwan", "Yes"),
    ('42"', 84, "Rib", "Jiunn Long", 1, "", "", "", 1, "", "Taiwan", "Yes"),
    ('44"', 88, "Rib", "Jiunn Long", 1, "", "", "", 1, "", "Taiwan", "Yes"),
    ('40"', 80, "Rib", "Fukuhara", 1, "", "", "", 1, "", "Japan", "Yes"),
    ('44"', 88, "Rib", "Fukuhara", 2, "", "", "", 2, "", "Japan", "Yes"),
    ('44"', 88, "Rib", "Pai Lung", 2, "", "", "", 2, "", "Taiwan", "Yes"),
    ('42"', 84, "Rib", "Pai Lung", 2, "", "", "", 2, "", "Taiwan", "Yes"),
    ('40"', 80, "Rib", "Pai Lung", 2, "", "", "", 2, "", "Taiwan", "Yes"),
    ('36"', 68, "Rib/Interlock", "Fukuhara", 1, "", 1, "", 1, "", "Taiwan", "Yes"),
    ('34"', 72, "Rib/Interlock", "Lisky", 1, "", 1, "", 1, "", "Taiwan", "Yes"),
    ('34"', 62, "Rib/Interlock", "Fukuhara", 1, "", 1, "", 1, "", "Taiwan", "Yes"),
    ('32"', 68, "Rib/Interlock", "Lisky", 1, "", 1, "", 1, "", "Taiwan", "Yes"),
    ('38"', 68, "Rib/Interlock", "Fukuhara", 1, "", 1, "", 1, "", "Japan", "Yes"),
    ('38"', 76, "Rib/Interlock", "Pai Lung", 1, "", 1, "", 1, "", "Taiwan", "Yes"),
    ('36"', 72, "Rib/Interlock", "Pai Lung", 2, "", 2, "", 2, "", "Taiwan", "Yes"),
    ('34"', 68, "Rib/Interlock", "Pai Lung", 3, "", 2, "", 3, "", "Taiwan", "Yes"),
    ('32"', 64, "Rib/Interlock", "Pai Lung", 1, "", 1, "", 1, "", "Taiwan", "Yes"),
]


def render_sm_profile_html() -> str:
    """Render S.M. Knitwears (S.M. Group) Knitting Machine Profile table."""
    trs = [
        "<tr>"
        '<th rowspan="2" style="background-color:#ffffff;color:#0f172a;border:1.5px solid #0f172a;width:8%;">Dia</th>'
        '<th rowspan="2" style="background-color:#ffffff;color:#0f172a;border:1.5px solid #0f172a;width:8%;">Feeder</th>'
        '<th rowspan="2" style="background-color:#ffffff;color:#0f172a;border:1.5px solid #0f172a;width:16%;">Type of Machine</th>'
        '<th rowspan="2" style="background-color:#ffffff;color:#0f172a;border:1.5px solid #0f172a;width:13%;">Brand</th>'
        '<th rowspan="2" style="background-color:#ffffff;color:#0f172a;border:1.5px solid #0f172a;width:9%;">No of Machine Set</th>'
        '<th colspan="5" style="background-color:#ffffff;color:#0f172a;border:1.5px solid #0f172a;width:25%;">Gauge &amp; Extra cylinder</th>'
        '<th rowspan="2" style="background-color:#ffffff;color:#0f172a;border:1.5px solid #0f172a;width:10%;">Orizin</th>'
        '<th rowspan="2" style="background-color:#ffffff;color:#0f172a;border:1.5px solid #0f172a;width:11%;">Lycra Attachment</th>'
        "</tr>",
        "<tr>"
        '<th style="background-color:#ffffff;color:#0f172a;border:1.5px solid #0f172a;">28</th>'
        '<th style="background-color:#ffffff;color:#0f172a;border:1.5px solid #0f172a;">24</th>'
        '<th style="background-color:#ffffff;color:#0f172a;border:1.5px solid #0f172a;">20</th>'
        '<th style="background-color:#ffffff;color:#0f172a;border:1.5px solid #0f172a;">18</th>'
        '<th style="background-color:#ffffff;color:#0f172a;border:1.5px solid #0f172a;">14</th>'
        "</tr>",
    ]
    for dia, feeder, mtype, brand, qty, g28, g24, g20, g18, g14, origin, lycra in SM_KNITWEARS_ROWS:
        is_shaded = mtype == "Auto Striper"
        bg = ' style="background-color:#e2e8f0;"' if is_shaded else ""
        trs.append(
            f"<tr{bg}>"
            f'<td class="total-col"{bg}><strong>{html.escape(dia)}</strong></td>'
            f'<td class="total-col"{bg}>{feeder}</td>'
            f'<td class="total-col"{bg}>{html.escape(mtype)}</td>'
            f'<td class="total-col"{bg}>{html.escape(brand)}</td>'
            f'<td class="total-col"{bg}><strong>{qty}</strong></td>'
            f'<td class="total-col"{bg}>{g28}</td>'
            f'<td class="total-col"{bg}>{g24}</td>'
            f'<td class="total-col"{bg}>{g20}</td>'
            f'<td class="total-col"{bg}>{g18}</td>'
            f'<td class="total-col"{bg}>{g14}</td>'
            f'<td class="total-col"{bg}>{html.escape(origin)}</td>'
            f'<td class="total-col"{bg}>{html.escape(lycra)}</td>'
            f"</tr>"
        )

    trs.append(
        "<tr>"
        '<td colspan="2" style="border:1.5px solid #0f172a;"></td>'
        '<td colspan="2" style="text-align:center;font-weight:800;border:1.5px solid #0f172a;padding:6px;">Total</td>'
        '<td class="total-col" style="font-weight:800;border:1.5px solid #0f172a;">99</td>'
        '<td class="total-col" style="font-weight:800;border:1.5px solid #0f172a;">5</td>'
        '<td class="total-col" style="font-weight:800;border:1.5px solid #0f172a;">66</td>'
        '<td class="total-col" style="font-weight:800;border:1.5px solid #0f172a;">41</td>'
        '<td class="total-col" style="font-weight:800;border:1.5px solid #0f172a;">26</td>'
        '<td class="total-col" style="font-weight:800;border:1.5px solid #0f172a;">9</td>'
        '<td colspan="2" style="background-color:#e2e8f0;border:1.5px solid #0f172a;"></td>'
        "</tr>"
    )

    return (
        f'<div class="mp-sheet-container" style="max-width:980px;margin-bottom:1rem;">'
        f'<table class="mp-sheet-table" style="font-size:0.84rem;">'
        f'<tbody>{"".join(trs)}</tbody>'
        f"</table>"
        f"</div>"
    )


GRAMTECH_SECTIONS = [
    (
        "High Speed Open Width Single Jersey Machine- 14 Sets",
        True,
        [
            (1, 32, "24,28", 102, "Open Dia", "PAILUNG", "TAIWAN", 3, "S/J , Lycra S/J and All S/J Derivatives Fabric", "100% Lycra Attachment"),
            (2, 32, "24", 102, "Open Dia", "JIUNN LONG", "TAIWAN", 2, "S/J , Lycra S/J and All S/J Derivatives Fabric", "100% Lycra Attachment"),
            (3, 34, "24,28", 108, "Open Dia", "PAILUNG", "TAIWAN", 2, "S/J , Lycra S/J and All S/J Derivatives Fabric", "100% Lycra Attachment"),
            (4, 34, "20,24", 108, "Open Dia", "JIUNN LONG", "TAIWAN", 3, "S/J , Lycra S/J and All S/J Derivatives Fabric", "100% Lycra Attachment"),
            (5, 36, "24", 116, "Open Dia", "PAILUNG", "TAIWAN", 1, "S/J , Lycra S/J and All S/J Derivatives Fabric", "100% Lycra Attachment"),
            (6, 36, "24", 116, "Open Dia", "JIUNN LONG", "TAIWAN", 2, "S/J , Lycra S/J and All S/J Derivatives Fabric", "100% Lycra Attachment"),
            (7, 38, "24", 120, "Open Dia", "PAILUNG", "TAIWAN", 1, "S/J , Lycra S/J and All S/J Derivatives Fabric", "100% Lycra Attachment"),
        ],
    ),
    (
        "Tube Single Jersey Machine- 3 Sets",
        False,
        [
            (8, 26, "24", 78, "Tube Dia", "ZENTEX", "SINGAPUR", 1, "S/J , Lycra S/J and All S/J Derivatives Fabric", "100% Lycra Attachment"),
            (9, 30, "24", 90, "Tube Dia", "ZENTEX", "SINGAPUR", 2, "S/J , Lycra S/J and All S/J Derivatives Fabric", "100% Lycra Attachment"),
        ],
    ),
    (
        "High Speed Tube Fleece Machine- 4 Sets",
        False,
        [
            (10, 34, "20,24", 108, "Tube Dia", "GOANG LIH", "TAIWAN", 2, "Fleece, Baby Fleece, Cross Fleece, Fleece Derivatives", "100% Lycra Attachment"),
            (11, 36, "20,24", 116, "Tube Dia", "GOANG LIH", "TAIWAN", 2, "Fleece, Baby Fleece, Cross Fleece, Fleece Derivatives", "100% Lycra Attachment"),
        ],
    ),
    (
        "TUBE RIB/ INTERLOCK Machine- 7 Sets",
        False,
        [
            (12, 32, "18", 64, "Tube Dia", "ZENTEX", "SINGAPUR", 1, "RIB, Lycra RIB and All RIB Derivatives Fabric", "100% Lycra Attachment"),
            (13, 34, "18", 68, "Tube Dia", "ZENTEX", "SINGAPUR", 1, "RIB, Lycra RIB and All RIB Derivatives Fabric", "100% Lycra Attachment"),
            (14, 36, "18", 72, "Tube Dia", "ZENTEX", "SINGAPUR", 1, "RIB, Lycra RIB and All RIB Derivatives Fabric", "100% Lycra Attachment"),
            (15, 38, "18", 72, "Tube Dia", "ZENTEX", "SINGAPUR", 1, "RIB, Lycra RIB and All RIB Derivatives Fabric", "100% Lycra Attachment"),
            (16, 40, "18,24", 80, "Tube Dia", "JIUNN LONG", "TAIWAN", 1, "RIB, Lycra RIB and All RIB Derivatives Fabric", "100% Lycra Attachment"),
            (17, 42, "18,24,28", 84, "Tube Dia", "JIUNN LONG", "TAIWAN", 2, "RIB, Lycra RIB and All RIB Derivatives Fabric", "100% Lycra Attachment"),
        ],
    ),
    (
        "Flat Knit Machines-4 Sets",
        False,
        [
            (18, 80, "14", 6, "", "KAUO HENG Co.", "Taiwan", 4, "Non Jacquard", "100% Lycra Attachment"),
        ],
    ),
]


def render_gramtech_profile_html() -> str:
    """Render Gram Tech (Sonali Textile) Knitting Machine Profile table matching reference image."""
    trs = [
        '<tr><td colspan="10" style="background-color:#f1f5f9;color:#0f172a;font-weight:800;text-align:center;font-size:1.1rem;padding:8px;border:1.5px solid #0f172a;">Total Number of Machines = 28 Sets</td></tr>'
    ]
    for sec_title, show_headers, rows in GRAMTECH_SECTIONS:
        trs.append(
            f'<tr><td colspan="10" style="background-color:#cbd5e1;color:#0f172a;font-weight:800;text-align:center;font-size:0.98rem;padding:7px;border:1.5px solid #0f172a;">{html.escape(sec_title)}</td></tr>'
        )
        if show_headers:
            trs.append(
                "<tr>"
                '<th style="background-color:#ffffff;color:#0f172a;border:1px solid #0f172a;width:5%;">SL. No.</th>'
                '<th style="background-color:#ffffff;color:#0f172a;border:1px solid #0f172a;width:7%;">Machine Dia</th>'
                '<th style="background-color:#ffffff;color:#0f172a;border:1px solid #0f172a;width:9%;">M/C Gauge</th>'
                '<th style="background-color:#ffffff;color:#0f172a;border:1px solid #0f172a;width:7%;">No. Of Feeders</th>'
                '<th style="background-color:#ffffff;color:#0f172a;border:1px solid #0f172a;width:9%;">Types Of Dia</th>'
                '<th style="background-color:#ffffff;color:#0f172a;border:1px solid #0f172a;width:11%;">Brand</th>'
                '<th style="background-color:#ffffff;color:#0f172a;border:1px solid #0f172a;width:9%;">Origin</th>'
                '<th style="background-color:#ffffff;color:#0f172a;border:1px solid #0f172a;width:8%;">M/c QUANTITY</th>'
                '<th style="background-color:#ffffff;color:#0f172a;border:1px solid #0f172a;width:21%;">Fabric Type</th>'
                '<th style="background-color:#ffffff;color:#0f172a;border:1px solid #0f172a;width:14%;">Remarks</th>'
                "</tr>"
            )
        for sl, dia, gg, fd, dtype, brand, origin, qty, ftype, rem in rows:
            trs.append(
                f"<tr>"
                f'<td class="total-col"><strong>{sl}</strong></td>'
                f'<td class="total-col"><strong>{dia}</strong></td>'
                f'<td class="total-col"><strong>{html.escape(gg)}</strong></td>'
                f'<td class="total-col"><strong>{fd}</strong></td>'
                f'<td class="total-col"><strong>{html.escape(dtype)}</strong></td>'
                f'<td class="total-col"><strong>{html.escape(brand)}</strong></td>'
                f'<td class="total-col"><strong>{html.escape(origin)}</strong></td>'
                f'<td class="total-col"><strong>{qty}</strong></td>'
                f'<td class="total-col"><strong>{html.escape(ftype)}</strong></td>'
                f'<td class="total-col"><strong>{html.escape(rem)}</strong></td>'
                f"</tr>"
            )

    return (
        f'<div class="mp-sheet-container" style="max-width:1020px;margin-bottom:1rem;">'
        f'<table class="mp-sheet-table" style="font-size:0.83rem;">'
        f'<tbody>{"".join(trs)}</tbody>'
        f"</table>"
        f"</div>"
    )


# Session state navigation (3-tier flow: 'landing' -> 'directory' -> 'industry_page')
if "current_view" not in st.session_state:
    st.session_state.current_view = "landing"
if "selected_industry_id" not in st.session_state:
    st.session_state.selected_industry_id = None
if "sidebar_industry_select" not in st.session_state:
    st.session_state.sidebar_industry_select = None
if "preselected_cluster" not in st.session_state:
    st.session_state.preselected_cluster = None


def navigate_to_landing():
    st.session_state.current_view = "landing"
    st.session_state.preselected_cluster = None
    st.session_state._sync_sidebar = True


def navigate_to_directory(cluster_filter=None):
    st.session_state.current_view = "directory"
    st.session_state.preselected_cluster = cluster_filter
    st.session_state._sync_sidebar = True


def navigate_to_industry(industry_id: int):
    st.session_state.selected_industry_id = industry_id
    st.session_state.current_view = "industry_page"
    st.session_state._sync_sidebar = True


# Load all industries for navigation & dashboard
all_industries = db.get_all_industries()
industry_map = {ind["id"]: ind for ind in all_industries}
total_ind = len(all_industries)
visited_cnt = sum(1 for i in all_industries if i["status"] == "Visited")
scheduled_cnt = sum(1 for i in all_industries if i["status"] == "Scheduled")
contacted_cnt = sum(1 for i in all_industries if i["status"] == "Contacted")
total_machines_all = sum(i["machine_count"] for i in all_industries)
total_contacts_all = sum(i["contact_count"] for i in all_industries)
total_updates_all = sum(i["update_count"] for i in all_industries)
profiled_industries = sorted(
    [i for i in all_industries if i["machine_count"] > 0],
    key=lambda x: -x["machine_count"],
)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown(
        '<div style="padding:0.4rem 0 0.8rem 0;">'
        '<div style="font-size:0.72rem;font-weight:700;letter-spacing:1.2px;color:#60a5fa;text-transform:uppercase;">Textile Intelligence</div>'
        '<div style="font-size:1.45rem;font-weight:800;color:#f8fafc;margin-top:2px;">🏭 Knit Industry CRM</div>'
        '<div style="font-size:0.8rem;color:#94a3b8;margin-top:2px;">Factory Profiles • Machinery • Visit Logs</div>'
        "</div>",
        unsafe_allow_html=True,
    )

    if st.button(
        "✨ Executive Landing Page",
        use_container_width=True,
        type="primary" if st.session_state.current_view == "landing" else "secondary",
    ):
        navigate_to_landing()
        st.rerun()

    if st.button(
        f"🏭 Industries Section ({total_ind})",
        use_container_width=True,
        type="primary" if st.session_state.current_view == "directory" else "secondary",
    ):
        navigate_to_directory()
        st.rerun()

    st.divider()
    st.caption("🔍 QUICK JUMP TO INDUSTRY PAGE")

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
        label_visibility="collapsed",
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
# TIER 1: EXECUTIVE LANDING PAGE
# ==============================================================================
if st.session_state.current_view == "landing":
    st.markdown(
        f'<div class="landing-hero">'
        f'<div class="hero-eyebrow">⚡ Bangladesh Knitwear &amp; Textile CRM Intelligence</div>'
        f'<h1 class="hero-title">Knit Industry Machinery &amp; Relationship Hub</h1>'
        f'<p class="hero-subtitle">'
        f'Centralized executive portal tracking <strong>{total_ind} knit composite factories</strong>, '
        f'<strong>{total_machines_all:,} circular &amp; flat-knit machines</strong> across <strong>{len(profiled_industries)} deep-profiled plants</strong>, '
        f'<strong>{total_contacts_all} key decision makers</strong>, and field visit meeting minutes.'
        f"</p>"
        f"</div>",
        unsafe_allow_html=True,
    )

    cta_c1, cta_c2, cta_c3 = st.columns([2.2, 2.2, 3.6])
    with cta_c1:
        if st.button("🚀 Explore All Industries Section →", type="primary", use_container_width=True):
            navigate_to_directory()
            st.rerun()
    with cta_c2:
        if st.button("Visited Factories Directory →", use_container_width=True):
            st.session_state.preselected_status = "Visited"
            navigate_to_directory()
            st.rerun()

    # 4 Glassmorphic Executive KPI Cards
    clusters_set = sorted(list({i["cluster"] for i in all_industries if i["cluster"]}))
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(
            f'<div class="kpi-card">'
            f'<div class="kpi-icon">🏭</div>'
            f'<div class="kpi-value">{total_ind}</div>'
            f'<div class="kpi-label">Partner &amp; Target Factories</div>'
            f'<div class="kpi-sub">100% Geo-Mapped Across {len(clusters_set)} Clusters</div>'
            f"</div>",
            unsafe_allow_html=True,
        )
    with k2:
        st.markdown(
            f'<div class="kpi-card">'
            f'<div class="kpi-icon">⚙️</div>'
            f'<div class="kpi-value">{total_machines_all:,}</div>'
            f'<div class="kpi-label">Logged Knitting Machines</div>'
            f'<div class="kpi-sub">Across {len(profiled_industries)} Full Machine Profile Sheets</div>'
            f"</div>",
            unsafe_allow_html=True,
        )
    with k3:
        st.markdown(
            f'<div class="kpi-card">'
            f'<div class="kpi-icon">👥</div>'
            f'<div class="kpi-value">{total_contacts_all}</div>'
            f'<div class="kpi-label">Verified Factory Contacts</div>'
            f'<div class="kpi-sub">GMs, AGMs, Supply Chain &amp; BUTEX Alumni</div>'
            f"</div>",
            unsafe_allow_html=True,
        )
    with k4:
        st.markdown(
            f'<div class="kpi-card">'
            f'<div class="kpi-icon">📈</div>'
            f'<div class="kpi-value">{visited_cnt + contacted_cnt + scheduled_cnt}</div>'
            f'<div class="kpi-label">Active Pipeline Factories</div>'
            f'<div class="kpi-sub">{visited_cnt} Visited • {contacted_cnt} Contacted • {scheduled_cnt} Scheduled</div>'
            f"</div>",
            unsafe_allow_html=True,
        )

    # Featured Factories with Full Machine Profiles
    st.markdown(
        '<div class="section-banner">'
        '<div><span style="font-size:1.15rem;font-weight:800;color:#f8fafc;">⚙️ Featured Factories with Complete Machine Profiles</span>'
        '<div style="font-size:0.82rem;color:#94a3b8;">Click any factory below to open its dedicated page and view its complete machinery breakdown</div></div>'
        f'<span class="status-badge status-Visited">{len(profiled_industries)} Profiled Plants • {total_machines_all:,} Machines</span>'
        "</div>",
        unsafe_allow_html=True,
    )

    p_cols = st.columns(3)
    for idx, p_ind in enumerate(profiled_industries):
        with p_cols[idx % 3]:
            with st.container(border=True):
                loc_str = ", ".join([p for p in [p_ind["location_area"], p_ind["cluster"]] if p]) or "Bangladesh"
                dist_str = f" • {p_ind['distance_km']} km" if p_ind["distance_km"] else ""
                st.markdown(
                    f'<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:8px;">'
                    f'<div class="factory-card-title">{html.escape(p_ind["name"])}</div>'
                    f'{status_badge_html(p_ind["status"])}'
                    f"</div>"
                    f'<div class="factory-card-loc">📍 {html.escape(loc_str)}{dist_str}</div>'
                    f'<div class="stat-chip-row">'
                    f'<span class="stat-chip stat-chip-highlight">⚙️ {p_ind["machine_count"]} Machines</span>'
                    f'<span class="stat-chip">👥 {p_ind["contact_count"]} Contacts</span>'
                    f'<span class="stat-chip">📝 {p_ind["update_count"]} Visits</span>'
                    f"</div>",
                    unsafe_allow_html=True,
                )
                bc1, bc2 = st.columns([2.2, 1])
                with bc1:
                    if st.button(
                        "Open Factory Page →",
                        key=f"landing_prof_{p_ind['id']}",
                        use_container_width=True,
                        type="primary",
                    ):
                        navigate_to_industry(p_ind["id"])
                        st.rerun()
                with bc2:
                    if p_ind["map_url"]:
                        st.link_button("🗺️ Map", p_ind["map_url"], use_container_width=True)

    # Explore by Industrial Cluster & Pipeline Status
    cl_col, pipe_col = st.columns([1.65, 1.35])

    with cl_col:
        st.markdown(
            '<div class="section-banner">'
            '<div><span style="font-size:1.1rem;font-weight:800;color:#f8fafc;">📍 Explore by Industrial Cluster</span>'
            '<div style="font-size:0.8rem;color:#94a3b8;">Filter the industry section by geographic manufacturing zone</div></div>'
            "</div>",
            unsafe_allow_html=True,
        )
        cluster_stats = defaultdict(lambda: {"count": 0, "machines": 0, "contacts": 0, "visited": 0})
        for ind in all_industries:
            c_name = ind["cluster"] or "Other"
            cluster_stats[c_name]["count"] += 1
            cluster_stats[c_name]["machines"] += ind["machine_count"]
            cluster_stats[c_name]["contacts"] += ind["contact_count"]
            if ind["status"] == "Visited":
                cluster_stats[c_name]["visited"] += 1

        c_grid = st.columns(2)
        for c_idx, (c_name, c_data) in enumerate(
            sorted(cluster_stats.items(), key=lambda x: (-x[1]["count"], x[0]))
        ):
            with c_grid[c_idx % 2]:
                with st.container(border=True):
                    st.markdown(
                        f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                        f'<span style="font-size:1.05rem;font-weight:800;color:#f8fafc;">📍 {html.escape(c_name)}</span>'
                        f'<span class="stat-chip stat-chip-highlight">{c_data["count"]} Factories</span>'
                        f"</div>"
                        f'<div style="font-size:0.8rem;color:#94a3b8;margin:6px 0 8px 0;">'
                        f'⚙️ <strong>{c_data["machines"]}</strong> Mach. • 👥 <strong>{c_data["contacts"]}</strong> Contacts • ✅ <strong>{c_data["visited"]}</strong> Visited'
                        f"</div>",
                        unsafe_allow_html=True,
                    )
                    if st.button(f"View {c_name} Factories →", key=f"cluster_btn_{c_name}", use_container_width=True):
                        navigate_to_directory(cluster_filter=c_name)
                        st.rerun()

    with pipe_col:
        st.markdown(
            '<div class="section-banner">'
            '<div><span style="font-size:1.1rem;font-weight:800;color:#f8fafc;">📊 CRM Outreach Pipeline</span>'
            '<div style="font-size:0.8rem;color:#94a3b8;">Current relationship status across all 32 factories</div></div>'
            "</div>",
            unsafe_allow_html=True,
        )
        status_counts = defaultdict(int)
        for ind in all_industries:
            status_counts[ind["status"]] += 1

        status_colors = {
            "Visited": "#10b981",
            "Follow-up": "#a855f7",
            "Scheduled": "#3b82f6",
            "Contacted": "#f59e0b",
            "Active Client": "#22c55e",
            "New": "#64748b",
        }
        with st.container(border=True):
            for st_name in ["Visited", "Follow-up", "Scheduled", "Contacted", "New"]:
                cnt = status_counts.get(st_name, 0)
                pct = int(round((cnt / total_ind) * 100)) if total_ind else 0
                bar_col = status_colors.get(st_name, "#3b82f6")
                st.markdown(
                    f'<div style="margin-bottom:14px;">'
                    f'<div style="display:flex;justify-content:space-between;font-size:0.86rem;font-weight:700;margin-bottom:5px;">'
                    f"<span>{html.escape(st_name)}</span>"
                    f'<span style="color:#94a3b8;">{cnt} Factories ({pct}%)</span>'
                    f"</div>"
                    f'<div style="width:100%;height:9px;background:rgba(148,163,184,0.15);border-radius:999px;overflow:hidden;">'
                    f'<div style="width:{max(pct, 3)}%;height:100%;background:{bar_col};border-radius:999px;"></div>'
                    f"</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
            if st.button("Open Full Industries Directory →", use_container_width=True, type="primary"):
                navigate_to_directory()
                st.rerun()


# ==============================================================================
# TIER 2: ALL INDUSTRIES DIRECTORY SECTION
# ==============================================================================
elif st.session_state.current_view == "directory" or st.session_state.selected_industry_id not in industry_map:
    # Breadcrumb back to Landing Page
    b_col1, b_col2 = st.columns([1.8, 6.2])
    with b_col1:
        if st.button("← ✨ Landing Page", use_container_width=True):
            navigate_to_landing()
            st.rerun()

    st.markdown(
        f'<div class="industry-header-box" style="padding:1.3rem 1.7rem;">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">'
        f"<div>"
        f'<div style="font-size:0.75rem;font-weight:700;color:#60a5fa;text-transform:uppercase;letter-spacing:1px;">Directory &amp; Search</div>'
        f'<h2 style="margin:2px 0 4px 0;font-size:1.75rem;font-weight:800;color:#f8fafc;">🏭 Knit Industries Section</h2>'
        f'<div style="font-size:0.88rem;color:#94a3b8;">Browse, filter, and open dedicated webpages for all <strong>{total_ind}</strong> knitting factories.</div>'
        f"</div>"
        f'<div class="stat-chip-row">'
        f'<span class="stat-chip stat-chip-highlight">🏭 {total_ind} Factories</span>'
        f'<span class="stat-chip">⚙️ {total_machines_all:,} Machines</span>'
        f'<span class="stat-chip">👥 {total_contacts_all} Contacts</span>'
        f'<span class="stat-chip">✅ {visited_cnt} Visited</span>'
        f"</div>"
        f"</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # Filter & Sort Bar
    f_col1, f_col2, f_col3, f_col4, f_col5 = st.columns([2.5, 1.8, 1.8, 1.6, 1.2])
    with f_col1:
        search_q = st.text_input(
            "🔎 Search Factory or Location",
            placeholder="e.g. MASCO, Fakir, L'Esquire, Tosrifa, Mawna...",
        )
    with f_col2:
        clusters = sorted(list({i["cluster"] for i in all_industries if i["cluster"]}))
        default_clusters = (
            [st.session_state.preselected_cluster]
            if st.session_state.get("preselected_cluster") in clusters
            else []
        )
        selected_clusters = st.multiselect("📍 Cluster", options=clusters, default=default_clusters)
    with f_col3:
        statuses = sorted(list({i["status"] for i in all_industries if i["status"]}))
        default_st = (
            [st.session_state.preselected_status]
            if st.session_state.get("preselected_status") in statuses
            else []
        )
        selected_statuses = st.multiselect("🏷️ Status", options=statuses, default=default_st)
    with f_col4:
        sort_by = st.selectbox(
            "↕️ Sort By",
            ["Most Machines First", "Factory Name (A–Z)", "Distance (Nearest First)", "Most Contacts First"],
        )
    with f_col5:
        view_mode = st.radio("View", ["Cards", "Table"], horizontal=True)

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

    if sort_by == "Most Machines First":
        filtered_industries.sort(key=lambda x: (-x["machine_count"], -x["contact_count"], x["name"]))
    elif sort_by == "Distance (Nearest First)":
        filtered_industries.sort(key=lambda x: (x["distance_km"] if x["distance_km"] is not None else 9999, x["name"]))
    elif sort_by == "Most Contacts First":
        filtered_industries.sort(key=lambda x: (-x["contact_count"], -x["machine_count"], x["name"]))
    else:
        filtered_industries.sort(key=lambda x: x["name"])

    st.caption(f"Showing **{len(filtered_industries)}** of **{total_ind}** industries")

    if view_mode == "Cards":
        cols_per_row = 3
        for idx in range(0, len(filtered_industries), cols_per_row):
            cols = st.columns(cols_per_row)
            for col_idx, ind in enumerate(filtered_industries[idx : idx + cols_per_row]):
                with cols[col_idx]:
                    with st.container(border=True):
                        loc_parts = [p for p in [ind["location_area"], ind["cluster"]] if p]
                        loc_str = ", ".join(loc_parts) if loc_parts else "Location not set"
                        dist_str = f" • {ind['distance_km']} km" if ind["distance_km"] else ""
                        mach_chip_cls = "stat-chip stat-chip-highlight" if ind["machine_count"] > 0 else "stat-chip"
                        visit_txt = f"🕒 Last Visit: {ind['last_visit_date']}" if ind["last_visit_date"] else "🕒 No visits logged yet"

                        st.markdown(
                            f'<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:8px;">'
                            f'<div class="factory-card-title">{html.escape(ind["name"])}</div>'
                            f'{status_badge_html(ind["status"])}'
                            f"</div>"
                            f'<div class="factory-card-loc">📍 {html.escape(loc_str)}{dist_str}</div>'
                            f'<div class="stat-chip-row">'
                            f'<span class="{mach_chip_cls}">⚙️ {ind["machine_count"]} Mach.</span>'
                            f'<span class="stat-chip">👥 {ind["contact_count"]} Contacts</span>'
                            f'<span class="stat-chip">📝 {ind["update_count"]} Visits</span>'
                            f"</div>"
                            f'<div style="font-size:0.75rem;color:#64748b;margin:6px 0 8px 0;">{html.escape(visit_txt)}</div>',
                            unsafe_allow_html=True,
                        )

                        btn_c1, btn_c2 = st.columns([2.2, 1])
                        with btn_c1:
                            if st.button(
                                "Open Industry Page →",
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
# TIER 3: DEDICATED INDUSTRY WEBPAGE
# ==============================================================================
else:
    industry_id = st.session_state.selected_industry_id
    industry = db.get_industry(industry_id)
    contacts = db.get_contacts(industry_id)
    updates = db.get_updates(industry_id)
    machines = db.get_machines(industry_id)
    total_mach_units = sum(m["quantity"] or 0 for m in machines)

    # Top Breadcrumb Bar (Landing Page -> Industries Section -> Current Factory)
    nav_c1, nav_c2, _ = st.columns([1.5, 1.7, 4.8])
    with nav_c1:
        if st.button("✨ Landing Page", use_container_width=True):
            navigate_to_landing()
            st.rerun()
    with nav_c2:
        if st.button("← 🏭 Industries Section", use_container_width=True):
            navigate_to_directory()
            st.rerun()

    # Dedicated Industry Header Box
    loc_bits = [b for b in [industry["location_area"], industry["cluster"]] if b]
    loc_display = ", ".join(loc_bits) if loc_bits else "Location not specified"
    dist_display = f" • {industry['distance_km']} km from Dhaka" if industry["distance_km"] else ""

    st.markdown('<div class="industry-header-box">', unsafe_allow_html=True)
    h_col1, h_col2 = st.columns([3.6, 1.4])
    with h_col1:
        st.markdown(
            f'<div style="font-size:0.75rem;font-weight:700;color:#60a5fa;text-transform:uppercase;letter-spacing:1.1px;margin-bottom:4px;">'
            f'Dedicated Industry Profile • {html.escape(industry["cluster"] or "Bangladesh")}'
            f"</div>"
            f'<h1 style="margin:0 0 8px 0;font-size:2.1rem;font-weight:800;color:#f8fafc;">🏭 {html.escape(industry["name"])}</h1>'
            f'<div style="font-size:0.95rem;color:#cbd5e1;margin-bottom:12px;">📍 <strong>Location:</strong> {html.escape(loc_display)}{html.escape(dist_display)}</div>'
            f'<div class="stat-chip-row">'
            f'<span class="stat-chip stat-chip-highlight">⚙️ {total_mach_units} Total Machines</span>'
            f'<span class="stat-chip">👥 {len(contacts)} Key Contacts</span>'
            f'<span class="stat-chip">📝 {len(updates)} Visit Logs</span>'
            f"</div>",
            unsafe_allow_html=True,
        )
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

        is_fakir = "fakir knitwear" in industry["name"].lower()
        is_masco = "masco" in industry["name"].lower()
        is_renaissance = "renaissance" in industry["name"].lower()
        is_adury = "adury" in industry["name"].lower()
        is_tosrifa = "tosrifa" in industry["name"].lower()
        is_sm = "s.m." in industry["name"].lower()
        is_gramtech = "gram tech" in industry["name"].lower() or "gramtech" in industry["name"].lower()
        fakir_data = db.get_fakir_knitting_data() if is_fakir else None

        if is_gramtech:
            mk1, mk2, mk3, mk4 = st.columns(4)
            mk1.metric("Total Circular Machines", "28 Sets")
            mk2.metric("Flat Knit Machines", "4 Sets")
            mk3.metric("Grand Total Machines", "32 Sets")
            mk4.metric("Machine Brands", "5 (Pailung, Jiunn Long, Zentex, Goang Lih, Kauo Heng)")

            st.markdown(render_gramtech_profile_html(), unsafe_allow_html=True)

        elif is_sm:
            mk1, mk2, mk3, mk4 = st.columns(4)
            mk1.metric("Total Machine Sets", "99")
            mk2.metric("Total Cylinders (28G–14G)", "147 (28G:5 | 24G:66 | 20G:41 | 18G:26 | 14G:9)")
            mk3.metric("Machine Categories", "7 (S/J, Open, Fleece, Striper, Rib, I/L)")
            mk4.metric("Machine Brands", "5 (Jiunn Long, Lisky, Fukuhara, Pai Lung, Goanglih)")

            st.markdown(render_sm_profile_html(), unsafe_allow_html=True)

        elif is_tosrifa:
            mk1, mk2, mk3, mk4 = st.columns(4)
            mk1.metric("Grand Total Machines", "69")
            mk2.metric("Circular Knitting Machines", "45 (10,480 kg/day)")
            mk3.metric("Flat Bed Knitting Machines", "24 (10,000 set/day)")
            mk4.metric("Machine Brands", "6 (Keum Yong, Mayer & Cie, Lisky, Point, Shima Seiki, Matsuya)")

            st.markdown(render_tosrifa_profile_html(), unsafe_allow_html=True)

        elif is_adury:
            mk1, mk2, mk3, mk4 = st.columns(4)
            mk1.metric("Grand Total Machines", "105")
            mk2.metric("Circular Knit Machines", "63")
            mk3.metric("Flat Knit (Collar & Cuff)", "42")
            mk4.metric("Fabrication Sections", "6")

            st.markdown(render_adury_profile_html(), unsafe_allow_html=True)

        elif is_renaissance:
            mk1, mk2, mk3, mk4 = st.columns(4)
            mk1.metric("Grand Total Machines", "79")
            mk2.metric("Circular Knitting Machines", "67")
            mk3.metric("Flat Knitting Machines", "12")
            mk4.metric("Machine Brands", "3 (Pailung, Goang Lih, Matsuya)")

            st.markdown(render_renaissance_profile_html(), unsafe_allow_html=True)

        elif is_masco:
            import masco_data

            mk1, mk2, mk3, mk4 = st.columns(4)
            mk1.metric("Grand Total Machines", "197")
            mk2.metric("Unit-1 (Rupganj — Circular)", "121")
            mk3.metric("Unit-2 (Tongi — Circular)", "48")
            mk4.metric("Unit-2 (Tongi — Collar)", "28")

            m_tab1, m_tab2 = st.tabs(
                [
                    "🏭 Knitting Unit-1 (Kendua, Kanchan, Rupganj — 121 Machines)",
                    "🏭 Knitting Unit-2 (111/1, Darail, Shataish, Tongi — 48 Circular + 28 Collar)",
                ]
            )

            with m_tab1:
                st.markdown(masco_data.render_masco_unit1_html(), unsafe_allow_html=True)

            with m_tab2:
                st.markdown(masco_data.render_masco_unit2_circular_html(), unsafe_allow_html=True)
                st.markdown(masco_data.render_masco_unit2_collar_html(), unsafe_allow_html=True)

        elif is_fakir and fakir_data:
            mk1, mk2, mk3, mk4 = st.columns(4)
            mk1.metric("Grand Total Machines", "167 (165 Opt.)")
            mk2.metric("Knitting Unit-1", "109 (107 Opt.)")
            mk3.metric("Knitting Unit-2", "58")
            mk4.metric("Machine Brands", "5")

            fk_tab1, fk_tab2, fk_tab3 = st.tabs(
                [
                    "🏭 Knitting Unit-1 (Sheet 1 — 109 Machines)",
                    "🏭 Knitting Unit-2 & Overall Summary (Sheet 2 — 58 Machines)",
                    "📊 Consolidated Table (Unit 1 + Unit 2)",
                ]
            )

            with fk_tab1:
                u1_blocks = fakir_data["unit1_blocks"]
                # Group blocks by row_start so left (col 1) and right (col 11) appear side by side just like Sheet1
                u1_by_row = defaultdict(list)
                for b in u1_blocks:
                    u1_by_row[b["row_start"]].append(b)
                for r_start in sorted(u1_by_row.keys()):
                    pair = sorted(u1_by_row[r_start], key=lambda x: x["col_start"])
                    c_left, c_right = st.columns(2)
                    with c_left:
                        st.markdown(render_fakir_block_html(pair[0]), unsafe_allow_html=True)
                    if len(pair) > 1:
                        with c_right:
                            st.markdown(render_fakir_block_html(pair[1]), unsafe_allow_html=True)

                st.markdown(render_fakir_summary_card_html(fakir_data["unit1_summary"]), unsafe_allow_html=True)

            with fk_tab2:
                u2_blocks = fakir_data["unit2_blocks"]
                u2_by_row = defaultdict(list)
                for b in u2_blocks:
                    u2_by_row[b["row_start"]].append(b)
                for r_start in sorted(u2_by_row.keys()):
                    pair = sorted(u2_by_row[r_start], key=lambda x: x["col_start"])
                    c_left, c_right = st.columns(2)
                    with c_left:
                        st.markdown(render_fakir_block_html(pair[0]), unsafe_allow_html=True)
                    if len(pair) > 1:
                        with c_right:
                            st.markdown(render_fakir_block_html(pair[1]), unsafe_allow_html=True)

                st.markdown(render_fakir_summary_card_html(fakir_data["unit2_summary"]), unsafe_allow_html=True)
                st.markdown(render_fakir_summary_card_html(fakir_data["overall_summary"]), unsafe_allow_html=True)

            with fk_tab3:
                st.markdown(render_fakir_summary_card_html(fakir_data["overall_summary"]), unsafe_allow_html=True)
                if machines:
                    st.markdown(render_machine_profile_html(industry, machines), unsafe_allow_html=True)

        elif not machines:
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
