#!/bin/sh
echo "Updating settings.ini"
python /plexanisync/settingsupdater.py

while true
do
  (cd /plexanisync && python PlexAniSync.py)
  sleep ${INTERVAL}
done
