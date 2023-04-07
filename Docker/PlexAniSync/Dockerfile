FROM python:3.11 AS builder

RUN pip install pipenv
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY Pipfile Pipfile.lock /
# Create /.venv with dependencies
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

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

COPY PlexAniSync.py requirements.txt custom_mappings_schema.json Docker/PlexAniSync/run/. /plexanisync/
COPY plexanisync /plexanisync/plexanisync

LABEL org.opencontainers.image.documentation=https://github.com/RickDB/PlexAniSync/blob/master/Docker/PlexAniSync/README.md

CMD ["/plexanisync/runsync.sh"]