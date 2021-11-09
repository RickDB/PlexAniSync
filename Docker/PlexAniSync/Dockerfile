FROM python:3.9-alpine

RUN apk add --no-cache --update ca-certificates tzdata build-base && \
    update-ca-certificates && \
    rm -rf /root/.cache

ENV PLEX_SECTION=Anime \
    PLEX_URL=http://127.0.0.1:32400 \
    PLEX_TOKEN='' \
    ANI_USERNAME='' \
    ANI_TOKEN='' \
    INTERVAL=3600 \
    PATH="${PATH}:~/.local/bin"

ADD ./* /plexanisync/
ADD Docker/PlexAniSync/run/* /plexanisync/

RUN cd /plexanisync && \
    python3 -m pip install -r requirements.txt && \
    cd ..

LABEL org.opencontainers.image.documentation=https://github.com/RickDB/PlexAniSync/blob/master/Docker/PlexAniSync/README.md

CMD ["/plexanisync/runsync.sh"]
