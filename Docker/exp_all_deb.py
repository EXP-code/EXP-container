"""Image for building EXP with MPI and CUDA based on the hpcbase recipe
   and our standard Ubuntu 24.04 development environment for Docker

Contents:

  * Ubuntu 24.04 
  * GNU compilers (upstream)
  * Python 2 and 3 (upstream)
  * OpenMPI, FFTW3, HDF5, Eigen3, PNG (upstream)
  * EXP, EXP-examples, pyEXP-examples, EXP-docs

Build notes:

  * The container build requires the following commands:
    $ hpccm --recipe exp_all_deb.py --format docker > Dockerfile
    $ docker build -t exp-test -f Dockerfile .
  or
    $ docker buildx build --platform=linux/amd64,linux/arm64 -t the9cat/exp:latest --push -f Dockerfile .

  * You may requiest a particular branch_name using:
    $ hpccm --recipe exp_all_deb.py --format docker --userarg branch=branch_name > Dockerfile

  * You will need to put the EXP.tar.gz file in the build directory. I
    like to make a fresh clone and run `git submodule update --init
    --recursive` before tarring it up.

"""
devel_image = 'ubuntu:24.04'
runtime_image = 'ubuntu:24.04'

##############
# Devel stage
##############

BRANCH = USERARG.get('branch', 'devel')

Stage0 += comment(__doc__, reformat=False)

Stage0 += baseimage(image=devel_image, _as='devel')

# Python (use OS package for now)
# Stage0 += python()

# GNU compilers
compiler = gnu()
Stage0 += compiler

# Get additional packages
Stage0 += apt_get(ospackages=['libopenmpi-dev', 'openmpi-bin',
                              'libfftw3-dev', 'libhdf5-dev',
                              'libhdf5-103-1t64',
                              'libhdf5-cpp-103-1t64',
                              'libhdf5-hl-100t64',
                              'libhdf5-hl-cpp-100t64',
                              'libeigen3-dev', 'libpng-dev',
                              'python3', '2to3', 'python3-dev',
                              'ca-certificates', 'wget', 'git', 'tar',
                              'cmake', 'make'])

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
    preconfigure=[
        'git config --global --add safe.directory /var/tmp/EXP',
        'git config --global --add safe.directory /var/tmp/EXP/extern/HighFive',
        'git config --global --add safe.directory /var/tmp/EXP/extern/pybind11',
        'git config --global --add safe.directory /var/tmp/EXP/extern/yaml-cpp',
        'git config --global --add safe.directory /var/tmp/EXP/extern/HighFive/deps/catch2'
    ],
    prefix='/usr/local/EXP',
    runtime_environment={
        'LD_LIBRARY_PATH': '/usr/local/EXP/lib',
        'LIBRARY_PATH': '/usr/local/EXP/lib',
        'PATH': '/usr/local/EXP/bin:${PATH}'},
    repository='https://github.com/EXP-code/EXP.git',
    repository_submodules=True,
    branch=BRANCH
)

################
# Runtime image
################

Stage1 += baseimage(image=runtime_image)

Stage1 += Stage0.runtime(_from='devel')

Stage1 += compiler

Stage1 += apt_get(ospackages=['libpython3.12-dev', 'libopenmpi-dev',
                              'openmpi-bin', 'less', 'libfftw3-dev',
                              'libhdf5-dev', 'libhdf5-103-1t64',
                              'libhdf5-cpp-103-1t64',
                              'libhdf5-hl-100t64',
                              'libhdf5-hl-cpp-100t64', 'ffmpeg',
                              'nano', 'libgsl-dev', 'libeigen3-dev',
                              'python3', '2to3',
                              'python3.12-dev', 'python3-setuptools',
                              'python3-distlib',
                              'python3-distutils-extra',
                              'python3.12-venv', 'python3-pip',
                              'python3-wheel', 'python3-pip-whl',
                              'libvtk9-dev', 'dvipng', 'unzip',
                              'make', 'busybox', 'git', 'rsync', 'wget'])

# Install EXP into the runtime image
#
Stage1 += copy(_from='devel',
               src='/usr/local/EXP/bin', dest='/usr/local/EXP/bin')
Stage1 += copy(_from='devel',
               src='/usr/local/EXP/lib', dest='/usr/local/EXP/lib')
Stage1 += copy(_from='devel',
                src='/usr/local/EXP/include', dest='/usr/local/EXP/include')

# Copy documentation from GitHub Pages
#
Stage1 += shell(commands=['mkdir -p /var/www/html', 'cd /var/www/html', 'wget -r -nH --cut-dirs=1 https://exp-code.github.io/EXP-docs/'])

# Add Python venv (needed for Ubuntu 24.04)
#
Stage1 += shell(commands=['python3 -m venv /opt/venv', '. /opt/venv/bin/activate'])

# Add Python and EXP to the path and library paths
#
Stage1 += environment(variables={'PATH': '/opt/venv/bin:/usr/local/EXP/bin:$PATH'})
Stage1 += environment(variables={'LIBRARY_PATH': '/usr/local/EXP/lib'})
Stage1 += environment(variables={'LD_LIBRARY_PATH': '/usr/local/EXP/lib'})
Stage1 += environment(variables={'PYTHONPATH': '/opt/venv/lib/python3.12/site-packages:/usr/local/EXP/lib/python3.12/site-packages'})

# Remove ubuntu user from the container (needed for Ubuntu 24.04)
#
Stage1 += shell(commands=['userdel -f ubuntu', 'rm -rf /home/ubuntu'])

# Some packages needed or useful for running pyEXP
#
Stage1 += pip(packages=['numpy', 'scipy', 'matplotlib', 'jupyter', 'h5py', 'mpi4py', 'PyYAML', 'pandas', 'astropy', 'galpy', 'pynbody', 'jupyterlab', 'jupyterlab_widgets', 'ipywidgets', 'k3d==2.16.1', 'jupyterhub', 'ipyparallel'], pip='/opt/venv/bin/pip3', ospackages=['python3-pip', 'python3-setuptools', 'python3-wheel', 'python3-pip-whl'])

# Work around to install AGAMA
#
Stage1 += shell(commands=['pip3 install --config-settings --build-option=--yes --no-build-isolation agama'])

# Build Gala with EXP support
#
Stage1 += shell(commands=['cd /usr/local', 'export GIT_SSL_NO_VERIFY=1', 'git clone https://github.com/adrn/gala.git', 'cd gala', 'export GALA_EXP_PREFIX=/usr/local/EXP/', 'python3 -m pip install -ve .'])

# Add EXP examples to /usr/local
#
Stage1 += shell(commands=['cd /usr/local',  'export GIT_SSL_NO_VERIFY=1', 'git clone https://github.com/EXP-code/EXP-examples EXP-examples', 'git clone https://github.com/EXP-code/pyEXP-examples pyEXP-examples', 'git clone https://github.com/EXP-code/EXP-tools'])

# Make data directories world read/write
#
Stage1 += shell(commands=['chmod -R 777 /opt/venv', 'chmod -R 777 /usr/local/pyEXP-examples', 'chmod -R 777 /usr/local/EXP-examples', 'chmod -R 777 /usr/local/EXP-tools'])
