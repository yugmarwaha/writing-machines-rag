# Project TODO

Agree on a language and local model runtime before choosing source filenames. Agree on what each part passes to the next.

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

- [ ] **Archive preparation.** Add an import script and a small sample dataset. Keep the fragment ID, contributor, quotation, and annotation for each record. Confirm what archive material can be committed before adding the full dataset.
- [ ] **Retrieval.** Add a module that builds the index and returns relevant fragment text and IDs. Include a contributor filter.
- [ ] **Answer generation.** Add a module that passes retrieved fragments to the local model and asks it to cite fragment IDs. Add one entry point that runs a question through the whole pipeline.

## Setup and handoff

- [ ] Add a dependency file once the team chooses a language and libraries.
- [ ] Update the [README](README.md) with installation steps, the model and runtime used, and a sample question with the command to run it.
- [ ] Run one sample question together and check that the cited IDs match the fragments the model received.

