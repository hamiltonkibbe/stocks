/**
 *
 *
 */
 
 #include "yahooFDS.h"
#include "historicalQuote.h"
 #include <iostream>
 #include <vector>
 #include <string>

 
 using namespace std;
 
 int main(int argc, char* argv[])
 {
   YahooFDS quote;
   const string ticker(argv[1]);
   string startd("1900/01/01");
   string endd("2012/11/07");
   boost::gregorian::date start(boost::gregorian::from_string(startd));
   boost::gregorian::date end(boost::gregorian::from_string(endd));
   vector<HistoricalQuote> prices;
   //cout << "Retrieving data for " << quote.get_name((const string &)ticker) << endl;
   //cout << "On: " << quote.get_stock_exchange((const string &)ticker) << endl;
   //cout << "Price: " << quote.get_price((const string &)ticker) << endl;
   //cout << "Change: " << quote.get_change((const string &)ticker) << endl;
   //cout << "Volume: " << quote.get_volume((const string &)ticker) << endl;
   //cout << "Avg. Volume: " << quote.get_avg_daily_volume((const string &)ticker) << endl;
   //cout << "Market Cap: " << quote.get_market_cap((const string &)ticker) << endl;
   quote.get_historical_prices(ticker, start, end, prices);
  // cout << "Name: " << quote.get_name((const string &)ticker) << endl;
 }