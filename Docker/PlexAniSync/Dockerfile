FROM python:3.11 AS builder

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
COPY Docker/PlexAniSync/pip.conf /etc/pip.conf
COPY requirements.txt .
# install dependencies to the local user directory (eg. /root/.local)
RUN pip install --user --no-warn-script-location -r requirements.txt

FROM python:3.11-slim

WORKDIR /plexanisync

# copy only the dependencies installation from the 1st stage image
COPY --from=builder /root/.local /root/.local
RUN chmod -R a+rX /root
# update PATH environment variable
ENV PATH=/root/.local:$PATH
ENV PYTHONPATH=/root/.local/lib/python3.11/site-packages

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