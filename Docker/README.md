# Docker

We provide premade Docker containers for Jupyter notebooks and Jupyter
lab, hosted by the Docker Hub. No building necessary.  All you need is
the [expbox](/Docker/expbox) script from this directory and `docker`.

If you do not have `docker` installed on your workstation or laptop,
you will need to do that first. See the [Installing
Docker](#Installing-Docker) section below. We recommend the community
edition of Docker but the Docker Desktop is available for Linux, Mac
OS X, and Windows. One the Desktop is installed, you will also have
the command-line interface needed by the script or for manually
running the container.  The Desktop version is the preferred
installation for Windows.

The EXP images on Docker Hub are labeled by a short git commit hash.
In addition, the latest build is tagged either `24`, `22` for the
latest `main` branch builds, `devel` for a development branch build,
or perhaps a custom tag for a particular bug fix or feature.  You will
automatically get the latest build of the `24` image the first time
you run the `expbox` script. After that first download, your Docker
image *will not* be automatically updated from the Hub.  To retrieve
an updated image, run the command

```
docker pull the9cat/exp:tag
```

to get the the image with a specific `tag` value.  For example:

```
docker pull the9cat/exp:24
```

to get the most recent build of the 24.04 image.

This container is designed to be run on a workstation or laptop,
rather than a cluster.  Rather than custom build HPC libraries for a
particular version of OpenMPI and Cuda, we build the Docker container
using a standard Ubuntu image and repository support packages.  For
those of you that want to make your own Docker image, please see
[Building a Docker image](#Building-a-Docker-image) below.  We use the
[HPC Container Maker](https://github.com/NVIDIA/hpc-container-maker)
to generate a Dockerfile from the Python recipe. We also supply the
Dockerfile that we used to make the Docker Hub image for EXP.

> [!NOTE]
> If you are having trouble getting the container to work, please update
> your Docker image using the command
> ```
> docker pull the9cat/exp:24
> ```
> and download the [latest version](https://github.com/EXP-code/EXP-container/blob/main/Docker/expbox)
> of `expbox` and try again.  If that doesn't help, please document your problem in the EXP-container
> [Issues](https://github.com/EXP-code/EXP-container/issues) tab. If the container works but the code
> is not performing as expected, please document your problem at
> at EXP [Issues](https://github.com/EXP-code/issues).

> [!NOTE]  
> The originally published EXP Docker image uses a Ubuntu 22.04
> base. This OS version deprecates system-wide `pip install`, but it
> is allowed and used to provide Python support. The latest stable
> Ubuntu release, 24.04, disallows it altogether. Recent images are
> built with 24.04 using global `venv` as recommended by Canonical.

> [!NOTE]
> If you are having trouble with `pip install` in your Docker container, try these first:
> - Update your `expbox` script to the
>   [latest version](https://github.com/EXP-code/EXP-container/blob/main/Docker/expbox)
> - Make sure that your path has `/opt/venv/bin` before any other
>   system path to ensure that it runs `/opt/venv/bin/pip`

> [!NOTE]  
> The previous EXP Docker images tagged with `latest` are now
> linked to the `24` image. Images with the 22.04 release are still available
> in DockerHub, tagged as `22` but are not being updated. Please grab
> the latest version of `expbox`
> [here](https://github.com/EXP-code/EXP-container/blob/main/Docker/expbox)
> to automatically get the latest image.

## Directory contents

| File              | Contents |
| ---               | ---      |
| expbox            | The most recent Bash script for getting and running the EXP Docker image |
| exp_all_deb.py    | HPC Container Maker recipe for building EXP *inside* of a container image using the Ubuntu 24.04 image |
| exp_all_deb_22.py | The deprecated HPC Container Maker recipe that uses system-wide pip installs |
| Dockerfile        | A Dockerfile to build the Ubuntu 24.04 produced by HPCCM, included for completeness |
| Dockerfile22      | A Dockerfile for the deprecated build, included for completeness |
| README.md         | This document |


## Usage

### Using the Docker image

If you do not have Docker installed on your workstation or laptop, see
the two sections below for brief instructions on how to install Docker
for Mac OS X and Linux. Alternatively, and recommended: use your
favorite search engine to find detailed Docker installation
instructions for your system.

This directory contains a Bash script called [expbox](/Docker/expbox)
that runs a Docker container to either (1) start Jupyter Notebook or
Jupyter Lab; or (2) start an interactive terminal session that maybe
be used to run `exp`. Try `expbox -h` to see the available options.
This script will automatically download a prebuilt Docker image from
the Docker Hub and start the container.  Then you should be up and
running.

The container includes the EXP _ReadTheDocs_ online documentation at
`http://localhost:8080` or, equivalently, `http://127.0.0.1:8080`.
The script automatically starts the web server on launch.  If port
8080 is not available on your system, the script will use the `lsof`
to identify an used port. This requires `sudo`.  Alternatively, you may 
choose your own port # using the `-P <port>` flag.

### Tips and hints for running EXP in Docker

- The `expbox` script with no options will start a Jupyter Notebook in
  your home directory using the first available open networking port
  beginning with 8888.  This requires `sudo`.  Alternatively, you can use
  the `-p <port>` option to specify a preferred port. To start the
  notebook in a different directory, add
  `-d <path_to_directory_here>`.
- The container name will be `expbox_<port>`. You can change the
  prefix name using the `-n <name>` option.
- The script attempts to find an unused port. If `docker` has an old
  stopped container with an inactive port, this strategy may result in
  the same assigned name.  When this happens, simply remove the
  container using the `docker rm -f expbox_<port>` command and try again.
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
- The `agama` package is also pre-installed in the latest 24.04 image.
- The `expbox` script runs in the same user account that launched
  it. This may result in your host shell profile being sourced.
- All additional Python packages are installed in a virtual
  environment located in `/opt/venv`. The current `expbox` launching
  script gives the user ownership of this directory.
- Additional packages can be installed by `pip install <package>`
  either manually or from a Jupyter cell using the `!pip install`
  command.   Your path will include `/opt/venv/bin/` by
  default. However, if your host-side shell profile is sourced, you
  may need to manually prepend `/opt/venv/bin/` to your path or source
  `/opt/venv/bin/activate` to do this.

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
package. By following the install instructions on the Docker website,
you will get both a Docker Desktop GUI and the command line interface

### Linux

Most distributions package the community edition of Docker. So check
your distribution for details. 

#### Ubuntu

Docker *is* in the main repository so a simple:

```
sudp apt install docker.io
```

is enough to get you going.  You will also want to add your user name to
the docker group:

```
sudo adduser <user> docker
```

to allow docker commands to be run *without* sudo.

There are installation alternatives to Canonical's repository.
Docker.com provides a Docker Desktop package. Also, you can use the
docker.com PPA for the latest, greatest community edition as follows.
First, update your existing list of packages and install a few
prerequisites which you probably already have:

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

### Windows
#### Docker Setup
1. Check whether you have Windows System Linux (WSL) installed on your computer. If you do, check that Ubuntu is installed and/or you can run bash commands. (You can check this by running `bash -v` and making sure you don’t get an error). If that works, skip to Step 4.

2. If you don’t have WSL with a working Linux installation, you need to install WSL. To do this, open a Command Prompt and run: 	
   ```  
   wsl --install
   ```
   **Note:** By default, this installs WSL2 and Ubuntu, but you can customize that with the instructions [here](https://learn.microsoft.com/en-us/windows/wsl/install).

3. Once WSL is installed, it will prompt you to set a username and password for your WSL Linux “machine.”

4. Now, install Docker Desktop from the following link: https://www.docker.com/products/docker-desktop/

   **Note:** When you open up the Desktop app, it will prompt you to make a Docker account. When starting Docker Desktop, it will ask you to sign in with your account. You can choose to skip this. If you do make an account, occasionally, even after you sign in, it will stay on the sign-in screen. Click the skip button, and it should show that you are signed in.

5. Install the Windows Terminal program either from the Microsoft Store or via this [link](https://apps.microsoft.com/detail/9n0dx20hk701?rtc=1&hl=en-us&gl=US).

6. Open up the Windows Terminal and use the down arrow along the top bar of the window to open an Ubuntu terminal (or use the shortcut Ctrl+Shift+5).

7. Now you need to add your username to the docker group. To do so, run the following command: 
   ```
   sudo usermod -a -G docker $USER
   ```

8. You will need to enter your Ubuntu password. 

9. Check that your username was added to the docker group by running
     ```   
     grep docker /etc/group
     ```

10. You should get something like `docker:x:1001:username`, though the number may be different.
11. Run the following command so that when you log in you will always be part of the `docker` group:
     ```
     newgrp docker 
     ```    

12. Logout of the terminal tab with `logout` and open up a new Ubuntu terminal.

#### EXP Container Setup
1. Download the expbox container script from https://github.com/EXP-code/EXP-container/blob/main/Docker/expbox and put it in the desired folder you want it to live in (e.g., your working directory for EXP stuff). If you want to put it in part of the WSL/Ubuntu area, you can follow the instructions on how to access it [here](https://www.howtogeek.com/426749/how-to-access-your-linux-wsl-files-in-windows-10/).

2. Now, we need to get the EXP image. In an Ubuntu terminal, pull the most updated image with the command: 
     ```
     docker pull the9cat/exp
     ```    
   Navigate to where you placed your expbox script. If you placed it in the WSL file area, you can navigate to it like you are using a Linux machine. More likely, though, you put it somewhere on your C: drive. You can navigate there via:
     ```   
     cd /mnt/c/Users/username/path/to/directory/with/expbox/script
     ```     

3. Make sure your Docker Desktop is running in the background. We can now run the expbox script.

   If your script is in your **WSL folders**, you can execute it with 
     ```
      ./expbox
     ```
   If your script is on your **C: drive**, you will need to specify your working directory, otherwise the script will default to your Ubuntu home directory (even if you navigated to where your expbox folder is). You can do so with the `-d` flag, i.e.,

     ```
     ./expbox -d /mnt/c/Users/username/path/to/working/directory
     ```      

   You can see other flags for customization by calling `/.expbox -h`

4. Your terminal tab will give you links to access the Jupyter server. You can copy and paste them into your browser, or open them directly from the terminal window by holding down Ctrl and clicking on one of the links.



## Building your own Docker image locally

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

## Building a new Docker Hub image

All collaboration members with read/write access to the repository can
trigger and run the workflow to build a new Docker image. Go to the
`Actions` tab in the repository and select the `Build Docker images on
native runners` workflow from the left-hand menu. Click on the `Run
workflow` button at the top of the build history panel and enter the
`exp` branch name and desired `tag` for the new image build. The
default values are `main` for the current stable branch with `24`.
For custom branches and tags, don't forget that you will need to
specify the custom `tag` to the [expbox](/Docker/expbox) script.

If you do not have read/write access to the repository and need a
Docker image for particular version of `exp`, please request this by
starting at `Github issue` in the EXP repo.
