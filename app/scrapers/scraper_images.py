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

def append_images_to_json(json_filename, from_idx, to_idx=0):
    parent_dir = (os.getcwd()) # makes it usable from "main.py", comment it out to run from current script file
    with open(parent_dir + '/quotes/'+json_filename, 'r') as f:
        quotes_json = json.load(f)
        if to_idx == 0:
            to_idx = len(quotes_json)
        idx = from_idx
    for each_dict in quotes_json[from_idx:to_idx]:
        if idx == to_idx:
            break
        else:
            quote = each_dict["poem"]
            keywords = get_keywords(quote)
            keywords = " ".join(keywords).replace(',','').replace('.','')
            output_dir = '/static/images/'+json_filename.split("_")[1].split('.')[0]
            arguments = {"keywords":keywords,
                         "limit":3,
                         "size":"medium",
                         "output_directory": parent_dir+output_dir,
                         "image_directory":str(idx),
                         "no_numbering": True}   #creating list of arguments
            if keywords != "":
                scrape_image(keywords,arguments)
                each_dict["image"] = output_dir + '/'+str(idx) + '/' #specifying path containing images for a particular quote
                print("Done image # ", idx)
            idx += 1 
    with open(parent_dir + '/quotes/'+json_filename, 'w') as outfile:
        json.dump(quotes_json, outfile)    
#        pprint(quotes_json)
def append_specificquoteimages_to_json(quote_list, json_filename):
    with open(parent_dir + '/quotes/'+json_filename) as f:
        quotes_json = json.load(f)
    for idx, each_dict in enumerate(quotes_json):
        quote = each_dict["poem"]
        if quote in quote_list:            
            keywords = get_keywords(quote)
            keywords = " ".join(keywords).replace(',','').replace('.','')
            output_dir = '/static/images/'+json_filename.split(".")[0]
            arguments = {"keywords":keywords,
                         "limit":4,
                         "size":"medium",
                         "output_directory": parent_dir+output_dir,
                         "image_directory":str(idx),
                         "no_numbering": True}   #creating list of arguments
#            print(keywords)
            scrape_image(keywords,arguments)
            each_dict["image"] = output_dir + '/'+str(idx) + '/' #specifying path containing images for a particular quote
    with open(parent_dir + '/quotes/'+'withimages_'+json_filename, 'w') as outfile:
        json.dump(quotes_json, outfile)  
        
def get_image_location(quote, json_filename):
    # RETURNS img_location and image_filename
    parent_dir = (os.getcwd()) # makes it usable from "main.py", comment it out to run from current script file
    with open(parent_dir + '/quotes/'+json_filename) as f:
        quotes_json = json.load(f)
    for idx, each_dict in enumerate(quotes_json):
        dict_quote = each_dict["poem"]
        if dict_quote == quote:
            if "image" in each_dict:
                image_location = each_dict["image"]
            else:
                append_images_to_json(json_filename, idx, idx+1)
                with open(parent_dir + '/quotes/'+json_filename) as updated_f:
                    updated_quotes_json = json.load(updated_f)                
                    image_location = updated_quotes_json[idx]["image"]
            image_filenames = []
            for root, dirs, files in os.walk(parent_dir+image_location):  
                for filename in files:
                    image_filenames.append(filename)
            image_name = random.sample(image_filenames,1)[0]
            return image_location, image_name
    return "", ""


############
# UNCOMMENT THIS CODE BLOCK TO SCRAPE IMAGES    
#
#file_name = "withimages_wiseoldsayings.json"
#quote_list = ["Anger ... it's a paralyzing emotion ... you can't get anything done", "Be believing, be happy, don't get discouraged. Things will work out"]
#append_specificquoteimages_to_json(quote_list, file_name)
#append_images_to_json(file_name, 300, 301)
############

#quote = "All the wonders you seek are within yourself"
#file_name = "withimages_wiseoldsayings.json"
#image_loc, img_name = get_image_location(quote, file_name)
#print(image_loc, img_name)
#quote="It's the life one wants to live"
#keywords = get_keywords(quote,['NOUN', 'ADJ','ADV','VERB'],stop_words=True)
#keywords = " ".join(keywords)
#print(keywords)
