#!/usr/bin/env python



class Backtester(object):
    def __init__(self, algorithm, dataset, initial_value=100000):
        self.algorithm
        self.dataset = dataset
        self.initial_value = 100000
        self.value = []
		benchmark = []
        
    def backtest(self):
        for tick_data in self.dataset:
            action = self.algorithm.tick(tick_data)
            benchmark.append()

