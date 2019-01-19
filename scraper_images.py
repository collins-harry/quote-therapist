from scrapers.google_images_download import google_images_download   #importing the library
import os
import sys
import json
from pprint import pprint

parent_dir = os.getcwd()
sys.path.append(parent_dir)
from quote_functions.get_keywords import get_keywords

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
    with open(parent_dir + '/quotes/'+'withimages_'+json_filename, 'w') as outfile:
        json.dump(quotes_json, outfile)    
        pprint(quotes_json)
        
        
def get_image_location(quote, json_filename):
    with open(parent_dir + '/quotes/'+json_filename) as f:
        quotes_json = json.load(f)
        quotes_json = quotes_json[:2]
        pprint(quotes_json)
    for each_dict in quotes_json:
        dict_quote = each_dict["poem"]
        if dict_quote == quote:
            image_location = each_dict["image"]
            return image_location
    return ""

      
if __name__ == '__main__':
    quote = "Acting deals with very delicate emotions. It is not putting up a mask. Each time an actor acts he does not hide; he exposes himself"

    file_name = "wiseoldsayings.json"
    #file_name = "data.json"
    append_images_to_json(file_name)
    #image_loc = get_image_location(quote, file_name)
    #print(image_loc)
    #quote="It's the life one wants to live"
    #keywords = get_keywords(quote,['NOUN', 'ADJ','ADV','VERB'],stop_words=True)
    #keywords = " ".join(keywords)
    #print(keywords)
