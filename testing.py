#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from scipy.stats import poisson

df = pd.read_csv('E_P_2002.csv', delimiter=',', low_memory=False, error_bad_lines=False)

print df