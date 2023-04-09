FROM python:3.11 AS builder

RUN apt-get update && \
    apt-get install -y build-essential

COPY requirements.txt .

# install dependencies to /venv
ENV PATH=/venv/bin:$PATH
RUN python -m venv /venv
RUN pip install -r requirements.txt

FROM python:3.11-slim

WORKDIR /plexanisync

# copy venv from builder
COPY --from=builder /venv /venv
ENV PATH=/venv/bin:$PATH

ENV PLEX_SECTION=Anime \
    PLEX_URL=http://127.0.0.1:32400 \
    PLEX_TOKEN='' \
    ANI_USERNAME='' \
    ANI_TOKEN='' \
    INTERVAL=3600

COPY sync.py requirements.txt custom_mappings_schema.json Docker/PlexAniSync/run/. /plexanisync/
COPY plexanisync /plexanisync/plexanisync

LABEL org.opencontainers.image.documentation=https://github.com/RickDB/PlexAniSync/blob/master/Docker/PlexAniSync/README.md

CMD ["/plexanisync/runsync.sh"]