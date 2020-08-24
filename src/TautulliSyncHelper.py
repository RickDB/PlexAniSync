import configparser
import logging
import os
import sys
from time import sleep

import coloredlogs

from src import anilist
from src import plexmodule
from src import PlexAniSync

# Logger settings
logger = logging.getLogger(__name__)
coloredlogs.install(fmt="%(asctime)s %(message)s", logger=logger)

# Enable this if you want to also log all messages coming from imported
# libraries
# coloredlogs.install(level='DEBUG')

if len(sys.argv) > 2:
    settings_file = sys.argv[1]
    logger.warning("Found settings file parameter and using: %s" % (settings_file))
else:
    settings_file = "settings.ini"

settings = PlexAniSync.read_settings(settings_file)
anilist_settings = settings["ANILIST"]
plex_settings = settings["PLEX"]

ANILIST_SKIP_UPDATE = anilist_settings["skip_list_update"].lower()
ANILIST_ACCESS_TOKEN = anilist_settings["access_token"].strip()

mapping_file = "custom_mappings.ini"

custom_mappings = PlexAniSync.read_custom_mappings(mapping_file=mapping_file)


# Startup section #


def start():
    if len(sys.argv) < 2:
        logger.error("No show title specified in arguments so cancelling updating")
        sys.exit()
    else:
        # If we have custom settings file parameter use different arg index to
        # keep legacy method intact
        if len(sys.argv) > 2:
            show_title = sys.argv[2]
        elif len(sys.argv) == 2:
            show_title = sys.argv[1]

        logger.info("Updating single show: %s" % (show_title))

    if ANILIST_SKIP_UPDATE == "true":
        logger.warning(
            "AniList skip list update enabled in settings, will match but NOT update your list"
        )

    # Wait a few a seconds to make sure Plex has processed watched states
    sleep(5.0)

    # Anilist
    anilist_username = anilist_settings["username"]
    anilist.custom_mappings = custom_mappings
    anilist.ANILIST_ACCESS_TOKEN = ANILIST_ACCESS_TOKEN
    anilist.ANILIST_SKIP_UPDATE = ANILIST_SKIP_UPDATE
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
            anilist.match_to_plex(
                anilist_series, plex_anime_series, plex_series_watched
            )

        logger.info("Plex to AniList sync finished")


if __name__ == "__main__":
    read_custom_mappings(mapping_file)
    start()
