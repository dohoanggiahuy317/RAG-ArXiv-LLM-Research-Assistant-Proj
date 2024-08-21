# Define the root directory of your project
ROOT_DIR="."

# Export PYTHONPATH to include the root directory
export PYTHONPATH="$ROOT_DIR"

python3 rag_core/pipeline/save_docs.py \
    --docs_path "./data/abstract" \
    --db_path "./database/rag_core/chroma_db" \
    --embedding_type 1