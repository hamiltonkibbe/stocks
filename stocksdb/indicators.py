#!/usr/bin/env python

import sys
sys.path.append('..')
from quant import analysis
from models import Quote, Indicator
from numpy import array, asarray, isnan, nan, where

def calculate_all(data):
    ids = data[0]
    raw = data[1]

    ma_5_day = analysis.moving_average(raw, 5)
    ewma_5_day = analysis.exp_weighted_moving_average(raw, 5)

    return array([Indicator(d[0],d[1],d[2]) for d in zip(ids,ma_5_day,ewma_5_day)])


def get_dataset(ticker, session, *columns):
    """ Get a numpy ndarray containing the specified columns
    TODO: Make this work
    """
    ticker = ticker.lower()
    return asarray(zip(*session.query(*columns).filter_by(Ticker=ticker).all()))


def update_ma_5_day(ticker, session):
    ticker = ticker.lower()
    data = asarray(zip(*[(quote.Id, quote.AdjClose, quote.Features.ma_5_day) for quote in session.query(Quote).filter_by(Ticker=ticker).all()]))
    ma = data[2].astype(float)
    to_update = where(isnan(ma))[0]
    for idx in to_update:
        if idx >= 4:
            val = analysis.moving_average(data[1][idx-4:idx+1], 5)[4]
            session.query(Indicator).filter_by(Id=data[0][idx]).update({'ma_5_day': val})
    session.commit()


def update_ma_10_day(ticker, session):
    ticker = ticker.lower()
    data = asarray(zip(*[(quote.Id, quote.AdjClose, quote.Features.ma_10_day) for quote in session.query(Quote).filter_by(Ticker=ticker).all()]))
    ma = data[2].astype(float)
    to_update = where(isnan(ma))[0]
    for idx in to_update:
        if idx >= 9:
            val = analysis.moving_average(data[1][idx-9:idx+1], 10)[9]
            session.query(Indicator).filter_by(Id=data[0][idx]).update({'ma_10_day': val})
    session.commit()









