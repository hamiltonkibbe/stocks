#!/usr/bin/env python

from database import StockDBManager
from datetime import date
import numpy as np

class IntradayQuotes(object):
    """
    API for retreiving intraday quotes from the stock database
    """
    def __init__(self):
        self.db = StockDBManager()

    def get_quote(self, ticker, date):
        """
        Return a quote for the given stock on the given date
        """
        return self.db.get_quotes(ticker, date)[0]

    def get_quotes(self, ticker, start_date, end_date):
        """
        Return a list of quotes for the given stoc from start_date to end-date
        """
        return self.db.get_quotes(ticker, start_date, end_date)


def generate_dataset(ticker):
    quotes = IntradayQuotes().get_quotes(ticker, date(1900,01,01), date.today())
    table = np.array([[q.Date.weekday(),
        q.AdjClose,q.Volume,
        q.Features.macd,
        q.Features.macd_signal,
        q.Features.macd_histogram]
        for q in quotes])
    return table


