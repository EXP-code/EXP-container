# EXP-apptainer

Recipes for creating Apptainer/Singularity containers for EXP.  We
provide examples for two strategies:
1. *Native* - EXP is built from source on the host and installed in
   the container
2. *HPCCM* - EXP is built inside of the containr using NVidia HPC
   Container Maker

## Organization

| Directory    | Contents |
| ---          | ---      |
| Native       | Apptainer definition files for various flavors |
| HPCCM        | HPC Container Maker recipe for building EXP *inside* of a container image |

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