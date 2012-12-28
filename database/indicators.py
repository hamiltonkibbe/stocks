#!/usr/bin/env python
""" indicators.py
"""
import sys
from ..quant import analysis
from .models import Quote, Indicator
from numpy import array, asarray, isnan, where

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

def get_dataset(ticker, session, *columns):
    """ Get a numpy ndarray containing the specified columns
    TODO: Make this work
    """
    ticker = ticker.lower()
    return asarray(zip(*session.query(columns)
                               .filter_by(Ticker=ticker)
                               .all()))
    # return asarray(zip(*session.query(*columns)
                               # .filter_by(Ticker=ticker)
                               # .all()))


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
        calc = analysis.moving_average(adj_close[start(range_data):end(range_data)],
                                       length)
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
        calc = analysis.exp_weighted_moving_average(adj_close[start(range_data):end(range_data)],
                                                    length)
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
        calc = col_fn(adj_close[start(range_data):end(range_data)], length)
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
        calc = analysis.momentum(adj_close[start(range_data):end(range_data)],
                                 length)
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
        # update_simple(ticker, length, session, 'ma_' + str(length) + '_day', analysis.moving_average)
        # update_simple(ticker, length, session, 'momentum_'+ str(length) + '_day', analysis.momentum)
        update_ma(ticker, length, session, False, check_all)
        update_momentum(ticker, length, session, False, check_all)
        update_pct_diff_ma(ticker, length, session, False, check_all)
        update_simple(ticker, length, session, 'moving_stdev_' + str(length) + '_day', analysis.moving_stdev, True, check_all)
        update_simple(ticker, length, session, 'moving_var_' + str(length) + '_day', analysis.moving_var, True, check_all)

    for length in [5, 10, 12, 20, 26, 50, 100, 200]:
        update_ewma(ticker, length, session, False, check_all)
        update_pct_diff_ma(ticker, length, session, False, check_all, exp=True)

        # update_simple(ticker, length, session, 'ewma_' + length + '_day', analysis.exp_weighted_moving_average)
    update_macd(ticker, session, False, check_all)
    #update_simple(ticker, 1, session, 'pct_change', analysis.percent_change, False, check_all)
    if commit:
        session.commit()
