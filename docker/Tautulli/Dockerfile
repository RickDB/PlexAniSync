FROM python:3.9 AS builder

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# install dependencies to /venv
ENV PATH=/venv/bin:$PATH
RUN python -m venv /venv
RUN pip install -r requirements.txt

FROM tautulli/tautulli

WORKDIR /plexanisync

# copy venv from builder
COPY --from=builder /venv /venv
ENV PATH=/venv/bin:$PATH

ENV PLEX_SECTION=Anime \
    PLEX_URL=http://127.0.0.1:32400 \
    PLEX_TOKEN='' \
    ANI_USERNAME='' \
    ANI_TOKEN=''

# copy code itself from context to image
COPY docker/Tautulli/run/start.sh /app/
COPY data /plexanisync/data
COPY scripts /plexanisync/scripts
COPY plexanisync /plexanisync/plexanisync
COPY plexanisync /plexanisync/plexanisync

# reset workdir to default one from tautulli
WORKDIR /app

LABEL autoheal=true
LABEL org.opencontainers.image.documentation=https://github.com/RickDB/PlexAniSync/blob/master/docker/Tautulli/README.md