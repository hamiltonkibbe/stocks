import numpy as np
import account
import actions
import utilities
""" tests.py

Unit tests for trading module
"""


# ------------------------------------------------
# Test Account
# ------------------------------------------------
def test_initial_account_value():
    """ [Account] Test value calculation
    """
    theAccount = account.Account()
    value =  theAccount.account_value()
    np.testing.assert_equal(value, theAccount.cash_value)


def test_cash_value():
    """ [Account] Test cash value calculation
    """
    theAccount = account.Account()
    theAccount._buy('test_security', 100, 1)
    value = theAccount.cash_value
    np.testing.assert_equal(value, 99900.0)

def test_position_security():
    """ [Account] Test position security name assignment
    """
    theAccount = account.Account()
    theAccount._buy('test_security', 100, 1)
    value = theAccount.positions['test_security'].security
    np.testing.assert_equal(value, 'test_security')


def test_position_n_shares():
    """ [Account] Test position number of shares assignment
    """
    theAccount = account.Account()
    theAccount._buy('test_security', 100, 1)
    value = theAccount.positions['test_security'].n_shares
    np.testing.assert_equal(value, 100)

def test_position_share_price():
    """ [Account] Test position share price assignment
    """
    theAccount = account.Account()
    theAccount._buy('test_security', 100, 1)
    value = theAccount.positions['test_security'].share_price
    np.testing.assert_equal(value, 1)


def test_commission():
    """ [Account] Test commission calculation
    """
    theAccount = account.Account(commission=10.0)
    theAccount._buy('test_security', 100, 1)
    value = theAccount.account_value()
    np.testing.assert_equal(value, 99990.0)



def test_trade():
    """ [Account] Test buy using trade method
    """
    theAccount = account.Account(commission=10.0)
    theAccount.trade(actions.BUY_LONG, 'test_security', 100, 1)
    value = theAccount.account_value()
    np.testing.assert_equal(value, 99990.0)

# ------------------------------------------------
# Test Utilities
# ------------------------------------------------

def test_share_calculator():
    """ [trading.utilities] Test calc number of shares calculation
    """
    shares = utilities.calc_number_of_shares(100, 33.0)
    np.testing.assert_equal(shares, 3)

def test_share_calculator_commission():
    """ [trading.utilities] Test calc number of shares commission calculation
    """
    shares = utilities.calc_number_of_shares(100,33.0, commission=5.00)
    np.testing.assert_equal(shares, 2)





if __name__ == '__main__':
    test_initial_account_value()

