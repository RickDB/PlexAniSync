import os
import time

import PlexAniSync
import settingsupdater


def run():
    while True:
        try:
            PlexAniSync.start()
        except (Exception, SystemExit):
            PlexAniSync.logger.exception("Sync cycle failed")

        interval = int(os.environ.get("INTERVAL", 0))
        if interval > 0:
            time.sleep(interval)
        else:
            print("Sync was completed and INTERVAL <= 0, quitting")
            break


if __name__ == "__main__":
    if not os.environ.get("SETTINGS_FILE"):
        print("Updating settings.ini")
        settingsupdater.write_settings_file()
    else:
        print("Using custom config: " + os.environ["SETTINGS_FILE"])
    run()
