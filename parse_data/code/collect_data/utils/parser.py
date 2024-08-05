import feedparser
import pandas as pd
import feedparser
import urllib.request as libreq

def get_data(base_url, query):
    # perform a GET request using the base_url and query
    with libreq.urlopen(base_url + query) as url:
        response = url.read()

    # parse the response using feedparser
    feed = feedparser.parse(response)

    return feed

def write_data(page, output_filename):
    new_df = pd.DataFrame(page)
    new_df.to_csv(output_filename, mode='a', index=False, header=False)
    
    # Reset the page dictionary and counter
    page = {
            "id": [],
            "link": [],
            "title": [],
            "abstract": [],
            "authors": [],
            "published": [],
        }
    return page