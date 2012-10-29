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



def update_macd(ticker, session, commit=True, check_all=False):
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


