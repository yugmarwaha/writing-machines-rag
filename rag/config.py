"""Settings shared by the whole pipeline. Change them here, not in the modules.

Each value is a team decision; see rag/README.md for why it was chosen.
"""

from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Data in, index out. indexes/ is gitignored because it is rebuilt from the data.
FRAGMENTS_PATH = REPO / "data" / "fragments.jsonl"
INDEX_DIR = REPO / "indexes"

# Ollama models. Both run on a 16 GB laptop (Mac or Windows).
EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL = "llama3.2:3b"

# nomic-embed-text was trained with these task prefixes; leaving them out
# lowers retrieval quality. Other embedding models may not need them.
DOC_PREFIX = "search_document: "
QUERY_PREFIX = "search_query: "

# How many fragments retrieval hands to the model per question.
TOP_K = 5

# Low temperature and a fixed seed so benchmark runs are repeatable.
TEMPERATURE = 0.2
SEED = 42
