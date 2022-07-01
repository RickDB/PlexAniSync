FROM tautulli/tautulli

WORKDIR /plexanisync

# copy only the dependencies installation from the 1st stage image
COPY --from=builder /root/.local /root/.local
RUN chmod -R a+rX /root
# update PATH environment variable
ENV PATH=/root/.local:$PATH
ENV PYTHONPATH=/root/.local/lib/python3.10/site-packages

ENV PLEX_SECTION=Anime \
    PLEX_URL=http://127.0.0.1:32400 \
    PLEX_TOKEN='' \
    ANI_USERNAME='' \
    ANI_TOKEN=''

# copy code itself from context to image
COPY Docker/Tautulli/run/start.sh /app/
COPY Docker/Tautulli/run/settingsupdater.py /plexanisync/
COPY . .

# reset workdir to default one from tautulli
WORKDIR /app

LABEL autoheal=true
LABEL org.opencontainers.image.documentation=https://github.com/RickDB/PlexAniSync/blob/master/Docker/Tautulli/README.md