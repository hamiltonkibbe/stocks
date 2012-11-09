/**
 * @file    HistoricalQuote.h
 * @author  Hamilton Kibbe ham@hamiltonkibbe.com
 *
 * @brief   Historical Quote
 *
 *
*/

#ifndef __HISTORICALQUOTE_H__
#define __HISTORICALQUOTE_H__

/* Third Party Header Files */
#include "boost/date_time/gregorian/gregorian.hpp"
#include <boost/algorithm/string.hpp>

/* Standard Header Files */
#include <string>


class HistoricalQuote
{
public:
    HistoricalQuote(std::string _Ticker,
                    std::string _Date,
                    double _Open,
                    double _High,
                    double _Low,
                    double _Close,
                    unsigned long _Volume,
                    double _AdjClose)
    {
        Ticker = _Ticker;
        boost::to_lower(Ticker);
        Date = boost::gregorian::date(boost::gregorian::from_string(_Date));
        Open = _Open;
        High = _High;
        Low = _Low;
        Close = _Close;
        Volume = _Volume;
        AdjClose = _AdjClose;
    }
    
    ~HistoricalQuote(){};

    std::string Ticker;
    boost::gregorian::date Date;
    double Open;
    double High;
    double Low;
    double Close;
    unsigned long Volume;
    double AdjClose; 
       
};

#endif