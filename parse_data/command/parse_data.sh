python3 parse_data/code/collect_data/parse_data.py \
    --base_url "https://export.arxiv.org/api/query?" \
    --output_filename 'data/papers_abstract.csv' \
    --total_results 300

python3 parse_data/code/collect_data/split_paper.py \
    --csv_filepath "data/papers_abstract.csv" \
    --output_dir "data"