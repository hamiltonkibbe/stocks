#!/usr/bin/env python
""" indicators.py
"""
import sys
from collections import namedtuple
import numpy as np
from numpy import array, asarray, isnan, where
from pandas import DataFrame
from sqlalchemy.orm import joinedload

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
'roc_5_day': indCalc(analysis.rate_of_change, 5, 4, None),
'roc_10_day': indCalc(analysis.rate_of_change, 10, 9, None),
'roc_20_day': indCalc(analysis.rate_of_change, 20, 19, None),
'roc_50_day': indCalc(analysis.rate_of_change, 50, 49, None),
'roc_100_day': indCalc(analysis.rate_of_change, 100, 99, None),
'roc_200_day': indCalc(analysis.rate_of_change, 200, 199, None),

# MACD
'macd': indCalc(analysis.macd, None, 25, ['ewma_12_day', 'ewma_26_day']),
'macd_signal': indCalc(analysis.macd_signal, None, 8, ['macd']),
'macd_histogram': indCalc(analysis.macd_hist, None, 0, ['macd', 'macd_signal'])
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
    cols = [indicator] if calc.columns is None else [indicator] + calc.columns

    data = get_columns(ticker, cols, session)
    # Find the empty rows
    rows_to_update = empty_rows(data[indicator], calc.nundefined)

    if len(rows_to_update) > 0:
        # generate list of arguments
        first_to_update = min(rows_to_update)
        update_range = rangeType(first_to_update - calc.nundefined, max(rows_to_update) + 1)
        args = get_args(indicator, data, update_range)

        # Calculate moving average
        calculated = calc.function(*args)

        # Update the database
        column = data[indicator]
        ids = data['ids']
        for row_index in rows_to_update:
            value  = calculated[row_index - first_to_update + calc.nundefined]

            (session.query(Indicator)
                    .filter_by(Id=ids[row_index])
                    .update({indicator: value}))

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
    calc = calculators[indicator]

    # Insert the length if necessary
    if calc.length is not None:
        args = args + [calc.length]

    # tack on the column data
    args = args + [np.array(data[indicator][start:end]).astype(float)]

    # tack on any other data if needed
    if calc.columns is not None:
        args = args + [np.array(data[col][start:end]).astype(float) for col in calc.columns]
    return args


def empty_rows(data, nundefined):
    return array([x for x in where(isnan(data.astype(float)))[0] if x >= nundefined])



def is_up_to_date(ticker, col_name, session):
    """ Check if column is up to date
    """
    last = (session.query(Quote).filter_by(Ticker=ticker)
                                .order_by(Quote.Date.desc())
                                .first())
    return getattr(last.Features, col_name) is not None



def get_columns(ticker, column_names, session):
    """ Get a numpy ndarray containing the specified columns
    TODO: Make this work
    """
    ticker = ticker.lower()
    keys = ['ids', 'adj_close'] + column_names
    values = []
    for q in session.query(Quote).options(joinedload(Quote.Features, innerJoin=True)).filter_by(Ticker=ticker).order_by(Quote.Date).all():
        values.append([q.Id, q.AdjClose] + [getattr(q.Features, name) for name in column_names])

    return DataFrame(values, columns=keys)
    #return dict(zip(keys,
    #            np.array(zip(*[(q.Id, q.AdjClose) + tuple([getattr(q.Features, name) for name in column_names])
    #                    for q in (session.query(Quote)
    #                                     .filter_by(Ticker=ticker)
    #                                     .all())]))))



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
    #for length in [5, 10, 20, 50, 100, 200]:
    for length in [5]:
    #update_indicator(ticker, 'ma_' + str(length) + '_day', session, False, check_all)
       # update_indicator(ticker, 'diff_ma_' + str(length) + '_day', session, False, check_all)
        #update_indicator(ticker, 'pct_diff_ma_' + str(length) + '_day', session, False, check_all)
        update_indicator(ticker, 'moving_stdev_' + str(length) + '_day', session, False, check_all)
        update_indicator(ticker, 'moving_var_' + str(length) + '_day', session, False, check_all)
        #update_indicator(ticker, 'momentum_' + str(length) + '_day', session, False, check_all)

    #for length in [5, 10, 12, 20, 26, 50, 100, 200]:
    #    update_indicator(ticker, 'ewma_' + str(length) + '_day', session, False, check_all)
    #    update_indicator(ticker, 'diff_ewma_' + str(length) + '_day', session, False, check_all)
    #    update_indicator(ticker, 'pct_diff_ewma_' + str(length) + '_day', session, False, check_all)

    #update_indicator(ticker, 'pct_change', session, False, check_all)
    #update_indicator(ticker, 'macd', session, True , check_all)
    #update_indicator(ticker, 'macd_signal', session, True, check_all)
    #update_indicator(ticker, 'macd_histogram', session, True, check_all)

    if commit:
        session.commit()
