"""Command-line entry point.

    python -m rag build                          # embed the archive (run once, and after data changes)
    python -m rag ask "question"                 # retrieve top fragments, then answer
    python -m rag ask "question" --entrant "Yug Marwaha"
    python -m rag ask "question" --entrant "Yug Marwaha" --all   # skip retrieval: give the model all of them
"""

import argparse

import ollama

from . import config
from .generate import answer, cited_ids
from .index import build_index, load_index, search
from .records import filter_by_entrant, load_records


def cmd_build(args):
    records = load_records()
    print(f"Embedding {len(records)} fragments with {config.EMBED_MODEL}...")
    build_index(records)
    print(f"Saved index to {config.INDEX_DIR}")


def cmd_ask(args):
    records = load_records()
    if args.all:
        if not args.entrant:
            raise SystemExit("--all needs --entrant (the whole archive is too much for one prompt).")
        chosen = filter_by_entrant(records, args.entrant)
        if not chosen:
            raise SystemExit(f"No fragments found for contributor {args.entrant!r}.")
        print(f"Using all {len(chosen)} fragments from {chosen[0]['entrant']} (no retrieval).\n")
    else:
        vectors = load_index(records)
        hits = search(args.question, records, vectors, k=args.k, entrant=args.entrant)
        chosen = [r for _, r in hits]
        print(f"Retrieved {len(hits)} fragments:")
        for score, r in hits:
            print(f"  #{r['id']:<4} {score:.3f}  {r['entrant']}: {r['fragment'][:70]}")
        print()

    print(f"Answer ({config.CHAT_MODEL}):\n")
    text = answer(args.question, chosen)
    print(text)

    # Check that the model only cited fragments it was actually given.
    given = {r["id"] for r in chosen}
    cited = cited_ids(text)
    print(f"\nCited: {sorted(cited) or 'none'}")
    if cited - given:
        print(f"WARNING: cited fragments the model was not given: {sorted(cited - given)}")


def main():
    parser = argparse.ArgumentParser(prog="python -m rag", description="Writing Machines archive chatbot")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("build", help="embed the archive and save the index").set_defaults(func=cmd_build)

    ask = sub.add_parser("ask", help="answer a question from the archive")
    ask.add_argument("question")
    ask.add_argument("--entrant", help='only use this contributor\'s fragments, e.g. "Yug Marwaha"')
    ask.add_argument("-k", type=int, default=config.TOP_K, help=f"fragments to retrieve (default {config.TOP_K})")
    ask.add_argument("--all", action="store_true", help="skip retrieval and give the model all of --entrant's fragments")
    ask.set_defaults(func=cmd_ask)

    args = parser.parse_args()
    try:
        args.func(args)
    except ConnectionError:
        raise SystemExit("Can't reach Ollama on localhost:11434. Start the Ollama app (or run `ollama serve`) and try again.")
    except ollama.ResponseError as e:
        if e.status_code == 404:
            raise SystemExit(f"Model not downloaded: {e.error}\nRun: ollama pull {config.CHAT_MODEL} && ollama pull {config.EMBED_MODEL}")
        raise


if __name__ == "__main__":
    main()
