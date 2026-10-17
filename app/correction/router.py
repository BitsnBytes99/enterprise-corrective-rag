def route_retrieval(grade):
    """
    Decide what to do based on retrieval quality.
    """

    if grade == "CORRECT":
        return "USE_CONTEXT"

    if grade == "AMBIGUOUS":
        return "REFINE_RETRIEVAL"

    if grade == "INCORRECT":
        return "REWRITE_QUERY"

    return "REFINE_RETRIEVAL"