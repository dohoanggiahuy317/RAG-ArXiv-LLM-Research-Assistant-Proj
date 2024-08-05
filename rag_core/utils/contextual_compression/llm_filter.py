from langchain.retrievers.document_compressors import LLMChainFilter
from langchain.retrievers import ContextualCompressionRetriever



def get_compressed_docs(question, llm, retriever):

    _filter = LLMChainFilter.from_llm(llm)
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=_filter, base_retriever=retriever
    )

    compressed_docs = compression_retriever.invoke(question)
    return compressed_docs
