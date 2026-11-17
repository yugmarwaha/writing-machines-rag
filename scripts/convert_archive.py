"""Convert the class archive spreadsheet into JSONL records for the RAG pipeline.

Usage: python scripts/convert_archive.py [input.xlsx] [output.jsonl]

Each output line is one fragment. `id` is the "Fragment No." the website
displays (what the chatbot cites); `archive_id` is the permanent entry ID from
the spreadsheet's `id` column. The `text` field (fragment + annotation)
is what gets embedded; the other fields are kept for filtering and citation.
"""

import json
import math
import sys
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parent.parent
DEFAULT_IN = REPO / "writing_machines.xlsx"
DEFAULT_OUT = REPO / "data" / "fragments.jsonl"


def clean(value):
    """Strip whitespace; turn empty cells into None."""
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    value = str(value).strip()
    return value or None


def to_record(row, site_no):
    fragment = clean(row["fragment"])
    annotation = clean(row["annotation"])
    return {
        "id": site_no,
        "archive_id": int(row["id"]),
        "entrant": clean(row["entrant"]),
        "category": clean(row["category"]),
        "text": f"{fragment}\n\nAnnotation: {annotation}",
        "fragment": fragment,
        "annotation": annotation,
        "source": clean(row["source"]),
        "source_url": clean(row["source_url"]),
        "is_quote": bool(row["is_quote"]),
    }


def main(src=DEFAULT_IN, dst=DEFAULT_OUT):
    df = pd.read_excel(src)
    # The website numbers entries 1, 2, 3... in the order added, skipping deleted
    # ones, so its "Fragment No." is the rank by the spreadsheet id.
    records = [to_record(row, n) for n, (_, row) in enumerate(df.sort_values("id").iterrows(), 1)]

    ids = [r["id"] for r in records]
    assert len(ids) == len(set(ids)), "duplicate fragment IDs"
    for r in records:
        assert r["fragment"] and r["annotation"] and r["entrant"], f"missing text in {r['id']}"

    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    with open(dst, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Wrote {len(records)} records to {dst}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
