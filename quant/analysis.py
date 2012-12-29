#!/usr/bin/env python
import numpy as np
from numpy import array, zeros, append, subtract, empty, nan
from pandas import Series, stats, concat


# ------------------------------------------------
# Moving Averages
# ------------------------------------------------

def moving_average(span, data):
    """ Calculate n-point moving average
    :param data: Data to average.
    :param span: Length of moving average window.
    :returns: Moving average as a numpy array.
    """
    return stats.moments.rolling_mean(data, span)


def exp_weighted_moving_average(span, data):
    """ Calculate n-point exponentially weighted moving average
    :param data: Data to average.
    :param span: Length of moving average window.
    :returns: Exponentially weighted moving average as a numpy array.
    """
    return stats.moments.ewma(data, span=span)

def mag_diff(data, average):
    return np.array([np.nan if avg is None or cur is None else (cur - avg) for cur, avg in zip(data, average)])

def percent_diff(data, average):
    return np.array([np.nan if avg is None or cur is None else ((cur - avg) / avg) for cur,avg in zip(data, average)])


# ------------------------------------------------
# Moving Statistics
# ------------------------------------------------


def percent_change(data):
    """ Calculate percent change in data

    """
    return array(Series(data).pct_change().values)



def moving_stdev(span, data):
    """ Calculate n-point moving standard deviation.
    :param data: Data to analyze.
    :param span: Length of moving window.
    :returns: Moving standard deviation as a numpy array.
    """
    return stats.moments.rolling_std(data, span)


def moving_var(span, data):
    """ Calculate n-point moving variance.
    :param data: Data to analyze.
    :param span: Length of moving window.
    :returns: moving variance as a numpy array.
    """
    return stats.moments.rolling_var(data, span)


# ------------------------------------------------
# Momentum Indicators
# ------------------------------------------------


def momentum(span, data):
    """ Calculate Momentum

    Momentum is defined as 100 times the ratio of the current value to the
    value *span - 1* days ago

    :param data: Raw data to analyze.
    :param span: number of days before to use in the calculation of the.
    momentum ratio.
    :returns: Momentum as a numpy array.
    """
    momentum = array([100 * (cur / prev) for cur, prev in zip(data[span-1:], data)])
    blank = zeros(span-1)
    blank[:] = nan
    return append(blank, momentum).astype(float)


def rate_of_change(span, data):
    """ Calculate rate of change
    """
    roc = array([((cur - prev) / prev) for cur, prev in zip(data[span-1:], data)])
    blank = zeros(span-1)
    blank[:] = nan
    return append(blank, roc).astype(float)


def velocity(span, data):
    """ Calculate velocity
    """
    velocity = np.array([((cur - prev) / (span - 1)) for cur, prev in zip(data[span-1:], data)])
    blank = zeros(span-1)
    blank[:] = nan
    return append(blank, velocity).astype(float)


def acceleration(span, data, velocity=None):
    """ Calculate acceleration
    """
    if velocity is None:
        velocity = velocity(data,span)
    acceleration = np.array([((cur - prev) / (span - 1)) for cur, prev in zip(velocity[span-1:], velocity)])
    blank = zeros(span-1)
    blank[:] = nan
    return append(blank, acceleration).astype(float)


def macd(data=None, fast_ewma=None, slow_ewma=None):
    """ Calculate Moving Average Convergence Divergence

    Moving Average Convergence Divergence is defined as the difference between
    the 12-day EWMA and the 26-day EWMA.

    :param data: (optional) Data to analyze.
    :param fast_ewma: (optional) 12-day EWMA for use in MACD calculation.
    :param slow_ewma: (optional) 26-day EWMA for use in MACD calculation.
    :returns: MACD as a numpy array.
    .. note::

        Either raw data or the 12 and 26 day EWMAs must be provided, all three
        are not necessary.
    """

    if fast_ewma is None and slow_ewma is None:
        if data is not None:
            slow_ewma = exp_weighted_moving_average(26, data)
            fast_ewma = exp_weighted_moving_average(12, data)
        else:
            pass
    return subtract(fast_ewma, slow_ewma).astype(float)


def macd_signal(data=None, macd=None):
    """ Calculate MACD signal

    The MACD signal is defined as the 9-day EWMA of the MACD.

    :param data: (Optional) Raw data to analyze.
    :param macd: (Optional) MACD to use in MACD signal calculation.
    :returns: MACD signal as a numpy array.
    .. note::

        Either raw data or the MACD must be provided, both ar not necessary
    """
    if macd is None:
        if data is not None:
            macd = macd(data)
        else:
            pass
        pass
    return exp_weighted_moving_average(9, macd)


def macd_hist(data=None, macd=None, macd_signal=None):
    """ Calculate MACD histogram

    The MACD Histogram is defined as the difference between the MACD signal
    and the MACD.

    :param data: (optional) Raw data to analyze.
    :param macd: (optional) MACD to use in MACD histogram calculation.
    :param macd_signal: (optional) MACD signal to use in MACD histogram
    calculation.
    :returns: MACD histogram as a numpy array.
    .. note::

        Either raw data or the MACD and MACD signal must be provided, all three
        are not necessary.
    """
    if macd is None and macd_signal is None:
        if data is not None:
            macd = macd(data)
            macd_signal = macd_signal(macd=macd)
        else:
            pass
    return subtract(macd, macd_signal)


def trix(data, span):
    """ Calculate TRIX

    TRIX is the percent change of the triple ewma'ed value
    """
    first = (exp_weighted_moving_average(data, span))[(span-1):]
    second = (exp_weighted_moving_average(first, span))[(span-1):]
    third = (exp_weighted_moving_average(second, span))[(span-1):]
    trix = [((cur - prev) / prev) for cur, prev in zip(third[span-1:], third)]
    blank = zeros(4 * (span-1))
    blank[:] = nan
    return append(blank, trix).astype(float)



def relative_strength_index(data, span):
    """ Calculate RSI
    """
    pass



def relative_momentum_index(data, span):
    """ Calculate RMI
    """
    pass
