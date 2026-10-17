from app.ingestion.loader import load_pdf
from app.ingestion.chunker import chunk_documents
from app.ingestion.embedder import get_embeddings

from app.retrieval.vector_store import (
    create_vector_store,
    retrieve_with_mmr
)

from app.correction.retrieval_refiner import refine_query


PDF_PATH = "data/reimbursement/FIN_AP_ExpenseandReimbursementPolicy.pdf"


# 1. Load document
documents = load_pdf(PDF_PATH)


# 2. Create chunks
chunks = chunk_documents(documents)


# 3. Load embeddings
embeddings = get_embeddings()


# 4. Create vector store
vector_store = create_vector_store(
    chunks,
    embeddings
)


# This is the query after the first rewrite
query = (
    "Is Wi-Fi or internet expense eligible for employee "
    "reimbursement under the reimbursement policy?"
)


print("\n==============================")
print("REFINED RETRIEVAL TEST")
print("==============================")


print("\nInitial query:")
print(query)


# 5. Refine the query
refined_query = refine_query(query)


print("\nRefined query:")
print(refined_query)


# 6. Retrieve again using the refined query
results = retrieve_with_mmr(
    vector_store,
    refined_query,
    k=5
)


# 7. Display results
print("\n==============================")
print("REFINED RETRIEVED DOCUMENTS")
print("==============================")


for i, document in enumerate(results):

    print(f"\n--- Result {i + 1} ---")

    print(
        f"Page: {document.metadata.get('page')}"
    )

    print("\nContent:")

    print(
        document.page_content[:500]
    )