import streamlit as st
from dotenv import load_dotenv
import os, sys
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)
from src.model.chat_model import MyChatBot
from src.task.retrieval import retrieve, generate
from src.langgraph_tracking import build_graph
from src.prompt.template import create_prompt
from src.state import State
from document_store.ingestion_pipeline import ingestion_pipeline
from dotenv import load_dotenv
import os

def initialize_rag_pipeline():
    try:
        # Load environment variables
        load_dotenv()
        
        # Initialize LLM
        from src.model import EmbeddingModel
        embedding = EmbeddingModel()
        llm = MyChatBot()
        embedding = EmbeddingModel()

        connection_string = os.getenv("CONNECTION_STRING")
        collection_name = "medallion_architecture"

        # Initialize vector store
        vector_store = embedding.connect_to_vector_store_embedding(
            connection_string, 
            collection_name=collection_name
        )
        
        return llm, vector_store
    except Exception as e:
        st.error(f"Error during initialization: {str(e)}")
        return None, None

def process_question(question: str, graph):
    try:
        # Create a placeholder for streaming response
        response_placeholder = st.empty()
        full_response = ""
        
        # Process the question through the RAG pipeline with streaming
        for message, metadata in graph.stream(
            {"question": question}, 
            stream_mode="messages"
        ):
            if hasattr(message, 'content'):
                # Format the response with different colors for different tags
                formatted_response = message.content
                formatted_response = formatted_response.replace("[CONTEXT]", "🔍 **Context:** ")
                formatted_response = formatted_response.replace("[/CONTEXT]", "")
                formatted_response = formatted_response.replace("[LLM]", "🤖 **AI Generated:** ")
                formatted_response = formatted_response.replace("[/LLM]", "")
                formatted_response = formatted_response.replace("[MIXED]", "🔄 **Combined:** ")
                formatted_response = formatted_response.replace("[/MIXED]", "")
                
                full_response += formatted_response
                response_placeholder.markdown(full_response)
        
        return full_response
    except Exception as e:
        st.error(f"Error processing question: {str(e)}")
        return None

def main():
    st.set_page_config(
        page_title="RAG Chatbot",
        page_icon="🤖",
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .stTextInput>div>div>input {
            font-size: 25px;
        }
        .stMarkdown {
            font-size: 25px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Title
    st.title("🤖 RAG Chatbot")
    st.markdown("Ask questions about your documents!")
    
    # Initialize RAG pipeline
    with st.spinner("Initializing RAG pipeline..."):
        llm, vector_store = initialize_rag_pipeline()
        
    if llm is None or vector_store is None:
        st.error("Failed to initialize RAG pipeline")
        return
        
    # Build the RAG graph
    with st.spinner("Building RAG graph..."):
        try:
            def retrieve_node(state):
                return retrieve(state, vector_store=vector_store)
                
            def generate_node(state):
                return generate(state, llm=llm, load_prompt=create_prompt)
                
            graph = build_graph(
                State,
                retrieve_node,
                generate_node
            )
        except Exception as e:
            st.error(f"Error building RAG graph: {str(e)}")
            return
    
    # Chat interface
    st.markdown("---")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Display assistant response
        with st.chat_message("assistant"):
            response = process_question(prompt, graph)
            if response:
                st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    ingestion_pipeline()
    main()