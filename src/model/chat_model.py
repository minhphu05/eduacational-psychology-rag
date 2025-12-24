from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
import yaml
with open("./config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

import os, sys
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)
from task.chat import ask, stream
from dotenv import load_dotenv
load_dotenv("/Users/kittnguyen/Documents/education-rag/.env")
class MyChatBot:
    def __init__(
        self, 
        llm_config=config["llm"]
    ):
        self.llm = ChatGoogleGenerativeAI(
            temperature=llm_config["temperature"],
            model=llm_config["model_name"],
            streaming=llm_config["streaming"]
        )   
    def ask(self, question):
        """
        Ask a question to the chatbot and return the response.
        :param question: The question to ask.
        :return: The response from the chatbot.
        """
        return ask(self.llm, question)
    def stream(self, question):
        """
        Stream the response from the chatbot for a given question.
        :param question: The question to ask.
        :return: The full response from the chatbot as a string.
        """
        return stream(self.llm, question)