#!/usr/bin/env python
""" dataset.py
Datasets
"""

import numpy as np
from pandas import concat
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
        self.symbols = symbols
        self._data = None
        self._initialize_dataset(symbols, sector, index, size)

    @property
    def pretty_data(self):
        """ Data from dataset with column headers
        """
        return self._data

    @property
    def raw_data(self):
        """ Raw data from dataset
        """
        return self._data.values


    def to_csv(self, filename, delimiter=','):
        """ Write Dataset to CSV file
        
        :param filename: Output file path.
        :param delimiter: (Optional) field delimiter to use in output file
        """
        index_label = ('Ticker', 'Date')
        self._data.to_csv(filename, index_label=index_label, sep=delimiter)


    def _initialize_dataset(self, symbols=None, sector=None, index=None, size=None):
        """ Generate the acutual data based on init
        TODO: Implement sector, index, and size
        """
                
        if sector is not None:
            # Do some function to get the list of symbols in the given sector
            self.symbols = []

        if index is not None:
            # Do some function to get the list of symbols in the given index
            self.symbols=[]
            
        if self.symbols is not None:
            data_frames = []
            # Generate Matricies for each symbol
            for ticker in self.symbols:
                data = get_raw_data(ticker)
                data_frames.append(data)
            # Concatenate Matricies
            self._data = concat(data_frames, keys=self.symbols)
                # Add each row to dataset
                #if self.data is None:
                #    self.data = data
                #    
                #else:
                #    self.data = np.vstack((self.data, data))
                
        if size is not None:
            # Do something to set the max size
            pass

    def __iter__(self):
        """ Get an iterator over the dataset
        """
        return self._data.__iter__()
        
    def __len__(self):
        """ Get the number of rows in the dataset
        """
        return self._data.__len__()

    def __getitem__(self, i)
        """ Get data by index
        """
        return self._data.__getitem__(i)
    

class MLDataset(Dataset):
    """ Dataset for Machine Learning

    Data set with training and target data for machine learning or regression 
    analysis.
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
        super(MLDataset, self).__init__(symbols, sector,index, size)
        self._ML_init(target_function)

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

    #def _initialize_dataset(self, symbols=None, sector=None, index=None, size=None, target_function=None):
        # """ Generate the acutual data based on init
        # TODO: Implement sector, index, and size
        # """
        # if self.symbols is not None:
            # data_frames = []
            # training_frames=[]
            # target_frames=[]
            
            # # Generate matricies for each symbol
            # for ticker in self.symbols:
                # data = get_raw_data(ticker)
                # data_frames.append(data)
                # training_frames.append(normalize(data.values.astype(float)))
                # target_frames.append(target_function(data))
            
            # # Concatenate matricies
            # self.data = concat(data_frames, keys=self.symbols)
            # self._training_data = np.vstack(tuple(training_frames))
            # self._target_data = np.vstack(tuple(target_frames))
                
                # # Add each row to dataset
                # #if self.data is None:
                # #    self.col_names = col_names
                # #    self.data = data
                # #    self._training_data = normalize(data[:,2:].astype(float))
                # #    self._target_data = target_function(data, col_names)
                # #else:
                # #    self.data = np.vstack((self.data, data))
                # #    self._training_data = np.vstack((self._training_data, normalize(data[:,2:].astype(float))))
                # #    self._target_data = np.append(self._target_data, target_function(data, col_names))
                
                
        # if sector is not None:
                # pass
        # if index is not None:
            # pass
        # if size is not None:
            # pass
        # #self._sanitize()
        
    def generate_target_data(self, target_function):
        """ Create target dataset for regression / machine learning
        
        :param target_function: Function to use to generate the target data. 
        target_function should take a pandas DataFrame and return a 1D numpy 
        array of the same length as the DataFrame.
        """
        # Generate target data arrays for each symbol
        for symbol in self.symbols:
            data = self._data[symbol]
            target_frames.append(target_function(data))
        
        # concatenate target arrays
        self._target_data = np.vstack(tuple(target_frames))
        
        # clean up
        to_delete = []
        for i in range(len(self._target_data)):
            if target_data[i] is none or not np.isfinite(target_data[i]):
                to_delete.append(i)
        
        self._target_data = np.delete(self._target_data, to_delete, 0)
        self._training_data = np.delete(self._training_data, to_delete, 0)
        self._data = self._data.drop(self._data.irow(i).name)
        
        
    def _ML_init(self,target_function):
        """ Initialize regression- / machine_learning- specific data.
        """
        training_frames = []
        
        # Generate normalized training matricies
        for symbol in self.symbols:
            data = self._data[symbol]
            training_frames.append(normalize(data.values.astype(float)))
            
        # concatenate training matricies
        self._training_data = np.vstack(tuple(training_frames))
        
        # Create target data
        if target_function is not None:
            self.generate_target_data(target_function)

    def __getitem__(self, i)
        """ Get data by index. return a tuple of training data and target
        """
        return (self._training_data[i], self._target_data[i])
