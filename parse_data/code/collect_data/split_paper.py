import argparse
import pandas as pd
import os
import logging

from parse_data.code.collect_data.utils.file_saver import save_abstract, save_pdf


def csv_2_txt(csv_filename, output_dir):
    # get the directory
    abstract_dir = output_dir + "/abstract"
    paper_dir = output_dir + "/paper"

    # Create the output directory if it doesn't exist
    if not os.path.exists(abstract_dir):
        os.makedirs(abstract_dir)
    if not os.path.exists(paper_dir):
        os.makedirs(paper_dir)
    
    # Read the input CSV file
    df = pd.read_csv(csv_filename)

    for _, row in df.iterrows():
        paper_id = row["id"].split("/")[-1]
        abstract_path = os.path.join(abstract_dir, f'{paper_id}.txt')
        paper_path = os.path.join(paper_dir, f'{paper_id}.txt')

        # Check if both abstract and paper already exist
        if os.path.exists(abstract_path) and os.path.exists(paper_path):
            logging.info(f"Skipping {paper_id}: File already exists")
            continue  # Skip to the next iteration

        try:
            # Save the abstract if it doesn't exist
            if not os.path.exists(abstract_path):
                save_abstract(row, abstract_dir)

            # Save the paper if it doesn't exist
            if not os.path.exists(paper_path):
                save_pdf(row, paper_dir)

        except Exception as e:
            logging.info(f"Error reading {row['id']}: {e}")

            

def split_paper_abstract(csv_filepath = "test/xxx.csv", output_dir="test"):

    # Setup logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


    # Split paper
    csv_2_txt(csv_filepath, output_dir)



# def main():
#     parser = argparse.ArgumentParser(description='convert csv to docx')
#     parser.add_argument('--csv_filepath', type=str, help='path to csv')
#     parser.add_argument('--output_dir', type=str, help='path to save docx', default=2)
#     args = parser.parse_args()

#     # Setup logging
#     logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


#     # Split paper
#     csv_2_txt(args.csv_filepath, args.output_dir)

# # Run the main function
# if __name__ == "__main__":   
#     main()