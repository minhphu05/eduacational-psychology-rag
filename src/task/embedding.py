def embedding(llm, all_splits: str) -> str:
    result = []
    for i in range(len(all_splits)):
        vector = llm.embed_query(all_splits[i].page_content)    
        result.append(vector)
    return result