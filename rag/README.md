# rag/ — the pipeline

Question in → relevant fragments retrieved → local model answers and cites them. Run it with `python -m rag` from the repo root (see the [root README](../README.md)).

## Files

| File | What it does |
| --- | --- |
| `config.py` | Every setting: data path, models, top-k, temperature, seed. Change settings here only. |
| `records.py` | Loads `data/fragments.jsonl`; filters by contributor. |
| `index.py` | Embeds fragments with Ollama, saves/loads the index, ranks fragments for a question. |
| `generate.py` | System prompt, fragment formatting, call to the chat model, cited-ID extraction. |
| `__main__.py` | Command line: `build` and `ask`. |

## How it works

1. **Build** (`python -m rag build`). Each record's `text` (fragment + annotation) goes to the embedding model, which returns a vector — a list of numbers capturing meaning. Vectors are scaled to length 1 and saved in `indexes/vectors.npy`; `indexes/meta.json` stores the model name and fragment IDs so a stale index is refused.
2. **Retrieve** (`ask`). The question is embedded the same way. A dot product with every fragment vector gives cosine similarity (1 = same direction/meaning). The top `TOP_K` win. `--entrant` limits ranking to one contributor's fragments.
3. **Generate.** The chosen fragments (site number, contributor, category, source, quotation, annotation) are pasted into the prompt. The system prompt tells the model to use only them and cite as `[#112]`.
4. **Check.** The CLI lists the cited IDs and warns if the model cited a fragment it was not given.

`--all --entrant NAME` skips steps 1–2 and gives the model every fragment from that contributor (the "all fragments" benchmark condition).

## Decisions (Nov 16–17, confirmed by Yug unless marked provisional)

| Setting | Value | Why |
| --- | --- | --- |
| Runtime | Ollama, installed natively, no Docker | Runs on Mac and Windows; on Mac, Docker can't use the Apple GPU, and Docker Desktop costs RAM on 16 GB laptops. Docker only if we deploy. Code talks to `localhost:11434` either way. |
| Index | NumPy matrix, no vector DB | 161 fragments; searching them all is instant. |
| Fragment IDs | Website "Fragment No." (`id` in the JSONL) | What readers see on the site. |
| Top-k | 5 | Starting point; benchmark can compare others. |
| Embedding model | `nomic-embed-text` (274 MB) | **Provisional (Claude's pick).** Small, common, runs anywhere. Needs the `search_document:`/`search_query:` prefixes. |
| Chat model | `llama3.2:3b` (2 GB) | Confirmed by Yug (Nov 17): enough for a ~160-fragment archive; fits 16 GB RAM easily. |
| Temperature / seed | 0.2 / 42 | **Provisional (Claude's pick).** Repeatable benchmark runs. |

## Changing the model

Edit `CHAT_MODEL` or `EMBED_MODEL` in `config.py` and `ollama pull` the new name. Changing `EMBED_MODEL` requires `python -m rag build` again (the CLI refuses an old index), and remove or change the prefixes if the new model doesn't use them.
