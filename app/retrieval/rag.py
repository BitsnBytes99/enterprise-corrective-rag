from app.generation.llm import get_llm
from app.generation.prompt import RAG_PROMPT


def generate_answer(query, documents):
    """
    Generate an answer using the retrieved documents.
    """

    context = "\n\n".join(
        document.page_content for document in documents
    )

    prompt = RAG_PROMPT.invoke(
        {
            "context": context,
            "question": query,
        }
    )

    llm = get_llm()

    response = llm.invoke(prompt)

    return response.content