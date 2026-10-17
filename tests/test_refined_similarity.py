from app.ingestion.loader import load_pdf
from app.ingestion.chunker import chunk_documents
from app.ingestion.embedder import get_embeddings
from app.retrieval.vector_store import create_vector_store


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


query = "employee reimbursement policy eligible expenses Wi-Fi internet service"


print("\n==============================")
print("REFINED QUERY - SIMILARITY TEST")
print("==============================")


print("\nQuery:")
print(query)


results = vector_store.similarity_search(
    query,
    k=5
)


print("\n==============================")
print("SIMILARITY RESULTS")
print("==============================")


for i, document in enumerate(results):

    print(f"\n--- Result {i + 1} ---")

    print(
        f"Page: {document.metadata.get('page')}"
    )

    print("\nContent:")

    print(
        document.page_content[:700]
    )