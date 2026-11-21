"""Status badge and single STATUS_COLORS dictionary."""

import html

STATUS_COLORS = {
    "New": {"css": "crm-badge-new", "hex": "#64748b"},
    "Contacted": {"css": "crm-badge-contacted", "hex": "#d97706"},
    "Scheduled": {"css": "crm-badge-scheduled", "hex": "#2563eb"},
    "Visited": {"css": "crm-badge-visited", "hex": "#16a34a"},
    "Follow-up": {"css": "crm-badge-follow-up", "hex": "#9333ea"},
    "Active Client": {"css": "crm-badge-active", "hex": "#0d9488"},
}


def status_badge(status: str) -> str:
    st_clean = (status or "New").strip()
    meta = STATUS_COLORS.get(st_clean, STATUS_COLORS["New"])
    return f'<span class="crm-badge {meta["css"]}">{html.escape(st_clean)}</span>'
