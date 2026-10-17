from app.ingestion.embedder import get_embeddings


embeddings = get_embeddings()

text = "Employees can claim reimbursement for approved business expenses."

vector = embeddings.embed_query(text)

print(f"\nEmbedding dimensions: {len(vector)}")
print(f"First 10 values: {vector[:10]}")