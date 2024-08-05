from langchain_chroma import Chroma

def chroma_retriever(embedding, db_path="./rag_core/database/chroma_db", search_type="similarity_score_threshold", score_threshold=0.5, k=3):
    db = Chroma(
        persist_directory=db_path, 
        embedding_function=embedding)

    retriever = db.as_retriever(
                            search_type=search_type, 
                            search_kwargs={
                                "score_threshold": score_threshold,
                                "k": k}
                            )
    
    return retriever