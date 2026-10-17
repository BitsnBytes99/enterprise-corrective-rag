from app.ingestion.loader import load_pdf
from app.ingestion.chunker import chunk_documents


PDF_PATH = "data/reimbursement/Sample_Financial_Reimbursement_Policy.pdf"


documents = load_pdf(PDF_PATH)

chunks = chunk_documents(documents)

print(f"\nTotal pages: {len(documents)}")
print(f"Total chunks: {len(chunks)}")

for i, chunk in enumerate(chunks[:5]):
    print(f"\n--- Chunk {i + 1} ---")
    print(chunk.page_content)
    print("\nMetadata:")
    print(chunk.metadata)