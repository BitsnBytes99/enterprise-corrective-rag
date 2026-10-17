from app.correction.query_rewriter import rewrite_query


query = "Can I get money back for wifi?"


rewritten_query = rewrite_query(query)


print("\n==============================")
print("QUERY REWRITER TEST")
print("==============================")

print("\nOriginal query:")
print(query)

print("\nRewritten query:")
print(rewritten_query)