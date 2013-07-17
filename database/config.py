#!/usr/bin/env python

import os
import sys

envkeys = ['STOCKS_SQL_HOSTNAME', 'STOCKS_SQL_USER', 'STOCKS_SQL_PASSWORD']

for key in envkeys:
    setattr(sys.modules[__name__], key, os.environ.get(key, None))


# MySQL settings
STOCKS_SQL_HOSTNAME = 'localhost'
STOCKS_SQL_USER = 'stocks'
STOCKS_SQL_PASSWORD = ''
STOCKS_SQL_DATABASE = 'stock_data'

