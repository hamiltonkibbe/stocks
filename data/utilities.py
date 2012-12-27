#!/usr/bin/env python
""" utilities.py
Utility functions
"""
import numpy as np
from pandas import DataFrame

from .datafeed import IntradayQuotes
from .datetime import date

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
    col_names = [
              'weekday',
              'adj_close',
              'Volume',
              'ma_5_day',
              'ma_10_day',
              'ma_20_day',
              'ma_50_day',
              'ma_100_day',
              'ma_200_day',
              'ewma_5_day',
              'ewma_10_day',
              'ewma_12_day',
              'ewma_20_day',
              'ewma_26_day',
              'ewma_50_day',
              'ewma_100_day',
              'ewma_200_day',
              'diff_ma_5_day',
              'diff_ma_10_day',
              'diff_ma_20_day',
              'diff_ma_50_day',
              'diff_ma_100_day',
              'diff_ma_200_day',
              'diff_ewma_5_day',
              'diff_ewma_10_day',
              'diff_ewma_12_day',
              'diff_ewma_20_day',
              'diff_ewma_26_day',
              'diff_ewma_50_day',
              'diff_ewma_100_day',
              'diff_ewma_200_day',
              'pct_diff_ma_5_day',
              'pct_diff_ma_10_day',
              'pct_diff_ma_20_day',
              'pct_diff_ma_50_day',
              'pct_diff_ma_100_day',
              'pct_diff_ma_200_day',
              'pct_diff_ewma_5_day',
              'pct_diff_ewma_10_day',
              'pct_diff_ewma_12_day',
              'pct_diff_ewma_20_day',
              'pct_diff_ewma_26_day',
              'pct_diff_ewma_50_day',
              'pct_diff_ewma_100_day',
              'pct_diff_ewma_200_day',
              'macd',
              'macd_signal',
              'macd_histogram']


    raw_data =  np.array([
        [q.Date,
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
         _diff_ma(5, q),
         _diff_ma(10, q),
         _diff_ma(20, q),
         _diff_ma(50, q),
         _diff_ma(100, q),
         _diff_ma(200, q),
         _diff_ewma(5, q),
         _diff_ewma(10, q),
         _diff_ewma(12, q),
         _diff_ewma(20, q),
         _diff_ewma(26, q),
         _diff_ewma(50, q),
         _diff_ewma(100, q),
         _diff_ewma(200, q),
         _pct_diff_ma(5, q),
         _pct_diff_ma(10, q),
         _pct_diff_ma(20, q),
         _pct_diff_ma(50, q),
         _pct_diff_ma(100, q),
         _pct_diff_ma(200, q),
         _pct_diff_ewma(5, q),
         _pct_diff_ewma(10, q),
         _pct_diff_ewma(12, q),
         _pct_diff_ewma(20, q),
         _pct_diff_ewma(26, q),
         _pct_diff_ewma(50, q),
         _pct_diff_ewma(100, q),
         _pct_diff_ewma(200, q),
         q.Features.macd,
         q.Features.macd_signal,
         q.Features.macd_histogram] for q in quotes])

        data = DataFrame(raw_data[:,1:], index=raw_data[:,0], columns=col_names).dropna()
        
    #rows_to_delete=[]
    #for i in range(len(data)):
    #    for val in data[i,2:]:
    #        if val is None or not np.isfinite(val):
    #            rows_to_delete.append(i)
    #data = np.delete(data, rows_to_delete, 0)

    return data

    
    
def _diff_ma(days, quote)
    col_name = 'ma_' + str(days) + '_day'
    moving_average = getattr(quote.Features, col_name)
    return ((quote.AdjClose - moving_average) 
            if moving_average else None)
        
    
def _diff_ewma(days, quote):
    col_name = 'ewma_' + str(days) + '_day'
    moving_average = getattr(quote.Features, col_name)
    return ((quote.AdjClose - moving_average) 
            if moving_average else None)
    
def _pct_diff_ma(days, quote):
    col_name = 'ma_' + str(days) + '_day'
    moving_average = getattr(quote.Features, col_name)
    return ((quote.AdjClose - moving_average / moving_average) 
            if moving_average else None)

def _pct_diff_ewma(days, quote):
    col_name = 'ewma_' + str(days) + '_day'
    moving_average = getattr(quote.Features, col_name)
    return ((quote.AdjClose - moving_average / moving_average) 
            if moving_average else None)