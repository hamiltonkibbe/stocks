#!/usr/bin/env python

from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Symbol(Base):
    """
    Stock Symbols Table Model
    """
    __tablename__ = 'Symbols'

    Ticker = Column(String(5), primary_key=True)
    Name = Column(String(128))
    Exchange = Column(String(50))
    Sector = Column(String(50))
    Industry = Column(String(50))
    Quotes = relationship('Quote')

    def __init__(self, Ticker, Name, Exchange=None, Sector=None, Industry=None):
        self.Ticker = Ticker
        self.Name = Name
        self.Exchange = Exchange
        self.Sector = Sector
        self.Industry = Industry

    def __repr__(self):
        return "<Symbol('%s','%s','%s','%s','%s')>" % \
            (self.Ticker, self.Name, self.Exchange, self.Sector, self.Industry)



class Quote(Base):
    """
    Stock Quotes Table Model
    """
    __tablename__ = 'Quotes'

    Id = Column(Integer, primary_key=True)
    Ticker = Column(String(5), ForeignKey('Symbols.Ticker'))
    Date = Column(Date)
    Open = Column(Float)
    High = Column(Float)
    Low = Column(Float)
    Close = Column(Float)
    Volume = Column(Float)
    AdjClose = Column(Float)
    Features = Relationship('Indicator', uselist=False, backref('Quotes'))

    def __init__(self, Ticker, Date, Open, High, Low, Close, Volume, AdjClose):
        self.Ticker = Ticker
        self.Date = Date
        self.Open = Open
        self.High = High
        self.Low = Low
        self.Close = Close
        self.Volume = Volume
        self.AdjClose = AdjClose

    def __repr__(self):
        return "<Quote(Date: %s,Symbol: %s, Open: %f, High: %f, Low: %f, Close: %f, Volume: %d, Adjusted Close: %f)>" % \
            (self.Date, self.Ticker, self.Open, self.High, self.Low,
            self.Close, self.Volume, self.AdjClose)


class Indicator(Base):
    """
    Financial Indicator table model
    """
    __tablename__ = 'Indicators'

    Id = Column(Integer,primary_key=True, ForeignKey('Quotes.Id'))

    # --------------------------------------------
    # Averages
    # --------------------------------------------

    # Moving Averages
    5_day_ma = Columnn(Float)
    10_day_ma = Column(Float)
    20_day_ma = Column(Float)
    50_day_ma = Column(Float)
    100_day_ma = Column(Float)
    200_day_ma = Column(Float)

    # Exponentially Weighted Moving Averages
    5_day_ewma = Column(Float)
    10_day_ewma = Column(Float)
    12_day_ewma = Column(Float)
    20_day_ewma = Column(Float)
    26_day_ewma = Column(Float)
    50_day_ewma = Column(Float)
    100_day_ewma = Column(Float)
    200_day_ewma = Column(Float)

    # --------------------------------------------
    # Difference from Averages
    # --------------------------------------------

    #Difference from Moving Averages
    diff_5_day_ma = Column(Float)
    diff_10_day_ma = Column(Float)
    diff_20_day_ma = Column(Float)
    diff_50_day_ma = Column(Float)
    diff_100_day_ma = Column(Float)
    diff_200_day_ma = Column(Float)
    diff_5_day_ewma = Column(Float)
    diff_10_day_ewma = Column(Float)
    diff_20_day_ewma = Column(Float)
    diff_100_day_ewma = Column(Float)
    diff_200_day_ewma = Column(Float)

    # Percent Difference from Moving Averages
    pct_diff_5_day_ma = Column(Float)
    pct_diff_10_day_ma = Column(Float)
    pct_diff_20_day_ma = Column(Float)
    pct_diff_50_day_ma = Column(Float)
    pct_diff_100_day_ma = Column(Float)
    pct_diff_200_day_ma = Column(Float)
    pct_diff_5_day_ewma = Column(Float)
    pct_diff_10_day_ewma = Column(Float)
    pct_diff_20_day_ewma = Column(Float)
    pct_diff_100_day_ewma = Column(Float)
    pct_diff_200_day_ewma = Column(Float)

    # --------------------------------------------
    # General Momentum Indicators
    # --------------------------------------------

    # Momentum
    5_day_momentum = Column(Float)
    10_day_momentum = Column(Float)
    20_day_momentum = Column(Float)
    50_day_momentum = Column(Float)
    100_day_momentum = Column(Float)
    200_day_momentum = Column(Float)

    # MACD
    macd = Columnn(Float)
    macd_signal = Column(Float)
    macd_histogram = Column(Float)


