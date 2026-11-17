# scripts/ — one-off data tools

| File | What it does |
| --- | --- |
| `convert_archive.py` | Reads `writing_machines.xlsx` (repo root) and writes `data/fragments.jsonl`. |

Run from the repo root: `python scripts/convert_archive.py` (optionally `[input.xlsx] [output.jsonl]`). It sorts rows by the spreadsheet id, numbers them 1, 2, 3… to match the website's "Fragment No.", and fails if an ID is duplicated or a fragment, annotation, or contributor is empty. Rerun it whenever a new spreadsheet export arrives, then rebuild the index (`python -m rag build`).

Needs `pandas` and `openpyxl` (in `requirements.txt`). The pipeline itself does not.
