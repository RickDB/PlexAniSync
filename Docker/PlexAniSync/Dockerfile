FROM python:3.9-alpine

RUN apk add --no-cache --update ca-certificates tzdata && \
    update-ca-certificates && \
    rm -rf /root/.cache

ENV PLEX_SECTION=Anime \
    PLEX_URL=http://127.0.0.1:32400 \
    PLEX_TOKEN='' \
    ANI_USERNAME='' \
    ANI_TOKEN='' \
    INTERVAL=3600

ENV PATH="${PATH}:~/.local/bin"

ADD ./* /plexanisync/

RUN cd /plexanisync && \
    python3 -m pip install -r requirements.txt && \
    cd ..

ADD Docker/PlexAniSync/run/* /plexanisync/
CMD ["/plexanisync/runsync.sh"]
