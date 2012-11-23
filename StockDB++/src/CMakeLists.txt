cmake_minimum_required(VERSION 2.6)

include_directories(../include)
file(GLOB HEADERS ../include/*.h*)
file(GLOB SRCS *.cpp)


# Boost
find_package(Boost COMPONENTS date_time)
if (BOOST_FOUND)
    include_directories(${BOOST_INCLUDE_DIR})
    add_definitions("-DHAS_BOOST")
endif()

# Curl
find_package(Curl)
if(CURL_FOUND)
    include_directories(${CURL_INCLUDE_DIR})
endif()


# MySQL
find_package(MySQLConnectorCPP REQUIRED)
if(MYSQLCONNECTORCPP_FOUND)
    include_directories(${MYSQLCONNECTORCPP_INCLUDE_DIR})
endif()


add_executable(

    StockDB
    ${SRCS}
    ${HEADERS}
    
)

target_link_Libraries( StockDB ${Boost_LIBRARIES} ${CURL_LIBRARIES} ${MYSQLCONNECTORCPP_LIBRARIES})