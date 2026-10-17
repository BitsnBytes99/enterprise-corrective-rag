from app.correction.retrieval_refiner import refine_query


query = (
    "Is Wi-Fi or internet expense eligible for employee "
    "reimbursement under the reimbursement policy?"
)


refined_query = refine_query(query)


print("\n==============================")
print("RETRIEVAL REFINER TEST")
print("==============================")


print("\nOriginal query:")
print(query)


print("\nRefined query:")
print(refined_query)
