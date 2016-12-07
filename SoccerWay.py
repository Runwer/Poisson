import pandas as pd
import urllib2
from bs4 import BeautifulSoup
import re
import urlparse
import json
from timestring import Date, Range
from datetime import datetime, timedelta

def getpage(url):
    page = urllib2.urlopen(url)
    return page.read()

def match_data(soup, url):
    dict = {}
    dict['date'] = Date(url[url.find('matches/')+8:url.find('/england')])
    if (Date(dict['date'])+85000) < datetime.now():
        dict['finalscore'] = soup.find('h3', {'class': 'thick scoretime '}).string.strip()
        dict['scores'] = []

        goals = soup.find('div', {'id': 'page_match_1_block_match_goals_13-wrapper'})

        for g in goals.find_all('tr', {'class': 'event    expanded'}):
            dict['scores'].append(
                {g.find('span', {'class': 'minute'}).string: g.find('td', {'class': 'event-icon'}).string})

        dict['teamH'] = soup.find('div', {'class': 'block_match_info real-content clearfix '}).find('h3', {
            'class': 'thick'}).findNext('a').string
        dict['teamA'] = \
        soup.find('div', {'class': 'block_match_info real-content clearfix '}).find_all('h3', {'class': 'thick'})[
            1].findNext('a').string
    return dict

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
        match_db[matchid] = match_data(soup, url)
    return new_urls

url_crawled = json.loads(open('crawled.json').read())
match_db = {}
url_to_crawl = ['http://www.soccerway.com/matches/2016/12/03/england/premier-league/manchester-city-football-club/chelsea-football-club/2241892']#json.loads(open('to_crawl.json').read())



i = 0
while True:
    #try:
    temp = url_to_crawl.pop()
    print temp
    url_crawled.append(temp)
    url_to_crawl = url_to_crawl + find_links(temp, url_crawled, url_to_crawl)
    #except:
    #    print temp
    #    break
    i += 1
    print i
    if i > 10:
        #with open('crawled.json', 'wb') as outfile:
        #    json.dump(url_crawled, outfile)
        #with open('to_crawl.json', 'wb') as outfile:
        #    json.dump(url_to_crawl, outfile)
        #with open('match_db.json', 'w') as fp:
        #    json.dump(match_db, fp)
        break



print url_to_crawl
print url_crawled
print match_db