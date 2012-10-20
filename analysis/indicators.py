#!/usr/bin/env python
from numpy import array
from pandas import Series, stats, concat

def moving_average(data, span):
	"""
	Calculate moving average of data and return as numpy array
	"""
	data = Series(data)
	return concat([stats.moments.expanding_mean(data[0:(span - 1)]), stats.moments.rolling_mean(data, span)[(span-1):]]).values


def exp_weighted_moving_average(data, span):
	"""
	Calculate exponentially weighted moving average of data and return as numpy array
	"""
	return stats.moments.ewma(data, span=span).values

def moving_stdev(data, span):
	data = Series(data)
	return concat([stats.moments.expanding_std(data[0:(span - 1)]), stats.moments.rolling_std(data, span)[(span-1):]]).values

def moving_var(data, span):
	data = Series(data)
	return concat([stats.moments.expanding_var(data[0:(span - 1)]), stats.moments.rolling_var(data, span)[(span-1):]]).values
	
