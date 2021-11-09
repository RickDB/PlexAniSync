FROM python:3.9-slim-buster

ENV PLEX_SECTION=Anime \
    PLEX_URL=http://127.0.0.1:32400 \
    PLEX_TOKEN='' \
    ANI_USERNAME='' \
    ANI_TOKEN='' \
    INTERVAL=3600

ENV PATH="${PATH}:~/.local/bin"

ADD ./* /plexanisync/

RUN cd /plexanisync && \
    python -m pip install -r requirements.txt && \
    cd ..

ADD Docker/PlexAniSync/run/* /plexanisync/

LABEL org.opencontainers.image.documentation=https://github.com/RickDB/PlexAniSync/blob/master/Docker/PlexAniSync/README.md

CMD ["/plexanisync/runsync.sh"]
