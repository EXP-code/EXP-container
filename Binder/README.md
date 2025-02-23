# Using EXP with BinderHub

This directory provides `Dockerfile` compatible with BinderHub for
EXP.

> [!NOTE]  
> TL;DR: Drop this `Dockerfile` in a directory identified to BinderHub
> as a repository and it will pull in everything it needs from github
> and build!


## Directory contents

| File              | Contents |
| ---               | ---      |
| Dockerfile        | A Dockerfile to build the Ubuntu 24.04 image with all the packages needed to run EXP in a Binder
| README.md         | This document |


## Tips and hints
- Like all `BinderHub` instances, the user is `jovyan` by default
- All Python packages are installed in a Python 3.12 virtual
environment located in `/opt/venv` which is owned by `jovyan`
- This allows you to use `pip install` in a Jupyter cell or terminal to install
additional packages as needed
- If your BinderHub server allows multiple cores, you will be able to
  use MPI and multi-threading automatically
- You can explore (and use!) the same Docker image by building it locally with
  `docker build` command in a local directory containing the Dockerfile:
  ```bash
  docker build -t binder-test .
  ```
  For example, you can launch a Jupyter Notebook server from the
  locally-built `binder-test` image at port 8901 with the following command:
  ``` bash
  docker run -it --rm -p 8901:8901 binder-test jupyter notebook --NotebookApp.default_url=/lab/ --ip=0.0.0.0 --port=8901

  ```
