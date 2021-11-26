FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PLEX_SECTION=Anime \
    PLEX_URL=http://127.0.0.1:32400 \
    PLEX_TOKEN='' \
    ANI_USERNAME='' \
    ANI_TOKEN='' \
    INTERVAL=3600

ENV PATH="${PATH}:~/.local/bin"

# run this before copying requirements for cache efficiency
RUN pip install --upgrade pip

#set work directory early so remaining paths can be relative
WORKDIR /plexanisync

# Adding requirements file to current directory
# just this file first to cache the pip install step when code changes
# Use copy since we are not getting anything from remote or URL
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

COPY Docker/PlexAniSync/run/. .
# copy code itself from context to image
COPY . .

LABEL org.opencontainers.image.documentation=https://github.com/RickDB/PlexAniSync/blob/master/Docker/PlexAniSync/README.md

CMD ["/plexanisync/runsync.sh"]