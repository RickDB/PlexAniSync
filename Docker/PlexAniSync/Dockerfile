ARG python_version=3.12

FROM ubuntu AS base
ARG python_version

RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python-${python_version} python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    python3 -m pip install pip && \
    update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3 1

FROM base AS builder

ENV CARGO_REGISTRIES_CRATES_IO_PROTOCOL=sparse

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    rustc \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
COPY Docker/PlexAniSync/pip.conf /etc/pip.conf
COPY requirements.txt .
# install dependencies to the local user directory (eg. /root/.local)
RUN --mount=type=tmpfs,target=/root/.cargo \
    CARGO_REGISTRIES_CRATES_IO_PROTOCOL=sparse \
    CARGO_HOME=/root/.cargo \
    pip install --user --no-warn-script-location -r requirements.txt

FROM base
ARG python_version

WORKDIR /plexanisync

# copy only the dependencies installation from the 1st stage image
COPY --from=builder /root/.local /root/.local
RUN chmod -R a+rX /root
# update PATH environment variable
ENV PATH=/root/.local:$PATH
ENV PYTHONPATH=/root/.local/lib/python${python_version}/site-packages

ENV PLEX_SECTION=Anime \
    PLEX_URL=http://127.0.0.1:32400 \
    PLEX_TOKEN='' \
    ANI_USERNAME='' \
    ANI_TOKEN='' \
    INTERVAL=3600

COPY PlexAniSync.py requirements.txt custom_mappings_schema.json Docker/PlexAniSync/run/. /plexanisync/
COPY plexanisync /plexanisync/plexanisync

LABEL org.opencontainers.image.documentation=https://github.com/RickDB/PlexAniSync/blob/master/Docker/PlexAniSync/README.md

CMD ["/plexanisync/runsync.sh"]