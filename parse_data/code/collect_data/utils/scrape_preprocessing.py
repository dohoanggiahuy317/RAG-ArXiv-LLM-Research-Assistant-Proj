import pandas as pd
import os
import logging


def create_output_file(output_filename):
    """
    Create a CSV file with the necessary columns if it does not exist.

    Args:
    output_filename (str): The path to the output CSV file.
    """
    
    # Get the directory path from the filename
    directory = os.path.dirname(output_filename)
    
    # Check if the directory exists, if not, create it
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Check if the file exists
    if not os.path.exists(output_filename):
        # Create the file with the necessary columns if it doesn't exist
        df = pd.DataFrame(columns=["id",
                                   'link', 
                                   'title', 
                                   'abstract',
                                   "authors",
                                   "published"])
        df.to_csv(output_filename, index=False)
    return


def get_processed_link(output_filename):
    """
    Get the set of URLs that have already been processed.

    Args:
    output_filename (str): The path to the output CSV file.

    Returns:
    set: A set of processed URLs.
    """
    print(output_filename)
    df = pd.read_csv(output_filename)
    processed_urls = set(df['link'])
    return processed_urls


def link_valid(curr_link, processed_links):
    # Skip already processed URLs
    if curr_link.strip("#").strip("/") in processed_links or curr_link in processed_links:
        logging.info(f"Skipping already processed paper: {curr_link}")
        return False
    
    return True