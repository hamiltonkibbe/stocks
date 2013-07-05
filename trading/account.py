#!/usr/bin/env python


class Account(object):
    def __init__(self, initial_value=100000, commission=0.00):
        self.cash_value = initial_value
        self.commission = commission
        self.positions = {}

    def account_value(self):
        securities_value = 0
        for k in self.positions.keys():
            securities_value += self.positions[k].value()
        return self.cash_value + securities_value

    def buy(self, security, n_shares, share_price):
        position = Position(security, n_shares, share_price, self.commission)
        self.cash_value -= position.cost_basis
        self.positions[security] = position

    def sell(self, security, n_shares, share_price):
        self.positions[security].tick(share_price)
        shares_held = self.positions[security].n_shares
        if shares_held >= n_shares:
            self.cash_value += (self.positions[security].value() + self.commission)
            self.positions.pop(security, None)
        else:
            self.positions[security].n_shares -= n_shares
            self.cash_value += share_price * n_shares - self.commission



class Position(object):
    def __init__(self, security, n_shares, share_price, commission=0):
        self.security = security
        self.n_shares = n_shares
        self.share_price = share_price
        self.cost_basis = self.commission + self.value()

    def tick(self, share_price):
        self.share_price = share_price
        self.value = self.n_shares * self.share_price

    def value(self):
        return self.share_price * self.n_shares

