# Docker

We provide a premade Docker container for Jupyter notebooks and
Jupyter lab, hosted by the Docker Hub. No building necessary.  All you
need is the `expbox` script from this directory and `docker`.

If you do not have `docker` installed on your workstation or laptop,
you will need to do that first. See the [Installing
Docker](#Installing_Docker) section below. We recommend the community
edition of Docker but the Docker Desktop is available for Linux, Mac
OS X, and Windows. One the desktop is installed, you will also have
the command-line interface needed by the script or for manually
running the container.  The Desktop version is the preferred
installation for Windows. Note: the EXP Docker container _should_ work
for Windows using WSL but it is not currently tested.

This container is designed to be run on a workstation or laptop,
rather than a cluster.  Rather than custom build HPC libraries for a
particular version of OpenMPI and Cuda, we build the Docker container
using a standard Ubuntu image and repository support packages.  For
those of you that want to make your own Docker image, please see
[Building a Docker image](#Building-a-Docker-image) below.  We use the
[HPC Container Maker](https://github.com/NVIDIA/hpc-container-maker)
to generate a Dockerfile from the Python recipe. We also supply the
Dockerfile that we used to make the Docker Hub image for EXP.

## Usage

### Using the Docker image

If you do not have Docker installed on your workstation or laptop, see
the two sections below for brief instructions on how to install Docker
for Mac OS X and Linux. Alternatively, and recommended: use your
favorite search engine to find detailed Docker installation
instructions for your system.

This directory contains a Bash script called `expbox` that runs a
Docker container to either (1) start Jupyter Notebook or Jupyter Lab;
or (2) start an interactive terminal session that maybe be used to run
`exp`. Try `expbox -h` to see the available options.  This script will
automatically download a prebuilt Docker image from the Docker Hub and
start the container.  Then you should be up and running.

### Tips and hints for running EXP in Docker

- The `expbox` script with no options will start a Jupyter Notebook in
  your home directory using the first available open networking port
  beginning with 8888. You can use the `-p <port>` option to specify a
  preferred port.
- The container name will be `expbox_<port>`. You can change the
  prefix name using the `-n <name>` option.
- The terminal session invoked with `-t` will give you a shell with
  user privileges and access to the EXP container. You can use this to
  run `exp` or any of the standalone routines that are part of the
  standard EXP build, such as initial condition generators and
  analysis routines in the EXP `utils` directory.  For example, you
  can use the session to start MPI simulations inside the
  container. This is a good way to experiment with and learn EXP by
  running the examples in the [EXP-examples
  repository](https://github.com/EXP-code/EXP-examples).
- You can use the `-l` option to start a Jupyter Lab session instead
  of Notebook.
- The container will be automatically stopped when you Control-C the
  Jupyter server or exit the terminal session. If you are done with
  your container, you can remove it by running `docker rm -f
  <container>`. List your current containers by running `docker ps`.
- The container contains the full EXP build including MPI and Python +
  Jupyter packages needed for pyEXP. Preinstalled Python packages
  include `jupyterlab`, `matplotlib`, `numpy`, `scipy`, `pandas`,
  `mpi4py`, `h5py`, `pyYAML`, `astropy`, `galpy`, `k3d` and
  `ipyparallel`.
- The `agama` package can be installed manually by starting a terminal
  in your running container, for example 

  ```
  docker exec -it expbox_8888 /bin/bash 
  ```

  if your container is named `expbox_8888`.  Then, execute `pip
  install agama` in the shell and answer the required interactive
  prompts.
- Additional packages can be installed by `pip install <package>`
  either manually or from a Jupyter cell using the `!pip install`
  command.

## Installing Docker

### Mac OS X

There are two main alternatives: using Homebrew or the Docker Desktop
app from Docker.com.

For Homebrew, you can try:

```
brew install --cask docker
```

See `https://docs.docker.com/desktop/install/mac-install/` for
instructions on how to install Docker for Mac OS X using a `.dmg`
package.

### Linux

Most distributions package the community edition of Docker. So check
your distribution for details. 

#### Ubuntu

Docker.com provides a Docker Desktop package. Alternatively, you can
use the docker.com PPA for the community edition as follows.  First,
update your existing list of packages and install a few prerequisites
which you probably already have:

```
sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common
```

Then add the GPG key for the official Docker repository to your system:

```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

Add the Docker repository to APT sources:

```
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

Finally, update your existing list of packages again for the addition
to be recognized and install:

```
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io
```

## Building a Docker image

Both a Dockerfile and an HPCCM recipe for making that Dockerfile is
provided here.

See the hints at the top of the Dockerfile for the build commands.
In short, there are two steps:

1. Create a build directory and put a tar file of the git cloned EXP
source into the build directory as `EXP.tar.gz`. Please make sure that
you selected the desired branch in git (or use the default `main`) and
have updated the submodules using `git submodule update --init
--recursive`. 

2. Build the Docker image using the Dockerfile. TL;DR:

```
docker build --tag exp .
```

The build commands used to make the images for the Docker Hub are in
the comments at top of the Dockerfile.

### Creating a new Dockerfile using HPCCM

If you want to generate a new Dockerfile using HPCCM, you will need to
install the HPC Container Maker (HPCCM) using `pip`
or `conda` as follows:

```
sudo pip install hpccm
```

or

```
conda install -c conda-forge hpccm
```

Then, create the Dockerfile by running

```
hpccm --recipe exp_all_deb.py --format docker > Dockerfile
```

