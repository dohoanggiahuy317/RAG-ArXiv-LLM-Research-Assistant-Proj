from langchain_chroma import Chroma

def chroma_vectorstore(texts, embedding, db_path="./rag_core/database/chroma_db", ids = None, save_local = True):
    
    if save_local:
        db = Chroma.from_documents(
                            texts, 
                            embedding,
                            ids, 
                            persist_directory=db_path,)
    else:
        db = Chroma.from_documents(
                            texts, 
                            embedding,
                            ids)
    
    return db