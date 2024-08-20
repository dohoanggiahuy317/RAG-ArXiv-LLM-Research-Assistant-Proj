# Define the root directory of your project
ROOT_DIR="."

# Export PYTHONPATH to include the root directory
export PYTHONPATH="$ROOT_DIR"

python3 finetune_embedder/code/data_prep.py \
    --csv_filename "data/papers_abstract.csv" \
    --output_dir "finetune_embedder/data"


python3 finetune_embedder/code/finetune.py \
    --dataset_train_path "finetune_embedder/data/data_label.json"  \
    --model_name "BAAI/bge-small-en-v1.5" \
    --epoch 10 \
    --batch_size 16 \
    --model_path "finetune_embedder/model/"
