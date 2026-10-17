from app.ingestion.loader import load_pdf


PDF_PATH = "data/reimbursement/Sample_Financial_Reimbursement_Policy.pdf"


documents = load_pdf(PDF_PATH)

print(f"\nTotal pages loaded: {len(documents)}")

for i, document in enumerate(documents[:2]):
    print(f"\n--- Page {i + 1} ---")
    print(document.page_content[:1000])
    print("\nMetadata:")
    print(document.metadata)