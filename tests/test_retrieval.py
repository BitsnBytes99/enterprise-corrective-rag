from app.ingestion.loader import load_pdf
from app.ingestion.chunker import chunk_documents
from app.ingestion.embedder import get_embeddings
from app.retrieval.vector_store import create_vector_store


PDF_PATH = "data/reimbursement/FIN_AP_ExpenseandReimbursementPolicy.pdf"


# Load and prepare documents
documents = load_pdf(PDF_PATH)
chunks = chunk_documents(documents)

# Create embeddings
embeddings = get_embeddings()

# Create vector store
vector_store = create_vector_store(chunks, embeddings)


# Test query
query = "What expenses are eligible for reimbursement?"

results = vector_store.similarity_search(query, k=3)


print(f"\nQuery: {query}")
print(f"Retrieved documents: {len(results)}")

for i, result in enumerate(results):
    print(f"\n--- Result {i + 1} ---")
    print(result.page_content)
    print("\nMetadata:")
    print(result.metadata)