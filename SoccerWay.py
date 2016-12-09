import pandas as pd
import urllib2
from bs4 import BeautifulSoup
import re
import urlparse, random
import json
from timestring import Date, Range
from datetime import datetime, timedelta
from selenium import webdriver
import argparse, os, time

def getpage(url):
    page = urllib2.urlopen(url)
    return page.read()

def match_data(soup, url):
    dict = {}
    dict['date'] = Date(url[url.find('matches/')+8:url.find('/england')])
    if (Date(dict['date'])+85000) < datetime.now():
        dict['finalscore'] = soup.find('h3', {'class': 'thick scoretime '}).string.strip()
        if dict['finalscore'] != '0 - 0':
            dict['scores'] = []
            try:
                goals = soup.find('div', {'id': 'page_match_1_block_match_goals_13-wrapper'})
                for g in goals.find_all('tr', {'class': 'event    expanded'}):
                    dict['scores'].append(
                        {g.find('span', {'class': 'minute'}).string: g.find('td', {'class': 'event-icon'}).string})
            except:
                try:
                    goals = soup.find('div', {'id': 'page_match_1_block_match_goals_12-wrapper'})
                    for g in goals.find_all('tr', {'class': 'event    expanded'}):
                        dict['scores'].append(
                            {g.find('span', {'class': 'minute'}).string: g.find('td', {'class': 'event-icon'}).string})
                except:
                    dict['scores'] = 'Missing'

        dict['teamH'] = soup.find('div', {'class': 'block_match_info real-content clearfix '}).find('h3', {
            'class': 'thick'}).findNext('a').string
        dict['teamA'] = \
        soup.find('div', {'class': 'block_match_info real-content clearfix '}).find_all('h3', {'class': 'thick'})[
            1].findNext('a').string
    dict['date'] = str(dict['date'])
    return dict

def find_links(url, old_urls, todo_urls):
    new_urls = []
    print url
    page = getpage(urlparse.urljoin('http://www.soccerway.com', url))
    soup = BeautifulSoup(page, "lxml")
    for tag in soup.findAll('a', href=True):
        tempTag = tag['href']
        for t in ['/?', '/map/', '/venue/', '/head2head/', '/#events', '/commentary/']:
            if t in tempTag:
                tempTag = tempTag[:tempTag.find(t[1:])]
        if ('england/premier-league' in tempTag or '/teams/england' in tempTag) and ('/statistics/' not in tempTag and '/venue' not in tempTag and '/transfer' not in tempTag) and (tempTag not in old_urls and tempTag not in todo_urls and tempTag not in new_urls) and all('/'+str(x)+'/' not in tempTag for x in match_db.keys()):
            new_urls.append(tempTag)
    if '/matches/20' in url and '/head2head/' not in url and '/commentary/' not in url and '/map/' not in url and 'venue' not in url and '#events' not in url:
        print url
        find_id = page.find('data-matchids="')
        matchid = page[find_id+15: page.find('"', find_id+15)]
        match_db[matchid] = match_data(soup, url)
    return new_urls

def match_links(url, old_urls, todo_urls):
    chrome_path = "/Users/runewerliin/PycharmProjects/AP_Linkedin/driver/chromedriver"
    browser = webdriver.Chrome(chrome_path)
    browser.get(urlparse.urljoin('http://www.soccerway.com', url))
    time.sleep(random.uniform(1, 2))
    #elem = browser.find_element_by_css_selector("a[class='previous']")[0]
    i = 0
    new_urls = []
    while True:
        elem = browser.find_element_by_id("page_team_1_block_team_matches_5_previous")
        elem.click()
        soup = BeautifulSoup(browser.page_source, "lxml")
        for tag in soup.findAll('a', href=True):
            tempTag = tag['href']
            if ('/england/premier-league/' in tempTag and 'matches/20' in tempTag) and (tempTag not in old_urls and tempTag not in todo_urls and tempTag not in new_urls):
                new_urls.append(tempTag)
        time.sleep(random.uniform(1, 2))
        i += 1
        if i >18:
            break
    return new_urls


url_crawled = json.loads(open('crawled.json').read())
match_db =  json.loads(open('match_db.json').read())
url_to_crawl = json.loads(open('to_crawl.json').read())

i = 0
while True:
    #try:
    temp = url_to_crawl.pop()
    url_crawled.append(temp)
    url_to_crawl = url_to_crawl + find_links(temp, url_crawled, url_to_crawl)
    #except:
    #    print temp
    #    break
    i += 1
    print i
    if i%10 == 0:
        with open('crawled.json', 'wb') as outfile:
            json.dump(url_crawled, outfile)
        with open('to_crawl.json', 'wb') as outfile:
            json.dump(url_to_crawl, outfile)
        with open('match_db.json', 'w') as fp:
            json.dump(match_db, fp)
    if i > 100000:
        break

# for url in ['http://nr.soccerway.com/teams/england/arsenal-fc/660/matches/', 'http://nr.soccerway.com/teams/england/manchester-city-football-club/676/matches/', 'http://nr.soccerway.com/teams/england/sunderland-association-football-club/683/matches/', 'http://nr.soccerway.com/teams/england/afc-bournemouth/711/matches/', 'http://nr.soccerway.com/teams/england/stoke-city-fc/690/matches/', 'http://nr.soccerway.com/teams/england/tottenham-hotspur-football-club/675/matches/', 'http://nr.soccerway.com/teams/england/sunderland-association-football-club/683/matches/', 'http://nr.soccerway.com/teams/england/crystal-palace-fc/679/matches', 'http://nr.soccerway.com/teams/england/west-ham-united-fc/684/matches', 'http://nr.soccerway.com/teams/england/everton-football-club/674/matches', 'http://nr.soccerway.com/teams/england/hull-city-afc/725/matches', 'http://nr.soccerway.com/teams/england/west-bromwich-albion-football-club/678/matches', 'http://nr.soccerway.com/teams/england/manchester-united-fc/662/matches/', 'http://nr.soccerway.com/teams/wales/swansea-city-afc/738/matches', 'http://nr.soccerway.com/teams/england/watford-football-club/696/matches/', 'http://nr.soccerway.com/teams/england/burnley-fc/698/matches/', 'http://nr.soccerway.com/teams/england/southampton-fc/670/matches/', 'http://nr.soccerway.com/teams/england/leicester-city-fc/682/matches/', 'http://nr.soccerway.com/teams/england/liverpool-fc/663/matches/', 'http://nr.soccerway.com/teams/england/chelsea-football-club/661/matches', 'http://nr.soccerway.com/teams/england/wolverhampton-wanderers-fc/680/matches', 'http://nr.soccerway.com/teams/england/blackburn-rovers-football-club/672/matches', 'http://nr.soccerway.com/teams/england/derby-county-fc/699/matches', 'http://nr.soccerway.com/teams/england/huddersfield-town-fc/726/matches', 'http://nr.soccerway.com/teams/england/birmingham-city-fc/669/matches', 'http://nr.soccerway.com/teams/england/ipswich-town-fc/685/matches', 'http://nr.soccerway.com/teams/england/reading-fc/688/matches', 'http://nr.soccerway.com/teams/england/aston-villa-football-club/665/matches', 'http://nr.soccerway.com/teams/england/wigan-athletic-football-club/686/matches', 'http://nr.soccerway.com/teams/england/newcastle-united-football-club/664/matches', 'http://nr.soccerway.com/teams/england/barnsley-fc/716/matches', 'http://nr.soccerway.com/teams/england/sheffield-wednesday-fc/719/matches', 'http://nr.soccerway.com/teams/england/fulham-football-club/667/matches', 'http://nr.soccerway.com/teams/england/queens-park-rangers-fc/702/matches']:
#     url_to_crawl = url_to_crawl + match_links(url,url_crawled,url_to_crawl)
#     with open('crawled.json', 'wb') as outfile:
#         json.dump(url_crawled, outfile)
#     with open('to_crawl.json', 'wb') as outfile:
#         json.dump(url_to_crawl, outfile)

