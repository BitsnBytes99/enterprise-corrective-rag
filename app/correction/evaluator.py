from app.generation.llm import get_llm


def evaluate_document(query, document):
    """
    Evaluate whether a retrieved document is relevant to the query.
    """

    llm = get_llm()

    evaluation_prompt = f"""
You are a retrieval evaluator for an enterprise RAG system.

Determine whether the retrieved document is relevant to answering
the user's question.

User question:
{query}

Retrieved document:
{document.page_content}

Return exactly one label:

RELEVANT
NOT_RELEVANT

Do not provide an explanation.
"""

    response = llm.invoke(evaluation_prompt)

    return response.content.strip()