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





