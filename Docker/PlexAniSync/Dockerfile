FROM python:3.9 AS builder

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /plexanisync

COPY requirements.txt .
# install dependencies to the local user directory (eg. /root/.local)
RUN pip install --user -r requirements.txt

FROM python:3.9-slim

WORKDIR /plexanisync

# copy only the dependencies installation from the 1st stage image
COPY --from=builder /root/.local /root/.local
# update PATH environment variable
ENV PATH=/root/.local:$PATH

ENV PLEX_SECTION=Anime \
    PLEX_URL=http://127.0.0.1:32400 \
    PLEX_TOKEN='' \
    ANI_USERNAME='' \
    ANI_TOKEN='' \
    INTERVAL=3600

COPY Docker/PlexAniSync/run/. .
# copy code itself from context to image
COPY . .

LABEL org.opencontainers.image.documentation=https://github.com/RickDB/PlexAniSync/blob/master/Docker/PlexAniSync/README.md

CMD ["/plexanisync/runsync.sh"]