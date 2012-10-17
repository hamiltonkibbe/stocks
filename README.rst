#############################
Quant Trading R&D Environment
#############################

**************
Stock Data DB
**************
Local stock quote storage for backtesting and algorithm training. 

database.py
===========

The StockDBManager manages the stock database. It retreives data from external 
sources and caches it locally in the database. When data is requested from the 
StockDBManager it will be served from the local database if it is cached, or 
from an external source otherwise.  All requested data is stored locally for 
faster retreval with subsequent requests. The manager also provides 
administrative tools for working with the database.

Getting started:
----------------

* Configure database settings in config.py
* Use ``StockDBManager.create_database()`` to create the database on local 
  machine
* Add stocks to the database with ``StockDBManager.add_stock(symbol)``. Once 
  a stock  is added,The quotes database is populated with historical quotes for 
  the stock. For convenience, ``python database.py add symbol`` adds the
  specified symbol to the stock database.
* ``StockDBManager.update_quotes(symbol)`` will update te given symbol's 
  quotes in the database. 
* ``StockDBManager.sync_quotes()`` updates quotess for all stocks in the 
  database and should be used daily to keep the database up to date. For 
  convenience, ``python database.py sync`` will bring all quotes up to date.
* Quotes are retreived through the interfaces in ``datafeed.py``.

datafeed
========
The datafeed objects are used to retreive quote data. As of right now it only
handles historical intraday quotes.

**************
Analysis Tools
**************
Common indicator calculations as well as Machine-learning predictors


