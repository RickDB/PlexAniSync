FROM python:3.9 AS builder

RUN pip install pipenv
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY Pipfile Pipfile.lock /
# Create /.venv with dependencies
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM tautulli/tautulli

WORKDIR /plexanisync

# Copy virtual env from builder
COPY --from=builder /.venv /.venv
# update PATH environment variable
ENV PATH="/.venv/bin:$PATH"

ENV PLEX_SECTION=Anime \
    PLEX_URL=http://127.0.0.1:32400 \
    PLEX_TOKEN='' \
    ANI_USERNAME='' \
    ANI_TOKEN=''

# copy code itself from context to image
COPY Docker/Tautulli/run/start.sh /app/
COPY TautulliSyncHelper.py requirements.txt custom_mappings_schema.json Docker/Tautulli/run/settingsupdater.py /plexanisync/
COPY plexanisync /plexanisync/plexanisync

# reset workdir to default one from tautulli
WORKDIR /app

LABEL autoheal=true
LABEL org.opencontainers.image.documentation=https://github.com/RickDB/PlexAniSync/blob/master/Docker/Tautulli/README.md