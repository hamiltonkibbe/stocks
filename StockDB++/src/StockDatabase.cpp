/**


*/

/* Project Header Files */
#include "stockDatabase.h"

/* Third Party Header Files */
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/ini_parser.hpp>
#include <cppconn/driver.h>
#include <cppconn/exception.h>
#include <cppconn/resultset.h>
#include <cppconn/statement.h>
#include <cppconn/prepared_statement.h>

/* Standard Header Files */
#include <iostream>

StockDatabase::StockDatabase()
{
    
    boost::property_tree::ptree pt;
    boost::property_tree::ini_parser::read_ini("../database.cfg", pt);
    auto host = pt.get<std::string>("database.host");
    auto user = pt.get<std::string>("database.user");
    auto password = pt.get<std::string>("database.password");
    auto database = pt.get<std::string>("database.database");
    
    con = std::unique_ptr<sql::Connection>(get_driver_instance()->connect(host, user, password));
    std::cout << "Connected..." << std::endl;
    con->setSchema(database);
}

StockDatabase::~StockDatabase()
{
    
}

void
StockDatabase::create()
{
    auto stmt = con->createStatement();

}
