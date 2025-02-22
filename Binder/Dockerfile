# Image for running EXP with Binder using with MPI based on
#    our standard Ubuntu 24.04 development environment for Docker
# 
# Contents:
# 
#   * Ubuntu 24.04 
#   * GNU compilers
#   * Python3, OpenMPI, FFTW3, HDF5, Eigen3, PNG
# 
# Build notes:
# 
#   * A local, test container build requires the following command:
#     $ docker build -t exp-test -f Dockerfile .
# 

# Break compile and install into separate stages to save space
FROM ubuntu:24.04 AS devel

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

# git@github.com:EXP-code/EXP.git
RUN mkdir -p /var/tmp && cd /var/tmp && export GIT_SSL_NO_VERIFY=1 && git clone https://github.com/EXP-code/EXP EXP && cd - && \
    cd /var/tmp/EXP && \
    git config --global --add safe.directory /var/tmp/EXP && \
    git config --global --add safe.directory /var/tmp/EXP/extern/HighFive && \
    git config --global --add safe.directory /var/tmp/EXP/extern/pybind11 && \
    git config --global --add safe.directory /var/tmp/EXP/extern/yaml-cpp && \
    git config --global --add safe.directory /var/tmp/EXP/extern/HighFive/deps/catch2 && \
    mkdir -p /usr/local/EXP/doc && \
    # cp -a /var/tmp/EXP/sphinx/* /usr/local/EXP/doc && \
    mkdir -p /var/tmp/EXP/build && cd /var/tmp/EXP/build && cmake -DCMAKE_INSTALL_PREFIX=/usr/local/EXP -D CMAKE_BUILD_TYPE=Release -D ENABLE_CUDA=NO -D ENABLE_USER=YES -D ENABLE_SLURM=NO -D ENABLE_PNG=NO -D ENABLE_VTK=NO -D FFTW_INCLUDE_DIRS=/usr/include/fftw3 -D Eigen3_DIR=/usr/share/eigen3/cmake -D CMAKE_INSTALL_PREFIX=/usr/local/EXP /var/tmp/EXP && \
    cmake --build /var/tmp/EXP/build --target all -- -j$(nproc) && \
    cmake --build /var/tmp/EXP/build --target install -- -j$(nproc) && \
    rm -rf /var/tmp/EXP

# Now for the runtime image
FROM ubuntu:24.04

# GNU compiler runtime
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        libgfortran5 \
        libgomp1 && \
    rm -rf /var/lib/apt/lists/*

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
	rsync \
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
        unzip && \
    rm -rf /var/lib/apt/lists/*

COPY --from=devel /usr/local/EXP/bin /usr/local/EXP/bin

COPY --from=devel /usr/local/EXP/lib /usr/local/EXP/lib

COPY --from=devel /usr/local/EXP/doc /var/www/html

ENV PATH=/opt/venv/bin:/usr/local/EXP/bin:$PATH

ENV LIBRARY_PATH=/usr/local/EXP/lib

ENV LD_LIBRARY_PATH=/usr/local/EXP/lib

ENV PYTHONPATH=/opt/venv/lib/python3.12/site-packages:/usr/local/EXP/lib/python3.12/site-packages

RUN python3 -m venv /opt/venv

# pip
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        python3-pip-whl \
        python3-setuptools \
        python3-wheel && \
    rm -rf /var/lib/apt/lists/*
RUN /opt/venv/bin/pip3 --no-cache-dir install numpy scipy matplotlib jupyter h5py mpi4py PyYAML k3d pandas astropy gala galpy pynbody jupyterlab jupyterhub ipyparallel

# Add a user with a home directory

ARG NB_USER=jovyan
ARG NB_UID=1000
ENV USER ${NB_USER}
ENV NB_UID ${NB_UID}
ENV HOME /home/${NB_USER}

# The default Ubuntu user has uid=1000 which clashes with the expected
# jovyan uid
RUN userdel -f ubuntu

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}

# Make sure the contents of our repo are in ${HOME}
RUN cd ${HOME} && export GIT_SSL_NO_VERIFY=1 && \
    git clone https://github.com/EXP-code/EXP-examples EXP-examples && \
    git clone https://github.com/EXP-code/pyEXP-examples pyEXP-examples
USER root
RUN chown -R ${NB_UID} ${HOME}
RUN chown -R ${NB_UID} /opt/venv
USER ${NB_USER}
WORKDIR ${HOME}

