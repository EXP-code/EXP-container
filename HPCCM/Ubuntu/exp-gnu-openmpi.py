"""Image for building EXP with MPI and CUDA based on the hpcbase recipe
   and our standard Ubuntu 22.04 development environment.

Contents:

  * CUDA version 11.7
  * FFTW version 3.3.8
  * GNU compilers (upstream)
  * HDF5 version 1.10.10
  * OpenMPI version 4.1.3 with PMIX, PMI2, and Infiniband support
  * Python 2 and 3 (upstream)
  * CMake (upstream)
  * Ubuntu 22.04 (if you want another image, you will need to update
    this configuration for the dependent packages.  Please add the appropriate
    usearg switches and contribute this back to the EXP repo, if you would.)
  * Ubuntu packages: libeigen3-dev libslurm37 libslurm-dev wget git tar

Build notes:

  * The container build requires the following commands:
    $ hpccm --cpu-target x86_64 --working-directory /src --recipe exp-gnu-openmpi.py --singularity-version=3.2 --format singularity > Singularity.def
    $ sudo apptainer build EXP.sif Singularity.def

  * You will need ensure that your environment has github access to
    the EXP repository.  I do this by 'sudo -i' and added an ssh-agent
    to shell.

"""

# Choose between either Ubuntu 22.04 (default) or CentOS 7
#
# This is just an example of how this might be done for future
# reference.  The full dependency list is for CentOS needs to be
# specified and the package specification switched in by another
# USERARG statement.
#
# Add '--userarg centos=true' to the command line to select CentOS

devel_image = 'nvcr.io/nvidia/cuda:11.7.1-devel-ubuntu22.04'
runtime_image = 'nvcr.io/nvidia/cuda:11.7.1-runtime-ubuntu22.04'
if USERARG.get('centos', False):
    devel_image = 'nvcr.io/nvidia/cuda:11.7-devel-centos7'
    runtime_image = 'nvcr.io/nvidia/cuda:11.7-runtime-centos7'

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

# Open Fabrics
Stage0 += mlnx_ofed()

# PMIX & PMI2
Stage0 += pmix(toolchain=compiler.toolchain,
               ospackages=['libhwloc-dev', 'libev-libevent-dev'])

Stage0 += slurm_pmi2(toolchain=compiler.toolchain)

# OpenMPI
Stage0 += openmpi(version='4.1.6', 
                  pmix=True, pmi='/usr/local/slurm-pmi2', 
                  ospackages=['file', 'hwloc', 'libslurm-dev'],
                  with_slurm=True,
                  infiniband=True,
                  cuda=True,
                  toolchain=compiler.toolchain)

# FFTW
Stage0 += fftw(version='3.3.8', mpi=True, toolchain=compiler.toolchain)

# HDF5
Stage0 += hdf5(version='1.10.10', toolchain=compiler.toolchain)

# CMake
Stage0 += cmake(eula=True)

# Get additional packages
Stage0 += apt_get(ospackages=['libeigen3-dev', 'libpng-dev',
                              'libvtk7-dev', 'python3-dev', 'wget',
                              'git', 'tar'])

# When the repository is public, we should be able to use the cmake
# recipe below after adjusting the url.  Note: this has not been
# tested.

# Create a build directory and configure EXP.  The options below
# should give you all that you need for most cases. Add additional
# CMake options as needed.
#
Stage0 += generic_cmake(
    cmake_opts=['-D CMAKE_BUILD_TYPE=Release',
                '-D CUDA_USE_STATIC_CUDA_RUNTIME=off',
                '-D ENABLE_CUDA=YES',
                '-D ENABLE_USER=YES',
                '-D ENABLE_DSMC=YES',
                '-D ENABLE_SLURM=NO',
                '-D ENABLE_PNG=NO',
                '-D ENABLE_VTK=NO',
                '-D Eigen3_DIR=/usr/share/eigen3/cmake',
                '-D FFTW_ROOT=/usr/local/fftw',
                '-D CMAKE_INSTALL_PREFIX=/usr/local/EXP'],
    preconfigure=['git submodule update --init --recursive', 
                  'git config --global --add safe.directory /src/EXP'],
    prefix='/usr/local/EXP',
    build_environment={'CUDAARCHS': '"61;62;70;72;75"'},
    runtime_environment={
        'LD_LIBRARY_PATH': '/usr/local/EXP/lib:${LD_LIBRARY_PATH}',
        'LIBRARY_PATH': '/usr/local/EXP/lib:${LIBRARY_PATH}',
        'PATH': '/usr/local/EXP/bin:${PATH}'},
    repository='https://github.com/EXP-code/EXP.git'
)

################
# Runtime image
################

Stage1 += baseimage(image=runtime_image)

Stage1 += Stage0.runtime(_from='devel')

Stage1 += compiler

Stage1 += apt_get(ospackages=['libpython3.10-dev', 'openmpi-bin', 'less', 'wget', 'git'])

# Install EXP into the runtime image
#
Stage1 += copy(_from='devel',
               src='/usr/local/EXP/bin', dest='/usr/local/EXP/bin')
Stage1 += copy(_from='devel',
               src='/usr/local/EXP/lib', dest='/usr/local/EXP/lib')

# Add EXP to the path and library paths
#
Stage1 += environment(variables={'PATH': '/usr/local/EXP/bin:$PATH'})
Stage1 += environment(variables={'LIBRARY_PATH': '/usr/local/EXP/lib:$LIBRARY_PATH'})
Stage1 += environment(variables={'LD_LIBRARY_PATH': '/usr/local/EXP/lib:$LD_LIBRARY_PATH'})

# Some packages needed or useful for running pyEXP
#
Stage1 += environment(variables={'PYTHONPATH': '/usr/local/EXP/lib/python3.10/site-packages:${PYTHONPATH}'})
Stage1 += pip(packages=['numpy', 'astropy', 'gala', 'galpy', 'pynbody', 'pandas', 'matplotlib', 'mpi4py', 'PyYAML'], pip='pip3', upgrade=True, ospackages=['python3-pip', 'python3-setuptools', 'python3-wheel', 'python3-pip-whl'])
