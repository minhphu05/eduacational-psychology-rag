def ask(llm, question: str) -> str:
    """
    Input: User questions
    """
    response = llm.invoke(question) # Đợi model trả xong --> Trả về 1 lần
    return response

def stream(llm, question: str) -> str:
    full_response = ""
    response = llm.stream(question) # Trả token dần dần (real-time)
    for token in response:
        if hasattr(token, 'content'):
            full_response += token.content
        else:
            full_response += str(token)
    return full_response