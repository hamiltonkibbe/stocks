cmake_minimum_required(VERSION 2.6)

include_directories(../include)
file(GLOB HEADERS ../include/*.h*)
file(GLOB SRCS *.cpp)

# Boost
FIND_PACKAGE(Boost COMPONENTS date_time)
IF (Boost_FOUND)
    INCLUDE_DIRECTORIES(${Boost_INCLUDE_DIR})
    ADD_DEFINITIONS("-DHAS_BOOST")
ENDIF()

# Curl
FIND_PACKAGE(CURL)
IF (CURL_FOUND)
    INCLUDE_DIRECTORIES(${Curl_INCLUDE_DIR})
ENDIF()


ADD_EXECUTABLE(

    StockDB
    ${SRCS}
    ${HEADERS}
    
)

TARGET_LINK_LIBRARIES( StockDB ${Boost_LIBRARIES} ${CURL_LIBRARIES})