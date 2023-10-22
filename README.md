# EXP-apptainer
Recipes for creating Apptainer/Singularity containers for EXP

## Organization

Each directory describes a _flavor_ for the container image.

| Directory    | Contents |
| ---          | ---      |
| Ubuntu       | Scripts to create a cpu and a cpu+gpu SIF image           |
| Ubuntu/focal | A definition file that works with 20.04 packages          |
| Ubuntu/jammy | A definition file that works with 22.04 packages          |
| HPCCM        | HPC Container Maker recipe for building EXP *inside* of a container image |

## Notes

- For all of these recipes, we recommend that you match the container
  version of MPI and Cuda to the host versions.  For example, we have
  found that even differences in the micro versions for OpenMPI can
  lead to problems.

- EXP has automatic slurm support built in, but this is not always
  successful from inside the container.  There is no significantly
  loss of functionality by disabling this in CMake using
  `-DENABLE_SLURM=OFF`.
  