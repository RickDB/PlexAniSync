FROM tautulli/tautulli

ENV PLEX_SECTION=Anime \
    PLEX_URL=http://127.0.0.1:32400 \
    PLEX_TOKEN='' \
    ANI_USERNAME='' \
    ANI_TOKEN=''

ADD ../../* /plexanisync/

RUN cd /plexanisync && \
    python -m pip install -r requirements.txt && \
    cd ..

LABEL autoheal=true

COPY ./run/start.sh /app/
COPY ./run/settingsupdater.py /plexanisync/
