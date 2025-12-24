import os, sys
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from langchain_text_splitters import RecursiveCharacterTextSplitter

import yaml
with open("./config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

TEXTSPLIT_CONFIG = config["text_splitter"]

def split_documents(
    docs,
    DOCUMENT_SPLITTING_CONFIG=TEXTSPLIT_CONFIG
):
    """
    Splits the provided documents into smaller chunks.
    
    :param documents: List of documents to be split.
    :return: List of split document chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=DOCUMENT_SPLITTING_CONFIG.get("chunk_size",1000), 
        chunk_overlap=DOCUMENT_SPLITTING_CONFIG.get("chunk_overlap", 200),
        add_start_index=DOCUMENT_SPLITTING_CONFIG.get("add_start_index", True)
    )

    chunks = text_splitter.split_documents(docs)
    if chunks:
        for i, chunk in enumerate(chunks[:5]):
            print(f"\n--- Chunk {i+1} ---")
            print(f"Source: {chunk.metadata["source"]}")
            print(f"Length: {len(chunk.page_content)} charaters.")
            print(f"Content: ")
            print(chunk.page_content)
            print("-" * 50)
        
        if len(chunks) > 5:
            print(f"\n... and {len(chunks) - 5} more chunks.")
    return chunks 