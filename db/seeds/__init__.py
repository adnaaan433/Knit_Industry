"""Run all idempotent factory machine profile seeds."""

from db.seeds import adury, fakir, gramtech, lesquire, masco, renaissance, sm_group, tosrifa

ALL_SEEDS = [
    lesquire.seed,
    fakir.seed,
    masco.seed,
    renaissance.seed,
    adury.seed,
    tosrifa.seed,
    sm_group.seed,
    gramtech.seed,
]


def run_all_seeds(conn):
    for seed_fn in ALL_SEEDS:
        seed_fn(conn)
