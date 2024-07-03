"""Image for building EXP with MPI and CUDA based on the hpcbase recipe
   and our standard Ubuntu 22.04 development environment for Docker

Contents:

  * Ubuntu 22.04 
  * GNU compilers (upstream)
  * Python 2 and 3 (upstream)
  * OpenMPI, FFTW3, HDF5, Eigen3, PNG (upstream)

Build notes:

  * The container build requires the following commands:
    $ hpccm --recipe exp_all_deb.py --format docker > Dockerfile
    $ docker build -t exp-test -f Dockerfile .
  or
    $ docker buildx build --platform=linux/amd64,linux/arm64 -t the9cat/exp:latest --push -f Dockerfile .

  * You will need to put the EXP.tar.gz file in the build directory. I
    like to make a fresh clone and run `git submodule update --init
    --recursive` before tarritn it up.

"""
devel_image = 'ubuntu:22.04'
runtime_image = 'ubuntu:22.04'

##############
# Devel stage
##############

Stage0 += comment(__doc__, reformat=False)

Stage0 += baseimage(image=devel_image, _as='devel')

# Python
Stage0 += python()

# GNU compilers
compiler = gnu()
Stage0 += compiler

# Get additional packages
Stage0 += apt_get(ospackages=['libopenmpi-dev', 'openmpi-bin',
                              'libfftw3-dev', 'libhdf5-dev',
                              'libhdf5-103', 'libeigen3-dev',
                              'libpng-dev', 'python3-dev', 'wget',
                              'git', 'tar', 'cmake', 'make'])

# Create a build directory and configure EXP.  The options below
# should give you all that you need for most cases. Add additional
# CMake options as needed.
#
Stage0 += generic_cmake(
    cmake_opts=['-D CMAKE_BUILD_TYPE=Release',
                '-D ENABLE_CUDA=NO',
                '-D ENABLE_USER=YES',
                '-D ENABLE_SLURM=NO',
                '-D ENABLE_PNG=NO',
                '-D ENABLE_VTK=NO',
                '-D FFTW_INCLUDE_DIRS=/usr/include/fftw3',
                '-D Eigen3_DIR=/usr/share/eigen3/cmake',
                '-D CMAKE_INSTALL_PREFIX=/usr/local/EXP'],
    preconfigure=['git config --global --add safe.directory /var/tmp/EXP', 'git config --global --add safe.directory /var/tmp/EXP/extern/HighFive', 'git config --global --add safe.directory /var/tmp/EXP/extern/pybind11', 'git config --global --add safe.directory /var/tmp/EXP/extern/yaml-cpp', 'git config --global --add safe.directory /var/tmp/EXP/extern/HighFive/deps/catch2'],
    prefix='/usr/local/EXP',
    runtime_environment={
        'LD_LIBRARY_PATH': '/usr/local/EXP/lib',
        'LIBRARY_PATH': '/usr/local/EXP/lib',
        'PATH': '/usr/local/EXP/bin:${PATH}'},
    package='EXP.tar.gz'
)

################
# Runtime image
################

Stage1 += baseimage(image=runtime_image)

Stage1 += Stage0.runtime(_from='devel')

Stage1 += compiler

Stage1 += apt_get(ospackages=['libpython3.10-dev', 'libopenmpi-dev', 'openmpi-bin', 'less', 'libfftw3-3', 'libhdf5-dev', 'libhdf5-103', 'libhdf5-cpp-103', 'ffmpeg', 'nano', 'libgsl-dev', 'libeigen3-dev', 'python3.10-dev', 'dvipng', 'unzip', 'make'])

# Install EXP into the runtime image
#
Stage1 += copy(_from='devel',
               src='/usr/local/EXP/bin', dest='/usr/local/EXP/bin')
Stage1 += copy(_from='devel',
               src='/usr/local/EXP/lib', dest='/usr/local/EXP/lib')

# Add EXP to the path and library paths
#
Stage1 += environment(variables={'PATH': '/usr/local/EXP/bin:$PATH'})
Stage1 += environment(variables={'LIBRARY_PATH': '/usr/local/EXP/lib'})
Stage1 += environment(variables={'LD_LIBRARY_PATH': '/usr/local/EXP/lib'})

# Some packages needed or useful for running pyEXP
#
Stage1 += environment(variables={'PYTHONPATH': '/usr/local/EXP/lib/python3.10/site-packages'})
Stage1 += pip(packages=['numpy', 'scipy', 'matplotlib', 'jupyter', 'h5py', 'mpi4py', 'PyYAML', 'k3d', 'pandas', 'astropy', 'gala', 'galpy', 'jupyterlab', 'ipyparallel'], pip='pip3', upgrade=True, ospackages=['python3-pip', 'python3-setuptools', 'python3-wheel', 'python3-pip-whl'])

# Jupyter Lab workaround
#
Stage1 += shell(commands=['yes | pip3 uninstall traitlets', 'pip install traitlets==5.9.0'])
