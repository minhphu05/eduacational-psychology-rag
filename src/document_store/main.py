import os, sys
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from document_store.documents_loader import DocumentStoring
from document_store.documents_splitter import split_documents
from document_store.pg_connection import connect_to_vector_store
from document_store.document_indexing import indexing
from model.embedding_model import EmbeddingModel
from dotenv import load_dotenv

def main():
    try:
        # Load environment variables
        load_dotenv("/Users/kittnguyen/Documents/education-rag/.env")
        # Define the path to the document directory
        LangChainDocument_PATH = "/Users/kittnguyen/Documents/education-rag/data"
        # Create an embedding model instance
        embedding_model = EmbeddingModel()
        print("Initializing Embedding Model...")
        # Initialize the document storing instance
        document_storing = DocumentStoring(LangChainDocument_PATH)
        print("Initializing Document Storing...")
        # Loading documents
        docs, docs_sources = document_storing.store_document()
        print("Loading documents...")
        # Splitting documents into chunks
        print("Splitting documents into chunks...")
        chunks = split_documents(docs)
        # Connect to vector store
        connection_string = os.getenv("CONNECTION_STRING")
        collection_name = "medallion_architecture"  # Set a specific collection name
        print(f"Connection String: {connection_string}")
        print("Connecting to vector store...")
        vector_store = embedding_model.connect_to_vector_store_embedding(
            connection_string, 
            collection_name=collection_name
        )
        print("✅ Successfully connected to vector store")
        # Indexing documents
        print("🔄 Indexing documents...")
        indexing(vector_store, chunks)
        print("✅ Documents indexed successfully")  
        return vector_store
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

if __name__ == "__main__":
    main()