def retrieve_top_chunks(query, vector_db, k=8, emergency_type="general"):
    """
    Emergency-Type Routing Retriever 
    Retrieves chunks only from relevant protocol documents.
    """

    filter_metadata = {"doc_type": emergency_type}

    return vector_db.max_marginal_relevance_search(
        query,
        k=k,
        fetch_k=20,
        lambda_mult=0.7,
        filter=filter_metadata
    )
