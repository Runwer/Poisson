#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from scipy.stats import poisson
import json
import pandas as pd
from datetime import datetime
from SocFunc import load_soc_data
from Betting_start import import_data

outputHead = ['id', 'Date', 'teamH', 'teamA', 'finalscore', '5 H', '5 A', '10 H', '10 A', '15 H', '15 A', '20 H',
              '20 A', '25 H', '25 A', '30 H', '30 A', '35 H', '35 A', '40 H', '40 A', '45 H', '45 A', '50 H',
              '50 A', '55 H', '55 A', '60 H', '60 A', '65 H', '65 A', '70 H', '70 A', '75 H', '75 A', '80 H',
              '80 A', '85 H', '85 A', '90 H', '90 A']

#import data from soccerway data
socdb = pd.DataFrame(load_soc_data("match_db.json"), columns=outputHead)

#set gamedb var
stats_db = None

team_hist = pd.DateOffset(months=10)
to_import = ['E_P_2000.csv', 'E_P_2001.csv', 'E_P_2002.csv', 'E_P_2003.csv', 'E_P_2004.csv', 'E_P_2005.csv', 'E_P_2006.csv', 'E_P_2007.csv', 'E_P_2008.csv', 'E_P_2009.csv', 'E_P_2010.csv', 'E_P_2011.csv', 'E_P_2012.csv', 'E_P_2013.csv', 'E_P_2014.csv', 'E_P_2015.csv', 'E_P_2016.csv']

#import data from stats website
for fil in to_import:
    stats_db = import_data(fil, stats_db)

#Change dates to readable dates
stats_db['Date'] = pd.to_datetime(stats_db['Date'],dayfirst = True)
print stats_db


