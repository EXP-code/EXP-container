# EXP-container

Recipes for creating [Docker](https://www.docker.com/) and [Apptainer](https://apptainer.org/)/[Singularity](https://docs.sylabs.io/guides/3.5/user-guide/index.html) containers for
EXP. Containers package code with its dependencies such that the code 
can easily be run anywhere. We provide examples for three strategies:

1. *Docker* - A Docker image with Jupyter and friends for pyEXP and
   EXP simulations is available on Docker Hub! Note that this container
   is designed to be run on a workstation or laptop -- _not_ a cluster.
   We also provide an HPCCM recipe and a Dockerfile for new builds.
2. *Binder* - A BinderHub compatible with all you need to run EXP and
   other widely used astronomy packages
3. *Native* - EXP is built from source on the host and installed in
   the container
4. *HPCCM* - EXP is built inside of the container using NVidia HPC
   Container Maker

These recipes are still _experimental_.  Please help us make these
better by posting issues on the GitHub repository and contributing
improvements through PRs.

## TL;DR Docker quick start

If your main interest is running the Docker container, download the
[expbox](/Docker/expbox) script, make the script executable, and put
it in your path as usual.  The script will retrieve the latest EXP
docker image, build a docker container, and run Jupyter or start an
interactive shell.  Please take a quick look at our [Docker
README](/Docker/README.md) for more details.

> [!NOTE] 
> This repository supports a Github Action to build the Docker images
> automatically from the `Dockerfile` in the `Docker` directory of this
> repository. The recipes here allow you to customize the container
> image.


## Organization

| Directory    | Contents |
| ---          | ---      |
| Docker       | Recipe for building a docker image containing EXP, Jupyter, and standard Python packages |
| Binder       | A Dockerfile that will work with BinderHub to automatically build and run EXP, JupyterLab, JupyterHub, and standard Python packages |
| Native       | Apptainer definition files for various flavors |
| HPCCM        | HPC Container Maker recipe for building EXP *inside* of a container image |

## Notes

- For Apptainer, we recommend that you match the container version of
  MPI and Cuda to the host versions.  For example, we have found that
  even differences in the micro versions for OpenMPI can lead to
  problems.

- EXP uses Slurm to detect remaining wall-clock time and terminate
  smoothly before exceeding the allocated time limit.  However, system
  slurm access is not always successful from inside the container.
  There is no significant loss of functionality by disabling this in
  CMake using `-DENABLE_SLURM=OFF` in the Apptainer definition file.

- All examples have been built in the Ubuntu environment.  However we
  successfully run an Ubuntu 24.04 container on a CentOS8-based
  cluster.  Please consider contributing back any successful variants
  for other Linux distributions

- The pyEXP build in the Apptainer container has been successfully
  tested with `mpi4py`, `numpy` and `matplotlib`.  `Astropy` has been
  included but not tested.
  
- The Docker container includes an internal MPI installation without
  Cuda and many more Python packages preinstalled, including:
  `jupyterlab`, `matplotlib`, `numpy`, `scipy`, `pandas`, `mpi4py`,
  `h5py`, `pyYAML`, `astropy`, `galpy`, `k3d` and `ipyparallel`.
