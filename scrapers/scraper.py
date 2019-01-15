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


def getPoems(soup, category_string):
    poems = soup.findAll("div", {"class": "quote_container"})

    lst = []
    for poem in poems:
        dct = {}
        poem = poem.text
        try:
            _, poem, author, _ = [x for x in poem.splitlines()]
            dct["poem"] = poem.strip()[2:-1]
            dct["author"] = author
            dct["category"] = category_string
            lst.append(dct)
        except:
            continue
    return lst


def getCategories(soup):
    pages = []
    categories = soup.findAll("div", {"class": "cat_list"})
    #categories = categories.findAll("a")
    categories = categories[0].find_all('li')
    for category in categories:
        pages.append(category.find("a", href=True)["href"])

    return pages


def writeJSON(all_poems, name):
    with open("qoutes/" + name + ".json", "w") as f:
        json.dump(all_poems, f)


def main():
    url = 'http://www.wiseoldsayings.com/'
    webpage = open_webpage(url)
    categories = getCategories(webpage)
    all_poems = []
    for category in categories:
        webpage = open_webpage(category)
        category_string = ' '.join(re.findall("\w+", category)[4:-1])
        pages = webpage.findAll("a", href=True)
        all_poems.extend(getPoems(webpage, category_string))
        print("Scraping category: ", category_string, " - page 1")
        try:
            pages = webpage.findAll("ul", {"class":"clear-fix-link"})
            if "page-2" in str(pages):
                webpage = open_webpage(category + "page-2/")
                all_poems.extend(getPoems(webpage, category_string))
                print("Scraping category: ", category, " - page 2")
        except:
            continue

        print("Scraped ", len(all_poems), " poems")
        writeJSON(all_poems, "wiseoldsayings")
        sleep(random.randint(1, 3))


if __name__ == '__main__':
    main()




