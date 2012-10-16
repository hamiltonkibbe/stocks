Quant Trading R&D Environment
========================

Stock Data DB
--------------
Local stock quote storage for backtesting and algorithm training. 

StockDBManager
^^^^^^^^^^^
The StockDBManager manages the stock database. It retreives data from external 
sources and caches it locally in the database. When data is requested from the 
StockDBManager it will be served from the local database if it is cached, or 
from an external source otherwise.  All requested data is stored locally for 
faster retreval with subsequent requests.

**Getting started:**

* Configure database settings in config.py
* use ``StockDBManager.create_database()`` to create the database on local machine
* Add stocks to the database with ``StockDBManager.add_stock()``
  The quotes database will be populated with historical quotes for the stock and subsequent calls to
  ``StockDBManager.update_quotes()`` will update that symbol's quotes in the database
* get quotes with ``

Analysis Tools
--------------
Common indicator calculations as well as Machine-learning predictors


