import urllib.request
from urllib.request import Request
from bs4 import BeautifulSoup
from time import sleep
import json
import random
import re


def open_webpage(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urllib.request.urlopen(req).read()
    return BeautifulSoup(webpage)


def getPoems(soup, category_string="no category"):
    poems = soup.findAll("font", {"color":"#333333", "size":2})
    lst = []
    for poem in poems[1:]:
        if poem.text != "Rate this Quote!":
            dct = {}
            dct["poem"] = poem.text
            dct["category"] = category_string
            lst.append(dct)

    return lst


def getCategories(soup):
    pages = []
    categories = soup.findAll("nobr")
    for category in categories:
        pages.append(category.find("a", href=True)["href"])

    return pages


def writeJSON(all_poems, name):
    with open("qoutes/" + name + ".json", "w") as f:
        json.dump(all_poems, f)


def main():
    url = 'http://www.quoteland.com/topic.asp'
    webpage = open_webpage(url)
    categories = getCategories(webpage)
    all_poems = []
    saved = 0
    for category in categories:
        category_url = "http://www.quoteland.com/topic/" + category
        temp = re.findall("\w+", category)
        category_string = ' '.join(temp[1:-2])
        print("Scraping catagory:", category_string)
        webpage = open_webpage(category_url)
        pages = webpage.findAll("table", {"class" : "pagination"})
        num_pages = len(pages[0].find_all("a"))
        for i in range(num_pages):
            print("Scraping page", i + 1, "out of", num_pages)
            if i == 0:
                page_url = category_url
            else:
                page_url = category_url + "?pg" + str(i + 1)

            try:
                webpage = open_webpage(page_url)
                all_poems.extend(getPoems(webpage, category_string))
            except:
                continue
            sleep(random.randint(1, 2))

        print("Scraped ", len(all_poems), " poems")
        if len(all_poems) > saved * 100:
            writeJSON(all_poems, "quoteland")
            saved = len(all_poems) / 100
        sleep(random.randint(1, 3))


if __name__ == '__main__':
    main()




