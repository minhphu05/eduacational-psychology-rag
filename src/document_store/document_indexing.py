def indexing(vector_store, all_splits):
    """
    Indexes the given documents into the vector store.

    Args:
        vector_store: The vector store to index the documents into.
        all_splits: A list of splits to be indexed.
    """
    if not all_splits:
        print("No all_splits to index.")
        return
    
    ids = vector_store.add_documents(documents = all_splits)
    print("Indexing completed.")
    