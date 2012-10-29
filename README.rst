#############################
Quant Trading R&D Environment
#############################

**************
Stock Data DB
**************
Local stock quote storage for backtesting and algorithm training. The database
serves as a local cache for stock data.  When data is requested from the 
``StockDBManager`` it will be served from the local database if available, or
rom an external source otherwise. All requested data is stored locally for 
faster retrieval during subsequent requests. 
database.py


database.py
===========
database.py contains definitions for all database-access related functionality
it may be run as a script to perform several database administration functions


**Getting started:**
* Configure database settings in config.py
* Use ``python database.py create`` to create the database on local 
  machine
* Add stocks to the database with ``python database.py add <symbol>``. Once 
  a stock  is added,The quotes database is populated with historical quotes for 
  the stock. 
* ``python database.py sync`` updates quotess for all stocks in the 
  database and should be used daily to keep the database up to date. 
* Quotes are retreived through the interfaces in ``datafeed.py``

datafeed.py
===========
The objects in datafeed  are used to retreive quote data. As of right now it
only handles historical intraday quotes.



**************
Analysis Tools
**************
Common indicator calculations as well as Machine-learning predictors


