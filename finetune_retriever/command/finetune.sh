# Define the root directory of your project
ROOT_DIR="."

# Export PYTHONPATH to include the root directory
export PYTHONPATH="$ROOT_DIR"

# python3 finetune_retriever/code/data_prep.py \
#     --csv_filename "data/papers_abstract.csv" \
#     --output_dir "finetune_retriever/data"


python3 finetune_retriever/code/finetune.py \
    --dataset_train_path "finetune_retriever/data/data_label.json"  \
    --model_name "BAAI/bge-small-en-v1.5" \
    --epoch 10 \
    --batch_size 16 \
    --model_path "finetune_retriever/model/finetune_v2/"
