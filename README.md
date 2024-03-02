# EXP-container

Recipes for creating Apptainer/Singularity and Docker containers for
EXP.  We provide examples for three strategies:
1. *Native* - EXP is built from source on the host and installed in
   the container
2. *HPCCM* - EXP is built inside of the container using NVidia HPC
   Container Maker
3. *Docker* - A docker image is built using EXP. We provide an HPCCM
   recipe for the Dockerfile.

These recipes are still _experimental_.  Please help us make these
better by posting issues on the GitHub repository and contributing
improvements through PRs.

## Quick start

If your main interest is running the Docker container, please take a
quick look at [Docker](/Docker/README.md) and grab and run the
[expbox](/Docker/expbox) script. The script will download the latest
EXP docker image, build a docker container, and run Jupyter or start
an interactive shell.

## Organization

| Directory    | Contents |
| ---          | ---      |
| Native       | Apptainer definition files for various flavors |
| HPCCM        | HPC Container Maker recipe for building EXP *inside* of a container image |
| Docker       | Recipe for building a docker image containing EXP, Jupyter, and standard Python packages |

## Notes

- For all of these recipes, we recommend that you match the container
  version of MPI and Cuda to the host versions.  For example, we have
  found that even differences in the micro versions for OpenMPI can
  lead to problems.

- EXP uses Slurm to detect remaining wall-clock time and terminate
  smoothly before exceeding the allocated time limit.  However, system
  slurm access is not always successful from inside the container.
  There is no significantly loss of functionality by disabling this in
  CMake using `-DENABLE_SLURM=OFF`.

- All examples have been built in the Ubuntu environment.  However we
  successfully run an Ubuntu 22.04 container on a CentOS8-based
  cluster.  Please consider contributing back any successful variants
  for other Linux distributions

- The pyEXP build in the HPCCM container has been successfully tested
  with `mpi4py`, `numpy` and `matplotlib`.  `Astropy` has been
  included but not tested.
  
- The docker container includes an internal MPI installation without
  Cuda.
