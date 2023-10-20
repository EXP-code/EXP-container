# HPCCM

HPC Container Maker generates Dockerfiles or Apptainer/Singularity
definition files from a high level Python recipe.

The goal here is to configure and build EXP inside the container,
including runtimes for EXP and pyEXP.  Note: this is a work in
progress.

## Usage

You will need to install the HPC Container Maker (HPCCM) using `pip`
or `conda` as follows:
- sudo pip install hpccm
- conda install -c conda-forge hpccm

Then run:
- hpccm --recipe exp-gnu-openmpi.py --singularity-version=3.2 --format singularity > Singularity.def
- sudo apptainer build EXP.sif Singularity.def

to make the container image.  You may need to adjust some of the
configuration details in the recipe file.  See the [HPCCM
documentation](https://github.com/NVIDIA/hpc-container-maker/blob/master/docs/getting_started.md)
for more details.

## Organization

Each directory describes a _flavor_ for the container image.

| Directory    | Contents |
| ---          | ---      |
| Ubuntu       | Scripts to create the cpu+gpu SIF image for 22.04

Please do contribute recipes for other flavors and platforms.
