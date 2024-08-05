from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda


import logging

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def prompt_template():
    
    template = """You are an assistant for question-answering tasks. 
    Use the following pieces of retrieved context to answer the question. 
    If you don't know the answer, just say that you don't know. 
    Keep the answer concise.

    Question: {question} 

    Context: {context} 

    Answer:"""

    custom_rag_prompt = PromptTemplate.from_template(template)
    return custom_rag_prompt



def get_LLM(compressed_docs, model="llama3"):

    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Get the Ollama
    logging.info("Preparing the prompt...")
    llm = OllamaLLM(model=model)

    formatted_doc = format_docs(compressed_docs)
    formatted_doc_runnable = RunnableLambda(lambda x: "" + formatted_doc)

    custom_rag_prompt = prompt_template()

    rag_chain = (
        {"context": formatted_doc_runnable, "question": RunnablePassthrough()}
        | custom_rag_prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain
