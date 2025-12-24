from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
import yaml
with open("./config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

import os, sys
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)


