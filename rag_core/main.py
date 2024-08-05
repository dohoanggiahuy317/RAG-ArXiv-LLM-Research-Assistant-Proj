from langchain_ollama import OllamaLLM

from pipeline.load_retriever import load_retriever
from pipeline.load_CCCompressor import load_CCCompressor
from pipeline.get_LLM import get_LLM

from rag_core.utils.contextual_compression.pretty_print import pretty_print_docs
from rag_core.utils.contextual_compression.get_paper import get_paper
from rag_core.utils.save_log import save_log
from rag_core.utils.vectorstore.chroma_vectorstore import chroma_vectorstore

import argparse
import logging

def main():

    # Parser for shell script
    parser = argparse.ArgumentParser(description='RAG Application')
    parser.add_argument('--question', type=str, help='User query')
    parser.add_argument('--compressor_type', type=int, help='type of retriever compressor')
    parser.add_argument('--db_path', type=str, default="./rag_core/database/denison/chroma_db", help='path to database')
    parser.add_argument('--k', type=int, default=3, help='Number of relevant docs')
    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Load neccessary components
    embedding, retriever = load_retriever(args.k, args.db_path)
    get_compressed_docs = load_CCCompressor(compressor_type = int(args.compressor_type))
    
    # Ranking the documents
    logging.info("Getting compressed_docs")
    abstracts = retriever.invoke(args.question)

    # Get the docs id
    abstracts_filename = list(map(lambda x: x.metadata["source"].split("/")[-1], abstracts))
    papers = get_paper(abstracts_filename)

    # Create retriever for paper
    db = chroma_vectorstore(papers, embedding, save_local=False)
    paper_retriever = db.as_retriever()

    llm = OllamaLLM(model="llama3")
    compressed_docs = get_compressed_docs(args.question, llm, paper_retriever)

    # Get response
    rag_chain = get_LLM(compressed_docs)

    logging.info("Inferencing response...")
    response = rag_chain.invoke(args.question)

    # Log the response
    logging.info(f"RESPONSE -- \n {response} \n")

    # Save the answer log to txt file
    save_log(
        "QUESTION: " + args.question + "\n\n" + "-"*50 + "\n\n"
        "RESPONSE: " + response + "\n\n" + "-"*50 + "\n\n"
        "METADATA: \n" + "\n".join(list(map(lambda x: str(x.metadata["source"]), compressed_docs))) + "\n\n" + "-"*50 + "\n\n"
        "DOCUMENTS: \n" + pretty_print_docs(compressed_docs),
        f"./rag_core/logs/response.txt"
    )

    return response

# Run the main function
if __name__ == "__main__":   
    main()


