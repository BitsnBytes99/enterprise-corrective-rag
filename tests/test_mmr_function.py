from app.ingestion.loader import load_pdf
from app.ingestion.chunker import chunk_documents
from app.ingestion.embedder import get_embeddings
from app.retrieval.vector_store import (
    create_vector_store,
    retrieve_with_mmr
)


PDF_PATH = "data/reimbursement/FIN_AP_ExpenseandReimbursementPolicy.pdf"


# Load document
documents = load_pdf(PDF_PATH)

# Create chunks
chunks = chunk_documents(documents)

# Load embeddings
embeddings = get_embeddings()

# Create vector store
vector_store = create_vector_store(
    chunks,
    embeddings
)


# Query
query = "What expenses are eligible for reimbursement?"


# Retrieve using our MMR function
results = retrieve_with_mmr(
    vector_store,
    query,
    k=5
)


print("\n==============================")
print("MMR FUNCTION TEST")
print("==============================")


for i, document in enumerate(results):

    print(f"\n--- Result {i + 1} ---")

    print(
        f"Page: {document.metadata.get('page')}"
    )

    print(
        f"Content: {document.page_content[:500]}"
    )