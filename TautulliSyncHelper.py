import configparser
import logging
import os
import sys
from time import sleep

import coloredlogs

from custom_mappings import read_custom_mappings
import anilist
import plexmodule
import graphql

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
        sys.exit()
    settings = configparser.ConfigParser()
    settings.read(settings_file)
    return settings


if len(sys.argv) > 2:
    SETTINGS_FILE = sys.argv[1]
    logger.warning(f"Found settings file parameter and using: {SETTINGS_FILE}")
else:
    SETTINGS_FILE = "settings.ini"

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
    if len(sys.argv) < 2:
        logger.error("No show title specified in arguments so cancelling updating")
        sys.exit()
    else:
        # If we have custom settings file parameter use different arg index to
        # keep legacy method intact
        if len(sys.argv) > 2:
            show_title = sys.argv[2]
        else:
            show_title = sys.argv[1]

        logger.info(f"Updating single show: {show_title}")

    anilist.CUSTOM_MAPPINGS = read_custom_mappings()

    if graphql.ANILIST_SKIP_UPDATE:
        logger.warning(
            "AniList skip list update enabled in settings, will match but NOT update your list"
        )

    # Wait a few a seconds to make sure Plex has processed watched states
    sleep(5.0)

    # Anilist
    anilist_username = anilist_settings["username"]
    anilist_series = anilist.process_user_list(anilist_username)

    # Plex
    if anilist_series is None:
        logger.error(
            "Unable to retrieve AniList list, check your username and access token"
        )
    elif not anilist_series:
        logger.error("No items found on your AniList list to process")
    else:
        plexmodule.plex_settings = plex_settings
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
