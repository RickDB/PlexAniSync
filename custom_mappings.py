# coding=utf-8
import logging
import os
import sys
from dataclasses import dataclass
from typing import List

import requests
import yamale
from yamale.yamale_error import YamaleError

logger = logging.getLogger("PlexAniSync")
MAPPING_FILE = "custom_mappings.yaml"
REMOTE_MAPPING_FILE = "remote_mappings.yaml"


@dataclass
class AnilistCustomMapping:
    season: int
    anime_id: int
    start: int


def read_custom_mappings():
    remote_custom_mapping = get_custom_mapping_web()

    custom_mappings = {}
    if not os.path.isfile(MAPPING_FILE):
        logger.info(f"[MAPPING] Custom map file not found: {MAPPING_FILE}")
        return
    else:
        logger.info(f"[MAPPING] Custom mapping found locally, using: {MAPPING_FILE}")

    schema = yamale.make_schema('./custom_mappings_schema.yaml', parser='ruamel')

    # Create a Data object
    file_mappings_local = yamale.make_data(MAPPING_FILE, parser='ruamel')

    try:
        # Validate data against the schema same as before.
        yamale.validate(schema, file_mappings_local)
        if remote_custom_mapping is not None:
            file_mappings_remote = yamale.make_data(content=remote_custom_mapping, parser='ruamel')
            yamale.validate(schema, file_mappings_remote)
    except YamaleError as e:
        logger.error('Custom Mappings validation failed!\n')
        for result in e.results:
            for error in result.errors:
                logger.error(f"{error}\n")
        sys.exit(1)
    if remote_custom_mapping is not None:
        for file_entry in file_mappings_local[0][0]['entries']:
            for file_entry_remote in file_mappings_remote[0][0]['entries']:
                series_mappings: List[AnilistCustomMapping] = []
                if file_entry['title'] == file_entry_remote['title']:
                    logger.info(f"[MAPPING] Custom mapping found duplicate..using {MAPPING_FILE} instead: {file_entry['title']}")
                    series_title = str(file_entry['title'])
                    synonyms: List[str] = file_entry.get('synonyms', [])
                    for file_season in file_entry['seasons']:
                        season = file_season['season']
                        anilist_id = file_season['anilist-id']
                        start = file_season.get('start', 1)
                        logger.info(
                            f"[MAPPING-LOCAL] Adding custom mapping | title: {series_title} | season: {season} | anilist id: {anilist_id} | start: {start}"
                        )
                        series_mappings.append(AnilistCustomMapping(season, anilist_id, start))
                else:
                    series_title = str(file_entry_remote['title'])
                    synonyms: List[str] = file_entry_remote.get('synonyms', [])
                    for file_season_remote in file_entry_remote['seasons']:
                        season = file_season_remote['season']
                        anilist_id = file_season_remote['anilist-id']
                        start = file_season_remote.get('start', 1)
                        logger.info(
                            f"[MAPPING-REMOTE] Adding custom mapping | title: {series_title} | season: {season} | anilist id: {anilist_id} | start: {start}"
                        )
                        series_mappings.append(AnilistCustomMapping(season, anilist_id, start))

                custom_mappings[series_title.lower()] = series_mappings
                for synonym in synonyms:
                    custom_mappings[synonym.lower()] = series_mappings
        return custom_mappings
    else:
        for file_entry in file_mappings_local[0][0]['entries']:
            series_title = str(file_entry['title'])
            synonyms: List[str] = file_entry.get('synonyms', [])
            series_mappings: List[AnilistCustomMapping] = []
            for file_season in file_entry['seasons']:
                season = file_season['season']
                anilist_id = file_season['anilist-id']
                start = file_season.get('start', 1)

                logger.info(
                    f"[MAPPING-LOCAL] Adding custom mapping | title: {series_title} | season: {season} | anilist id: {anilist_id} | start: {start}"
                )
                series_mappings.append(AnilistCustomMapping(season, anilist_id, start))

            custom_mappings[series_title.lower()] = series_mappings
            for synonym in synonyms:
                custom_mappings[synonym.lower()] = series_mappings
    return custom_mappings


# Get the custom mappings from web then checks if the file is valid first.
def get_custom_mapping_web():
    if not os.path.isfile(REMOTE_MAPPING_FILE):
        logger.info(f"[MAPPING-REMOTE] Remote mapping: {REMOTE_MAPPING_FILE} file not found, skipping")
        return None
    else:
        logger.info(f"[MAPPING-REMOTE] Remote mapping: {REMOTE_MAPPING_FILE} found, using")
        remote_mappings_urls = []
        custom_mappings_remote = []
        custom_mappings_web = ''

        schema = yamale.make_schema('./remote_mappings_schema.yaml', parser='ruamel')

        # Create a Data object
        file_mappings = yamale.make_data(REMOTE_MAPPING_FILE, parser='ruamel')

        try:
            # Validate data against the schema same as before.
            yamale.validate(schema, file_mappings)
        except YamaleError as e:
            logger.error('Remote Mappings validation failed!\n')
            for result in e.results:
                for error in result.errors:
                    logger.error(f"{error}\n")
            logger.error("[MAPPING-REMOTE] Remote Mappings validation failed!")
            sys.exit(1)

        # loop through the remote mappings and add urls to the list
        for file_entry in file_mappings[0][0]['remotes']:
            remote_map_name = str(file_entry['name'])
            urls: List[str] = file_entry.get('urls', [])
            # append urls to  list remote_mappings
            for url in urls:
                remote_mappings_urls.append(url)
                logger.info(f"[MAPPING-REMOTE] Adding remote mapping: {remote_map_name} | url: {url}")

        # Get url and read the data
        for urls in remote_mappings_urls:
            response = requests.get(urls)
            if response.status_code == 200:
                custom_mappings_remote.append(response.text)

        # join the data from the list into one string
        custom_mappings_web = '\n'.join(custom_mappings_remote)

        # remove enteries key from string but leave the first one.
        custom_mappings_web = custom_mappings_web.replace('\nentries:', '\n')

        # add the first enteries key back to the string
        custom_mappings_web = 'entries:\n' + custom_mappings_web

        return custom_mappings_web
