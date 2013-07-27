#!/usr/bin/env python
#
#  Copyright 2013 Hamilton Kibbe (hamilton.kibbe@gmail.com)
#


import urllib
from datetime import date

""" googlefinance

This module provides a Python API for retrieving stock data from Google Finance.

"""

# Google doesn't like Python's user agent...
class FirefoxOpener(urllib.FancyURLopener):
    version = 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'

def __request(symbol):
    url = 'http://google.com/finance/historical?q=%s&output=csv' % symbol
    opener = FirefoxOpener()
    return opener.open(url).read().strip().strip('"')


def get_historical_prices(symbol, start_date=None, end_date=None):
    """
    Get historical prices for the given ticker symbol.

    Returns a nested list. fields are Date, Open, High, Low, Close, Volume.
    """
    return [data.split() for data in __request(symbol).split('\n')]


