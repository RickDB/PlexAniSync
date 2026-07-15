ARG PYTHON_VERSION=3.13

FROM python:${PYTHON_VERSION}-trixie AS builder

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    scons \
    musl-tools \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /build

COPY Docker/PlexAniSync/pip.conf /etc/pip.conf
COPY requirements.txt .
RUN pip install --no-warn-script-location -r requirements.txt pyinstaller

COPY PlexAniSync.py custom_mappings_schema.json Docker/PlexAniSync/run/runsync.py Docker/PlexAniSync/run/settingsupdater.py ./
COPY plexanisync ./plexanisync

RUN pyinstaller --onefile --name plexanisync runsync.py

# staticx needs patchelf to rewrite the ELF for static linking, but the latest
# patchelf PyPI wheel (0.17.2.4) crashes staticx with
# "Assertion `splitIndex != -1' failed" during that rewrite; pin the last
# version confirmed to work with staticx until that's resolved upstream.
RUN pip install "patchelf==0.13.1.0" staticx
RUN python -m staticx dist/plexanisync dist/plexanisync-static

FROM busybox:latest

WORKDIR /plexanisync

# The static binary needs nothing else from the image to run; busybox is here
# purely so `docker exec -it <container> sh` still works for debugging.
COPY --from=builder /build/dist/plexanisync-static /plexanisync/plexanisync
COPY custom_mappings_schema.json /plexanisync/

ENV PLEX_SECTION=Anime \
    PLEX_URL=http://127.0.0.1:32400 \
    PLEX_TOKEN='' \
    ANI_USERNAME='' \
    ANI_TOKEN='' \
    INTERVAL=3600

LABEL org.opencontainers.image.documentation=https://github.com/RickDB/PlexAniSync/blob/master/Docker/PlexAniSync/README.md

CMD ["/plexanisync/plexanisync"]
