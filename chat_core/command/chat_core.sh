# Define the root directory of your project
ROOT_DIR="."

# Export PYTHONPATH to include the root directory
export PYTHONPATH="$ROOT_DIR"


python3 chat_core/chatbot.py \
    --question "How can Large Language Models (LLMs) be susceptible to adversarial attacks, and what are the implications of such vulnerabilities?" \
    --compressor_type 1 \
    --db_path "./database/rag_core/chroma_db_custom_embedding" \
    --user_id "Huy" \
    --conversation_id "1" \
    --k 3 \
    --embedding_type 1




# python3 chat_core/chatbot.py \
#     --question "How can Large Language Models (LLMs) be susceptible to adversarial attacks, and what are the implications of such vulnerabilities?" \
#     --compressor_type 1 \
#     --db_path "./database/rag_core/chroma_db" \
#     --user_id "admin" \
#     --conversation_id "1" \
#     --k 3 \
#     --embedding_type 1


# python3 chat_core/chatbot.py \
#     --question "How does the “LLM-as-a-Judge” metric align with human judgment in assessing bias in LLM-generated responses?" \
#     --compressor_type 1 \
#     --db_path "./database/rag_core/chroma_db" \
#     --user_id "admin" \
#     --conversation_id "1" \
#     --k 3 \
#     --embedding_type 1

# python3 chat_core/chatbot.py \
#     --question "What are the key strengths and weaknesses of different model families in responding to adversarial prompts aimed at eliciting biased outputs?" \
#     --compressor_type 1 \
#     --db_path "./database/rag_core/chroma_db" \
#     --user_id "admin" \
#     --conversation_id "1" \
#     --k 3 \
#     --embedding_type 1




# =================== #
# =================== #
# =================== #
# =================== #


# python3 chat_core/chatbot.py \
#     --question "How can Large Language Models (LLMs) be susceptible to adversarial attacks, and what are the implications of such vulnerabilities?" \
#     --compressor_type 1 \
#     --db_path "./database/rag_core/chroma_db_local_embedding" \
#     --user_id "admin" \
#     --conversation_id "2" \
#     --k 3 \
#     --embedding_type 2


# python3 chat_core/chatbot.py \
#     --question "How does the “LLM-as-a-Judge” metric align with human judgment in assessing bias in LLM-generated responses?" \
#     --compressor_type 1 \
#     --db_path "./database/rag_core/chroma_db_local_embedding" \
#     --user_id "admin" \
#     --conversation_id "2" \
#     --k 3 \
#     --embedding_type 2

# python3 chat_core/chatbot.py \
#     --question "What are the key strengths and weaknesses of different model families in responding to adversarial prompts aimed at eliciting biased outputs?" \
#     --compressor_type 1 \
#     --db_path "./database/rag_core/chroma_db_local_embedding" \
#     --user_id "admin" \
#     --conversation_id "2" \
#     --k 3 \
#     --embedding_type 2




# =================== #
# =================== #
# =================== #
# =================== #


# python3 chat_core/chatbot.py \
#     --question "How can Large Language Models (LLMs) be susceptible to adversarial attacks, and what are the implications of such vulnerabilities?" \
#     --compressor_type 1 \
#     --db_path "./database/rag_core/chroma_db_local_embedding" \
#     --user_id "admin" \
#     --conversation_id "3" \
#     --k 3 \
#     --embedding_type 2


# python3 chat_core/chatbot.py \
#     --question "How does the “LLM-as-a-Judge” metric align with human judgment in assessing bias in LLM-generated responses?" \
#     --compressor_type 1 \
#     --db_path "./database/rag_core/chroma_db_local_embedding" \
#     --user_id "admin" \
#     --conversation_id "3" \
#     --k 3 \
#     --embedding_type 2

# python3 chat_core/chatbot.py \
#     --question "What are the key strengths and weaknesses of different model families in responding to adversarial prompts aimed at eliciting biased outputs?" \
#     --compressor_type 1 \
#     --db_path "./database/rag_core/chroma_db_local_embedding" \
#     --user_id "admin" \
#     --conversation_id "3" \
#     --k 3 \
#     --embedding_type 2