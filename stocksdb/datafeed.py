#!/usr/bin/env python
""" datafeed.py
Data sources
"""
from database import StockDBManager
from datetime import date
import numpy as np


class IntradayQuotes(object):
    """
    API for retreiving intraday quotes from the stock database
    """
    def __init__(self):
        self.stock_db = StockDBManager()


    def get_quote(self, ticker, qdate):
        """
        Return a quote for the given stock on the given date
        """
        return self.stock_db.get_quotes(ticker, qdate)[0]


    def get_quotes(self, ticker, start_date, end_date):
        """
        Return a list of quotes for the given stoc from start_date to end-date
        """
        return self.stock_db.get_quotes(ticker, start_date, end_date)


class Dataset(object):
    """ Dataset for analysis
    """
    def __init__(self, tickers=None, sector=None, index=None):
        """
        """

        self.data = None
        self.target_data = None
        self.meta_data = None


        if sector is not None:
            pass

        for ticker in tickers:
            quotes = IntradayQuotes().get_quotes(ticker,
                                                 date(1900, 01, 01),
                                                 date.today())
            # Create Dataset
            data = np.array([np.array(
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
                 q.Features.ewma_12_day,
                 q.Features.ewma_20_day,
                 q.Features.ewma_26_day,
                 q.Features.ewma_50_day,
                 q.Features.ewma_100_day,
                 q.Features.ewma_200_day,
                 (q.AdjClose - q.Features.ma_5_day)
                    if q.Features.ma_5_day else None,
                 (q.AdjClose - q.Features.ma_10_day)
                    if q.Features.ma_10_day else None,
                 (q.AdjClose - q.Features.ma_20_day)
                    if q.Features.ma_20_day else None,
                 (q.AdjClose - q.Features.ma_50_day)
                    if q.Features.ma_50_day else None,
                 (q.AdjClose - q.Features.ma_100_day)
                    if q.Features.ma_100_day else None,
                 (q.AdjClose - q.Features.ma_200_day)
                    if q.Features.ma_200_day else None,
                 (q.AdjClose - q.Features.ewma_5_day)
                    if q.Features.ewma_5_day else None,
                 (q.AdjClose - q.Features.ewma_10_day)
                    if q.Features.ewma_10_day else None,
                 (q.AdjClose - q.Features.ewma_12_day)
                    if q.Features.ewma_12_day else None,
                 (q.AdjClose - q.Features.ewma_20_day)
                    if q.Features.ewma_20_day else None,
                 (q.AdjClose - q.Features.ewma_50_day)
                    if q.Features.ewma_50_day else None,
                 (q.AdjClose - q.Features.ewma_100_day)
                    if q.Features.ewma_100_day else None,
                 (q.AdjClose - q.Features.ewma_200_day)
                    if q.Features.ewma_200_day else None,
                 q.Features.macd,
                 q.Features.macd_signal,
                 q.Features.macd_histogram])
                for q in quotes])

            # Create target data
            target_data = np.zeros(len(quotes))
            for i in range(len(quotes) - 10):
                target_data[i] = np.array([ 1 if (quotes[i + 10].AdjClose /
                                       quotes[i].AdjClose > 1.1) else 0])

            # Create Meta-Data
            meta_data = np.array(
                [np.array([q.Ticker, q.Date]) for q in quotes])

            # Add each row to datase
            if self.data is None:
                self.data = data
                self.target_data = target_data
                self.meta_data = meta_data

            else:
                self.data = np.vstack((self.data, data))
                self.target_data = np.append(self.target_data, target_data, axis=1)
                self.meta_data = np.vstack((self.meta_data, meta_data))

        # Clean up
        self._sanitize()

    def get_data(self):
        """ Get the raw data from the dataset

        :returns: Data and Labels/target data as a tuple
        """
        return (self.data, self.target_data)


    def to_csv(self, filename):
        """ Write dataset to CSV file

        :param filename: Name of the file to write.
        :type filename: str
        """

        # Column Titles
        header_info = ['Ticker', 'Date', 'Weekday', 'Adjusted Close', 'Volume',
                       '5 Day Moving Average', '10 Day Moving Average',
                       '20 Day Moving Average', '50 Day Moving Average',
                       '100 Day Moving Average', '200 Day Moving Average',
                       '5 Day EWMA', '10 Day EWMA', '12 Day EWMA',
                       '20 Day EWMA', '26 Day EWMA', '50 Day EWMA',
                       '100 Day EWMA', '200 Day EWMA', 'Diff 5 Day MA',
                       'Diff 10 Day MA', 'Diff 20 Day MA', 'Diff 50 Day MA',
                       'Diff 100 Day MA', 'Diff 200 Day MA', 'Diff 5 Day EWMA',
                       'Diff 10 Day EWMA', 'Diff 12 Day EWMA',
                       'Diff 20 Day EWMA', 'Diff 26 Day EWMA',
                       'Diff 50 Day EWMA', 'Diff 100 Day EWMA',
                       'Diff 200 Day EWMA', 'MACD', 'MACD Signal',
                       'MACD Histogram', 'Target']

        # Generate full matrix
        csv_data = np.append(self.meta_data, self.data, axis=1)
        csv_data = np.append(csv_data, self.target_data, axis=1)
        csv_data = np.append(header_info, csv_data)

        # Write CSV file
        np.savetxt(filename, csv_data, fmt='%.3e', delimiter=',')

    def _sanitize(self):
        """ Clean up datasets

        Removes any rows with empty fields
        """
        delrows = []
        for i in range(len(self.data)):
            delrow = False

            # Find incomplete rows
            for val in self.data[i]:
                if not isinstance(val, float) or (val is None):
                    delrow = True
            if delrow:
                delrows.append(i)

        # Remove rows marked for deletion
        self.data = np.delete(self.data, delrows, 0).astype(float)
        self.target_data = np.delete(self.target_data,
                                     delrows, 0).astype(float)

        self.meta_data = np.delete(self.meta_data,
                                   delrows, 0)
