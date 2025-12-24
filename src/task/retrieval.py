from task.chat import stream
def retrieve(state, vector_store):
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}

def generate(state, llm, create_prompt):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    prompt = create_prompt(context=docs_content, question=state["question"])
    # Format the prompt template with the variables
    formatted_prompt = prompt.format_messages(
        context=docs_content,
        question=state["question"]
    )
    # Get streaming response using the stream function
    try:
        response = stream(llm, formatted_prompt)
        return {"answer": response}
    except Exception as e:
        print(f"Error in generate: {str(e)}")
        return {"answer": ""}