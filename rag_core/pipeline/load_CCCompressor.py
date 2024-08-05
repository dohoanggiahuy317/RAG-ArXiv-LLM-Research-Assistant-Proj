from rag_core.utils.contextual_compression import llm_extract, llm_filter

import logging

def load_CCCompressor(compressor_type=3):
    
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    if compressor_type == 1:
        logging.info("Get LLM_FILTER compressor")
        return llm_filter.get_compressed_docs
    if compressor_type == 2:
        logging.info("Get LLM_EXTRACT compressor")
        return llm_extract.get_compressed_docs

    return llm_extract.get_compressed_docs
