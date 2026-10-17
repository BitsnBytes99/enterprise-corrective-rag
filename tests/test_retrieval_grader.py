print("TEST FILE STARTED")


from app.ingestion.loader import load_pdf
from app.ingestion.chunker import chunk_documents
from app.ingestion.embedder import get_embeddings
from app.retrieval.vector_store import create_vector_store
from app.correction.retrieval_grader import grade_retrieval


PDF_PATH = "data/reimbursement/FIN_AP_ExpenseandReimbursementPolicy.pdf"


# 1. Load PDF
print("\nLoading PDF...")
documents = load_pdf(PDF_PATH)

# 2. Create chunks
print("Creating chunks...")
chunks = chunk_documents(documents)

# 3. Create embeddings
print("Loading embedding model...")
embeddings = get_embeddings()

# 4. Create vector store
print("Creating vector store...")
vector_store = create_vector_store(
    chunks,
    embeddings
)


# 5. User query
query = "What expenses are eligible for reimbursement?"


# 6. Retrieve documents with similarity scores
print("Retrieving documents...")

results = vector_store.similarity_search_with_score(
    query,
    k=5
)


# Extract documents for the grader
retrieved_documents = [
    document
    for document, score in results
]


# 7. Grade retrieval
print("Grading retrieval...")

grade = grade_retrieval(
    query,
    retrieved_documents
)


# 8. Display results
print("\n==============================")
print("RETRIEVAL GRADING")
print("==============================")

print(f"\nQuery: {query}")
print(f"Retrieved documents: {len(results)}")
print(f"Retrieval grade: {grade}")

print("\nSources:")

for i, (document, score) in enumerate(results):

    print(f"\n--- Document {i + 1} ---")

    print(f"Page: {document.metadata.get('page')}")

    print(f"Similarity score: {score}")

    print("\nContent:")
    print(document.page_content[:700])