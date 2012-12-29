#!/usr/bin/env python
""" indicators.py
"""
import sys
from collections import namedtuple
import numpy as np
from numpy import array, asarray, isnan, where

from ..quant import analysis
from .models import Quote, Indicator

# Create class for holding calculation info
indCalc = namedtuple('indCalc', ['function', 'length', 'nundefined', 'columns'])
rangeType = namedtuple('rangeType', ['min', 'max'])

calculators = {
# Moving average
'ma_5_day' : indCalc(analysis.moving_average, 5, 4, None),
'ma_10_day': indCalc(analysis.moving_average, 10, 9, None),
'ma_20_day': indCalc(analysis.moving_average, 20, 19, None),
'ma_50_day': indCalc(analysis.moving_average, 50, 49, None),
'ma_100_day': indCalc(analysis.moving_average, 100, 99, None),
'ma_200_day': indCalc(analysis.moving_average, 200, 199, None),

# Exponentially weighted moving average
'ewma_5_day' : indCalc(analysis.exp_weighted_moving_average, 5, 4, None),
'ewma_10_day' : indCalc(analysis.exp_weighted_moving_average, 10, 9, None),
'ewma_12_day' : indCalc(analysis.exp_weighted_moving_average, 12, 11, None),
'ewma_20_day' : indCalc(analysis.exp_weighted_moving_average, 20, 19, None),
'ewma_26_day' : indCalc(analysis.exp_weighted_moving_average, 26, 25, None),
'ewma_50_day' : indCalc(analysis.exp_weighted_moving_average, 50, 49, None),
'ewma_100_day' : indCalc(analysis.exp_weighted_moving_average, 100, 99, None),
'ewma_200_day' : indCalc(analysis.exp_weighted_moving_average, 200, 199, None),

# Magnitude difference from moving average
'diff_ma_5_day': indCalc(analysis.mag_diff, None, 0, ['ma_5_day']),
'diff_ma_10_day': indCalc(analysis.mag_diff, None, 0, ['ma_10_day']),
'diff_ma_20_day': indCalc(analysis.mag_diff, None, 0, ['ma_20_day']),
'diff_ma_50_day': indCalc(analysis.mag_diff, None, 0, ['ma_50_day']),
'diff_ma_100_day': indCalc(analysis.mag_diff, None, 0, ['ma_100_day']),
'diff_ma_200_day': indCalc(analysis.mag_diff, None, 0, ['ma_200_day']),

# Magnitude difference from EWMA
'diff_ewma_5_day': indCalc(analysis.mag_diff, None, 0, ['ewma_5_day']),
'diff_ewma_10_day': indCalc(analysis.mag_diff, None, 0, ['ewma_10_day']),
'diff_ewma_12_day': indCalc(analysis.mag_diff, None, 0, ['ewma_12_day']),
'diff_ewma_20_day': indCalc(analysis.mag_diff, None, 0, ['ewma_20_day']),
'diff_ewma_26_day': indCalc(analysis.mag_diff, None, 0, ['ewma_26_day']),
'diff_ewma_50_day': indCalc(analysis.mag_diff, None, 0, ['ewma_50_day']),
'diff_ewma_100_day': indCalc(analysis.mag_diff, None, 0, ['ewma_100_day']),
'diff_ewma_200_day': indCalc(analysis.mag_diff, None, 0, ['ewma_200_day']),

# Percent difference from moving average
'pct_diff_ma_5_day': indCalc(analysis.percent_diff, None, 0, ['ma_5_day']),
'pct_diff_ma_10_day': indCalc(analysis.percent_diff, None, 0, ['ma_10_day']),
'pct_diff_ma_20_day': indCalc(analysis.percent_diff, None, 0, ['ma_20_day']),
'pct_diff_ma_50_day': indCalc(analysis.percent_diff, None, 0, ['ma_50_day']),
'pct_diff_ma_100_day': indCalc(analysis.percent_diff, None, 0, ['ma_100_day']),
'pct_diff_ma_200_day': indCalc(analysis.percent_diff, None, 0, ['ma_200_day']),

# Percent difference from EWMA
'pct_diff_ewma_5_day': indCalc(analysis.percent_diff, None, 0, ['ewma_5_day']),
'pct_diff_ewma_10_day': indCalc(analysis.percent_diff, None, 0, ['ewma_10_day']),
'pct_diff_ewma_12_day': indCalc(analysis.percent_diff, None, 0, ['ewma_12_day']),
'pct_diff_ewma_20_day': indCalc(analysis.percent_diff, None, 0, ['ewma_20_day']),
'pct_diff_ewma_26_day': indCalc(analysis.percent_diff, None, 0, ['ewma_26_day']),
'pct_diff_ewma_50_day': indCalc(analysis.percent_diff, None, 0, ['ewma_50_day']),
'pct_diff_ewma_100_day': indCalc(analysis.percent_diff, None, 0, ['ewma_100_day']),
'pct_diff_ewma_200_day': indCalc(analysis.percent_diff, None, 0, ['ewma_200_day']),

# Percent change
'pct_change': indCalc(analysis.percent_change, None, 0, None),

# Standard Deviation
'moving_stdev_5_day': indCalc(analysis.moving_stdev, 5, 4, None),
'moving_stdev_10_day': indCalc(analysis.moving_stdev, 10, 9, None),
'moving_stdev_20_day': indCalc(analysis.moving_stdev, 20, 19, None),
'moving_stdev_50_day': indCalc(analysis.moving_stdev, 50, 49, None),
'moving_stdev_100_day': indCalc(analysis.moving_stdev, 100, 99, None),
'moving_stdev_200_day': indCalc(analysis.moving_stdev, 200, 199, None),

# Variance
'moving_var_5_day': indCalc(analysis.moving_var, 5, 4, None),
'moving_var_10_day': indCalc(analysis.moving_var, 10, 9, None),
'moving_var_20_day': indCalc(analysis.moving_var, 20, 19, None),
'moving_var_50_day': indCalc(analysis.moving_var, 50, 49, None),
'moving_var_100_day': indCalc(analysis.moving_var, 100, 99, None),
'moving_var_200_day': indCalc(analysis.moving_var, 200, 199, None),

# Momentum
'momentum_5_day': indCalc(analysis.momentum, 5, 4, None),
'momentum_10_day': indCalc(analysis.momentum, 10, 9, None),
'momentum_20_day': indCalc(analysis.momentum, 20, 19, None),
'momentum_50_day': indCalc(analysis.momentum, 50, 49, None),
'momentum_100_day': indCalc(analysis.momentum, 100, 99, None),
'momentum_200_day': indCalc(analysis.momentum, 200, 199, None),

# Rate of Change
'roc_5_day': indcalc(analysis.rate_of_change, 5, 4, None),
'roc_10_day': indcalc(analysis.rate_of_change, 10, 9, None),
'roc_20_day': indcalc(analysis.rate_of_change, 20, 19, None),
'roc_50_day': indcalc(analysis.rate_of_change, 50, 49, None),
'roc_100_day': indcalc(analysis.rate_of_change, 100, 99, None),
'roc_200_day': indcalc(analysis.rate_of_change, 200, 199, None)
}



def update_indicator(ticker, indicator, session, commit=True, check_all=False):
    """ Update indicator column in database
    """
    
    # Grab some info
    ticker = ticker.lower()
    calc = calculators[indicator]
    
    # See if there is anything to do
    if not check_all and is_up_to_date(ticker, indicator, session):
        return
    
    # Get the columns we need to calculate the indicator
    cols = (indicator) if calc.columns is None else (indicator, *calc.columns)
    data = get_columns(ticker, cols, session)

    # Find the empty rows
    rows_to_update, update_range = empty_rows(data[indicator], calc.nundefined)

    if len(rows_to_update) > 0:
        # generate list of arguments
        update_range = rangeType(min(rows_to_update) - calc.nundefined, max(rows_to_update))
        args = get_args(indicator, data, update_range)
        
        # Calculate moving average
        calculated = calc.function(*args)
        
        # Update the database
        for row in rows_to_update:
            value = calculated[row - min(rows_to_update) + calc.nundefined]
            (session.query(Indicator)
                    .filter_by(Id=ids[idx])
                    .update({col_name: val}))
        
        # Commit changes
        if commit:
            session.commit()
    
    
def get_args(indicator, data, range_data=None):
    """ Get arguments to pass to indicator calculation function
    """
    args = []
    start = 0
    end = len(data[indicator])
    
    # Get the range to work on
    if range_data is not None:
        start = range_data.min
        end = range_data.max
        
    # Calculation info
    calc = calculators(indicator)

    # Insert the length if necessary
    if calc.length is not None:
        args = args + [calc.length]
    
    # tack on the column data
    args = args + [np.array(data[indicator][start:end])]
    
    # tack on any other data if needed
    if calc.columns is not None:
        args = args + [np.array(data[col][start:end]) for col in calc.columns]
    return args
    
    
def empty_rows(data, nundefined):
    return array([x for x in where(isnan(data))[0] if x >= nundefined])
    

def find_needs_updating(data, length):
    """ Get list of missing data
    """
    to_update = array([x for x in where(isnan(data))[0] if x >= (length - 1)])
    if len(to_update) > 0:
        return (to_update, {'min': min(to_update), 'max': max(to_update), 'len': length})
    else:
        return (to_update, {'min': 0, 'max': 0, 'len': length})

def is_up_to_date(ticker, col_name, session):
    """ Check if column is up to date
    """
    last = (session.query(Quote).filter_by(Ticker=ticker)
                                .order_by(Quote.Date.desc())
                                .first())
    return getattr(last.Features, col_name) is not None

def get_column(ticker, col_name, session):
    """ Get column from database as an array
    """
    # return DataFrame(array([[q.Id, q.AdjClose, getattr(q.Features, col_name)]
                         # for q in (session.query(Quote)
                                          # .filter_by(Ticker=ticker)
                                          # .all())]),
                         # columns = ['ids', 'adj_close', col_name])

    return asarray(zip(*[(q.Id, q.AdjClose, getattr(q.Features, col_name))
                        for q in (session.query(Quote)
                                         .filter_by(Ticker=ticker)
                                         .all())]))

def start(range_data):
    """ Get starting index
    Map the starting index for the subset of data used to generate the transform
    to a real index in the dataset
    """
    return (range_data['min'] - (range_data['len'] - 1))

def end(range_data):
    """ Get ending index
    Map the ending index for the subset of data used to generate the transform
    to a real index in the dataset
    """
    return (range_data['max'] + 1)

def calc_index(index, range_data):
    """ Map calculated index
    Map index from the real dataset into the subset returned from the transform
    calculation
    """
    return index + (range_data['len'] - (range_data['min'] + 1))

def get_columns(ticker, column_names, session):
    """ Get a numpy ndarray containing the specified columns
    TODO: Make this work
    """
    ticker = ticker.lower()
    columns = [getattr(q.Features, name) for name in column_names]
    
    return dict(zip((['ids','adj_close'] + column_names),
                (zip(*[(q.Id, q.AdjClose, *columns)
                        for q in (session.query(Quote)
                                         .filter_by(Ticker=ticker)
                                         .all())]))))
                                         


                               
                           
def update_ma(ticker, length, session, commit=True, check_all=False):
    """ Update moving average columns in database

    :param ticker: Ticker symbol of stock to update.
    :type ticker: str
    :param length: Length of moving average to update.
    :type length: int
    :param session: SQLAlchemy database session to use.
    :type session: session
    :param commit: (Optional) Whether or not database changes should be
    committed
    :type commit: bool
    :param check_all: (Optional) Whether or not to check for and update holes
    in the data
    :type check_all: bool
    """
    ticker = ticker.lower()
    col_name = 'ma_' + str(length) + '_day'

    if not check_all and is_up_to_date(ticker, col_name, session):
        return

    data = get_column(ticker, col_name, session)
    ids = data[0]
    adj_close = data[1].astype(float)
    ma = data[2].astype(float)
    to_update, range_data = find_needs_updating(ma, length)

    if len(to_update) > 0:
        calc = analysis.moving_average(length, adj_close[start(range_data):end(range_data)])
        for idx in to_update:
            val = calc[calc_index(idx, range_data)]

            (session.query(Indicator)
                    .filter_by(Id=ids[idx])
                    .update({col_name: val}))
        if commit:
            session.commit()


def update_ewma(ticker, length, session, commit=True, check_all=False):
    """ Update exponentially weighted moving average columns in database

    :param ticker: Ticker symbol of stock to update.
    :type ticker: str
    :param length: Length of exponentially weighted moving average to update.
    :type length: int
    :param session: SQLAlchemy database session to use.
    :type session: session
    :param commit: (Optional) Whether or not database changes should be
    committed
    :type commit: bool
    :param check_all: (Optional) Whether or not to check for and update holes
    in the data
    :type check_all: bool
    """
    ticker = ticker.lower()
    col_name = 'ewma_' + str(length) + '_day'

    if not check_all and is_up_to_date(ticker, col_name, session):
        return

    data = get_column(ticker, col_name, session)
    ids = data[0]
    adj_close = data[1].astype(float)
    ma = data[2].astype(float)

    to_update, range_data = find_needs_updating(ma, length)
    if len(to_update) > 0:
        calc = analysis.exp_weighted_moving_average(length, adj_close[start(range_data):end(range_data)])
        for idx in to_update:
            val = calc[calc_index(idx, range_data)]
            (session.query(Indicator)
                    .filter_by(Id=ids[idx])
                    .update({col_name: val}))
        if commit:
            session.commit()


def update_pct_diff_ma(ticker, length, session, commit=True, check_all=False, exp=False):
    ticker = ticker.lower()
    if not exp:
        col_name = 'pct_diff_ma_' + str(length) + '_day'
    else:
        col_name= 'pct_diff_ewma_' + str(length) + '_day'

    if not check_all and is_up_to_date(ticker, col_name, session):
        return


    data = get_column(ticker, col_name, session)
    ids = data[0]
    adj_close = data[1].astype(float)
    diff = data[2].astype(float)

    to_update, range_data = find_needs_updating(diff, 1)
    if len(to_update) > 0:
        calc = analysis.percent_diff(adj_close[start(range_data):end(range_data)], diff[start(range_data):end(range_data)])

    for idx in to_update:
        val = calc[calc_index(idx, range_data)]
        session.query(Indicator).filter_by(Id=ids[idx]).update({col_name: val})
    if commit:
        session.commit()


def update_simple(ticker, length, session, col_name, col_fn, commit=True, check_all=False):
    if not check_all and is_up_to_date(ticker, col_name, session):
        return
    data = get_column(ticker, col_name, session)
    ids = data[0]
    adj_close = data[1].astype(float)
    column = data[2].astype(float)

    to_update, range_data = find_needs_updating(column, length)

    if len(to_update) > 0:
        calc = col_fn(length, adj_close[start(range_data):end(range_data)])
        for idx in to_update:
            val = calc[calc_index(idx, range_data)]

            (session.query(Indicator)
                    .filter_by(Id=ids[idx])
                    .update({col_name: val}))
        if commit:
            session.commit()


def update_momentum(ticker, length, session, commit=True, check_all=False):
    """ Update momentum columns in database

    :param ticker: Ticker symbol of stock to update.
    :type ticker: str
    :param length: Length of momentum calculation to update.
    :type length: int
    :param session: SQLAlchemy database session to use.
    :type session: session
    :param commit: (Optional) Whether or not database changes should be
    committed
    :type commit: bool
    :param check_all: (Optional) Whether or not to check for and update holes
    in the data
    :type check_all: bool
    """
    ticker = ticker.lower()
    col_name = 'momentum_' + str(length) + '_day'


    if not check_all and is_up_to_date(ticker, col_name, session):
        return

    data = get_column(ticker, col_name, session)
    ids = data[0]
    adj_close = data[1].astype(float)
    mom = data[2].astype(float)
    to_update, range_data = find_needs_updating(mom, length)

    if len(to_update) > 0:
        calc = analysis.momentum(length, adj_close[start(range_data):end(range_data)])
                             
        for idx in to_update:
            val = calc[calc_index(idx,range_data)]
            (session.query(Indicator)
                    .filter_by(Id=ids[idx])
                    .update({col_name: val}))
        if commit:
            session.commit()

    # ticker = ticker.lower()

    # col_name = 'momentum_' + str(length) + '_day'


    # if not check_all and is_up_to_date(ticker, col_name, session):
        # return

    # data = get_column(ticker, col_name, session)
    # ids = data[0]
    # adj_close = data[1].astype(float)
    # mom = data[2].astype(float)
    # to_update, range_data = find_needs_updating(mom, length + 1)

    # if len(to_update) > 0:
        # _min = range_data['min']
        # _max = range_data['max']
        # calc = analysis.momentum(adj_close[_min - length:end(range_data)],
                                 # length)

        # for idx in to_update:
            # val = calc[(idx - _min) + length]
            # (session.query(Indicator)
                    # .filter_by(Id=ids[idx])
                    # .update({col_name: val}))
        # if commit:
            # session.commit()


def update_macd(ticker, session, commit=True, check_all=False):
    """ Update MACD for given stock in database

    :param ticker: Ticker symbol of stock to update.
    :type ticker: str
    :param session: SQLAlchemy database session to use.
    :type session: session
    :param commit: (Optional) Whether or not database changes should be
    committed
    :type commit: bool
    :param check_all: (Optional) Whether or not to check for and update holes
    in the data
    :type check_all: bool
    """
    ticker = ticker.lower()
    length = 26
    if not check_all:
        last = (session.query(Quote)
                       .filter_by(Ticker=ticker)
                       .order_by(Quote.Date.desc())
                       .first())

        if last.Features.macd is not None:
            return

    data = asarray(zip(*[(q.Id, q.Features.ewma_12_day,q.Features.ewma_26_day,q.Features.macd)
                         for q in (session.query(Quote).filter_by(Ticker=ticker).all())]))

    ids = data[0]
    fast_ewma = data[1].astype(float)
    slow_ewma = data[2].astype(float)
    macd = data[3].astype(float)

    to_update, range_data = find_needs_updating(macd, length)
    if len(to_update) > 0:
        _min = range_data['min']
        _max = range_data['max']
        macd = analysis.macd(fast_ewma=fast_ewma[_min - 8:_max + 1],
                             slow_ewma=slow_ewma[_min - 8:_max + 1])
        macd_signal = analysis.macd_signal(macd=macd)
        macd = macd[8:]
        macd_signal = macd_signal[8:]
        for idx in to_update:
            calc_macd = macd[idx - _min]
            calc_macd_sig = macd_signal[idx - _min]
            (session.query(Indicator)
                    .filter_by(Id=ids[idx])
                    .update({'macd': calc_macd,
                             'macd_signal': calc_macd_sig,
                             'macd_histogram': calc_macd_sig - calc_macd}))
        if commit:
            session.commit()


def update_all(ticker, session, commit=True, check_all=False):
    """ Update all columns in the Indicators table

    :param ticker: Ticker symbol of stock to update.
    :type ticker: str
    :param session: SQLAlchemy database session to use.
    :type session: session
    :param commit: (Optional) Whether or not database changes should be
    committed
    :type commit: bool
    :param check_all: (Optional) Whether or not to check for and update holes
    in the data
    :type check_all: bool
    """
    ticker = ticker.lower()
    for length in [5, 10, 20, 50, 100, 200]:
        update_indicator(ticker, 'ma_' + str(length) + '_day', session, False, check_all)
        update_indicator(ticker, 'moving_stdev_' + str(length) + '_day', session, False, check_all)
        # update_simple(ticker, length, session, 'ma_' + str(length) + '_day', analysis.moving_average)
        # update_simple(ticker, length, session, 'momentum_'+ str(length) + '_day', analysis.momentum)
        #update_ma(ticker, length, session, False, check_all)
        #update_momentum(ticker, length, session, False, check_all)
        #update_pct_diff_ma(ticker, length, session, False, check_all)
        #update_simple(ticker, length, session, 'moving_stdev_' + str(length) + '_day', analysis.moving_stdev, True, check_all)
        #update_simple(ticker, length, session, 'moving_var_' + str(length) + '_day', analysis.moving_var, True, check_all)
     
    #for length in [5, 10, 12, 20, 26, 50, 100, 200]:
        #update_ewma(ticker, length, session, False, check_all)
        #update_pct_diff_ma(ticker, length, session, False, check_all, exp=True)

        # update_simple(ticker, length, session, 'ewma_' + length + '_day', analysis.exp_weighted_moving_average)
    #update_macd(ticker, session, False, check_all)
    #update_simple(ticker, 1, session, 'pct_change', analysis.percent_change, False, check_all)
    if commit:
        session.commit()
