#!/usr/bin/env python
""" utilities.py
Utility functions
"""
import numpy as np
from datafeed import IntradayQuotes
from datetime import date

def get_raw_data(ticker, start=date(1900, 01, 01), end=date.today()):
    """ Generate an array of quotes and indicators for the given stock
    :param ticker: Ticker of the security to quote.
    :param start: (Optional) Start of date range to get.
    :param end: (Optional) End of date range to get.
    :returns: tuple containing (raw data, ticker_and_date_info)
    """
    # Get quotes
    quotes = IntradayQuotes().get_quotes(ticker, start, end)
    # Generate matrix
    
    dtypes = np.dtype([('ticker', str, 5), 
              ('date', date),
              ('weekday', float),
              ('adj_close', float),
              ('Volume', float),
              ('ma_5_day', float),
              ('ma_10_day', float),
              ('ma_20_day', float),
              ('ma_50_day', float),
              ('ma_100_day', float),
              ('ma_200_day', float),
              ('ewma_5_day', float),
              ('ewma_10_day', float),
              ('ewma_12_day', float),
              ('ewma_20_day', float),
              ('ewma_26_day', float),
              ('ewma_50_day', float),
              ('ewma_100_day', float),
              ('ewma_200_day', float),
              ('diff_ma_5_day', float),
              ('diff_ma_10_day', float),
              ('diff_ma_20_day', float),
              ('diff_ma_50_day', float),
              ('diff_ma_100_day', float),
              ('diff_ma_200_day', float),
              ('diff_ewma_5_day', float),
              ('diff_ewma_10_day', float),
              ('diff_ewma_12_day', float),
              ('diff_ewma_20_day', float),
              ('diff_ewma_26_day', float),
              ('diff_ewma_50_day', float),
              ('diff_ewma_100_day', float),
              ('diff_ewma_200_day', float),
              ('macd', float),
              ('macd_signal', float),
              ('macd_histogram', float)])
              
    
    data =  (np.array([np.array(
        [q.Ticker, 
         q.Date, 
         q.Date.weekday(),
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
        for q in quotes], dtype=dtypes)
    
    # Column names
    col_names = np.array([dt[0] for dt in dtypes])
    
    return data, col_names
