from app.generation.llm import get_llm


def refine_query(query):
    """
    Refine a query when retrieval is relevant but incomplete.
    """

    llm = get_llm()

    prompt = f"""
You are a retrieval refinement component in an enterprise RAG system.

The initial retrieval found partially relevant information, but the
context was not sufficient to answer the user's question confidently.

Create a more specific search query that focuses on the exact policy
concept needed to answer the question.

Rules:

1. Preserve the original intent.
2. Focus on the specific policy category or expense involved.
3. Use terminology likely to appear in enterprise policy documents.
4. Do not answer the question.
5. Do not invent policy rules.
6. Return ONLY the refined search query.

Original query:
{query}

Refined search query:
"""

    response = llm.invoke(prompt)

    return response.content.strip()