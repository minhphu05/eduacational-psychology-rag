from dotenv import load_dotenv
import os
from src.model.chat_model import MyChatBot
from langchain_core.messages import HumanMessage, SystemMessage
from src.document_store.documents_loader import DocumentStoring
from src.document_store.ingestion_pipeline import ingestion_pipeline
from src.task.retrieval import retrieve, generate
from src.state import State
from src.prompt.template import create_prompt
from src.langgraph_tracking import build_graph
# from app import initialize_rag_pipeline
import re

def initialize_vector_store():
    """
    Initialize and return the vector store with documents.
    Returns:
        vector_store: The initialized vector store instance
    """
    try:
        # Load environment variables
        load_dotenv("/Users/kittnguyen/Documents/education-rag/.env")
        print("✅ Environment variables loaded successfully")
        
        # Initialize vector store
        print("🔄 Initializing vector store...")
        vector_store = ingestion_pipeline()
        if vector_store is None:
            raise Exception("Failed to initialize vector store")
        print("✅ Vector store initialized successfully")
        
        return vector_store
    except Exception as e:
        print(f"❌ Error during vector store initialization: {str(e)}")
        return None

def initialize_llm():
    """
    Initialize and return the LLM model.
    Returns:
        llm: The initialized LLM instance
    """
    try:
        print("🔄 Initializing LLM...")
        llm = MyChatBot()
        print("✅ LLM initialized successfully")
        return llm
    except Exception as e:
        print(f"❌ Error during LLM initialization: {str(e)}")
        return None

def initialize_rag_pipeline():
    """
    Initialize the complete RAG pipeline including LLM and vector store.
    Returns:
        tuple: (llm, vector_store) if successful, (None, None) if failed
    """
    try:
        # Initialize LLM
        llm = initialize_llm()
        if llm is None:
            return None, None

        # Initialize vector store
        vector_store = initialize_vector_store()
        if vector_store is None:
            return None, None
        
        return llm, vector_store
    except Exception as e:
        print(f"❌ Error during RAG pipeline initialization: {str(e)}")
        return None, None

def process_question(question: str, graph):
    """
    Process a question through the RAG pipeline with streaming.
    Args:
        question (str): The question to process
        graph: The RAG graph instance
    Returns:
        bool: True if successful, None if failed
    """
    try:
        # Process the question through the RAG pipeline with streaming
        print("\n📝 Answer:")
        for message, metadata in graph.stream(
            {"question": question}, 
            stream_mode="messages"
        ):
            if hasattr(message, 'content'):
                print(message.content, end="", flush=True)
        print()  # Add newline at the end
        return True
    except Exception as e:
        print(f"❌ Error processing question: {str(e)}")
        return None

def main():
    # Initialize the RAG pipeline
    llm, vector_store = initialize_rag_pipeline()
    if llm is None or vector_store is None:
        print("❌ Failed to initialize RAG pipeline")
        return

    # Build the RAG graph
    try:
        print("🔄 Building RAG graph...")
        # Create functions that will be used in the graph
        def retrieve_node(state):
            return retrieve(state, vector_store=vector_store)
            
        def generate_node(state):
            return generate(state, llm=llm, create_prompt=create_prompt)
            
        graph = build_graph(
            State,
            retrieve_node,
            generate_node
        )
        print("✅ RAG graph built successfully!")
    except Exception as e:
        print(f"❌ Error building RAG graph: {str(e)}")
        return

    # Interactive Q&A loop
    print("\n🤖 RAG Pipeline is ready! Type 'exit' to quit.")
    while True:
        try:
            question = input("\n❓ Please enter your question: ").strip()
            
            if question.lower() == 'exit':
                print("👋 Goodbye!")
                break
                
            if not question:
                print("⚠️ Please enter a valid question")
                continue
                
            print(f"\n🔄 Processing your question: {question}")
            process_question(question, graph)
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {str(e)}")

if __name__ == "__main__":
    main()

