#!/usr/bin/env python
#
#  This is based on Corey Goldberg's (corey@goldb.org) ystockquote module, with 
#  additional api methods exposed
# 
#
#  Copyright 2012 Hamilton Kibbe (hamilton.kibbe@gmail.com)
#
#  license: GNU LGPL
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.


import urllib
from datetime import date
from time import mktime, strptime

indicators = {'bank_prime_loan_rate': 'WPRIME.txt',
              'consumer_price_index': 'SOMETHING'}


def _get_url(fname):
    return 'http://research.stlouisfed.org/fred2/data/' + fname

def _get_raw(fname):
    raw =[i.strip().split() for i in urllib.urlopen(_get_url(fname)).readlines()]
    raw = raw[raw.index(['DATE','VALUE']) + 1:]
    return {'dates':[date.fromtimestamp(mktime(strptime(row[0],'%Y-%m-%d')))  for row in raw],'values': [float(row[1]) for row in raw]}

def get(indicator):
    return _get_raw(indicators[indicator])






