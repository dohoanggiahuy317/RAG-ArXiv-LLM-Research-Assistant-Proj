import os
import logging

from langchain_community.document_loaders import PyPDFLoader

def save_abstract(row, output_dir):
    text = row['abstract']
    paper_id = row["id"].split("/")[-1]
    
    # Define the output file path
    output_txt_path = os.path.join(output_dir, f'{paper_id}.txt')
    
    # Write the modified text to a new .txt file
    with open(output_txt_path, 'w') as file:
        file.write(text)
    
    logging.info(f"Saved abstract {paper_id}")

def save_pdf(row, output_dir):
    paper_id = row["id"].split("/")[-1]
    paper_link = "https://arxiv.org/pdf/" + row["link"].split("/")[-1]


    # Define the output file path
    output_txt_path = os.path.join(output_dir, f'{paper_id}.txt')

    # Read the pdf
    loader = PyPDFLoader(paper_link)
    pages = loader.load_and_split()

    content = ""
    for page in pages:
        content += page.page_content + "\n\n"

    # Write the modified text to a new .txt file
    with open(output_txt_path, 'w') as file:
        file.write(content)
    
    logging.info(f"Saved paper    {paper_id}")