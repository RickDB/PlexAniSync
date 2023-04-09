FROM python:3.11 AS builder

RUN apt-get update && \
    apt-get install -y build-essential libssl-dev libffi-dev python3-dev cargo && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PIP_DEFAULT_TIMEOUT=100
ENV PIP_NO_CACHE_DIR=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=true

RUN python -m pip install --upgrade pip
RUN pip install poetry
COPY pyproject.toml poetry.lock /
RUN poetry install --no-interaction --no-ansi --only main

FROM python:3.11-slim

WORKDIR /plexanisync

# Copy virtual env from builder
COPY --from=builder /.venv /.venv
# update PATH environment variable
ENV PATH="/.venv/bin:$PATH"

ENV PLEX_SECTION=Anime \
    PLEX_URL=http://127.0.0.1:32400 \
    PLEX_TOKEN='' \
    ANI_USERNAME='' \
    ANI_TOKEN='' \
    INTERVAL=3600

COPY sync.py custom_mappings_schema.json Docker/PlexAniSync/run/. /plexanisync/
COPY plexanisync /plexanisync/plexanisync

LABEL org.opencontainers.image.documentation=https://github.com/RickDB/PlexAniSync/blob/master/Docker/PlexAniSync/README.md

CMD ["/plexanisync/runsync.sh"]