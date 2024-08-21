from rag_core.utils.embedding import get_embedding, get_local_embedding
from rag_core.utils.retriever.chroma_retriever import chroma_retriever

import logging

def load_retriever(k, embedding_type=1, db_path="./rag_core/database/chroma_db", model_path="finetune_embedder/models/v1"):
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Get the embedding
    if int(embedding_type) == 1:
        embedding = get_embedding()
    else:
        embedding = get_local_embedding(model_path)

    # Select the retriever
    logging.info(f"Load retriever")
    retriever = chroma_retriever(embedding, db_path=db_path, k=k)
    
    return embedding, retriever