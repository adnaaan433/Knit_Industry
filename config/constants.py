"""Single source of truth for application constants."""

STATUS_OPTIONS = [
    "New",
    "Contacted",
    "Scheduled",
    "Visited",
    "Follow-up",
    "Active Client",
]

STATUS_RANK = {
    "New": 0,
    "Contacted": 1,
    "Scheduled": 2,
    "Visited": 3,
    "Follow-up": 4,
    "Active Client": 5,
}

FABRICATION_TYPES = [
    "Single Jersey",
    "Fleece",
    "H/Jersey",
    "Rib",
    "Interlock",
]

DOUBLE_BED_FABRICATIONS = {"rib", "interlock"}

VISIT_TYPES = [
    "Factory Visit",
    "Phone / WhatsApp Follow-up",
    "Sample / Technical Trial",
    "Commercial / Price Discussion",
    "General Update",
]

DEFAULT_BRANDS = [
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
]
