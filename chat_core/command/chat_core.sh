# Define the root directory of your project
ROOT_DIR="."

# Export PYTHONPATH to include the root directory
export PYTHONPATH="$ROOT_DIR"

python3 chat_core/chatbot.py \
    --question "what do you know about LLM" \
    --compressor_type 1 \
    --db_path "./rag_core/database/chroma_db" \
    --user_id "admin" \
    --conversation_id "1" \
    --k 3
