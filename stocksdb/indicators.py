#!/usr/bin/env python

import sys
sys.path.append('..')
from quant import analysis
from models import Quote, Indicator
from numpy import array

def calculate_all(data):
    ids = data[0]
    raw = data[1]

    ma_5_day = analysis.moving_average(raw, 5)
    ewma_5_day = analysis.exp_weighted_moving_average(raw, 5)

    return array([Indicator(d[0],d[1],d[2]) for d in zip(ids,ma_5_day,ewma_5_day)])


