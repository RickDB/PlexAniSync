#!/bin/bash
run() {
  while true
  do
    (cd /plexanisync && python Scripts/PlexAniSync.py)
    sleep ${INTERVAL}
  done
}

####
# Main body of script
###

if [[ -z ${SETTINGS_FILE} ]]; then
  echo "Updating settings.ini"
  python /plexanisync/settingsupdater.py
  run
else
  echo "Using custom config: "${SETTINGS_FILE}
  run
fi

