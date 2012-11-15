/**
 * @file    stockDB.h
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
#include <cppconn/driver.h>
#include <cppconn/exception.h>
#include <cppconn/resultset.h>
#include <cppconn/statement.h>
#include <cppconn/prepared_statement.h>



/* Standard Header Files */
#include <string>


class StockDatabase
{
public:
   
    StockDatabase();
    ~StockDatabase();
    
private:


};

#endif