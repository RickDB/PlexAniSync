FROM python:3.13-trixie AS builder

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/* && \
    # distroless keeps its python3 binary at /usr/bin/python; symlinking it here
    # to this image's /usr/local/bin/python before creating the venv means the
    # venv's interpreter symlink still resolves once /venv is copied there.
    ln -s /usr/local/bin/python /usr/bin/python

RUN /usr/bin/python -m venv /venv
RUN /venv/bin/pip install --upgrade pip

# Build the venv as a separate stage so it's only rebuilt when requirements.txt changes
FROM builder AS build-venv
COPY Docker/PlexAniSync/pip.conf /etc/pip.conf
COPY requirements.txt .
RUN /venv/bin/pip install --disable-pip-version-check -r requirements.txt

FROM gcr.io/distroless/python3-debian13:latest

WORKDIR /plexanisync

COPY --from=build-venv /venv /venv

ENV PLEX_SECTION=Anime \
    PLEX_URL=http://127.0.0.1:32400 \
    PLEX_TOKEN='' \
    ANI_USERNAME='' \
    ANI_TOKEN='' \
    INTERVAL=3600

COPY PlexAniSync.py requirements.txt custom_mappings_schema.json Docker/PlexAniSync/run/. /plexanisync/
COPY plexanisync /plexanisync/plexanisync

LABEL org.opencontainers.image.documentation=https://github.com/RickDB/PlexAniSync/blob/master/Docker/PlexAniSync/README.md

ENTRYPOINT ["/venv/bin/python3", "/plexanisync/runsync.py"]