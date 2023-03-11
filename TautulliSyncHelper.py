import configparser
import logging
import os
import sys
from time import sleep

import coloredlogs

from plexanisync.anilist import Anilist
from plexanisync.custom_mappings import read_custom_mappings
from plexanisync.plexmodule import PlexModule
from plexanisync._version import __version__

# Logger settings
logger = logging.getLogger("PlexAniSync")
coloredlogs.install(fmt="%(asctime)s %(message)s", logger=logger)

# Enable this if you want to also log all messages coming from imported
# libraries
# coloredlogs.install(level='DEBUG')

## Settings section ##


def read_settings(settings_file) -> configparser.ConfigParser:
    if not os.path.isfile(settings_file):
        logger.critical(f"[CONFIG] Settings file file not found: {settings_file}")
        sys.exit(1)
    settings = configparser.ConfigParser()
    settings.read(settings_file, encoding="utf-8")
    return settings


SETTINGS_FILE = os.getenv("SETTINGS_FILE") or "settings.ini"

if len(sys.argv) < 2:
    logger.error("No show title specified in arguments so cancelling updating")
    sys.exit(1)
elif len(sys.argv) > 2:
    SETTINGS_FILE = sys.argv[1]
    logger.warning(f"Found settings file parameter and using: {SETTINGS_FILE}")
    # If we have custom settings file parameter use different arg index to
    # keep legacy method intact
    show_title = sys.argv[2]
else:
    show_title = sys.argv[1]

settings = read_settings(SETTINGS_FILE)
anilist_settings = settings["ANILIST"]
plex_settings = settings["PLEX"]


## Startup section ##
def start():
    logger.info(f"PlexAniSync - version: {__version__}")
    logger.info(f"Updating single show: {show_title}")

    custom_mappings = read_custom_mappings()

    if anilist_settings.getboolean("skip_list_update", False):
        logger.warning(
            "AniList skip list update enabled in settings, will match but NOT update your list"
        )

    if anilist_settings.getboolean("plex_episode_count_priority", False):
        logger.warning(
            "Plex episode watched count will take priority over AniList, this will always update AniList watched count over Plex data"
        )

    anilist = Anilist(anilist_settings, custom_mappings)
    anilist_series = anilist.process_user_list()

    # Plex
    if anilist_series is None:
        logger.error(
            "Unable to retrieve AniList list, check your username and access token"
        )
    else:
        # Wait a few a seconds to make sure Plex has processed watched states
        sleep(5.0)
        plexmodule = PlexModule(plex_settings)
        plex_anime_series = plexmodule.get_anime_shows_filter(show_title)

        if plex_anime_series is None:
            logger.error("Found no Plex shows for processing")
            plex_series_watched = None
        else:
            plex_series_watched = plexmodule.get_watched_shows(plex_anime_series)

        if plex_series_watched is None:
            logger.error("Found no watched shows on Plex for processing")
        else:
            anilist.match_to_plex(anilist_series, plex_series_watched)

        logger.info("Plex to AniList sync finished")


if __name__ == "__main__":
    start()
