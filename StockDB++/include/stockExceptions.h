

#ifndef __STOCKEXCEPTIONS_H__
#define __STOCKEXCEPTIONS_H__

#include <exception>


using namespace std;

class TickerNameException:
    public exception
{
    virtual const char* what() const throw()
    {
        return "Invalid ticker symbol.";
    }
};









#endif