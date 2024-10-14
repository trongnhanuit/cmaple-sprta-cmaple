#!bin/bash

###### handle arguments ######

work_dir=$1 # build-default dir
code_dir=$2 # repo dir


### pre steps #####

#module load openmpi/4.1.5 boost/1.84.0 eigen/3.3.7 llvm/17.0.1

#export OMPI_CC=clang
#export OMPI_CXX=clang++


#export CC=clang
#export CXX=clang++


#export LDFLAGS="-L/apps/llvm/17.0.1/lib"
#export CPPFLAGS="-I/apps/llvm/17.0.1/lib/clang/17/include"


############

echo "Building CMAPLE baseline"

mkdir -p "$work_dir"
cd $work_dir
#cmake -DCMAKE_CXX_FLAGS="$LDFLAGS $CPPFLAGS" -DCMAKE_C_COMPILER=mpicc -DCMAKE_CXX_COMPILER=mpicxx -DEIGEN3_INCLUDE_DIR=/apps/eigen/3.3.7/include/eigen3 $code_dir
cmake -DCMAKE_C_COMPILER=gcc -DCMAKE_CXX_COMPILER=g++ $code_dir
make -j
