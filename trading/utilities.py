#!/usr/bin/env python

from math import floor

def calc_number_of_shares(cash, price, commission=0.00):
    return floor((cash - commission) / price)

