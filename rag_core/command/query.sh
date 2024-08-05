# Define the root directory of your project
ROOT_DIR="."

# Export PYTHONPATH to include the root directory
export PYTHONPATH="$ROOT_DIR"

python3 rag_core/main.py \
    --question "what do you know about LLM" \
    --compressor_type 2 \
    --db_path "./rag_core/database/chroma_db" \
    --k 2
