Quant Trading R&D Environment
========================

Stock Data DB
--------------
Local stock quote storage for backtesting and algorithm training. 

Configure database settings in config.py
*   use ``StockDBManager.create_database()`` to create the database on local machine
*   Add stocks to the database with ``StockDBManager.add_stock()``
    The quotes database will be populated with historical quotes for the stock and subsequent calls to
    ``update_quotes()`` will update that symbol's quotes in the database


Analysis Tools
--------------
Common indicator calculations as well as Machine-learning predictors


