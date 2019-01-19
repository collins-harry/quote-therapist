import os
import sys
import json
from pprint import pprint
import random

parent_dir = os.path.dirname(os.getcwd())
sys.path.append(parent_dir)
from quote_mappers.quote_functions.get_keywords import get_keywords
from scrapers.google_images_download import google_images_download   #importing the library


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
        output_dir = '/static/images/'+json_filename.split(".")[0]
        arguments = {"keywords":keywords,
                     "limit":4,
                     "size":"medium",
                     "output_directory": parent_dir+output_dir,
                     "image_directory":str(idx),
                     "no_numbering": True}   #creating list of arguments
        scrape_image(keywords,arguments)
        each_dict["image"] = output_dir + '/'+str(idx) + '/' #specifying path containing images for a particular quote
    with open(parent_dir + '/quotes/'+'withimages_'+json_filename, 'w') as outfile:
        json.dump(quotes_json, outfile)    
#        pprint(quotes_json)
        
def get_image_location(quote, json_filename):
    # RETURNS img_location and image_filename
    parent_dir = (os.getcwd())
    with open(parent_dir + '/quotes/'+json_filename) as f:
        quotes_json = json.load(f)
        quotes_json = quotes_json[:2]
    for each_dict in quotes_json:
        dict_quote = each_dict["poem"]
        if dict_quote == quote:
            image_location = each_dict["image"]
            image_filenames = []
            for root, dirs, files in os.walk(parent_dir+image_location):  
                for filename in files:
                    image_filenames.append(filename)
            image_name = random.sample(image_filenames,1)[0]
            return image_location, image_name
    return "", ""

############
# UNCOMMENT THIS CODE BLOCK TO SCRAPE IMAGES    

#file_name = "wiseoldsayings.json"
#append_images_to_json(file_name)
############
    

#quote = "Acting deals with very delicate emotions. It is not putting up a mask. Each time an actor acts he does not hide; he exposes himself"
#file_name = "withimages_wiseoldsayings.json"
#image_loc, img_name = get_image_location(quote, file_name)
#print(image_loc, img_name)
#quote="It's the life one wants to live"
#keywords = get_keywords(quote,['NOUN', 'ADJ','ADV','VERB'],stop_words=True)
#keywords = " ".join(keywords)
#print(keywords)