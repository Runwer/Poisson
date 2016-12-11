#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from scipy.stats import poisson
import json
import pandas as pd
from datetime import datetime
from SocFunc import load_soc_data
from Betting_start import import_data, find_constants, att_def, match_calc, odds_calc

game_db = None

team_hist = pd.DateOffset(months=10)
to_import = ['E_P_2000.csv', 'E_P_2001.csv', 'E_P_2002.csv', 'E_P_2003.csv', 'E_P_2004.csv', 'E_P_2005.csv', 'E_P_2006.csv', 'E_P_2007.csv', 'E_P_2008.csv', 'E_P_2009.csv', 'E_P_2010.csv', 'E_P_2011.csv', 'E_P_2012.csv', 'E_P_2013.csv', 'E_P_2014.csv', 'E_P_2015.csv', 'E_P_2016.csv']

for fil in to_import:
    game_db = import_data(fil, game_db)

#print game_db
#Change dates to readable dates
game_db['Date'] = pd.to_datetime(game_db['Date'],dayfirst = True)

#JUST TESTING
date_m1 = pd.to_datetime('3-12-2016',dayfirst = True)

totpay = {}
for i in range(2000,6209):
        row = game_db.iloc[i]
    #try:
        wp, oup, pay, hg, ag = odds_calc(game_db, row['Date'], row['HomeTeam'], row['AwayTeam'], [row['BbAvH'], row['BbAvD'], row['BbAvA']], [row['BbAv>2.5'], row['BbAv<2.5']], row['FTHG'], row['FTAG'], team_hist)
        print str(row['HomeTeam']) + ' vs. ' + str(row['AwayTeam']) + '...  ' + str(hg) + ' - ' + str(ag)
        print wp
        print oup
        print pay
        if str(row['Date'].month) in totpay:
            totpay[str(row['Date'].month)] += pay
        else:
            totpay[str(row['Date'].month)] = pay
        print totpay
        print row['Date']
        print [row['BbAvH'], row['BbAvD'], row['BbAvH']], [row['BbAv>2.5'], row['BbAv<2.5']]
        print '.........'
        if i%20 == 0:
            print i
    #except:
    #    print i
