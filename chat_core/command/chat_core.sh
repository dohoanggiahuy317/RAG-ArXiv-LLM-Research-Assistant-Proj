# Define the root directory of your project
ROOT_DIR="."

# Export PYTHONPATH to include the root directory
export PYTHONPATH="$ROOT_DIR"

python3 chat_core/chatbot.py \
    --question "How can Large Language Models (LLMs) be susceptible to adversarial attacks, and what are the implications of such vulnerabilities?" \
    --compressor_type 1 \
    --db_path "./rag_core/database/chroma_db" \
    --user_id "admin" \
    --conversation_id "1" \
    --k 3 \
    --embedding_type 1


python3 chat_core/chatbot.py \
    --question "How do the LLM-based bias evaluation metrics proposed in this work compare to existing human-generated templates and annotations?" \
    --compressor_type 1 \
    --db_path "./rag_core/database/chroma_db" \
    --user_id "admin" \
    --conversation_id "1" \
    --k 3 \
    --embedding_type 1

python3 chat_core/chatbot.py \
    --question "What are the key strengths and weaknesses of different model families in responding to adversarial prompts aimed at eliciting biased outputs?" \
    --compressor_type 1 \
    --db_path "./rag_core/database/chroma_db" \
    --user_id "admin" \
    --conversation_id "1" \
    --k 3 \
    --embedding_type 1




# =================== #
# =================== #
# =================== #
# =================== #


python3 chat_core/chatbot.py \
    --question "How can Large Language Models (LLMs) be susceptible to adversarial attacks, and what are the implications of such vulnerabilities?" \
    --compressor_type 1 \
    --db_path "./rag_core/database/chroma_db_local_embedding" \
    --user_id "admin" \
    --conversation_id "2" \
    --k 3 \
    --embedding_type 2


python3 chat_core/chatbot.py \
    --question "How do the LLM-based bias evaluation metrics proposed in this work compare to existing human-generated templates and annotations?" \
    --compressor_type 1 \
    --db_path "./rag_core/database/chroma_db_local_embedding" \
    --user_id "admin" \
    --conversation_id "2" \
    --k 3 \
    --embedding_type 2

python3 chat_core/chatbot.py \
    --question "What are the key strengths and weaknesses of different model families in responding to adversarial prompts aimed at eliciting biased outputs?" \
    --compressor_type 1 \
    --db_path "./rag_core/database/chroma_db_local_embedding" \
    --user_id "admin" \
    --conversation_id "2" \
    --k 3 \
    --embedding_type 2