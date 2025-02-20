# Using EXP with BinderHub

This directory provides `Dockerfile` compatible with BinderHub for
EXP.

> [!Note]__
> TL;DR: All you need is to drop this `Dockerfile` in a directory
> that is part of the BinderHub repository and it will build.


## Directory contents

| File              | Contents |
| ---               | ---      |
| Dockerfile        | A Dockerfile to build the Ubuntu 24.04 image with all the packages needed to run EXP in a Binder
| README.md         | This document |


## Tips and hints
- Like all `BinderHub` instances, the user is `jovyan` by default.
- All Python packages are installed in a Python 3.12 virtual
environment located in `/opt/venv` and is owned by `jovyan`
- You may use `pip install` in a Jupyter cell or terminal to install
additional packages as needed.
- You can explore the Docker image by building it locally with
`docker build` command in a local directory containing the Dockerfile:
```bash
docker build -t binder-test .
```
