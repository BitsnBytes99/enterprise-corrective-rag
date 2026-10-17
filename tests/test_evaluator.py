from app.ingestion.loader import load_pdf
from app.ingestion.chunker import chunk_documents
from app.ingestion.embedder import get_embeddings
from app.retrieval.vector_store import create_vector_store
from app.correction.evaluator import evaluate_document


PDF_PATH = "data/reimbursement/FIN_AP_ExpenseandReimbursementPolicy.pdf"


# Load and prepare the knowledge base
documents = load_pdf(PDF_PATH)
chunks = chunk_documents(documents)

embeddings = get_embeddings()

vector_store = create_vector_store(chunks, embeddings)


# User query
query = "What expenses are eligible for reimbursement?"


# Retrieve documents
results = vector_store.similarity_search(query, k=3)


# Evaluate each retrieved document
print("\n==============================")
print("RETRIEVAL EVALUATION")
print("==============================")

for i, document in enumerate(results):

    evaluation = evaluate_document(query, document)

    print(f"\nDocument {i + 1}")
    print(f"Page: {document.metadata.get('page_label')}")
    print(f"Evaluation: {evaluation}")