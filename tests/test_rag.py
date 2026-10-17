from app.ingestion.loader import load_pdf
from app.ingestion.chunker import chunk_documents
from app.ingestion.embedder import get_embeddings
from app.retrieval.vector_store import create_vector_store
from app.retrieval.rag import generate_answer


PDF_PATH = "data/reimbursement/FIN_AP_ExpenseandReimbursementPolicy.pdf"


# 1. Load documents
documents = load_pdf(PDF_PATH)

# 2. Create chunks
chunks = chunk_documents(documents)

# 3. Create embeddings
embeddings = get_embeddings()

# 4. Create vector store
vector_store = create_vector_store(chunks, embeddings)


# 5. User query
query = "What expenses are eligible for reimbursement?"

# 6. Retrieve relevant documents
results = vector_store.similarity_search(query, k=3)

# 7. Generate answer
answer = generate_answer(query, results)


print("\n==============================")
print("QUERY")
print("==============================")
print(query)

print("\n==============================")
print("ANSWER")
print("==============================")
print(answer)

print("\n==============================")
print("SOURCES")
print("==============================")

for i, document in enumerate(results):
    print(f"\nSource {i + 1}:")
    print(f"Page: {document.metadata.get('page_label')}")
    print(f"File: {document.metadata.get('source')}")