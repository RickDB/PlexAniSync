FROM python:3.10 AS builder

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# install dependencies to the local user directory (eg. /root/.local)
RUN pip install --user --no-warn-script-location -r requirements.txt
