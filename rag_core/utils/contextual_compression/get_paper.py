import logging
from langchain_community.document_loaders import TextLoader


def get_paper(abstracts_filename, folder_path="./data/paper"):
    # Set up logging
    logging.info("START - loading documents")
    
    # Load document
    papers = []
    for abstract in abstracts_filename:
        loader = TextLoader(folder_path + f"/{abstract}")
        papers.append(loader.load()[0])

    # Successful
    logging.info(f"DONE - loaded {len(papers)} documents")

    return papers

