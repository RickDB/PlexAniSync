FROM python:3.11-slim

# update base
RUN apt-get update -y -qq
RUN apt-get dist-upgrade -y -qq
RUN apt-get autoremove -y -qq

# install pipx
RUN pip install --upgrade pip
RUN pip install pipx
RUN pipx ensurepath

# install poetry
RUN pipx --global install poetry

# setup user, bash default shell
RUN useradd app -m -s /bin/bash
RUN mkdir -p /config && chown -R app /config
USER app
SHELL ["/bin/bash", "-c"]

WORKDIR /plexanisync

# Copy App files
COPY pyproject.toml poetry.lock PlexAniSync.py custom_mappings_schema.json Docker/PlexAniSync/run/. /plexanisync/
COPY plexanisync /plexanisync/plexanisync

# install app dependencies
RUN poetry install --no-interaction --no-ansi --no-cache --quiet

# activate venv
RUN source $(poetry env info --path)/bin/activate

# default settings
ENV PLEX_SECTION=Anime \
    PLEX_URL=http://127.0.0.1:32400 \
    PLEX_TOKEN='' \
    ANI_USERNAME='' \
    ANI_TOKEN='' \
    INTERVAL=3600

LABEL org.opencontainers.image.documentation=https://github.com/RickDB/PlexAniSync/blob/master/Docker/PlexAniSync/README.md

CMD ["/plexanisync/runsync.sh"]
