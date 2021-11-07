#!/usr/bin/env bash


PUID=${PUID:-1000}
PGID=${PGID:-1000}

groupmod -o -g "$PGID" tautulli
usermod -o -u "$PUID" tautulli

chown -R tautulli:tautulli /config
chown -R tautulli:tautulli /plexanisync

echo "Updating settings.ini"
gosu tautulli "python" "/plexanisync/settingsupdater.py"

echo "Running Tautulli using user tautulli (uid=$(id -u tautulli)) and group tautulli (gid=$(id -g tautulli))"
exec gosu tautulli "$@"
