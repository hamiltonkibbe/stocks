/**
 * @file    yahooFDS.h
 * @author  Hamilton Kibbe ham@hamiltonkibbe.com
 *
 * @brief   Access stock data from the Yahoo! Finance API
 *
 *
*/

#ifndef __YAHOOFDS_H__
#define __YAHOOFDS_H__

/* Project Header Files */
#include "financialDataSource.h"
#include "stockExceptions.h"
#include "historicalQuote.h"

/* Standard Header Files */
#include <iosfwd>




/* Forward Declarations */
typedef void CURL;


/** Yahoo Stock Quotes API
 *
*/
class YahooFDS : public FinancialDataSource
{
    
public:

    YahooFDS();
    ~YahooFDS();
    
    double get_price(const std::string &symbol);
    double get_change(const std::string &symbol);
    double get_market_cap(const std::string &symbol);
    double get_book_value(const std::string &symbol);
    double get_ebitda(const std::string &symbol);
    double get_dividend_per_share(const std::string &symbol);
    double get_dividend_yield(const std::string &symbol);
    double get_earnings_per_share(const std::string &symbol);
    double get_52_week_high(const std::string &symbol);
    double get_52_week_low(const std::string &symbol);
    double get_50day_moving_avg(const std::string &symbol);
    double get_200day_moving_avg(const std::string &symbol);
    double get_price_earnings_ratio(const std::string &symbol);
    double get_price_earnings_growth_ratio(const std::string &symbol);
    double get_price_sales_ratio(const std::string &symbol);
    double get_price_book_ratio(const std::string &symbol);
    double get_short_ratio(const std::string &symbol);
    
    unsigned get_volume(const std::string &symbol);
    unsigned  get_avg_daily_volume(const std::string &symbol);
    
    std::string get_name(const std::string &symbol);
    std::string get_stock_exchange(const std::string &symbol);
    std::string get_sector(const std::string &symbol);
    std::string get_industry(const std::string &symbol);
    
    void get_historical_prices(const std::string &symbol,
                                boost::gregorian::date &start,
                                boost::gregorian::date &end,
                                quoteVector_t &quotes);
    
    
private:
    
    CURL *curl;
    std::ostringstream stream;
    
    std::string get_url(const std::string &ticker, const std::string &stat);
    std::string request(const std::string &url);
    static size_t write_data(char *ptr, size_t size, size_t nmemb, void * userdata);
    
};





#endif

