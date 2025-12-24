from langchain_core.documents import Document
from typing_extensions import List, TypedDict
import os, sys
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)
from prompt.template import create_prompt
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from task.retrieval import retrieve, generate

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str


