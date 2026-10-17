from app.generation.llm import get_llm


def rewrite_query(query):
    """
    Rewrite a user query to improve document retrieval.
    """

    llm = get_llm()

    prompt = f"""
You are a query rewriting component in an enterprise employee
assistant and Corrective RAG system.

Rewrite the user's question to improve retrieval from enterprise
documents such as HR policies, IT policies, leave policies,
reimbursement policies, and onboarding documents.

Rules:

1. Preserve the user's original intent exactly.
2. Do not change "reimbursement" into "refund".
3. Use precise enterprise-policy terminology when appropriate.
4. Expand informal terms into clearer terminology.
5. Do not add assumptions or information that was not implied.
6. Do not answer the question.
7. Return ONLY the rewritten query.

Example:

User:
"Can I get money back for wifi?"

Better rewrite:
"Is Wi-Fi or internet expense eligible for employee reimbursement
under the reimbursement policy?"

User question:
{query}

Rewritten query:
"""

    response = llm.invoke(prompt)

    return response.content.strip()