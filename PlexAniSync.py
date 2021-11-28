# coding=utf-8
import configparser
import logging
import logging.handlers
import os
import sys

import coloredlogs

from custom_mappings import read_custom_mappings
import anilist
import plexmodule
import graphql
from _version import __version__

# Logger settings
LOG_FILENAME = "PlexAniSync.log"
logger = logging.getLogger("PlexAniSync")

# Add the rotating log message handler to the standard log
handler = logging.handlers.RotatingFileHandler(
    LOG_FILENAME, maxBytes=10000000, backupCount=5, encoding="utf-8"
)
handler.setLevel(logging.INFO)
logger.addHandler(handler)

# Debug log
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler("PlexAniSync-DEBUG.log", "w", "utf-8")],
)

# Install colored logs
coloredlogs.install(fmt="%(asctime)s %(message)s", logger=logger)


# Enable this if you want to also log all messages coming from imported libraries
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

if len(sys.argv) > 1:
    SETTINGS_FILE = sys.argv[1]
    logger.warning(f"Found settings file parameter and using: {SETTINGS_FILE}")

settings = read_settings(SETTINGS_FILE)
anilist_settings = settings["ANILIST"]
plex_settings = settings["PLEX"]

graphql.ANILIST_ACCESS_TOKEN = anilist_settings["access_token"].strip()

if "skip_list_update" in anilist_settings:
    graphql.ANILIST_SKIP_UPDATE = anilist_settings["skip_list_update"].lower().strip() == "true"

if "plex_episode_count_priority" in anilist_settings:
    anilist.ANILIST_PLEX_EPISODE_COUNT_PRIORITY = (
        anilist_settings["plex_episode_count_priority"].lower().strip() == "true"
    )

if "log_failed_matches" in anilist_settings:
    anilist.ANILIST_LOG_FAILED_MATCHES = (
        anilist_settings["log_failed_matches"].lower().strip() == "true"
    )


## Startup section ##
def start():
    logger.info(f"PlexAniSync - version: {__version__}")

    anilist.CUSTOM_MAPPINGS = read_custom_mappings()

    if graphql.ANILIST_SKIP_UPDATE:
        logger.warning(
            "AniList skip list update enabled in settings, will match but NOT update your list"
        )

    if anilist.ANILIST_PLEX_EPISODE_COUNT_PRIORITY:
        logger.warning(
            "Plex episode watched count will take priority over AniList, this will always update AniList watched count over Plex data"
        )

    anilist.clean_failed_matches_file()

    # Anilist
    anilist_username = anilist_settings["username"]
    anilist_series = anilist.process_user_list(anilist_username)

    # Plex
    if anilist_series is None:
        logger.error(
            "Unable to retrieve AniList list, check your username and access token"
        )
    else:
        if not anilist_series:
            logger.error(
                "No items found on your AniList list for additional processing later on"
            )

        plexmodule.plex_settings = plex_settings
        plex_anime_series = plexmodule.get_anime_shows()

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
