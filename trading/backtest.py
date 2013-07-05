#!/usr/bin/env python

from .account import Account
from . import actions


class Backtester(object):
    def __init__(self, algorithm, dataset, initial_value=100000):
        self.account = Account(initial_value)
        self.initial_value = initial_value
        self.dataset = dataset
        self.value = []
		benchmark = []
        self.first = True

    def backtest(self):
        for tick_data in self.dataset:
            action = self.algorithm.tick(tick_data)
            if self.first:

            benchmark.append()





