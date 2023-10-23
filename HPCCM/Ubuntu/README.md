# HPCCM recipes

## Notes

Because EXP is pre-release and is not public, you will need to:
1. `git clone` the repository from github into a local directory called
   `EXP` 
2. `cd EXP` and run `git submodule update --init --recursive`
3. Tar up the top level directory for EXP to `EXP.tar.gz`
4. Then, specify the full path for resulting tar ball to
   the `package` option in `generic_cmake()` command in the recipe file.
When EXP becomes public (soon!), we will be able to use the more
convenient `repository` option instead.

The 'shell' recipe uses primitive shell commands rather than the more
portable `generic_cmake()` recipe.  This is a bit of a hack, but it
works and may be a useful starting point for sitauations that require
a more flexible recipe.

## Contents

| Script                    | Description                                 |
| ---                       | ---                                         |
| exp-gnu-openmpi.py        | Create the cpu+gpu SIF image for 22.04      |
| exp-gnu-openmpi-shell.py  | As above but using shell commands for cmake |
| Singularity.def           | Sample definition file produced by `hpccm`  |

