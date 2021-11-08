FROM tautulli/tautulli

ENV PLEX_SECTION=Anime \
    PLEX_URL=http://127.0.0.1:32400 \
    PLEX_TOKEN='' \
    ANI_USERNAME='' \
    ANI_TOKEN=''

ADD ./* /plexanisync/

RUN cd /plexanisync && \
    python -m pip install -r requirements.txt && \
    cd ..

LABEL autoheal=true
LABEL org.opencontainers.image.documentation=https://github.com/RickDB/PlexAniSync/blob/master/Docker/Tautulli/README.md

COPY Docker/Tautulli/run/start.sh /app/
COPY Docker/Tautulli/run/settingsupdater.py /plexanisync/
