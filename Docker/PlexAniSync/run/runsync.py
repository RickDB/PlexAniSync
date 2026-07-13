import os
import subprocess
import sys
import time

PLEXANISYNC_DIR = os.path.dirname(os.path.abspath(__file__))


def run():
    while True:
        subprocess.run(
            [sys.executable, os.path.join(PLEXANISYNC_DIR, "PlexAniSync.py")], check=True
        )
        interval = int(os.environ.get("INTERVAL", 0))
        if interval > 0:
            time.sleep(interval)
        else:
            print("Sync was completed and INTERVAL <= 0, quitting")
            break


if __name__ == "__main__":
    if not os.environ.get("SETTINGS_FILE"):
        print("Updating settings.ini")
        subprocess.run(
            [sys.executable, os.path.join(PLEXANISYNC_DIR, "settingsupdater.py")], check=True
        )
    else:
        print("Using custom config: " + os.environ["SETTINGS_FILE"])
    run()
