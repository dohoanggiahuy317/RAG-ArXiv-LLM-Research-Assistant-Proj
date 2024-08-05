from langchain_community.embeddings import HuggingFaceBgeEmbeddings


def get_embedding():
    model_name = "BAAI/bge-small-en"
    model_kwargs = {"device": "cpu"}
    encode_kwargs = {"normalize_embeddings": True}
    
    embedding = HuggingFaceBgeEmbeddings(
        model_name=model_name, 
        model_kwargs=model_kwargs, 
        encode_kwargs=encode_kwargs
    )

    return embedding