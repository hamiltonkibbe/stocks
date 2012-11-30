#!/bin/bash


wget http://mirrors.syringanetworks.net/gnu/gsl/gsl-1.15.tar.gz
wget http://downloads.sourceforge.net/project/mlpy/mlpy%203.5.0/mlpy-3.5.0.tar.gz
tar xvf gsl-1.15.tar.gz
tar xvf mlpy-3.5.0.tar.gz

cd gsl-1.15
./configure --prefix=$VIRTUAL_ENV 
make && make install

cd ../mlpy-3.5.0
python setup.py build_ext --include-dirs=$VIRTUAL_ENV/include --rpath=$VIRTUAL_ENV/lib ==library-dirs=$VIRTUAL_ENV/lib --libraries=gsl
python setup.py install

cd ..
sudo rm -r mlpy-3.5.0*
sudo rm -r gsl-1.15*

