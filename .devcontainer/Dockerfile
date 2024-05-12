ARG PYTHON_VERSION=3.11
FROM mcr.microsoft.com/devcontainers/python:${PYTHON_VERSION}

# update base
RUN apt-get update -y -qq
RUN apt-get dist-upgrade -y -qq
RUN apt-get autoremove -y -qq

# install pipx
RUN pip install --upgrade pip
RUN pip install pipx
RUN pipx ensurepath
RUN pipx install poetry flake8 pytest pylint
