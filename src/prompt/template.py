from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

# def create_prompt(
#     context: str,
#     query: str
# ):
#     """
#     Load prompt
#     """
#     system_template = """You are a helpful AI assistant. Use the following pieces of context to answer the question at the end.
# If you don't know the answer, just say that you don't know, don't try to make up an answer."""
    
#     human_template = f"""Context information is below:
# ---------------------
# {context}
# ---------------------

# Question: {query}

# Answer:"""
#     messages = [
#         SystemMessage(content=system_template),
#         HumanMessage(content=human_template)
#     ]
#     return messages

def create_prompt(context, question):
    return ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a helpful AI assistant. Use the context to answer the question. "
            "If you don't know the answer, say you don't know."
        ),
        (
            "human",
            """Context:
---------------------
{context}
---------------------

Question: {question}

Answer:"""
        )
    ])