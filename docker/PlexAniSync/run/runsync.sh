#!/bin/bash
run() {
  while true
  do
    (cd /plexanisync && python scriptsPlexAniSync.py)
    sleep ${INTERVAL}
  done
}

####
# Main body of script
###

if [[ -z ${SETTINGS_FILE} ]]; then
  echo "Updating settings.ini"
  python /plexanisync/scripts/settingsupdater.py
  run
else
  echo "Using custom config: "${SETTINGS_FILE}
  run
fi

