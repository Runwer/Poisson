#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from scipy.stats import poisson
import json

dict = json.loads(open('match_db.json').read())
print dict