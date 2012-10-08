#!/usr/bin/env python

import MySQLdb as mdb
import ystockquote as quotes
import config


def create_database():
    """
    Create stock database tables
    """
    with connect() as cur:
        cur.execute("CREATE TABLE IF NOT EXISTS Symbols( \
            Ticker CHAR(5) PRIMARY KEY, \
            Name CHAR(128), \
            Exchange CHAR(50) \
            )")
        
        cur.execute("CREATE TABLE IF NOT EXISTS Quotes( \
            Id INT PRIMARY KEY AUTO_INCREMENT, \
            Ticker CHAR(5), \
            Date DATE, \
            Open DOUBLE, \
            High DOUBLE, \
            Low DOUBLE, \
            Close DOUBLE, \
            Volume DOUBLE, \
            FOREIGN KEY (Ticker) REFERENCES Symbols(Ticker) \
            )")   


def connect():
    """ 
    Connect to the stock data DB
    """
    return mdb.connect(config.sql_hostname,config.sql_user,config.sql_password,config.sql_database)




def add_stock(ticker, name):
    """
    Add a stock to the stock database
    """
    ticker = ticker.lower()
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM Symbols WHERE Ticker = '%s'" % ticker)

    if cur.fetchone() is None:
	print "That one's new!"
        data = quotes.get_historical_prices(ticker,'1000101','20121008')
        data = data[len(data) - 1:0:-1]
        cur.execute("INSERT INTO Symbols(Ticker,Name,Exchange) \
            VALUES('%s','%s','%s')" 
            % (ticker,name,quotes.get_stock_exchange(ticker).strip('\'\"')))
        for quote in data:
            cur.execute("INSERT INTO Quotes(Ticker,Date,Open,High,Low,Close,Volume) \
                VALUES('%s','%s', %s, %s, %s, %s, %s)" 
                % (ticker,quote[0],quote[1],quote[2],quote[3],quote[4],quote[5]))
 
    else:
        print "Already have it!"
    con.commit()
    con.close()

def get_quotes(ticker):
    
    ticker = ticker.lower()
    con = connect()
    cur = con.cursor()
    data = quotes.get_historical_prices(ticker,'1000101','20121008')
    data = data[len(data) - 1:0:-1]
    for quote in data:
        cur.execute("INSERT INTO Quotes(Ticker,Date,Open,High,Low,Close,Volume) VALUES('%s','%s', %s, %s, %s, %s, %s)" % (ticker,quote[0],quote[1],quote[2],quote[3],quote[4],quote[5]))
    con.commit()
    con.close()     
