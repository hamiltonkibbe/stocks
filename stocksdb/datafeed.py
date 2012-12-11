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

class Dataset(object):
    """ Dataset
    """
    def __init__(self,ticker):

        self.quotes = IntradayQuotes().get_quotes(ticker, date(1900,01,01), date.today())
        self.data = np.array([np.array(
            [q.Date.weekday(),
            q.AdjClose,
            q.Volume,
            q.Features.ma_5_day,
            q.Features.ma_10_day,
            q.Features.ma_20_day,
            q.Features.ma_50_day,
            q.Features.ma_100_day,
            q.Features.ma_200_day,
            q.Features.ewma_5_day,
            q.Features.ewma_10_day,
            q.Features.ewma_26_day,
            q.Features.ewma_50_day,
            q.Features.ewma_100_day,
            q.Features.ewma_200_day,
            (q.AdjClose - q.Features.ma_5_day) if q.Features.ma_5_day else None,
            (q.AdjClose - q.Features.ma_10_day) if q.Features.ma_10_day else None,
            (q.AdjClose - q.Features.ma_20_day) if q.Features.ma_20_day else None,
            (q.AdjClose - q.Features.ma_50_day) if q.Features.ma_50_day else None,
            (q.AdjClose - q.Features.ma_100_day) if q.Features.ma_100_day else None,
            (q.AdjClose - q.Features.ma_200_day) if q.Features.ma_200_day else None,
            q.Features.macd,
            q.Features.macd_signal,
            q.Features.macd_histogram])
            for q in self.quotes])

        # Create target data
        self.target_data = np.zeros(len(self.quotes))
        for i in range(len(self.quotes) - 10):
            self.target_data[i] = 1 if (self.quotes[i+10].AdjClose / self.quotes[i].AdjClose > 1.1) else 0

        self._sanitize()


    def _sanitize(self):
        """ Clean up datasets
        """
        delrows = []
        # Go through each row
        for i in range(len(self.data)):
            delrow = False
            x = self.data[i]

            # Find incomplete rows
            for val in x:
                if not isinstance(val,float) or (val is None):
                    delrow = True
            if delrow:
                delrows.append(i)

        # Remove rows marked for deletion
        self.data = np.delete(self.data, delrows, 0)
        self.target_data = np.delete(self.target_data, delrows, 0)




