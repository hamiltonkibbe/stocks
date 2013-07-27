#!/usr/bin/env python
""" netfronds.py

Python interface for accessing Netfronds tick data
"""

import urllib
from datetime import date, datetime, timedelta
from time import mktime, strptime

_exchange_code = {
        'NYSE':'N',
        'NASDAQ': 'O',
        'AMEX': 'A'}

def _get_url(symbol, exchange, tickdate, data_type='tick'):
    args = 'date=%s&paper=%s.%s&csv_format=txt' % (tickdate.strftime('%Y%m%d'), symbol.upper(), _exchange_code[exchange.upper()])

    if data_type == 'tick':
        url = 'http://hopey.netfonds.no/tradedump.php?'+args
    else:
        url = 'http://hopey.netfonds.no/posdump.php?'+args
    return url


def _get_ticks(symbol, exchange, tickdate):
    raw = [row.split() for row in urllib.urlopen(_get_url(symbol, exchange, tickdate)).read().split('\n')][1:]
    data = []
    for row in raw:
        if len(row) >= 3:
            data.append(row)
    timestamps = [datetime.strptime(row[0], '%Y%m%dT%H%M%S') for row in data]
    dates = [timestamp.date() for timestamp in timestamps]
    times = [(timestamp + timedelta(hours=-6)).time()  for timestamp in timestamps]
    prices = [float(row[1]) for row in data]
    quantities = [int(row[2]) for row in data]
    return {
            'dates': dates,
            'times': times,
            'prices': prices,
            'quantities': quantities}


def _get_books(symbol, exchange, tickdate):
    raw = [row.split() for row in urllib.urlopen(_get_url(symbol, exchange,tickdate,'book')).read().split('\n')][1:]
    data = []
    for row in raw:
        if len(row) >= 7:
            data.append(row)
    timestamps = [datetime.strptime(row[0], '%Y%m%dT%H%M%S') for row in data]
    dates = [timestamp.date() for timestamp in timestamps]
    times = [(timestamp + timedelta(hours=-6)).time()  for timestamp in timestamps]
    bids = [float(row[1]) for row in data]
    bid_depths = [int(row[2]) for row in data]
    offers = [float(row[4]) for row in data]
    offer_depths = [int(row[5]) for row in data]

    return {
            'bids': bids,
            'bid_depths': bid_depths,
            'offers': offers,
            'offer_depths': offer_depths}

def get(symbol, exchange, tickdate, data_type='tick'):
    if data_type == 'tick':
        return _get_ticks(symbol, exchange, tickdate)
    elif data_type == 'book':
        return _get_books(symbol, exchange, tickdate)
    else:
        pass


