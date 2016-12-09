#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse, os, time
import urlparse, random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup, NavigableString

test = {}


#getSharesComp('https://www.linkedin.com/company/audience_project/notifications?trk=top_nav_notifications')
def ViewBot(browser):
    browser.get('http://nr.soccerway.com/national/england/premier-league/20162017/regular-season/r35992/matches/')
    while True:
        try:
            #browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(2.5, 3.9))
            try:
                a = browser.find_element_by_class_name("feed-show-more")
            except Exception, e:
                #print str(e)
                print 'Cant find view more'
            try:
                a.click()
                clicks += 1
            except Exception, e:
                print a
                #print str(e)
                print "Can't click View more"
                cantview += 1
                time.sleep(random.uniform(1.5, 2.9))

        except:
            break

        if clicks > 1 and cantview > 1:
            break

    page = BeautifulSoup(browser.page_source, "lxml")
    getSharesComp(page, test)

def main():
    #parser = argparse.ArgumentParser()
    #parser.add_argument("email", help = "linkedin email")
    #parser.add_argument("password", help = "linkedin password")
    #args = parser.parse_args()

    #browser = webdriver.Firefox()
    chrome_path = "/Users/runewerliin/PycharmProjects/AP_Linkedin/driver/chromedriver"
    browser = webdriver.Chrome(chrome_path)
    browser.get("http://nr.soccerway.com/national/england/premier-league/20162017/regular-season/r35992/matches/")
    time.sleep(random.uniform(3.5, 6.9))
    #elem = browser.find_element_by_css_selector("a[class='previous']")[0]
    elem = browser.find_element_by_id("page_competition_1_block_competition_matches_7_previous")
    elem.click()
    time.sleep(random.uniform(3.5, 6.9))
    #os.system('clear')
    #print "[+] Succes! Logged in - Bot started"
    #ViewBot(browser)
    browser.close()

main()

