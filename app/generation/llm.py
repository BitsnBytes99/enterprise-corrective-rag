from langchain_ollama import ChatOllama


def get_llm():
    """
    Create and return the local Ollama chat model.
    """

    llm = ChatOllama(
        model="qwen3:8b",
        temperature=0
    )

    return llm