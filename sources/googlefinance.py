#!/usr/bin/env python
#
#  Copyright 2013 Hamilton Kibbe (hamilton.kibbe@gmail.com)
#


import urllib
from datetime import date, datetime

""" googlefinance

This module provides a Python API for retrieving stock data from Google Finance.

"""
_month_dict = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12}


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

    price_data = [data.split(',') for data in __request(symbol).split('\n')[1:]]
    for quote in price_data:
        quote[0] = _format_date(quote[0])
    return price_data

def _format_date(datestr):
    """ Change datestr from google format ('20-Jul-12') to the format yahoo uses ('2012-07-20')
    """
    parts = datestr.split('-')
    day = int(parts[0])
    month = _month_dict[parts[1]]
    year = int('20'+ parts[2])
    return date(year, month, day).strftime('%Y-%m-%d')
