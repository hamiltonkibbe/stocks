#!/usr/bin/env python

import sys
sys.path.append('..')
from quant import analysis
from models import Quote, Indicator
from numpy import arange, array, asarray, isnan, nan, where


def get_dataset(ticker, session, *columns):
    """ Get a numpy ndarray containing the specified columns
    TODO: Make this work
    """
    ticker = ticker.lower()
    return asarray(zip(*session.query(*columns).filter_by(Ticker=ticker).all()))



def update_ma(ticker, length, session, commit=True, check_all=False):
    """ Update moving average columns in database

    :param ticker: Ticker symbol of stock to update.
    :type ticker: str
    :param length: Length of moving average to update.
    :type length: int
    :param session: SQLAlchemy database session to use.
    :type session: session
    :param commit: (Optional) Whether or not database changes should be committed
    :type commit: bool
    :param check_all: (Optional) Whether or not to check for and update holes in the data
    :type check_all: bool
    """
    ticker=ticker.lower()
    col_name = 'ma_' + str(length) + '_day'
    if not check_all:
        last = session.query(Quote).filter_by(Ticker=ticker).order_by(Quote.Date.desc()).first()
        if getattr(last.Features, col_name) is not None:
            return
    data = asarray(zip(*[(q.Id, q.AdjClose, getattr(q.Features, col_name)) for q in session.query(Quote).filter_by(Ticker=ticker).all()]))
    ids = data[0]
    adj_close = data[1].astype(float)
    ma = data[2].astype(float)
    to_update = array([x for x in where(isnan(ma))[0] if x >= (length - 1)])
    if len(to_update) > 0:
        _min = min(to_update)
        _max = max(to_update)
        calc = analysis.moving_average(adj_close[_min - (length - 1):_max + 1], length)
        for idx in to_update:
            val = calc[idx + (length - (_min + 1))]
            session.query(Indicator).filter_by(Id=ids[idx]).update({col_name: val})
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
    :param commit: (Optional) Whether or not database changes should be committed
    :type commit: bool
    :param check_all: (Optional) Whether or not to check for and update holes in the data
    :type check_all: bool
    """
    ticker=ticker.lower()
    col_name = 'ewma_' + str(length) + '_day'
    if not check_all:
        last = session.query(Quote).filter_by(Ticker=ticker).order_by(Quote.Date.desc()).first()
        if getattr(last.Features, col_name) is not None:
            return
    data = asarray(zip(*[(q.Id, q.AdjClose, getattr(q.Features, col_name)) for q in session.query(Quote).filter_by(Ticker=ticker).all()]))
    ids = data[0]
    adj_close = data[1].astype(float)
    ma = data[2].astype(float)
    to_update = array([x for x in where(isnan(ma))[0] if x >= (length - 1)])
    if len(to_update) > 0:
        _min = min(to_update)
        _max = max(to_update)
        calc = analysis.exp_weighted_moving_average(adj_close[_min - (length - 1):_max + 1], length)
        for idx in to_update:
            val = calc[idx + (length - (_min + 1))]
            session.query(Indicator).filter_by(Id=ids[idx]).update({col_name: val})
        if commit:
            session.commit()


def update_momentum(ticker, length, session, commit=True, check_all=False):
    """ Update momentum columns in database

    :param ticker: Ticker symbol of stock to update.
    :type ticker: str
    :param length: Length of exponentially weighted moving average to update.
    :type length: int
    :param session: SQLAlchemy database session to use.
    :type session: session
    :param commit: (Optional) Whether or not database changes should be committed
    :type commit: bool
    :param check_all: (Optional) Whether or not to check for and update holes in the data
    :type check_all: bool
    """
    ticker=ticker.lower()
    col_name = 'momentum_' + str(length) + '_day'
    if not check_all:
        last = session.query(Quote).filter_by(Ticker=ticker).order_by(Quote.Date.desc()).first()
        if getattr(last.Features, col_name) is not None:
            return
    data = asarray(zip(*[(q.Id, q.AdjClose, getattr(q.Features, col_name)) for q in session.query(Quote).filter_by(Ticker=ticker).all()]))
    ids = data[0]
    adj_close = data[1].astype(float)
    mom = data[2].astype(float)
    to_update = array([x for x in where(isnan(mom))[0] if x >= length])
    if len(to_update) > 0:
        _min = min(to_update)
        _max = max(to_update)
        calc = analysis.momentum(adj_close[_min - length:_max + 1], length)
        for idx in to_update:
            val = calc[idx - length]
            session.query(Indicator).filter_by(Id=ids[idx]).update({col_name: val})
        if commit:
            session.commit()



def update_macd(ticker, session, commit=True, check_all=False):
    """ Update MACD for given stock in database

    :param ticker: Ticker symbol of stock to update.
    :type ticker: str
    :param session: SQLAlchemy database session to use.
    :type session: session
    :param commit: (Optional) Whether or not database changes should be committed
    :type commit: bool
    :param check_all: (Optional) Whether or not to check for and update holes in the data
    :type check_all: bool
    """
    ticker = ticker.lower()
    if not check_all:
        last = session.query(Quote).filter_by(Ticker=ticker).order_by(Quote.Date.desc()).first()
        if last.Features.macd is not None:
            return
    data = asarray(zip(*[(q.Id, q.Features.ewma_12_day, q.Features.ewma_26_day, q.Features.macd) for q in session.query(Quote).filter_by(Ticker=ticker).all()]))
    ids = data[0]
    fast_ewma = data[1].astype(float)
    slow_ewma = data[2].astype(float)
    macd = data[3].astype(float)

    to_update = array([x for x in where(isnan(macd))[0] if x >= 25])
    if len(to_update) > 0:
        _min = min(to_update)
        _max = max(to_update)
        macd = analysis.macd(fast_ewma=fast_ewma[_min - 8:_max+1], slow_ewma=slow_ewma[_min - 8:_max+1])
        macd_signal = analysis.macd_signal(macd=macd)
        macd = macd[8:]
        macd_signal = macd_signal[8:]
        for idx in to_update:
            calc_macd = macd[idx - _min]
            calc_macd_sig = macd_signal[idx - _min]
            session.query(Indicator).filter_by(Id=ids[idx]).update({'macd': calc_macd, 'macd_signal': calc_macd_sig, 'macd_histogram': calc_macd_sig - calc_macd})
        if commit:
            session.commit()




def update_all(ticker, session, commit=True, check_all=False):
    """ Update all columns in the Indicators table

    :param ticker: Ticker symbol of stock to update.
    :type ticker: str
    :param session: SQLAlchemy database session to use.
    :type session: session
    :param commit: (Optional) Whether or not database changes should be committed
    :type commit: bool
    :param check_all: (Optional) Whether or not to check for and update holes in the data
    :type check_all: bool
    """
    ticker = ticker.lower()
    for length in [5, 10, 20, 50, 100, 200]:
        update_ma(ticker, length, session, False, check_all)
        #update_momentum(ticker, length, session, False, check_all)
    for length in [5, 10, 12, 20, 26, 50, 100, 200]:
        update_ewma(ticker, length, session, False, check_all)
    update_macd(ticker, session, False, check_all)
    if commit:
        session.commit()

