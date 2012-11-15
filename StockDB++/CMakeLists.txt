# StockDB++ CMake File
# Builds the StockDB application

# Minimum Required Version
cmake_minimum_required(VERSION 2.6)

# Set project name
project(StockDB)

# C++11
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

# Set Build output directory
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/bin)

# Add source directory
add_subdirectory(src)
