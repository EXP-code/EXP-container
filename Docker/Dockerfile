# Image for building EXP with MPI and CUDA based on the hpcbase recipe
#    and our standard Ubuntu 24.04 development environment for Docker
# 
# Contents:
# 
#   * Ubuntu 24.04 
#   * GNU compilers (upstream)
#   * Python 2 and 3 (upstream)
#   * OpenMPI, FFTW3, HDF5, Eigen3, PNG (upstream)
#   * EXP, EXP-examples, pyEXP-examples, EXP-docs
# 
# Build notes:
# 
#   * The container build requires the following commands:
#     $ hpccm --recipe exp_all_deb.py --format docker > Dockerfile
#     $ docker build -t exp-test -f Dockerfile .
#   or
#     $ docker buildx build --platform=linux/amd64,linux/arm64 -t the9cat/exp:latest --push -f Dockerfile .
# 
#   * You will need to put the EXP.tar.gz file in the build directory. I
#     like to make a fresh clone and run `git submodule update --init
#     --recursive` before tarring it up.
# 
# 

FROM ubuntu:24.04 AS devel

ARG BRANCH=main

# GNU compiler
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        g++ \
        gcc \
        gfortran && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        2to3 \
        ca-certificates \
        cmake \
        git \
        libeigen3-dev \
        libfftw3-dev \
        libhdf5-103-1t64 \
        libhdf5-cpp-103-1t64 \
        libhdf5-dev \
        libhdf5-hl-100t64 \
        libhdf5-hl-cpp-100t64 \
        libopenmpi-dev \
        libpng-dev \
        make \
        openmpi-bin \
        python3 \
        python3-dev \
        tar \
        wget && \
    rm -rf /var/lib/apt/lists/*

# https://github.com/EXP-code/EXP.git
RUN mkdir -p /var/tmp && cd /var/tmp && git clone --depth=1 --branch $BRANCH https://github.com/EXP-code/EXP.git EXP && cd - && \
    cd /var/tmp/EXP && \
    git config --global --add safe.directory /var/tmp/EXP && \
    git config --global --add safe.directory /var/tmp/EXP/extern/HighFive && \
    git config --global --add safe.directory /var/tmp/EXP/extern/pybind11 && \
    git config --global --add safe.directory /var/tmp/EXP/extern/yaml-cpp && \
    git config --global --add safe.directory /var/tmp/EXP/extern/HighFive/deps/catch2 && \
    mkdir -p /var/tmp/EXP/build && cd /var/tmp/EXP/build && cmake -DCMAKE_INSTALL_PREFIX=/usr/local/EXP -D CMAKE_BUILD_TYPE=Release -D ENABLE_CUDA=NO -D ENABLE_USER=YES -D ENABLE_SLURM=NO -D ENABLE_PNG=NO -D ENABLE_VTK=NO -D FFTW_INCLUDE_DIRS=/usr/include/fftw3 -D Eigen3_DIR=/usr/share/eigen3/cmake -D CMAKE_INSTALL_PREFIX=/usr/local/EXP /var/tmp/EXP && \
    cmake --build /var/tmp/EXP/build --target all -- -j$(nproc) && \
    cmake --build /var/tmp/EXP/build --target install -- -j$(nproc) && \
    rm -rf /var/tmp/EXP

FROM ubuntu:24.04

# GNU compiler runtime
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        libgfortran5 \
        libgomp1 && \
    rm -rf /var/lib/apt/lists/*

# https://github.com/EXP-code/EXP.git
COPY --from=devel /usr/local/EXP /usr/local/EXP
ENV LD_LIBRARY_PATH=/usr/local/EXP/lib \
    LIBRARY_PATH=/usr/local/EXP/lib \
    PATH=/usr/local/EXP/bin:${PATH}

# GNU compiler
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        g++ \
        gcc \
        gfortran && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        2to3 \
        busybox \
        dvipng \
        ffmpeg \
        git \
        less \
        libeigen3-dev \
        libfftw3-dev \
        libgsl-dev \
        libhdf5-103-1t64 \
        libhdf5-cpp-103-1t64 \
        libhdf5-dev \
        libhdf5-hl-100t64 \
        libhdf5-hl-cpp-100t64 \
        libopenmpi-dev \
        libpython3.12-dev \
        libvtk9-dev \
        make \
        nano \
        openmpi-bin \
        python3 \
        python3-distlib \
        python3-distutils-extra \
        python3-pip \
        python3-pip-whl \
        python3-setuptools \
        python3-wheel \
        python3.12-dev \
        python3.12-venv \
        rsync \
        unzip \
        wget && \
    rm -rf /var/lib/apt/lists/*

COPY --from=devel /usr/local/EXP/bin /usr/local/EXP/bin

COPY --from=devel /usr/local/EXP/lib /usr/local/EXP/lib

RUN mkdir -p /var/www/html && \
    cd /var/www/html && \
    wget -r -nH --cut-dirs=1 https://exp-code.github.io/EXP-docs/

RUN python3 -m venv /opt/venv && \
    . /opt/venv/bin/activate

ENV PATH=/opt/venv/bin:/usr/local/EXP/bin:$PATH

ENV LIBRARY_PATH=/usr/local/EXP/lib

ENV LD_LIBRARY_PATH=/usr/local/EXP/lib

ENV PYTHONPATH=/opt/venv/lib/python3.12/site-packages:/usr/local/EXP/lib/python3.12/site-packages

RUN userdel -f ubuntu && \
    rm -rf /home/ubuntu

# pip
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        python3-pip-whl \
        python3-setuptools \
        python3-wheel && \
    rm -rf /var/lib/apt/lists/*
RUN /opt/venv/bin/pip3 --no-cache-dir install numpy scipy matplotlib jupyter h5py mpi4py PyYAML k3d pandas astropy gala galpy pynbody jupyterlab jupyterhub ipyparallel

RUN pip3 install --config-settings --build-option=--yes --no-build-isolation agama

RUN cd /usr/local && \
    export GIT_SSL_NO_VERIFY=1 && \
    git clone https://github.com/EXP-code/EXP-examples EXP-examples && \
    git clone https://github.com/EXP-code/pyEXP-examples pyEXP-examples && \
    git clone https://github.com/EXP-code/EXP-tools && \
    cd pyEXP-examples && \
    git checkout haloVel

RUN chmod -R 777 /opt/venv && \
    chmod -R 777 /usr/local/pyEXP-examples && \
    chmod -R 777 /usr/local/EXP-examples && \
    chmod -R 777 /usr/local/EXP-tools
