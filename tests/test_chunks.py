from app.ingestion.loader import load_pdf
from app.ingestion.chunker import chunk_documents


PDF_PATH = "data/reimbursement/FIN_AP_ExpenseandReimbursementPolicy.pdf"


documents = load_pdf(PDF_PATH)

chunks = chunk_documents(documents)


print("\n==============================")
print("CHUNK INSPECTION")
print("==============================")

print(f"\nPages: {len(documents)}")
print(f"Chunks: {len(chunks)}")


for i, chunk in enumerate(chunks):

    print(f"\n--- Chunk {i} ---")

    print(f"Page: {chunk.metadata.get('page')}")

    print(f"Length: {len(chunk.page_content)}")

    print("\nContent:")
    print(chunk.page_content[:300])