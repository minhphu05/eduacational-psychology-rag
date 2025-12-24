from langchain_postgres import PGVector

def connect_to_vector_store(embedding_model, connection_string=None, collection_name=None):
    """
    Connects to a PostgreSQL vector store using the provided embeddings.
    :param embeddings: The embeddings model to use for the vector store.
    :param connection_string: The connection string for the PostgreSQL database.
    :param collection_name: The name of the collection in the vector store.
    """
    return PGVector(
        embeddings=embedding_model,
        collection_name=collection_name,
        connection=connection_string
    )