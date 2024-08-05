from rag_core.utils.document_loader import load_docs_from_folder
from rag_core.utils.vectorstore.chroma_vectorstore import chroma_vectorstore
from rag_core.utils.embedding import get_embedding

import logging
import argparse

def save_embedding(folder_path, db_path=None):

    # Get the vector store
    vectorstore = chroma_vectorstore

    # init the path if None
    if db_path == None:
        db_path = "./rag_core/database/chroma_db"


    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Load DOCX files from a folder
    documents = load_docs_from_folder(folder_path)
    ids = list(map(lambda x: x.metadata["source"].split("/")[-1], documents))

    # Load into database
    logging.info("Save documents to vector database")
    embedding = get_embedding()
    db = vectorstore(documents, embedding, db_path, ids)
    logging.info("Sucessfully saved documents to vector database")

    return db, embedding

def main():
    # Parser for shell script
    parser = argparse.ArgumentParser(description='RAG Application')
    parser.add_argument('--docs_path', type=str, help='User docs')
    parser.add_argument('--db_path', type=str, help='path to database')
    args = parser.parse_args()
    
    save_embedding(folder_path=args.docs_path, db_path=args.db_path)

if __name__ == "__main__":
    main()