from langchain_ollama import OllamaLLM

from chat_core.utils.get_history import get_runnable_history
from chat_core.utils.get_prompt import prompt_template

from rag_core.pipeline.load_retriever import load_retriever
from rag_core.pipeline.load_CCCompressor import load_CCCompressor
from rag_core.pipeline.get_LLM import format_docs

from rag_core.utils.save_log import add_log
from rag_core.utils.contextual_compression.pretty_print import pretty_print_docs
from rag_core.utils.contextual_compression.get_paper import get_paper
from rag_core.utils.vectorstore.chroma_vectorstore import chroma_vectorstore


import argparse
import logging


def chat(question, compressor_type,
        db_path, user_id,
        conversation_id, k,
        embedding_type, model_path,
    ):

    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Load neccessary components
    embedding, retriever = load_retriever(k=k, embedding_type=embedding_type, db_path = db_path, model_path=model_path)
    get_compressed_docs = load_CCCompressor( compressor_type = int(compressor_type))

    # Ranking the documents
    logging.info("Getting compressed_docs")
    abstracts = retriever.invoke(question)
    llm = OllamaLLM(model="llama3")

    # Get prompt for the question
    prompt = prompt_template()
    runnable = prompt | llm

    try:
        if len(abstracts) == 0:

            # Get chat history
            runnable_with_history = get_runnable_history(runnable)

            response = runnable_with_history.invoke(
                {
                    "question": question,
                    "context": "No relevant paper"
                },
                config={"configurable": 
                        {
                            "user_id": user_id, 
                            "conversation_id": conversation_id,
                        }},
            )

            # Save the answer log to txt file
            add_log(
                "USER: " + question + "\n\n"
                "SYSTEM: " + response  + "\n\n" + "-"*50 + "\n",
                f"./chat_core/logs/{str(user_id)}-{conversation_id}/compressor_{str(compressor_type)}/chat/response.txt"
            )

            add_log(
                "QUESTION: " + question + "\n\n" + "-"*50 + "\n\n"
                "RESPONSE: " + response + "\n\n" + "-"*50 + "\n\n"
                "METADATA: \n" + "-"*50 + "\n\n",
                f"./chat_core/logs/{str(user_id)}-{conversation_id}/compressor_{str(compressor_type)}/info/response.txt"
            )

            logging.info(f"RESPONSE -- \n {response} \n")

            return response, []
        
        else:
            # Get the docs id
            abstracts_filename = list(map(lambda x: x.metadata["source"].split("/")[-1], abstracts))
            papers = get_paper(abstracts_filename)

            # Create retriever for paper
            db = chroma_vectorstore(papers, embedding, save_local=False)
            paper_retriever = db.as_retriever()

            compressed_docs = get_compressed_docs(question, llm, paper_retriever)
            formatted_doc = format_docs(compressed_docs)

            # Get chat history
            runnable_with_history = get_runnable_history(runnable)

            response = runnable_with_history.invoke(
                {
                    "question": question,
                    "context": formatted_doc
                },
                config={"configurable": 
                        {
                            "user_id": user_id, 
                            "conversation_id": conversation_id,
                        }},
            )

            # Save the answer log to txt file
            add_log(
                "USER: " + question + "\n\n"
                "SYSTEM: " + response  + "\n\n" + "-"*50 + "\n",
                f"./chat_core/logs/{str(user_id)}-{conversation_id}/compressor_{str(compressor_type)}/chat/response.txt"
            )

            add_log(
                "QUESTION: " + question + "\n\n" + "-"*50 + "\n\n"
                "RESPONSE: " + response + "\n\n" + "-"*50 + "\n\n"
                "METADATA: \n" + "\n".join(list(map(lambda x: str(x.metadata["source"]), compressed_docs))) + "\n\n" + "-"*50 + "\n\n"
                "DOCUMENTS: \n" + pretty_print_docs(compressed_docs) + "\n\n" + ("-"*50 + "\n" + "-"*50 + "\n" + "-"*50) + "\n",
                f"./chat_core/logs/{str(user_id)}-{conversation_id}/compressor_{str(compressor_type)}/info/response.txt"
            )

            logging.info(f"RESPONSE -- \n {response} \n")
            
            return response, abstracts_filename
        
    except Exception as e:
        return "Error: " + str(e), ""





# def main():

#     # Parser for shell script
#     parser = argparse.ArgumentParser(description='RAG Application')
#     parser.add_argument('--question', type=str, help='User query')
#     parser.add_argument('--compressor_type', type=int, help='type of retriever compressor')
#     parser.add_argument('--db_path', type=str, default="./rag_core/database/chroma_db", help='path to database')
#     parser.add_argument('--user_id', type=str, help='user id')
#     parser.add_argument('--conversation_id', type=str, help='conversation id')
#     parser.add_argument('--k', type=int, default=3, help='Number of relevant docs')
#     parser.add_argument('--embedding_type', type=int, default=1, help='embedding_type')
#     parser.add_argument('--model_path', type=str, default="finetune_embedder/models/v1", help='embedding_type')

#     args = parser.parse_args()

#     # Set up logging
#     logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#     # Load neccessary components
#     embedding, retriever = load_retriever(k=args.k, embedding_type=args.embedding_type, db_path = args.db_path)
#     get_compressed_docs = load_CCCompressor( compressor_type = int(args.compressor_type))

#     # Ranking the documents
#     logging.info("Getting compressed_docs")
#     abstracts = retriever.invoke(args.question)

#     # Get the docs id
#     abstracts_filename = list(map(lambda x: x.metadata["source"].split("/")[-1], abstracts))
#     papers = get_paper(abstracts_filename)

#     # Create retriever for paper
#     db = chroma_vectorstore(papers, embedding, save_local=False)
#     paper_retriever = db.as_retriever()

#     llm = OllamaLLM(model="llama3")
#     compressed_docs = get_compressed_docs(args.question, llm, paper_retriever)


#     # Get prompt for the question
#     prompt = prompt_template()
#     runnable = prompt | llm
#     formatted_doc = format_docs(compressed_docs)

#     # Get chat history
#     runnable_with_history = get_runnable_history(runnable)

#     response = runnable_with_history.invoke(
#         {
#             "question": args.question,
#             "context": formatted_doc
#         },
#         config={"configurable": 
#                 {
#                     "user_id": args.user_id, 
#                     "conversation_id": args.conversation_id,
#                 }},
#     )

#     # Save the answer log to txt file
#     add_log(
#         "USER: " + args.question + "\n\n"
#         "SYSTEM: " + response  + "\n\n" + "-"*50 + "\n",
#         f"./chat_core/logs/{str(args.user_id)}-{args.conversation_id}/compressor_{str(args.compressor_type)}/chat/response.txt"
#     )

#     add_log(
#         "QUESTION: " + args.question + "\n\n" + "-"*50 + "\n\n"
#         "RESPONSE: " + response + "\n\n" + "-"*50 + "\n\n"
#         "METADATA: \n" + "\n".join(list(map(lambda x: str(x.metadata["source"]), compressed_docs))) + "\n\n" + "-"*50 + "\n\n"
#         "DOCUMENTS: \n" + pretty_print_docs(compressed_docs) + "\n\n" + ("-"*50 + "\n" + "-"*50 + "\n" + "-"*50) + "\n",
#         f"./chat_core/logs/{str(args.user_id)}-{args.conversation_id}/compressor_{str(args.compressor_type)}/info/response.txt"
#     )

#     logging.info(f"RESPONSE -- \n {response} \n")
#     return response


# if __name__ == "__main__":
#     main()