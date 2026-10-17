from langchain_chroma import Chroma


def create_vector_store(documents, embeddings):
    """
    Create a fresh Chroma vector store from document chunks.
    """

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        ids=[
            f"chunk_{i}"
            for i in range(len(documents))
        ],
        collection_name="enterprise_documents",
        persist_directory="chroma_db"
    )

    return vector_store


def retrieve_with_mmr(vector_store, query, k=5):
    """
    Retrieve diverse documents using Maximal Marginal Relevance.
    """

    documents = vector_store.max_marginal_relevance_search(
        query,
        k=k,
        fetch_k=10,
        lambda_mult=0.5
    )

    return documents