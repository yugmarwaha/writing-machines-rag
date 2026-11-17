# Agent guide

Read this first, then the [root README](README.md) (setup and usage) and the README of any folder you touch. Every folder's README explains its files and the decisions behind them, so you shouldn't need to read code to orient yourself.

## Project

An English 178 (Writing Machines) class project. Three students (Yug, Reyansh, Arvind) are building a command-line RAG chatbot over the class fragment archive. It uses a small open-weight model run locally with Ollama. Yug owns the pipeline and model integration, Reyansh the archive data, and Arvind benchmarking. A chat interface belongs to a teammate and is out of scope for the pipeline code. Course notes, deadlines, and research questions live outside this repo in the parent folder (`../project-context.md`), which may not exist on teammates' machines.

## Get to a working state

1. Follow README "Setup" steps 1–6 (Python 3.10+, native Ollama, `ollama pull` both models, venv + `pip install -r requirements.txt`, `python -m rag build`).
2. Verify: `python -m rag ask "Can a machine understand meaning?"` prints 5 retrieved fragments, an answer, and `Cited: [...]` with no WARNING line.
3. If the spreadsheet changed: `python scripts/convert_archive.py`, then `python -m rag build`.

There is no test suite yet. Steps 2–3 are the check.

## Conventions

- **Folder READMEs are part of the code.** When you change a module, setting, or decision, update that folder's README (and the root README if usage or setup changes) in the same change. A new folder gets its own README and a row in the root README's repository map.
- **Settings live only in `rag/config.py`.** Record each one in the decisions table in `rag/README.md`. Mark it **Provisional (Claude's pick)** until a human confirms it.
- **Tell Yug about every decision**, including small parameters such as top-k, models, temperature, and prompt wording. Say which choices were his and which were yours.
- **Never edit `data/fragments.jsonl` by hand.** Fix the spreadsheet or the converter and regenerate it.
- **Fragment numbers:** the JSONL `id` and the chatbot's `[#N]` citations use the website's "Fragment No.". `archive_id` is the spreadsheet's internal id. They differ, e.g. site #112 is archive id 120.
- **Must run on 16 GB Mac and Windows laptops.** Use `pathlib`, avoid shell-only steps, and keep models small enough to need about 3 GB of RAM. Use native Ollama, not Docker (Docker is only for deployment, if that happens).
- **Don't commit or push** unless Yug asks.

## Open items

See [TODO.md](TODO.md). Both models are confirmed (`llama3.2:3b`, `nomic-embed-text`); temperature 0.2 and seed 42 are still provisional. Teammates test Windows setup themselves. Saving `--all` and retrieved answers side by side for benchmarking is a possible next step.
