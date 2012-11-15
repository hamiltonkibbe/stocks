/**
 * @file    stockDatabase.h
 * @author  Hamilton Kibbe ham@hamiltonkibbe.com
 *
 * @brief   stockDB interface
 *
 *
*/

#ifndef __stockDB_H__
#define __stockDB_H__

/* Third Party Header Files */
#include "mysql_connection.h"

/* Standard Header Files */
#include <memory>
#include <string>


class StockDatabase
{
public:
   
    StockDatabase();
    ~StockDatabase();
    
    void create();
    
    
private:
    
    std::unique_ptr<sql::Connection> con;
};

#endif