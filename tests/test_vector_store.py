from app.ingestion.loader import load_pdf
from app.ingestion.chunker import chunk_documents
from app.ingestion.embedder import get_embeddings
from app.retrieval.vector_store import create_vector_store


PDF_PATH = "data/reimbursement/FIN_AP_ExpenseandReimbursementPolicy.pdf"


# 1. Load PDF
documents = load_pdf(PDF_PATH)

# 2. Create chunks
chunks = chunk_documents(documents)

# 3. Create embedding model
embeddings = get_embeddings()

# 4. Create vector store
vector_store = create_vector_store(chunks, embeddings)

print(f"\nPages loaded: {len(documents)}")
print(f"Chunks created: {len(chunks)}")
print("Vector store created successfully.")