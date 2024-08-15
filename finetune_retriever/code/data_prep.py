import os
import pandas as pd
import argparse
import json
import logging

from collections import defaultdict

# Convert to json
def to_json(data, file_path):
    json_file = open(file_path, 'w')
    json.dump(data, json_file, indent=4)


def csv_2_label(csv_filename, output_dir):

    # Init the path if not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get the abstract by authors
    authors_2_abstracts = defaultdict(list)
    df = pd.read_csv(csv_filename)
    for _, row in df.iterrows():
        abstract = row["abstract"]
        authors =  eval(row["authors"])
        authors = list(map(lambda x: x['name'], authors))

        for author in authors:
            authors_2_abstracts[author].append(abstract)

    # Logging
    logging.info(f"Proccessed {len(authors_2_abstracts)} authors.")

    # labeling data
    train_data = []
    for _, papers in authors_2_abstracts.items():
        if len(papers) > 1:
            example = {
                "query": None,
                "pos": [],
                "neg": ["[None]"]
            }

            # Save to example
            example["query"] = papers[0]
            example["pos"] = papers[1:]

            train_data.append(example)

    # Logging
    logging.info(f"Labeled {len(train_data)} data.")


    # Save to json
    to_json(train_data, output_dir + "/data_label.json")

    return train_data


def main():
    parser = argparse.ArgumentParser(description='convert csv to docx')
    parser.add_argument('--csv_filename', type=str, help='path to csv')    
    parser.add_argument('--output_dir', type=str, help='path to csv')
    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Label data
    csv_2_label(args.csv_filename, args.output_dir)

# Run the main function
if __name__ == "__main__":
    main()