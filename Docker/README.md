# Docker

We use the HPC Container Maker to generate a Dockerfile from the
Python recipe.  This container is designed to be run on a workstation
or laptop, rather than a cluster. Rather than custom build HPC
libraries for a particular version of OpenMPI and Cuda, we build the
Docker container using a standard Ubuntu image and repository support
packages.

You will need Docker installed on your workstation or laptop. See
installation hints below. I prefer the community edition of Docker but
the Docker Desktop is available for Linux, Mac OS X, and Windows. The
Desktop is the preferred path for Windows. Note: the Docker container
_should_ work for Windows but it is not currently tested.

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
`exp`. Try `expbox -h` to see the available options.

This script will automatically download a prebuilt Docker image from
the Docker Hub and start the container.  Then you should be up and
running.

### Mac OS X

You will first need to install docker, if you don't have it
already. For Mac OS X, there are two main alternatives: using
Homebrew or the Docker Desktop app from Docker.com. 

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

For Ubuntu, you can use the docker.com PPA as follows. First, 

First, update your existing list of packages and install a few prerequisites
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

## Building a docker image

Both a Dockerfile and a an HPCCM recipe for making that Dockerfile is
provided here.

See the hints at the top of the Dockerfile for the build commands.
There are two steps:
1. Create a build directory and put a tar file of the git cloned EXP
source into the build directory as `EXP.tar.gz`. Please make sure that
you selected the desired branch in git (or use the default `main`) and
have updated the submodules using `git submodule update --init
--recursive`. 
2. Build the Docker image using the Dockerfile. TL;DR:
```
docker build --tag exp .
```
But please see the top of the Dockerfile for explicit build commands.

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
