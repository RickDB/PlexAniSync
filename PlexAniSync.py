# coding=utf-8
import logging
import logging.handlers
import os
import sys

import coloredlogs

import anilist
import graphql
import plexmodule
from custom_mappings import read_custom_mappings
from misc.config import Config
from misc.log import logger
from notifications import Notifications

__version__ = "1.3.12"

# Load logger
log = logger.get_logger('PlexAniSync')


############################################################
# MISC
############################################################

def init_notifications():
    # noinspection PyBroadException
    try:
        for notification_name, notification_config in cfg.notifications.items():
            if notification_name.lower() == 'verbose':
                continue

            notify.load(**notification_config)
    except Exception:
        log.exception("Exception initializing notification agents: ")
    return


notify = Notifications()

# Notifications
init_notifications()

# Install colored logs
coloredlogs.install(fmt="%(asctime)s %(message)s", logger=logger)

# Enable this if you want to also log all messages coming from imported libraries
# coloredlogs.install(level='DEBUG')


config = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "config.json")
cache_file = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "cache.db")
log_file = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "activity.log")

# Load config
cfg = Config(configfile=config, cachefile=cache_file, logfile=log_file).cfg


## Settings section ##
graphql.ANILIST_SKIP_UPDATE = cfg.ANILIST.skip_list_update
anilist.ANILIST_ACCESS_TOKEN = cfg.ANILIST.access_token.strip()
anilist.ANILIST_PLEX_EPISODE_COUNT_PRIORITY = cfg.ANILIST.plex_episode_count_priority
anilist.ANILIST_LOG_FAILED_MATCHES = cfg.core.logFailedMatches
anilist_username = cfg.ANILIST.username


## Startup section ##
def start():
    logging.info(f"PlexAniSync - version: {__version__}")

    anilist.CUSTOM_MAPPINGS = read_custom_mappings()

    if graphql.ANILIST_SKIP_UPDATE:
        logging.warning(
            "AniList skip list update enabled in settings, will match but NOT update your list"
        )

    if anilist.ANILIST_PLEX_EPISODE_COUNT_PRIORITY:
        logging.warning(
            "Plex episode watched count will take priority over AniList, this will always update AniList watched count over Plex data"
        )

    anilist.clean_failed_matches_file()

    # Anilist
    anilist_series = anilist.process_user_list(anilist_username)

    # Plex
    if anilist_series is None:
        logging.error(
            "Unable to retrieve AniList list, check your username and access token"
        )
    else:
        if not anilist_series:
            logging.error(
                "No items found on your AniList list for additional processing later on"
            )

        plex_anime_series = plexmodule.get_anime_shows()

        if plex_anime_series is None:
            logging.error("Found no Plex shows for processing")
            plex_series_watched = None
        else:
            plex_series_watched = plexmodule.get_watched_shows(plex_anime_series)

        if plex_series_watched is None:
            logging.error("Found no watched shows on Plex for processing")
        else:
            anilist.match_to_plex(anilist_series, plex_series_watched)

    logging.info("Plex to AniList sync finished")


if __name__ == "__main__":
    start()
