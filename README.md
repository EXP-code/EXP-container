# EXP-apptainer
Recipes for creating Apptainer/Singularity containers for EXP

## Organization

Each directory describes a _flavor_ for the container image.

| Directory    | Contents |
| ---          | ---      |
| Ubuntu       | Scripts to create a cpu and a cpu+gpu image
| Ubuntu/focal | A definition file that works with 20.04 packages
| Ubuntu/jammy | A definition file that works with 20.04 packages

Currently, we only have Ubuntu/jammy and Ubuntu/focal.  But these can
be easily adapted and modified for your needs.  Please contribute your
recipes for other OS containers to help out others.

## Usage notes

The image has `exp` as its run executable.  This allows you to run EXP from OpenMPI.  For example, suppose that you want to run the `DiskHaloA` example from `EXP-examples`.  Assume that this directory is `/data/DiskHaloA`.  Then you can launch EXP wit the command:
```
mpirun apptainer run --bind /data --home /data/DiskHaloA /path/to/EXP.sif
```

Before doing this, you will need to modify `config.yml` as follows:
- Change the `ldlibdir` option to `/usr/local/lib/user`
- Change the `outdir` option to `/data/DiskHaloA`

## Some notes on the build scripts

1. Change your CMake install directory to point to a staging directory.  In the scripts, I use `/home/weinberg/stage`.  You can change this to suit yourself, of course.
2. Every file in the staging directory will be copied to `/usr/local` in the container.
3. You can copy or link other files into the `/usr/local` in the container to suite your specific needs.
4. EXP depends on a few libraries for CUDA and HDF5 support.  The script copies them directly rather than loading the full package set for each of these.  You may need to tweak this when porting to a new OS version.
5. These scripts assume Apptainer.  If you are using SingularityCE, change the final command from `apptainer` to `singularity`.
6. Also, in that final command, change `jammy` to `focal`, if you want 20.04 rather than 22.04.
7. The script is intended to be run from the OS-specific directory; in this case `Ubuntu`.
