import json
import pandas as pd
from datetime import datetime

def load_soc_data(fil):
    with open(fil) as f:
        data = json.load(f)

    finalout = []
    for i in data:
        scoretimes = {'5': [0, 0], '10': [0, 0], '15': [0, 0], '20': [0, 0], '25': [0, 0], '30': [0, 0], '35': [0, 0],
                      '40': [0, 0], '45': [0, 0], '50': [0, 0], '55': [0, 0], '60': [0, 0], '65': [0, 0], '70': [0, 0],
                      '75': [0, 0], '80': [0, 0], '85': [0, 0], '90': [0, 0]}
        try:
            if data[i]['finalscore'] == '0 - 0':
                print '0-0'
            elif data[i]['scores'] != 'Missing':
                for s in data[i]['scores']:
                    for t in s:
                        templist = s[t].split('-')
                        templist = map(int, templist)
                        if t[-1:] == "'":
                            minut = t[:-1]

                        else:
                            minut = t[:2]
                        minut_interval = ((int(minut) - 1) / 5) * 5 + 5

                        # sum(scoretimes[str(minut_interval)])

                        while True:
                            if sum(templist) > sum(scoretimes[str(minut_interval)]):
                                scoretimes[str(minut_interval)] = templist
                                if minut_interval == 90:
                                    break
                                minut_interval += 5
                            else:
                                break

            tempout = []
            for minuts in range(5, 95, 5): tempout = tempout + scoretimes[str(minuts)]
            output = [i, data[i]['date'], data[i]['teamH'], data[i]['teamA'], data[i]['finalscore']] + tempout
            finalout.append(output)
        except:
            print 'problem'
            print i

    return finalout



