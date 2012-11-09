/**


*/

/* Project Header Files */
#include "yahooFDS.h"

/* Third Party Header Files */
#include <boost/algorithm/string.hpp>
#include <curl/curl.h>

/* Standard Header Files */
#include <iostream>
#include <sstream>
#include <algorithm>



using namespace boost::gregorian;

YahooFDS::YahooFDS()
{
    curl = curl_easy_init();
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_data);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &stream);
}


YahooFDS::~YahooFDS()
{
    curl_easy_cleanup(curl);
}


double
YahooFDS::get_price(const std::string &symbol)
{
    std::string val = request(get_url(symbol, "l1"));
    if (val.find("0.00") == 0 || val.find("N/A") != std::string::npos)
        throw TickerNameException();
    return atof(val.c_str());
}


double
YahooFDS::get_change(const std::string &symbol)
{
    std::string val = request(get_url(symbol, "c1"));
    if (val.find("0.00") == 0 || val.find("N/A") != std::string::npos)
        throw TickerNameException();
    return atof(val.c_str());
}


double
YahooFDS::get_market_cap(const std::string &symbol)
{
    double cap = 0.0;
    std::string val = request(get_url(symbol, "j1"));
    if (val.find("0.00") == 0 || val.find("N/A") != std::string::npos)
        throw TickerNameException();
    if (val.find("M") != std::string::npos)
        cap = atof(val.c_str()) * 1000000;
    else if (val.find("B") != std::string::npos)
        cap = atof(val.c_str()) * 1000000000;
    else if (val.find("K") != std::string::npos)
        cap = atof(val.c_str()) * 1000;
        
    return cap;
}


double
YahooFDS::get_book_value(const std::string &symbol)
{
    std::string val = request(get_url(symbol, "b4"));
    if (val.find("0.00") == 0 || val.find("N/A") != std::string::npos)
        throw TickerNameException();
    return atof(val.c_str());
}


double
YahooFDS::get_ebitda(const std::string &symbol)
{
    std::string val = request(get_url(symbol, "j4"));
    if (val.find("0.00") == 0 || val.find("N/A") != std::string::npos)
        throw TickerNameException();
    return atof(val.c_str());
}

double
YahooFDS::get_dividend_per_share(const std::string &symbol)
{
    std::string val = request(get_url(symbol, "d"));
    if (val.find("0.00") == 0 || val.find("N/A") != std::string::npos)
        throw TickerNameException();
    return atof(val.c_str());
}

double
YahooFDS::get_dividend_yield(const std::string &symbol)
{
    std::string val = request(get_url(symbol, "y"));
    if (val.find("0.00") == 0 || val.find("N/A") != std::string::npos)
        throw TickerNameException();
    return atof(val.c_str());
}


double
YahooFDS::get_earnings_per_share(const std::string &symbol)
{
    std::string val = request(get_url(symbol, "e"));
    if (val.find("0.00") == 0 || val.find("N/A") != std::string::npos)
        throw TickerNameException();
    return atof(val.c_str());
}


double
YahooFDS::get_52_week_high(const std::string &symbol)
{
    std::string val = request(get_url(symbol, "k"));
    if (val.find("0.00") == 0 || val.find("N/A") != std::string::npos)
        throw TickerNameException();
    return atof(val.c_str());
}


double
YahooFDS::get_52_week_low(const std::string &symbol)
{
    std::string val = request(get_url(symbol, "j"));
    if (val.find("0.00") == 0 || val.find("N/A") != std::string::npos)
        throw TickerNameException();
    return atof(val.c_str());
}


double
YahooFDS::get_50day_moving_avg(const std::string &symbol)
{
    std::string val = request(get_url(symbol, "m3"));
    if (val.find("0.00") == 0 || val.find("N/A") != std::string::npos)
        throw TickerNameException();
    return atof(val.c_str());
}


double
YahooFDS::get_200day_moving_avg(const std::string &symbol)
{
    std::string val = request(get_url(symbol, "m4"));
    if (val.find("0.00") == 0 || val.find("N/A") != std::string::npos)
        throw TickerNameException();
    return atof(val.c_str());
}


double
YahooFDS::get_price_earnings_ratio(const std::string &symbol)
{
    std::string val = request(get_url(symbol, "r"));
    if (val.find("0.00") == 0 || val.find("N/A") != std::string::npos)
        throw TickerNameException();
    return atof(val.c_str());
}


double
YahooFDS::get_price_earnings_growth_ratio(const std::string &symbol)
{
    std::string val = request(get_url(symbol, "r5"));
    if (val.find("0.00") == 0 || val.find("N/A") != std::string::npos)
        throw TickerNameException();
    return atof(val.c_str());
}


double
YahooFDS::get_price_sales_ratio(const std::string &symbol)
{
    std::string val = request(get_url(symbol, "p5"));
    if (val.find("0.00") == 0 || val.find("N/A") != std::string::npos)
        throw TickerNameException();
    return atof(val.c_str());
}



double
YahooFDS::get_price_book_ratio(const std::string &symbol)
{
    std::string val = request(get_url(symbol, "p6"));
    if (val.find("0.00") == 0 || val.find("N/A") != std::string::npos)
        throw TickerNameException();
    return atof(val.c_str());
}

double
YahooFDS::get_short_ratio(const std::string &symbol)
{
    std::string val = request(get_url(symbol, "s7"));
    if (val.find("0.00") == 0 || val.find("N/A") != std::string::npos)
        throw TickerNameException();
    return atof(val.c_str());
}



unsigned
YahooFDS::get_volume(const std::string &symbol)
{
    std::string val = request(get_url(symbol, "v"));
    if (val.find("0.00") == 0 || val.find("N/A") == 0)
        throw TickerNameException();
    return atoi(val.c_str());
}


unsigned
YahooFDS::get_avg_daily_volume(const std::string &symbol)
{
    std::string val = request(get_url(symbol, "a2"));
    if (val.find("0.00") == 0 || val.find("N/A") != std::string::npos)
        throw TickerNameException();
    return atoi(val.c_str());
}


std::string
YahooFDS::get_name(const std::string &symbol)
{
    std::string val = request(get_url(symbol, "n"));
    std::string u_symbol = symbol;
    boost::to_upper(u_symbol);
    if (val.find(u_symbol) == 1)
        throw TickerNameException();
    val.erase(remove(val.begin(), val.end(), '\"'), val.end());
    val.erase(remove(val.begin(), val.end(), '\n'), val.end());
    return val;
}


std::string
YahooFDS::get_stock_exchange(const std::string &symbol)
{
    std::string val = request(get_url(symbol, "x"));
    if (val.find("N/A") == 1)
        throw TickerNameException();
    val.erase(remove(val.begin(), val.end(), '\"'), val.end());
    val.erase(remove(val.begin(), val.end(), '\n'), val.end());
    if (val.find("NasdaqNM") != std::string::npos)
        val = "Nasdaq";
    return val;
}





void
YahooFDS::get_historical_prices(const std::string &symbol,
                                    date &start,
                                    date &end,
                                    quoteVector_t &quotes)
{
    std::vector<std::string> quoteStrings;
    date::ymd_type start_d = start.year_month_day();
    date::ymd_type end_d = end.year_month_day();
    std::ostringstream url;
    url << "http://ichart.yahoo.com/table.csv?s=" << symbol << "&d=" \
                                                << end_d.month - 1 << "&e=" \
                                                << end_d.day << "&f=" \
                                                << end_d.year << "&a=" \
                                                << start_d.month - 1 << "&b=" \
                                                << start_d.day << "&c=" \
                                                << start_d.year << "&ignore=.csv";
    
    boost:split(quoteStrings, (const std::string &)request(url.str()), boost::is_any_of("\n"),boost::token_compress_on); 
    quoteStrings.erase(quoteStrings.begin());
    quoteStrings.erase(quoteStrings.end());
      
    for (std::vector<std::string>::reverse_iterator it = quoteStrings.rbegin(); it < quoteStrings.rend(); it++)
    {
        std::vector<std::string> temp;
        boost::split(temp, *it, boost::is_any_of(", "));
        HistoricalQuote quote(symbol,
                              temp.at(0),
                              atof(temp.at(1).c_str()),
                              atof(temp.at(2).c_str()),
                              atof(temp.at(3).c_str()),
                              atof(temp.at(4).c_str()),
                              atol(temp.at(5).c_str()),
                              atof(temp.at(6).c_str()));
        quotes.push_back(quote);
    }
    std::cout << "Got " << quotes.size() << " quotes!" << endl;
}



std::string
YahooFDS::request(const std::string &url)
{
    stream.str("");
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_perform(curl);
    return stream.str();
}


std::string
YahooFDS::get_url(const std::string &ticker, const std::string &stat)
{
    std::ostringstream urls;
    urls << "http://download.finance.yahoo.com/d/quotes.csv?s=" << ticker << "&f=" << stat;
    return urls.str();
}


size_t
YahooFDS::write_data(char *ptr, size_t size, size_t nmemb, void * userdata)
{
    std::ostringstream *stream = (std::ostringstream*)userdata;
    size_t count = size * nmemb;
    stream->write(ptr, count);
    return count;
}