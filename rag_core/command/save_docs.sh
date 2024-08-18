# Define the root directory of your project
ROOT_DIR="."

# Export PYTHONPATH to include the root directory
export PYTHONPATH="$ROOT_DIR"

python3 rag_core/pipeline/save_docs.py \
    --docs_path "./data/abstract" \
    --db_path "./rag_core/database/chroma_db_local_embedding_v2" \
    --embedding_type 2