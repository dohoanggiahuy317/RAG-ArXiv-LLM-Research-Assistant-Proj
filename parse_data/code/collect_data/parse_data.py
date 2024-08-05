import argparse
import logging
import time

from utils.parser import write_data, get_data
from utils.scrape_preprocessing import create_output_file, get_processed_link # type: ignore
from utils.scrape_preprocessing import link_valid



def lazy_parsing(base_url, processed_links, query):
    # Initialize containers for page data and counters
    page = {
            "id": [],
            "link": [],
            "title": [],
            "abstract": [],
            "authors": [],
            "published": [],
        }
    
    # Fetch data
    feed = get_data(base_url, query)

    # Run through each entry, and print out information
    for entry in feed.entries:
        if link_valid(entry.link, processed_links):
            page["id"].append(entry.id)
            page["link"].append(entry.link)
            page["title"].append(entry.title)
            page["abstract"].append(entry.summary)
            page["authors"].append(entry.authors)
            page["published"].append(entry.published)
            logging.info(f"Saved!")


    return page



def main():
    """
    Main function to set up logging, initialize the loader, and start parsing.
    """

    parser = argparse.ArgumentParser(description='Scrap content from a link')
    parser.add_argument('--base_url',               
                        type=str, 
                        help='link of the root url')
    
    parser.add_argument('--search_query',                  
                        type=str, 
                        help='query pattern',
                        default='cat:%22cs.CL%22')
    parser.add_argument('--start_index',                  
                        type=int, 
                        help='start index of arxiv',
                        default=0)
    parser.add_argument('--total_results', 
                        type=int, 
                        help='total paper threshold', 
                        default=10)
    parser.add_argument('--results_per_iteration', 
                        type=int, 
                        help='lazy loading threshold', 
                        default=2)
    parser.add_argument('--sortBy', 
                        type=str, 
                        help='sort by', 
                        default="submittedDate")
    parser.add_argument('--sortOrder', 
                        type=str, 
                        help='sort order', 
                        default="descending")
    
    parser.add_argument('--waitTime', 
                        type=int, 
                        help='time wait after each iteration', 
                        default=0.5)
    parser.add_argument('--output_filename', 
                        type=str, 
                        help='path to content file in csv')
    
    args = parser.parse_args()

    # Setup logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Output filename
    create_output_file(args.output_filename)

    # Start parsing the documents
    fail_queries, processed_links = set(), get_processed_link(args.output_filename)

    # Start scraping    
    logging.info(f"Starting to scrape...")
    total = 0

    for start_query in range(args.start_index, args.total_results, args.results_per_iteration):
        query = ('search_query=%s&start=%i&max_results=%i&sortBy=%s&sortOrder=%s') % (args.search_query, start_query, args.results_per_iteration, args.sortBy, args.sortOrder)

        try:
            # Lazy load each batch
            logging.info(f"Processing {args.results_per_iteration} documents (total {total} documents)...")
            page = lazy_parsing(args.base_url, processed_links, query)

            # Saved loaded Linked
            for link in page["link"]:
                processed_links.add(link)

            # write data
            write_data(page, args.output_filename)
            total += args.results_per_iteration

            # logging info
            logging.error(f"Time sleep for {args.waitTime} seconds...")
            time.sleep(int(args.waitTime))
   
        except Exception as e:
            fail_queries.add(query)
            logging.error(f"Error processing URL {query}: {e}")



    # Scrape fail documents
    if len(fail_queries):
        logging.info(f"Starting to scrape fail queries...")
        total = 0
        
        for query in fail_queries:
            try:
                # Lazy load each batch
                page = lazy_parsing(args.base_url, processed_links, query)

                # Saved loaded Linked
                for link in page["link"]:
                    processed_links.add(link)

                # write data
                write_data(page, args.output_filename)
                total += args.results_per_iteration

                # logging info
                logging.info(f"Processed and saved {args.results_per_iteration} documents (total {total} documents)")
                
            except Exception as e:
                # logging info
                logging.error(f"Error processing URL {query}: {e}")


# Run the main function
if __name__ == "__main__":   
    main()