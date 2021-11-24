FROM tautulli/tautulli

RUN apt-get update && \
    apt-get install -y build-essential

ENV PLEX_SECTION=Anime \
    PLEX_URL=http://127.0.0.1:32400 \
    PLEX_TOKEN='' \
    ANI_USERNAME='' \
    ANI_TOKEN=''

# run this before copying requirements for cache efficiency
RUN pip install --upgrade pip

#set work directory early so remaining paths can be relative
WORKDIR /plexanisync

# Adding requirements file to current directory
# just this file first to cache the pip install step when code changes
# Use copy since we are not getting anything from remote or URL
COPY requirements.txt .
COPY Docker/Tautulli/run/start.sh /app/
COPY Docker/Tautulli/run/settingsupdater.py /plexanisync/

# Install dependencies
RUN python3 -m pip install -r requirements.txt

COPY ./* /plexanisync/

LABEL autoheal=true
LABEL org.opencontainers.image.documentation=https://github.com/RickDB/PlexAniSync/blob/master/Docker/Tautulli/README.md

ENTRYPOINT ["/app/start.sh"]