# Project TODO

Language: Python. Runtime: Ollama, installed natively (Nov 17). Each part passes JSONL records → index → retrieved records → answer; see [rag/README.md](rag/README.md).

## Team ownership

- **Reyansh** converts the archive into a dataset.
- **Yug** builds the RAG pipeline and connects it to a model.
- **Arvind** benchmarks the shared chatbot.
- **All three** contribute to documentation. 

## Team target dates

| Milestone | Date recorded by team |
| --- | --- |
| Archive index | November 14 |
| RAG pipeline | November 17 |
| Benchmarking | November 19 |

The course project drafts are on November 16 and 20. Clarify whether “archive index” means Reyansh’s dataset handoff or the searchable index built during pipeline work.

## Shared RAG pipeline

- [x] **Archive preparation.** Add an import script and a small sample dataset. Keep the fragment ID, contributor, quotation, and annotation for each record. The team confirmed the archive spreadsheet and generated JSONL can be committed. Converter: `scripts/convert_archive.py` → `data/fragments.jsonl` (see the dataset note in the parent folder).
- [x] **Retrieval.** Add a module that builds the index and returns relevant fragment text and IDs. Include a contributor filter.
- [x] **Answer generation.** Add a module that passes retrieved fragments to the local model and asks it to cite fragment IDs. Add one entry point that runs a question through the whole pipeline.

## Setup and handoff

- [x] Add a dependency file once the team chooses a language and libraries.
- [x] Update the [README](README.md) with installation steps, the model and runtime used, and a sample question with the command to run it.
- [ ] Reyansh and Arvind set up from the README on their own laptops (they handle Windows themselves).
- [x] Chat model: `llama3.2:3b` (confirmed Nov 17; no 4B comparison). Embedding model `nomic-embed-text` confirmed Nov 17.
- [ ] Run one sample question together and check that the cited IDs match the fragments the model received. (The CLI now warns automatically; also check that each citation's *content* matches — the Nov 17 smoke test misdescribed #97.)
- [ ] Command-line only for now; a chat interface belongs to another teammate.

