#!/bin/bash

# cmake.sh
# Basically does what you'd expect cmake clean to do and runs cmake in the local
# directory


# Clean up old CMake files
if [ -d build/ ]
then
    rm -r build/*
else
    mkdir build
fi

# Run CMake
cd build
cmake ..

# Build the executable
if [ $# -ne 0 -a $1=='build' ]
then
    make
fi

# Leave us back where we started
cd ..

