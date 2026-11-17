"""Load fragment records from the JSONL file made by scripts/convert_archive.py."""

import json

from .config import FRAGMENTS_PATH


def load_records(path=FRAGMENTS_PATH):
    """Return the fragment records as a list of dicts, in file order."""
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def filter_by_entrant(records, entrant):
    """Keep one contributor's fragments (case-insensitive). None keeps everyone."""
    if not entrant:
        return records
    wanted = entrant.strip().lower()
    return [r for r in records if r["entrant"].lower() == wanted]
