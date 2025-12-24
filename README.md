# RAG Chatbot with LangChain & LangGraph

A sophisticated Retrieval-Augmented Generation (RAG) chatbot built with LangChain, LangGraph, and Streamlit. This application enables intelligent question-answering by combining document retrieval with AI-powered response generation using Gemini models.

## 🌟 Features

- 🤖 **Advanced RAG Pipeline**: Built with LangGraph for sophisticated question-answering workflows
- 📚 **Document Processing**: Automatic PDF processing and vector embeddings storage
- 💬 **Dual Interface**: 
  - Web interface with Streamlit for interactive chat
  - Command-line interface for terminal-based interaction
- ⚡ **Real-time Streaming**: Live response streaming for better user experience  
- 📝 **Persistent Chat**: Chat history preservation in web interface
- 🔄 **OpenAI Integration**: Gemini-2.5-flash for text generation and text-embedding-004 for embeddings
- 🐘 **PostgreSQL + pgvector**: High-performance vector storage and similarity search
- 🐳 **Docker Support**: Complete containerization with Docker Compose
- 🏗️ **Modular Architecture**: Clean separation of concerns with organized project structure

## 📋 Prerequisites

- Python 3.12+
- GOOGLE API key
- PostgreSQL with pgvector extension
- Docker and Docker Compose (optional)
- Required Python packages (see requirements.txt)

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

1. **Clone the repository:**
```bash
git clone https://github.com/minhphu05/eduacational-psychology-rag.git
cd education-rag
```

2. **Set up environment variables:**
```bash
# Create .env file
echo "GOOGLE_API_KEY=your_api_key_here" > .env
echo "CONNECTION_STRING=postgresql+psycopg2://minhphu:minhphu123@localhost:5433/vector_db" >> .env
```

3. **Start the application:**
```bash
# Start PostgreSQL and the app
docker-compose up -d

# View logs
docker-compose logs -f app
```

4. **Access the application:**
   - Web Interface: http://localhost:8501
   - PostgreSQL: localhost:5433

### Option 2: Local Development

1. **Clone and setup:**
```bash
git clone https://github.com/minhphu05/eduacational-psychology-rag.git
cd education-rag
```

2. **Create virtual environment:**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Setup PostgreSQL:**
```sql
-- Install PostgreSQL and pgvector extension
CREATE DATABASE vector_db;
\c vector_db;
CREATE EXTENSION vector;
```

5. **Environment configuration:**
```bash
# Create .env file with:
GOOGLE_API_KEY=your_gemini_api_key
CONNECTION_STRING=postgresql+psycopg2://postgres:password@localhost:5433/vector_db
```

6. **Run the application:**
```bash
# Web interface
streamlit run app.py

# Command line interface
python main.py
```

## 📁 Project Structure

```
LangChainProject/
├── app.py                    # Streamlit web application
├── main.py                   # Command-line interface
├── requirements.txt          # Python dependencies
├── docker-compose.yml        # Docker services configuration
├── Dockerfile               # Container build instructions
├── README.md                # Project documentation
├── .env                     # Environment variables (create this)
│
├── config/                  # Configuration management
│   ├── __init__.py
│   ├── config.py           # LLM, embedding, and text splitting configs
│   └── llm_config.py
│
├── src/                    # Core application source code
│   ├── __init__.py
│   ├── state.py           # Application state management
│   ├── langgraph_tracking.py  # LangGraph workflow orchestration
│   │
│   ├── document_store/    # Document processing pipeline
│   │   ├── __init__.py
│   │   ├── loader.py      # Document loading utilities
│   │   ├── splitter.py    # Text chunking strategies
│   │   ├── document_indexing.py    # Vector indexing
│   │   ├── document_connecting.py  # Database connections
│   │   ├── check_pg_connection.py  # PostgreSQL health checks
│   │   └── main.py        # Document pipeline orchestration
│   │
│   ├── model/             # AI model configurations
│   │   ├── __init__.py
│   │   ├── chat_model.py  # LLM wrapper and configuration
│   │   └── embedding_model.py  # Embedding model setup
│   │
│   ├── prompt_template/   # Prompt engineering
│   │   ├── __init__.py
│   │   └── template.py    # RAG prompt templates
│   │
│   └── task/              # Core RAG operations
│       ├── __init__.py
│       ├── chat.py        # Chat functionality
│       ├── embedding.py   # Document embedding tasks
│       └── rag.py         # RAG pipeline implementation
│
└── data/                  # Data storage
    ├── documents/         # Processed documents
    ├── embedding/         # Vector embeddings cache
    └── raw/              # Source documents (PDF files)
        └── tam-ly-hoc-dai-cuong.pdf
```

## 🔧 Configuration

### Environment Variables

```bash
# Required
GOOGLE_API_KEY=your_gemini_api_key_here

# Database connection
CONNECTION_STRING=postgresql+psycopg2://minhphu:minhphu123@localhost:5433/vector_db

# Optional: Customize collection name
COLLECTION_NAME=medallion_architecture
```

## 🛠️ Usage Examples

### Web Interface (Streamlit)
```bash
streamlit run app.py
```
- Interactive chat interface
- Real-time response streaming
- Chat history preservation
- Formatted responses with context tags

### Command Line Interface
```bash
python main.py
```
- Terminal-based Q&A
- Direct pipeline interaction
- Useful for testing and debugging

### Sample Questions
- "What are the main concepts in psychology?"
- "Explain the difference between classical and operant conditioning"
- "What is cognitive psychology about?"

## 🏗️ Architecture

### RAG Pipeline Flow
1. **Document Processing**: PDF documents are loaded and split into chunks
2. **Vector Embedding**: Text chunks are converted to vectors using GoogleGenerativeAI embeddings
3. **Storage**: Vectors are stored in PostgreSQL with pgvector extension
4. **Retrieval**: User questions trigger similarity search for relevant context
5. **Generation**: LLM generates responses using retrieved context and question
6. **Streaming**: Responses are streamed back to user interface

### LangGraph Workflow
```mermaid
graph TD
    A[User Question] --> B[Retrieve Node]
    B --> C[Context Retrieval]
    C --> D[Generate Node]
    D --> E[LLM Response]
    E --> F[Streamed Output]
```

### Technology Stack
- **Framework**: LangChain + LangGraph
- **LLM**: Gemini-2.5-flash
- **Embeddings**: Gemini text-embedding-004
- **Vector Database**: PostgreSQL + pgvector
- **Web Interface**: Streamlit
- **Containerization**: Docker + Docker Compose
- **Language**: Python 3.12

## 🚧 Development

### Adding New Documents
1. Place PDF files in `data/raw/` directory
2. Run the document processing pipeline:
```python
from src import test_document_pipeline
vector_store = test_document_pipeline()
```

### Customizing Prompts
Edit templates in `src/prompt_template/template.py`:
```python
def load_prompt():
    return """
    Use the following context to answer the question.
    Context: {context}
    Question: {question}
    Answer:
    """
```

### Model Configuration
Modify settings in `config/config.py` to:
- Change LLM models
- Adjust temperature and token limits  
- Configure chunking strategy
- Set embedding parameters

### Database Management
```bash
# Connect to PostgreSQL
docker exec -it <container_name> psql -U postgres -d vector_db

# View collections
SELECT * FROM langchain_pg_collection;

# Check embeddings
SELECT COUNT(*) FROM langchain_pg_embedding;
```

## 🐳 Docker Operations

```bash
# Build and start services
docker-compose up --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Remove volumes (caution: deletes data)
docker-compose down -v

# Scale app instances
docker-compose up --scale app=2
```

## 🔍 Troubleshooting

### Common Issues

**1. OpenAI API Key Error**
```bash
Error: Gemini API key not found
Solution: Ensure GOOGLE_API_KEY is set in .env file
```

**2. PostgreSQL Connection Error**
```bash
Error: Could not connect to database
Solution: Check CONNECTION_STRING and ensure PostgreSQL is running
```

**3. Document Loading Issues**
```bash
Error: No documents found
Solution: Ensure PDF files are in data/raw/ directory
```

**4. Memory Issues**
```bash
Error: Out of memory during embedding
Solution: Reduce batch_size in EMBEDDING_CONFIG
```

### Performance Optimization

- **Embedding Batch Size**: Adjust based on available memory
- **Chunk Size**: Balance between context and performance
- **Connection Pooling**: Configure for high-concurrency scenarios
- **Caching**: Implement Redis for frequent queries

## 📊 Monitoring

### Health Checks
```python
# Database connection
from src.document_store.check_pg_connection import check_connection
check_connection()

# Vector store status
from src.model.embedding_model import EmbeddingModel
embedding = EmbeddingModel()
status = embedding.get_vector_store_status()
```

### Metrics
- Response time per query
- Document retrieval accuracy
- Token usage tracking
- Database query performance

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push to branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open Pull Request**

### Development Guidelines
- Follow PEP 8 style guidelines
- Add type hints where applicable
- Include docstrings for functions
- Write unit tests for new features
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

⭐ **Star this repository if you find it helpful!** 