from app.correction.router import route_retrieval


test_cases = [
    "CORRECT",
    "AMBIGUOUS",
    "INCORRECT",
]


print("\n==============================")
print("ROUTER TEST")
print("==============================")


for grade in test_cases:

    route = route_retrieval(grade)

    print(
        f"Grade: {grade:<10} -> Route: {route}"
    )