#!/usr/bin/env python
""" dataset.py
Datasets
"""

import numpy as np
from sklearn.preprocessing import normalize

from .datafeed import IntradayQuotes
from .utilities import get_raw_data


class Dataset(object):
    """ Dataset Class
    """
    def __init__(self, symbols=None, sector=None,
                 index=None, size=None):
        """ Create an instance of the Dataset class

        :param symbols: List of securities to include in dataset
        :param sector: List of sectors to include in dataset
        :param index: List of indicies to include in dataset
        :param size: Maximum number of rows to include in dataset
        :param data_callback: function called for each set of data added to the set
        the function should take a numPy ndarray of data as an argument. the return
        value is ignored.
        """
        self.data = None
        self.col_names = None
        self._initialize_dataset(symbols, sector, index, size)

    @property
    def pretty_data(self):
        """ Data from dataset with column headers
        """
        return np.vstack((self.col_names, self.data))

    @property
    def raw_data(self):
        """ Raw data from dataset
        """
        return self.data


    def to_csv(self, filename):
        """ Write Dataset to CSV file
        """
        np.savetxt(filename, self.pretty_data, delimiter=',')


    def _initialize_dataset(self, symbols=None, sector=None, index=None, size=None, data_callback=None):
        """ Generate the acutual data based on init
        TODO: Implement sector, index, and size
        """
        if symbols is not None:
            for ticker in symbols:
                data, col_names = get_raw_data(ticker)

                # Add each row to dataset
                if self.data is None:
                    self.data = data
                    self.col_names = col_names
                else:
                    self.data = np.vstack((self.data, data))
        if sector is not None:
                pass
        if index is not None:
            pass
        if size is not None:
            pass



    def _sanitize(self):
        """ Clean up datasets
        Removes any rows with empty fields
        """
        delrows = []
        for i in range(len(self.data)):
            delrow = False

            # Find incomplete rows
            for val in self.data[i,2:]:
                if not isinstance(val, float) or (val is None) or not np.isfinite(val):
                    delrow = True
            if delrow:
                delrows.append(i)

        # Remove rows marked for deletion
        self.data = np.delete(self.data, delrows, 0)


    def __len__(self):
        """ Get the number of rows in the dataset
        """
        return len(self.data)

    def __iter__(self):
        """ Get an iterator over the dataset
        """
        return iter(self.data)


class MLDataset(Dataset):
    """ Dataset for Machine Learning

    Data set that provides training and target data for machine learning
    """
    def __init__(self, symbols=None, sector=None, index=None, size=None, target_function=None):
        """ Create an instance of the MLDataset class

        :param symbols: List of securities to include in dataset
        :param sector: List of sectors to include in dataset
        :param index: List of indicies to include in dataset
        :param size: Maximum number of rows to include in dataset
        :param target_function: function that generates target data for machine
        learning / regression. The function should take a numpy array and
        return a 1D numpy array.
        """
        # Initialize class
        self._training_data = None
        self._target_data = None
        self._initialize_dataset(symbols, sector, index, size)

    @property
    def training_data(self):
        """ Training dataset for regression / machine learning
        """
        return np.array(self._training_data).astype(float)

    @property
    def target_data(self):
        """ Target data for regression / machine learning
        """
        return self._target_data.astype(float)
    
    def _initialize_dataset(self, symbols=None, sector=None, index=None, size=None, target_function=None):
        """ Generate the acutual data based on init
        TODO: Implement sector, index, and size
        """
        if symbols is not None:
            for ticker in symbols:
                data, col_names = get_raw_data(ticker)

                # Add each row to dataset
                if self.data is None:
                    self.col_names = col_names
                    self.data = data
                    self._training_data = normalize(data[:,2:])
                    self._target_data = target_function(data, col_names)
                else:
                    self.data = np.vstack((self.data, data))
                    self._training_data = np.vstack((self._training_data, normalize(data[:,2:])))
                    self._target_data = np.append(self._target_data, target_function(data, col_names))
                    
        if sector is not None:
                pass
        if index is not None:
            pass
        if size is not None:
            pass
        self._sanitize()


    def _sanitize(self):
        """ Clean up datasets

        Remove any rows with empty fields or fields of incorrect type...
        """
        delrows = []
        for i in range(len(self.data)):
            delrow = False

            # Find incomplete rows
            for val in self.data[i]:
                if (not isinstance(val, float)) or (val is None) or (not np.isfinite(val)):
                    delrow = True
            if self.target:
                if (self._target_data[i] is None) or (not np.isfinite(self._target_data[i])):
                    delrow = True

            if delrow:
                delrows.append(i)

        # Remove rows marked for deletion
        self.data = np.delete(self.data, delrows, 0)
        self._training_data = np.delete(self._training_data, delrows, 0)
        self._target_data = np.delete(self._target_data, delrows, 0)

