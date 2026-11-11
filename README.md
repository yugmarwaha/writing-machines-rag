# Writing Machines RAG

A collaborative project for English 178: Writing Machines. We’re building a chatbot that answers questions about our class fragment archive and cites the fragments it uses.

**Status:** Planning. The pipeline and setup instructions are forthcoming.

## Planned pipeline

1. **Archive preparation.** Convert archive entries into records that preserve fragment IDs, contributors, quotations, and annotations.
2. **Retrieval.** Embed the fragment text and build a searchable index. Retrieve relevant fragments for a question, with the option to filter by contributor.
3. **Answer generation.** Pass the retrieved text and fragment IDs to an existing open-weight language model running locally. Ask the model to explain its interpretation and cite the fragments that support it.

The initial plan is to run the model on a MacBook. The specific model and runtime are still open.

## Collaboration and evaluation

All three students will build the shared pipeline together. Once it works, each student will use it to investigate a different research question and evaluate their own results.

One planned study asks whether the chatbot can find an idea that keeps coming up in a contributor’s fragments and explain how it might have influenced the quotes they picked. It will compare the same model’s answers when given all of that contributor’s fragments, if they fit, and when given only a retrieved subset. Each answer will be checked for support from at least two specific fragments.

## Archive

[Writing Machines class fragment archive](https://amarella1697.github.io/ENGL-178-Writing-Machines-Website/)

## Next steps

See [TODO.md](TODO.md) for the planned files and build checklist.
