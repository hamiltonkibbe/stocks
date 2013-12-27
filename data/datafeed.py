#!/usr/bin/env python
""" datafeed.py
Data sources
"""
from ..database import Client

class IntradayQuotes(object):
    """
    API for retreiving intraday quotes from the stock database
    """
    def __init__(self, ):
        self.stock_db = Client()


    def get_quote(self, ticker, date):
        """ Get a single stock quote
        Return a quote for the given stock on the given date
        :param ticker: Ticker symbol of the security to quote.
        :param date: Date to quote as a string or a
        ``Datetime.date`` object.
        :returns: Quote for the given security and date
        """
        return self.stock_db.get_quotes(ticker, date)[0]


    def get_quotes(self, ticker, start_date, end_date):
        """ Get a series of quotes
        Return a list of quotes for the given security from start_date to
        end-date
        :param ticker: Ticker symbol of the security to quote.
        :param start_date: Starting date of quote list as a string or a
        ``Datetime.date`` object.
        :param end_date: Ending date of qoute list as a string or a
        ``Datetime.date`` object.
        :returns: List of quotes for the given security and date range
        """
        return self.stock_db.get_quotes(ticker, start_date, end_date, eager_load=True)


class TickQuotes(object):
    """
    API for retreiving tick-by-tick data from the stock database
    """
    def __init__(self):
        self.stock_db = Client()

    def get_quotes(self, ticker):
        pass

