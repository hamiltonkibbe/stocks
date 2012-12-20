import numpy as np
import analysis
""" tests.py

Unit tests for quant module
"""

# arrays for testing
zeros_array = np.zeros(10)
ones_array = np.ones(10)
lin_ramp = np.arange(10)
exp_ramp = np.array([x**2 for x in lin_ramp])
nan_array = np.array([np.nan, np.nan, np.nan, np.nan, np.nan, 
                      np.nan, np.nan, np.nan, np.nan, np.nan])

# ------------------------------------------------
# Moving Averages
# ------------------------------------------------


def test_zero_length_moving_average():
    result = analysis.moving_average(lin_ramp, 0)
    np.testing.assert_array_equal(result, nan_array)
    
def test_unit_length_moving_average():
    result = analysis.moving_average(lin_ramp, 1)
    np.testing.assert_array_equal(result, lin_ramp)

def test_moving_average_with_zeros():
    result = analysis.moving_average(zeros_array, 3)
    np.testing.assert_array_equal(result, [np.nan, np.nan, 0, 0, 0, 0, 0, 0, 0, 0])
    
def test_moving_average_with_ones():
    result = analysis.moving_average(ones_array, 3)
    np.testing.assert_array_equal(result, [np.nan, np.nan, 1, 1, 1, 1, 1, 1, 1, 1])

def test_moving_average_with_ramp():
    result = analysis.moving_average(lin_ramp, 3)
    np.testing.assert_array_equal(result, [np.nan, np.nan, 1, 2, 3, 4, 5, 6, 7, 8])
    
    
    
def test_unit_length_exp_weighted_moving_average():
    result = analysis.exp_weighted_moving_average(lin_ramp, 1)
    np.testing.assert_array_equal(result, lin_ramp)
    
def test_exp_weighted_moving_average_with_zeros():
    result = analysis.exp_weighted_moving_average(zeros_array, 3)
    np.testing.assert_array_equal(result, zeros_array)
    
def test_exp_weighted_moving_average_with_ones():
    result = analysis.exp_weighted_moving_average(ones_array, 3)
    np.testing.assert_array_equal(result, ones_array)

def test_exp_weighted_moving_average_with_ramp():
    result = analysis.exp_weighted_moving_average(lin_ramp, 3)
    matlab_result = [0, 0.66666667, 1.42857143, 2.26666667, 3.16129032, 
                     4.0952381, 5.05511811, 6.03137255, 7.01761252, 8.00977517]
                     
    np.testing.assert_array_almost_equal(result, matlab_result)
    

# ------------------------------------------------
# Moving Statistics
# ------------------------------------------------

def test_percent_change():
    result = analysis.percent_change(lin_ramp)
    matlab_result = [np.nan, np.inf, 1, 0.5, 0.333333333333333, 0.25, 0.2, 
                     0.166666666666667, 0.142857142857143, 0.125]
    
    np.testing.assert_array_almost_equal(np.nan_to_num(result), 
                                         np.nan_to_num(matlab_result))

def test_moving_stdev():
    result = analysis.moving_stdev(exp_ramp,4)
    matlab_result = [np.nan, np.nan, np.nan, 4.041451884327381, 
                     6.557438524302000, 9.110433579144299, 11.676186592091330, 
                     14.247806848775006, 16.822603841260722, 19.399312702601950]
                     
    np.testing.assert_array_almost_equal(result, matlab_result)

    
def test_moving_variance():
    result = analysis.moving_var(exp_ramp, 4)
    matlab_result = [np.nan, np.nan, np.nan,  16.333333333333332, 43, 83, 
                     136.3333333333333, 203, 283,  376.3333333333333]
    
    np.testing.assert_array_almost_equal(result, matlab_result)
    
    
# ------------------------------------------------
# Momentum Indicators
# ------------------------------------------------

def test_momentum():
    result = analysis.momentum(exp_ramp, 4)
    matlab_result = [np.nan, np.nan, np.nan, np.nan, 0, 1600, 600, 400, 300, 200, 200]
    print result
    np.testing.assert_array_almost_equal(result, matlab_result)
    
