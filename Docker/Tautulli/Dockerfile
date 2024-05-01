FROM python:3.12 AS builder

RUN apt-get update && \
    apt-get install -y \
    build-essential rustc git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
COPY Docker/Tautulli/pip.conf /etc/pip.conf
COPY requirements.txt .
# install dependencies to the local user directory (eg. /root/.local)
RUN pip install --user --no-warn-script-location -r requirements.txt

FROM tautulli/tautulli

WORKDIR /plexanisync

# copy only the dependencies installation from the 1st stage image
COPY --from=builder --chown=tautulli:tautulli /root/.local /home/tautulli/.local
# update PATH environment variable
ENV PATH=/home/tautulli/.local:$PATH
ENV PYTHONPATH=/home/tautulli/.local/lib/python3.9/site-packages

ENV PLEX_SECTION=Anime \
    PLEX_URL=http://127.0.0.1:32400 \
    PLEX_TOKEN='' \
    ANI_USERNAME='' \
    ANI_TOKEN=''

# copy code itself from context to image
COPY Docker/Tautulli/run/start.sh /app/
COPY TautulliSyncHelper.py requirements.txt custom_mappings_schema.json Docker/Tautulli/run/settingsupdater.py /plexanisync/
COPY plexanisync /plexanisync/plexanisync

# reset workdir to default one from tautulli
WORKDIR /app

LABEL autoheal=true
LABEL org.opencontainers.image.documentation=https://github.com/RickDB/PlexAniSync/blob/master/Docker/Tautulli/README.md