from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
import torch


def get_embedding():
    device = "cuda" if torch.cuda.is_available() else "cpu"


    model_name = "BAAI/bge-small-en"
    model_kwargs = {"device": device}
    encode_kwargs = {"normalize_embeddings": True}
    
    embedding = HuggingFaceBgeEmbeddings(
        model_name=model_name, 
        model_kwargs=model_kwargs, 
        encode_kwargs=encode_kwargs
    )

    return embedding

def get_local_embedding(model_path):
    device = "cuda" if torch.cuda.is_available() else "cpu"

    model_name = model_path
    model_kwargs = {"device": device}
    encode_kwargs = {"normalize_embeddings": True}
    
    embedding = HuggingFaceEmbeddings(
        model_name=model_name, 
        model_kwargs=model_kwargs, 
        encode_kwargs=encode_kwargs
    )

    return embedding