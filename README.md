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