"""Ask the local chat model to answer from the fragments it is given."""

import re

import ollama

from . import config

SYSTEM_PROMPT = """You answer questions about a class archive of fragments: quotations \
(or paraphrases) chosen by students, each with the student's annotation.

Rules:
- Use only the fragments provided below. Do not rely on outside knowledge of the sources.
- Cite every fragment you use by its number in square brackets, e.g. [#112].
- Explain how each cited fragment supports your point.
- If the fragments do not support an answer, say so plainly."""


def format_fragment(r):
    lines = [f"[#{r['id']}] Contributor: {r['entrant']} | Category: {r['category']}"]
    if r.get("source"):
        lines.append(f"Source: {r['source']}")
    label = "Quotation" if r["is_quote"] else "Fragment (not a direct quotation)"
    lines.append(f"{label}: {r['fragment']}")
    lines.append(f"Annotation: {r['annotation']}")
    return "\n".join(lines)


def build_prompt(question, records):
    context = "\n\n".join(format_fragment(r) for r in records)
    return f"Fragments:\n\n{context}\n\nQuestion: {question}"


def answer(question, records):
    """Return the model's answer to `question` using only `records` as evidence."""
    response = ollama.chat(
        model=config.CHAT_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_prompt(question, records)},
        ],
        options={"temperature": config.TEMPERATURE, "seed": config.SEED},
    )
    return response["message"]["content"]


def cited_ids(text):
    """Fragment numbers cited in an answer, e.g. "[#112]" -> {112}."""
    return {int(n) for n in re.findall(r"#(\d+)", text)}
