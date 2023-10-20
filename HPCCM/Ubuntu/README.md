# Notes on these scripts

Ideally, one would use the `generic_cmake` building block to generate
EXP from the github repository.  Unfortunatly, this requires a direct
URL to the github repository, which will not work until the repository
is public.

The work around is to git clone the repository locally, run git
subversion, and then tar up the top level directory for unpacking into
the container.

## Files

| Script                    | Description |
| ---                       | ---         |
| exp-gnu-openmpi.py        | Create the cpu+gpu SIF image for 22.04 |
| exp-gnu-openmpi-public.py | Create the cpu+gpu SIF image for 22.04 for public EXP repo|
| Singularity.def           | Sample definition file |

