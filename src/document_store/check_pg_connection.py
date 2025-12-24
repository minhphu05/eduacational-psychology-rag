import os
from langchain_postgres import PGVector
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

dotenv_path = "/Users/kittnguyen/Documents/education-rag/.env"
load_dotenv(dotenv_path)

CONNECTION_STRING = os.getenv("CONNECTION_STRING")
print(f"Connect: {CONNECTION_STRING}")

# Khởi tạo embedding model
embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

# Create a connection to vector store
vector_store = PGVector(
    embeddings=embeddings,
    collection_name="testing",
    connection=CONNECTION_STRING
)
print("Vector store connected!")