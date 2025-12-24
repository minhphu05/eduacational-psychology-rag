from langchain_google_genai import GoogleGenerativeAIEmbeddings
import yaml
with open("./config/config.yaml", "r") as f:
    config = yaml.safe_load(f)
import os, sys
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)
embedding_config = config["embedding"]

class EmbeddingModel:
    def __init__(
        self,
        embedding_config=embedding_config
    ):
        """
        Initializes the EmbeddingModel with the specified configuration.
        
        :param embedding_config: Configuration for the embedding model.
        """
        self.embedding_model = GoogleGenerativeAIEmbeddings(
            model=embedding_config["model_name"]
        )
        
    def connect_to_vector_store_embedding(self, connection_string=None, collection_name=None):
            """
            Connects to the vector store using the initialized embedding model.
            :return: The connected vector store instance.
            """
            from document_store.pg_connection import connect_to_vector_store
            return connect_to_vector_store(self.embedding_model, connection_string=connection_string, collection_name=collection_name)

    