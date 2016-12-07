import pandas as pd
import urllib2
from bs4 import BeautifulSoup
import re
import urlparse
import json

page = urllib2.urlopen('http://nr.soccerway.com/matches/2016/12/03/england/premier-league/manchester-city-football-club/chelsea-football-club/2241892/').read()
soup = BeautifulSoup(page, "lxml")

def match_data(soup):
    dict = {'finalscore': soup.find('h3', {'class': 'thick scoretime '}).string.strip(), 'scores': []}

    goals = soup.find('div', {'id': 'page_match_1_block_match_goals_13-wrapper'})

    for g in goals.find_all('tr', {'class': 'event    expanded'}):
        dict['scores'].append(
            {g.find('span', {'class': 'minute'}).string: g.find('td', {'class': 'event-icon'}).string})

    dict['teamH'] = soup.find('div', {'class': 'block_match_info real-content clearfix '}).find('h3', {
        'class': 'thick'}).findNext('a').string
    dict['teamA'] = \
    soup.find('div', {'class': 'block_match_info real-content clearfix '}).find_all('h3', {'class': 'thick'})[
        1].findNext('a').string
    dict['date'] = soup.find('div', {'class': 'block_match_info real-content clearfix '}).find('span', {
        'class': 'timestamp'}).string
    return dict

print match_data(soup)


