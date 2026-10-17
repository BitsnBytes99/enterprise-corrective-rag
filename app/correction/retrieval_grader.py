from app.generation.llm import get_llm


def grade_retrieval(query, documents):
    """
    Evaluate the overall quality of retrieved documents.
    """

    llm = get_llm()

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    prompt = f"""
You are a retrieval quality evaluator for an enterprise RAG system.

Evaluate whether the retrieved context is sufficient to answer
the user's question.

User question:
{query}

Retrieved context:
{context}

Classify the retrieval into exactly one of these categories:

CORRECT
- The context contains sufficient information to answer the question.

AMBIGUOUS
- The context is related to the question but is incomplete or only
  partially sufficient.

INCORRECT
- The context is irrelevant or does not provide useful information
  for answering the question.

Return ONLY one label:
CORRECT
AMBIGUOUS
INCORRECT
"""

    response = llm.invoke(prompt)

    result = response.content.strip().upper()

    if "CORRECT" in result:
        return "CORRECT"

    if "AMBIGUOUS" in result:
        return "AMBIGUOUS"

    if "INCORRECT" in result:
        return "INCORRECT"

    return "AMBIGUOUS"