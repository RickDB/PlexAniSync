#!/bin/bash
run() {
  while true; do
    python PlexAniSync.py
    if [ ${INTERVAL} -gt 0 ]; then
      sleep ${INTERVAL}
    else
      echo "Sync was completed and INTERVAL <= 0, quitting"
      break
    fi
  done
}

####
# Main body of script
###

if [[ -z ${SETTINGS_FILE} ]]; then
  echo "Updating settings.ini"
  python settingsupdater.py
  run
else
  echo "Using custom config: "${SETTINGS_FILE}
  run
fi
