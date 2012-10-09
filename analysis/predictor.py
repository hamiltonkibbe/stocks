#!/usr/bin/env python

from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

number_of_features = 5 

seven_day_future_prices = SupervisedDataSet(number_of_features,1)

