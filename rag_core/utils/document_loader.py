from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader

import logging

# Define function to load DOCX files from a folder
def load_docs_from_folder(folder_path):

    # Set up logging
    logging.info("START - loading documents")
    
    # Load document
    loader = DirectoryLoader(folder_path, glob="**/*.txt", loader_cls=TextLoader, show_progress=True)
    docs = loader.load()

    # Successful
    logging.info(f"DONE - loaded {len(docs)} documents")

    return docs