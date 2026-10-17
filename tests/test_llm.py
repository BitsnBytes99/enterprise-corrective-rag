from app.generation.llm import get_llm


llm = get_llm()

response = llm.invoke(
    "Explain in one sentence what an employee reimbursement policy is."
)

print("\nResponse:")
print(response.content)