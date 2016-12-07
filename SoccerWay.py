import pandas as pd
import urllib2
from bs4 import BeautifulSoup
import re
import urlparse
import json

def getpage(url):
    page = urllib2.urlopen(url)
    return page.read()

def find_links(url, old_urls, todo_urls):
    new_urls = []
    page = getpage(urlparse.urljoin('http://www.soccerway.com', url))
    soup = BeautifulSoup(page, "lxml")
    for tag in soup.findAll('a', href=True):
        tempTag = tag['href']
        if '/?' in tempTag:
            tempTag = tempTag[:tempTag.find('?')]
        if ('england/premier-league' in tempTag or '/teams/england' in tempTag) and (tempTag not in old_urls and tempTag not in todo_urls) and all('/'+str(x)+'/' not in tempTag for x in match_db.keys()):
            new_urls.append(tempTag)
    if '/matches/20' in url:
        find_id = page.find('data-matchids="')
        matchid = page[find_id+15: page.find('"', find_id+15)]
        match_db[matchid] =0
    return new_urls

url_crawled = json.loads(open('crawled.json').read())
match_db = {}
url_to_crawl = json.loads(open('to_crawl.json').read())



i = 0
while True:
    try:
        temp = url_to_crawl.pop()
        url_crawled.append(temp)
        url_to_crawl = url_to_crawl + find_links(temp, url_crawled, url_to_crawl)
    except:
        break
    i += 1
    print i
    if i > 10:
        with open('crawled.json', 'wb') as outfile:
            json.dump(url_crawled, outfile)
        with open('to_crawl.json', 'wb') as outfile:
            json.dump(url_to_crawl, outfile)
        with open('match_db.json', 'w') as fp:
            json.dump(match_db, fp)
        break



print url_to_crawl
print url_crawled
print match_db