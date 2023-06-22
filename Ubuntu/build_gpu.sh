#!/bin/sh

# Script to construct an EXP Singularity container with CUDA runtime


# This gets the top directory location of the script
TOPDIR=$(cd -P -- "$(dirname -- "$0")" && pwd -P)

# Current build directory
echo "The current build directory"
pwd

# Location of the EXP installation which now includes all the data
# directories
STAGEDIR=/home/weinberg/stage

# Use "make prefix=$STAGEDIR" from EXP to install into a staging directory
# Tar up the EXP install from the $STAGEDIR directory

echo "Tar up EXP"
cd $STAGEDIR
tar cvz -h -f $TOPDIR/EXP.tar.gz .

# You can put other executables in to the tar file as well, or make a
# sandbox version and copy them in later

# Copy CUDA runtime libraries to build directory.  This needs to be
# adjusted for whatever CUDA version you are using
echo "Copy CUDA runtime"
cp /usr/local/cuda/targets/x86_64-linux/lib/libcudart.so.11.0 $TOPDIR
cp /usr/local/cuda/targets/x86_64-linux/lib/libnvToolsExt.so.1 $TOPDIR

# HDF5 dependencies
#
echo "Copy HDF5 runtime"
cp /usr/lib/x86_64-linux-gnu/libhdf5_serial_cpp.so.103 $TOPDIR
cp /usr/lib/x86_64-linux-gnu/libhdf5_serial.so.103 $TOPDIR

# Build the Singularity image
echo "Building singularity"
cd $TOPDIR
pwd

sudo apptainer build --notest EXP.sif jammy/EXP
