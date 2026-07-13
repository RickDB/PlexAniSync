ARG PYTHON_VERSION=3.13

FROM python:${PYTHON_VERSION}-trixie AS builder

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN python -m venv /venv
RUN /venv/bin/pip install --upgrade pip

# Build the venv as a separate stage so it's only rebuilt when requirements.txt changes
FROM builder AS build-venv
COPY Docker/PlexAniSync/pip.conf /etc/pip.conf
COPY requirements.txt .
RUN /venv/bin/pip install --disable-pip-version-check -r requirements.txt

FROM gcr.io/distroless/python3-debian13:latest

WORKDIR /plexanisync

# Only the venv's site-packages are needed; distroless's own python3 runs the
# code, with PYTHONPATH pointing at these installed dependencies.
ARG PYTHON_VERSION
COPY --from=build-venv /venv/lib/python${PYTHON_VERSION}/site-packages /venv/lib/python${PYTHON_VERSION}/site-packages
ENV PYTHONPATH=/venv/lib/python${PYTHON_VERSION}/site-packages

ENV PLEX_SECTION=Anime \
    PLEX_URL=http://127.0.0.1:32400 \
    PLEX_TOKEN='' \
    ANI_USERNAME='' \
    ANI_TOKEN='' \
    INTERVAL=3600

COPY PlexAniSync.py requirements.txt custom_mappings_schema.json Docker/PlexAniSync/run/. /plexanisync/
COPY plexanisync /plexanisync/plexanisync

LABEL org.opencontainers.image.documentation=https://github.com/RickDB/PlexAniSync/blob/master/Docker/PlexAniSync/README.md

CMD ["/plexanisync/runsync.py"]