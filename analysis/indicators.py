#!/usr/bin/env python




from numpy import array
from pandas import Series, stats, concat



# ------------------------------------------------
# Moving Averages
# ------------------------------------------------


def moving_average(data, span):
	""" Calculate n-point moving average
    :param data: Data to average
    :param span: Length of moving average window
    :returns: Moving average as a numpy array
	"""
	data = Series(data)
	return stats.moments.rolling_mean(data, span).values


def exp_weighted_moving_average(data, span):
	""" Calculate n-point exponentially weighted moving average
    :param data: Data to average
    :param span: Length of moving average window
    :returns: Exponentially weighted moving average as a numpy array
	"""
	return stats.moments.ewma(data, span=span).values



# ------------------------------------------------
# Moving Statistics
# ------------------------------------------------
def moving_stdev(data, span):
	""" Calculate n-point moving standard deviation
    :param data: Data to analyze
    :param span: Length of moving window
    :returns: Moving standard deviation as a numpy array
    """
    data = Series(data)
	return stats.moments.rolling_std(data, span).values

def moving_var(data, span):
    """ Calculate n-point moving variance
    :param data: Data to analyze
    :param span: Length of moving window
    :returns: moving variance as a numpy array
    """
	data = Series(data)
	return stats.moments.rolling_var(data, span).values

# ------------------------------------------------
# Momentum Indicators
# ------------------------------------------------

def macd(data, 12_day_ewma=None, 26_day_ewma=None):
    """ Calculate Moving Average Convergence Divergence
    :param data: Data to analyze
    :param 12_day_ewma: (optional) 12-day EWMA for use in MACD calculation
    :param 26_day_ewma: (optional) 26-day EWMA for use in MACD calculation
    :returns: MACD as a numpy array
    """
    pass

def macd_hist(data, macd=None, macd_signal=None):
    """ Calculate MACD histogram

    """
    pass

def macd_signal(data, macd=None):
    """ Calculate MACD signal
    """
    pass

def momentum(data, span):
    """ Calculate Momentum
    """
    pass


