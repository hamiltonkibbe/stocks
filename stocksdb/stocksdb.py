#!/usr/bin/env python

import ystockquote as quotes
import config
from datetime import date
from models  import Symbol, Quote
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Set up database session
Base = declarative_base()
if config.sql_password == '':
    engine_config = 'mysql://%s@%s/%s' % (config.sql_user, config.sql_hostname, config.sql_database)
else:
    engine_config = 'mysql://%s:%s@%s/%s' % (config.sql_user, config.sql_password, config.sql_hostname, config.sql_database)
Engine = create_engine(engine_config)
Session = sessionmaker()
Session.configure(bind=Engine)

def create_database():
    """
    Create stock database tables
    """
    Base.metadata.create_all(Engine)


def add_stock(ticker, name, sector=None, industry=None):
    """
    Add a stock to the stock database
    """
    ticker = ticker.lower()
    stock = Symbol(ticker, name, sector, industry)
    session = Session()
    
    if bool(session.query(Symbol).filter_by(Ticker=ticker).count()):
        print "Stock %s already exists!" % (ticker.upper())
    else:
        print "Adding %s to database" % (ticker.upper())
        session.add(stock)
        session.add_all(_get_quotes(ticker, date(1900,01,01), date.today()))
    
    session.commit()
    session.close()

def _get_quotes(ticker, start_date, end_date):
    """
    Get quotes from Yahoo Finance
    """
    ticker = ticker.lower()
    start = start_date.strftime("%Y%m%d")
    end = end_date.strftime("%Y%m%d")
    data = quotes.get_historical_prices(ticker, start, end)
    data = data[len(data)-1:0:-1]
    return [Quote(ticker,val[0],val[1],val[2],val[3],val[4],val[5]) for val in data]

def update_quotes(ticker):
    pass

