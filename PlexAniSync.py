import collections
import configparser
import coloredlogs
import json
import logging
import os
import re
import requests
import sys
from guessit import guessit
from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer

import anilist
import plexmodule

# Logger settings
logger = logging.getLogger('PlexAniSync')
coloredlogs.install(fmt='%(asctime)s %(message)s', logger=logger)

# Enable this if you want to also log all messages coming from imported libraries
# coloredlogs.install(level='DEBUG')

## Settings section ##


def read_settings(settings_file):
    if not os.path.isfile(settings_file):
        logger.critical(
            '[CONFIG] Settings file file not found: %s' % (settings_file))
        sys.exit()
    settings = configparser.ConfigParser()
    settings.read(settings_file)
    return settings


settings_file = 'settings.ini'
settings = read_settings(settings_file)
anilist_settings = settings['ANILIST']
plex_settings = settings['PLEX']

ANILIST_SKIP_UPDATE = anilist_settings['skip_list_update'].lower()
ANILIST_ACCESS_TOKEN = anilist_settings['access_token'].strip()

mapping_file = 'custom_mappings.ini'
custom_mappings = []


def read_custom_mappings(mapping_file):
    if not os.path.isfile(mapping_file):
        logger.info(
            '[MAPPING] Custom map file not found: %s' % (mapping_file))
    else:
        logger.info('[MAPPING] Custom map file found: %s' % (mapping_file))
        file = open(mapping_file, "r")
        for line in file:
            try:
                mappingSplit = line.split('^')
                series_title = mappingSplit[0]
                season = mappingSplit[1]
                anime_id = int(mappingSplit[2])

                logger.info(
                    "[MAPPING] Adding custom mapping | title: %s | season: %s | anilist id: %s" %
                    (series_title, season, anime_id))
                mapping = anilist.anilist_custom_mapping(
                    series_title, season, anime_id)
                custom_mappings.append(mapping)
            except BaseException:
                logger.error(
                    '[MAPPING] Invalid entry found for line: %s' %
                    (line))

## Startup section ##


def start():
    if ANILIST_SKIP_UPDATE == 'true':
        logger.warning(
            'AniList skip list update enabled in settings, will match but NOT update your list')

    # Anilist
    anilist_username = anilist_settings['username']
    anilist.custom_mappings = custom_mappings
    anilist.ANILIST_ACCESS_TOKEN = ANILIST_ACCESS_TOKEN
    anilist.ANILIST_SKIP_UPDATE = ANILIST_SKIP_UPDATE
    anilist_series = anilist.process_user_list(anilist_username)

    # Plex
    if not anilist_series:
        logger.error(
            'Unable to retrieve AniList list, check your username and access token')
    else:
        plexmodule.plex_settings = plex_settings
        plex_anime_series = plexmodule.get_anime_shows()
        if(plex_anime_series is None):
            logger.error('Found no Plex shows for processing so exiting')
            return None

        plex_series_watched = plexmodule.get_watched_shows(plex_anime_series)
        if(plex_series_watched is None):
            logger.error(
                'Found no watched shows on Plex for processing so exiting')
            return None

        anilist.match_to_plex(
            anilist_series,
            plex_anime_series,
            plex_series_watched)

        logger.info('Plex to AniList sync finished')


if __name__ == '__main__':
    read_custom_mappings(mapping_file)
    start()
