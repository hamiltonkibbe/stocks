#!/usr/bin/env python
""" dataset.py
Datasets
"""
import numpy as np
from datafeed import IntradayQuotes
from utilities import get_raw_data


class Dataset(object:
    """ Abstract Dataset
    """
    def __init__(self, symbols=None, sector=None, index=None, size=None):
        
        self.data = None
        self._initialize_dataset(self, symbols=symbols, sector=sector, index=index, size=size)

    def __len__(self):
        """ Get the number of rows in the dataset
        """
        return len(self.data)
    
    def __iter__(self):
        """ Get an iterator over the dataset
        """
        return iter(self.data)

    def get_data(self):
    
        """ Get Data from Dataset
        """
        return self.data

    def to_csv(self, filename):
        """ Write Dataset to CSV file
        """
        np.savetxt(filename, csv_data, delimiter=',')
        

    def _initialize_dataset(self, symbols=None, sector=None, index=None, size=None):
        """ Generate the acutual data
        """
        if symbols is not None:
            for ticker in symbols:
                data, meta_data = get_raw_data(ticker)
                data = np.append(meta_data, data, 1)
                # Add each row to dataset
                if self.data is None:
                    self.data = data
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
            for val in self.data[i][2:]:
                if not isinstance(val, float) or (val is None):
                    delrow = True
            if delrow:
                delrows.append(i)

        # Remove rows marked for deletion
        self.data = np.delete(self.data, delrows, 0).astype(float)
                    
    

class MLDataset(Dataset):
    """ Dataset for Machine Learning 
    """
    def __init__(self, symbols=None, sector=None, index=None):
        """
        """
        
        # Set up 
        self.target_data = None
        self.meta_data = None
        super(MLDataset, self).__init__()
        
    def __iter__(self):
        """ Get an iterator over the dataset
        """
        return iter(zip(self.data,self.target_data))
        
    def _initialize_dataset(self, symbols=None, sector=None, index=None, size=None):
        if sector is not None:
            pass
        if index is not None:
            pass
        for ticker in symbols:
            data, meta_data = get_raw_data(ticker)
            # Create target data
            target_data = np.zeros(len(quotes))
            for i in range(len(quotes) - 10):
                target_data[i] = np.array([ 1 if (quotes[i + 10].AdjClose /
                                       quotes[i].AdjClose > 1.1) else 0])

            # Add each row to datase
            if self.data is None:
                self.data = data
                self.target_data = target_data
                self.meta_data = meta_data
            else:
                self.data = np.vstack((self.data, data))
                self.target_data = np.append(self.target_data, target_data, axis=1)
                self.meta_data = np.vstack((self.meta_data, meta_data))
        # Clean up
        self._sanitize()


    def get_data(self):
        """ Get the raw data from the dataset

        :returns: Data and Labels/target data as a tuple
        """
        return zip(self.data, self.target_data)

    def to_csv(self, filename):
        """ Write dataset to CSV file
        
        :param filename: Name of the file to write.
        :type filename: str
        """

        # Column Titles
        header_info = ['Ticker', 'Date', 'Weekday', 'Adjusted Close', 'Volume',
                       '5 Day Moving Average', '10 Day Moving Average',
                       '20 Day Moving Average', '50 Day Moving Average',
                       '100 Day Moving Average', '200 Day Moving Average',
                       '5 Day EWMA', '10 Day EWMA', '12 Day EWMA',
                       '20 Day EWMA', '26 Day EWMA', '50 Day EWMA',
                       '100 Day EWMA', '200 Day EWMA', 'Diff 5 Day MA',
                       'Diff 10 Day MA', 'Diff 20 Day MA', 'Diff 50 Day MA',
                       'Diff 100 Day MA', 'Diff 200 Day MA', 'Diff 5 Day EWMA',
                       'Diff 10 Day EWMA', 'Diff 12 Day EWMA',
                       'Diff 20 Day EWMA', 'Diff 26 Day EWMA',
                       'Diff 50 Day EWMA', 'Diff 100 Day EWMA',
                       'Diff 200 Day EWMA', 'MACD', 'MACD Signal',
                       'MACD Histogram', 'Target']

        # Generate full matrix
        csv_data = np.append(self.meta_data, self.data, axis=1)
        csv_data = np.append(csv_data, self.target_data, axis=1)
        csv_data = np.append(header_info, csv_data)

        # Write CSV file
        np.savetxt(filename, csv_data, fmt='%.3e', delimiter=',')

        
    def _sanitize(self):
        """ Clean up datasets

        Remove any rows with empty fields or fields of incorrect type...
        """
        delrows = []
        for i in range(len(self.data)):
            delrow = False

            # Find incomplete rows
            for val in self.data[i]:
                if not isinstance(val, float) or (val is None):
                    delrow = True
            if delrow:
                delrows.append(i)

        # Remove rows marked for deletion
        self.data = np.delete(self.data, delrows, 0).astype(float)
        self.target_data = np.delete(self.target_data,
                                     delrows, 0).astype(float)

        self.meta_data = np.delete(self.meta_data,
                                   delrows, 0)
                                   

