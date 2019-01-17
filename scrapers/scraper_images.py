from google_images_download import google_images_download   #importing the library
import os
import sys
import json
from pprint import pprint

parent_dir = os.path.dirname(os.getcwd())
sys.path.append(parent_dir)
from quote_mappers.quote_functions.get_keywords import get_keywords

def scrape_image(keywords, search_arguments):
    response = google_images_download.googleimagesdownload()   #class instantiation
    paths = response.download(search_arguments)   #passing the arguments to the function
    #print(paths)   #printing absolute paths of the downloaded images    
    
#scrape_image("But all the clocks in the city...")

def append_images_to_json(json_filename):
    with open(parent_dir + '/quotes/'+json_filename) as f:
        quotes_json = json.load(f)
        quotes_json = quotes_json[:2]
    for idx, each_dict in enumerate(quotes_json):
        quote = each_dict["poem"]
        keywords = get_keywords(quote)
        keywords = " ".join(keywords).replace(',','').replace('.','')
        arguments = {"keywords":keywords,
                     "limit":4,
                     "size":"medium",
                     "output_directory":(parent_dir+'/images/'+json_filename.split(".")[0]),
                     "image_directory":str(idx)}   #creating list of arguments
        scrape_image(keywords,arguments)
        each_dict["image"] = '/images/'+ str(idx) + '/' #specifying path containing images for a particular quote
        pprint(quotes_json)

file_name = "wiseoldsayings.json"
append_images_to_json(file_name)
#quote="It's the life one wants to live"
#keywords = get_keywords(quote,['NOUN', 'ADJ','ADV','VERB'],stop_words=True)
#keywords = " ".join(keywords)
#print(keywords)