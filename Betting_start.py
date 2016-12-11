#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from scipy.stats import poisson


def import_data(filename, df):
    try:
        return pd.concat([df, pd.read_csv(filename, delimiter=',', low_memory=False)])
    except:
        return pd.read_csv(filename, delimiter=',', low_memory=False)

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')

#Function to find constants (average goals and home vs. away coefficient
def find_constants(df, date_of_match):
    hgC =  df['FTHG'].loc[(df['Date'] > (date_of_match - pd.DateOffset(years=3))) & (df['Date'] < date_of_match)].mean()
    agC = df['FTAG'].loc[(df['Date'] > (date_of_match - pd.DateOffset(years=3))) & (df['Date'] < date_of_match)].mean()
    return [hgC+agC, hgC/((agC+hgC)/2)]

#FIND ATT and DEF for two given teams in time range
def att_def(df, team, date_of_match, team_hist):
    return (df['FTHG']
                .loc[(df['Date'] > (date_of_match - team_hist)) & (df['Date'] < date_of_match) & (df['HomeTeam'] == team)]
                .append(
                df['FTAG']
                .loc[(df['Date'] > (date_of_match - team_hist)) & (df['Date'] < date_of_match) & (df['AwayTeam'] == team)]
                )).mean(), (
            df['FTAG']
                .loc[(df['Date'] > (date_of_match - team_hist)) & (df['Date'] < date_of_match) & (df['HomeTeam'] == team)]
                .append(
                df['FTHG']
                .loc[(df['Date'] > (date_of_match - team_hist)) & (df['Date'] < date_of_match) & (df['AwayTeam'] == team)]
                )).mean()



def match_calc(df, date, team1, team2, team_hist):
    constants = find_constants(df, date)
    if team1 in df['HomeTeam'].values:
        ht_att, ht_defs = att_def(df, team1, date, team_hist)
    else:
        print 'No such HomeTeam: ' + team1
    if team2 in df['AwayTeam'].values:
        at_att, at_defs = att_def(df, team2, date, team_hist)
    else:
        print 'No such AwayTeam: ' + team2
    ht_final = at_defs/(constants[0]/2)*ht_att*constants[1]
    at_final = ht_defs/(constants[0]/2)*at_att*(2-constants[1])
    #print ht_final
    #print at_final

    ht_score = poisson.pmf([0,1,2,3,4,5,6,7,8,9], ht_final)
    at_score = poisson.pmf([0,1,2,3,4,5,6,7,8,9], at_final)

    df_g = pd.DataFrame(np.random.randn(10,10), index=range(0,10), columns=range(0,10))
    for hs in range(0, len(ht_score)):
        for aws in range(0, len(at_score)):
            df_g.iloc[hs].iloc[aws] = ht_score[hs] * at_score[aws]

    winner = [0,0,0]
    ou = [0,0]
    for h in range(0,10):
        for a in range(0,10):
            if h > a:
                winner[0] += float(df_g.iloc[h].iloc[a])
            if h == a:
                winner[1] += float(df_g.iloc[h].iloc[a])
            if h < a:
                winner[2] += float(df_g.iloc[h].iloc[a])
            if h + a > 2.5:
                ou[0] += float(df_g.iloc[h].iloc[a])
            if h + a < 2.5:
                ou[1] += float(df_g.iloc[h].iloc[a])
    winner = [1 / x for x in winner]
    ou = [1 / x for x in ou]
    return winner, ou

def odds_calc(df, date, team1, team2, winodds, ouodds, hg, ag, team_hist):
    # FORMAT FOR ODDS LIST
    #winodds = ['BbMxH', 'BbMxD', 'BbMxH']
    #ouodds = ['BbMx>2.5', 'BbMx<2.5']
    playbig = 50
    playsmall = 20
    winner_play = [0,0,0]
    ou_play = [0,0]
    winner, ou =  match_calc(df, date, team1, team2, team_hist)
    for i in range(0,3):
        if (1/winodds[i]) * 1.1 < 1/winner[i]:
            winner_play[i] = playbig
        elif 1/winodds[i] < 1/winner[i]:
            winner_play[i] = playsmall
    for i in range(0, 2):
        if (1 / ouodds[i]) * 1.1 < 1 / ou[i]:
            ou_play[i] = playbig
        elif 1 / ouodds[i] < 1 / ou[i]:
            ou_play[i] = playsmall
    payout = - sum(winner_play) - sum(ou_play)
    if hg > ag:
        payout += winodds[0] * winner_play[0]
    elif hg == ag:
        payout += winodds[1] * winner_play[1]
    elif hg < ag:
        payout += winodds[2] * winner_play[2]
    if hg+ag > 2.5:
        payout += ouodds[0] * ou_play[0]
    else:
        payout += ouodds[1] * ou_play[1]
    return winner_play, ou_play, payout, hg, ag


#print odds_calc(game_db, date_m1, 'Everton', 'Liverpool', [2.2, 2, 1.56], [1.8, 2.1], 2, 1)

#print totpay
#print match_calc(game_db, (game_db.iloc[6209].loc['Date']) + pd.DateOffset(months=1), 'Middlesbrough', 'Hull')