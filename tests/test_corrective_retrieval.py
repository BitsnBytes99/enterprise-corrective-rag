from app.ingestion.loader import load_pdf
from app.ingestion.chunker import chunk_documents
from app.ingestion.embedder import get_embeddings

from app.retrieval.vector_store import (
    create_vector_store,
    retrieve_with_mmr
)

from app.correction.query_rewriter import rewrite_query
from app.correction.retrieval_grader import grade_retrieval


PDF_PATH = "data/reimbursement/FIN_AP_ExpenseandReimbursementPolicy.pdf"


# 1. Load document
documents = load_pdf(PDF_PATH)


# 2. Create chunks
chunks = chunk_documents(documents)


# 3. Load embedding model
embeddings = get_embeddings()


# 4. Create vector store
vector_store = create_vector_store(
    chunks,
    embeddings
)


# 5. Original user query
query = "Can I get money back for wifi?"


print("\n==============================")
print("CORRECTIVE RETRIEVAL TEST")
print("==============================")


print("\nOriginal query:")
print(query)


# 6. Rewrite query
rewritten_query = rewrite_query(query)


print("\nRewritten query:")
print(rewritten_query)


# 7. Retrieve using MMR
results = retrieve_with_mmr(
    vector_store,
    rewritten_query,
    k=5
)


# 8. Grade retrieved context
grade = grade_retrieval(
    rewritten_query,
    results
)


print("\n==============================")
print("RETRIEVAL GRADE")
print("==============================")


print(f"\nGrade: {grade}")


# 9. Display retrieved documents
print("\n==============================")
print("RETRIEVED DOCUMENTS")
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