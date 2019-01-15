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

def getLetters(soup):
    pages = []
    letters = soup.find('td', {'style': 'padding-bottom:7px;background-image:url(/images/_index_bg.gif);background-repeat: repeat-x;'}).findAll("a", {'href': re.compile('/famous_authors/')})
    #categories = categories.findAll("a")
    #categories = categories[0]
    for letter in letters:
        pages.append(letter["href"])
    return pages

def getAuthors(soup):
    authors = soup.find('table', {'bordercolor': '#FFFFFF'}).findAll("a", {'href': re.compile('/authors/')})
    #categories = categories.findAll("a")
    #categories = categories[0]
    pages = [author['href'] for author in authors]
    return pages

def getQoutes(soup, author):
    qoutes = soup.find("td", {"width": "460"}).findAll('div', {'style':'font-size:12px;font-family:Arial;'})
    lst = []
    for qoute in qoutes:
        dct = dict()
        dct['poem'] = qoute.text
        dct['author'] = author
        lst.append(dct)
    return lst

    


    #lst = []
    #for poem in poems:
    #    dct = {}
    #    poem = poem.text
    #    try:
    #        _, poem, author, _ = [x for x in poem.splitlines()]
    #        dct["poem"] = poem.strip()[2:-1]
    #        dct["author"] = author
    #        dct["category"] = category_string
    #        lst.append(dct)
    #    except:
    #        continue
    #return lst



def writeJSON(all_poems, name):
    with open("qoutes/" + name + ".json", "w") as f:
        json.dump(all_poems, f)


def main():
    url = 'http://www.famousquotesandauthors.com'
    
    webpage = open_webpage(url)
    letter_urls = getLetters(webpage)
    print('finished getting letter homepages')

    author_urls = []
    for url_affix in letter_urls:
        webpage = open_webpage(url + url_affix)
        author_url = getAuthors(webpage)
        author_urls += author_url
        

    total_qoutes = 0
    all_qoutes = []
    print('finished collecting author homepages')
    for index, url_affix in enumerate(author_urls):
        try:
            author = url_affix.split('/')[2].split('.')[0]
        except:
            author = 'na'
            print(url_affix)
        try:
            webpage = open_webpage(url + url_affix)
        except:
            print(url_affix, '  87')
        qoutes = getQoutes(webpage, author)
        total_qoutes += len(qoutes)
        all_qoutes += qoutes
        if index % 50 == 0:
            print(f'qoutes so far: {total_qoutes}')
    

    print(f"Scrapped {len(all_qoutes)} qoutes")
    writeJSON(all_qoutes, "harry_sayings")
    sleep(random.randint(1, 3))

if __name__ == '__main__':
    main()




