#!/usr/bin/env python
#
#  Copyright 2013 Hamilton Kibbe (hamilton.kibbe@gmail.com)
#


import urllib
from datetime import date

""" googlefinance

This module provides a Python API for retrieving stock data from Google Finance.

"""


def __request(symbol):
    url = 'http://google.com/finance/historical?q=%s&output=csv' % symbol
    return urllib.urlopen(url).read().strip().strip('"')


def get_historical_prices(symbol, start_date, end_date):
    """
    Get historical prices for the given ticker symbol.

    Returns a nested list. fields are Date, Open, High, Low, Close, Volume.
    """
    return [data.split() for data in __request(symbol).split('\n')]


