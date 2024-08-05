from rag_core.utils.embedding import get_embedding
from rag_core.utils.retriever.chroma_retriever import chroma_retriever

import logging

def load_retriever(k, db_path="./rag_core/database/chroma_db"):
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Get the embedding
    embedding = get_embedding()

    # Select the retriever
    logging.info(f"Load retriever")
    retriever = chroma_retriever(embedding, db_path=db_path, k=k)
    
    return embedding, retriever