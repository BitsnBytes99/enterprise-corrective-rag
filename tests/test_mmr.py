from app.ingestion.loader import load_pdf
from app.ingestion.chunker import chunk_documents
from app.ingestion.embedder import get_embeddings
from app.retrieval.vector_store import create_vector_store


PDF_PATH = "data/reimbursement/FIN_AP_ExpenseandReimbursementPolicy.pdf"


# 1. Load PDF
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

query = "What expenses are eligible for reimbursement?"


# -----------------------------
# Normal Similarity Search
# -----------------------------

similarity_results = vector_store.similarity_search(
    query,
    k=5
)


print("\n==============================")
print("NORMAL SIMILARITY SEARCH")
print("==============================")

for i, document in enumerate(similarity_results):

    print(f"\n--- Result {i + 1} ---")
    print(f"Page: {document.metadata.get('page')}")
    print(f"Content: {document.page_content[:500]}")


# -----------------------------
# MMR Search
# -----------------------------

mmr_results = vector_store.max_marginal_relevance_search(
    query,
    k=5,
    fetch_k=10,
    lambda_mult=0.5
)


print("\n==============================")
print("MMR SEARCH")
print("==============================")

for i, document in enumerate(mmr_results):

    print(f"\n--- Result {i + 1} ---")
    print(f"Page: {document.metadata.get('page')}")
    print(f"Content: {document.page_content[:500]}")