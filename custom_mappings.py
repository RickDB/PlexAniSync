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
    custom_mappings = {}
    if not os.path.isfile(MAPPING_FILE):
        logger.info(f"[MAPPING] Custom map file not found: {MAPPING_FILE}")
        return
    else:
        logger.info(f"[MAPPING] Custom mapping found locally, using: {MAPPING_FILE}")

    remote_custom_mapping = get_custom_mapping_remote()

    schema = yamale.make_schema('./custom_mappings_schema.yaml', parser='ruamel')

    # Create a Data object
    file_mappings_local = yamale.make_data(MAPPING_FILE, parser='ruamel')
    try:
        # Validate data against the schema same as before.
        yamale.validate(schema, file_mappings_local)
    except YamaleError as e:
        logger.error('Custom Mappings validation failed!\n')
        for result in e.results:
            for error in result.errors:
                logger.error(f"{error}\n")
        sys.exit(1)
    if remote_custom_mapping is not None:
        # loop through list tuple
        for _, value in enumerate(remote_custom_mapping):
            mapping_location = value[0]
            yaml_content = value[1]
            try:
                file_mappings_remote = yamale.make_data(content=yaml_content, parser='ruamel')
                yamale.validate(schema, file_mappings_remote)
            except YamaleError as e:
                logger.error(f'Custom Mappings {mapping_location} validation failed!\n')
                for result in e.results:
                    for error in result.errors:
                        logger.error(f"{error}\n")
                sys.exit(1)

            for file_entry in file_mappings_local[0][0]['entries']:
                for file_entry_remote in file_mappings_remote[0][0]['entries']:
                    series_mappings: List[AnilistCustomMapping] = []
                    if file_entry['title'] == file_entry_remote['title']:
                        logger.info(f"[MAPPING] Custom mapping found duplicate: {file_entry['title']} using {MAPPING_FILE} instead: {mapping_location}")
                        series_title = str(file_entry['title'])
                        synonyms: List[str] = file_entry.get('synonyms', [])
                        for file_season in file_entry['seasons']:
                            season = file_season['season']
                            anilist_id = file_season['anilist-id']
                            start = file_season.get('start', 1)
                            logger.info(
                                f"[MAPPING] Adding custom mapping from {MAPPING_FILE}"
                                f"| title: {series_title} | season: {season} | anilist id: {anilist_id} | start: {start}"
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
                                f"[MAPPING] Adding custom mapping from {mapping_location}"
                                f"| title: {series_title} | season: {season} | anilist id: {anilist_id} | start: {start}"
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
                    f"[MAPPING] Adding custom mapping from {MAPPING_FILE}"
                    f"| title: {series_title} | season: {season} | anilist id: {anilist_id} | start: {start}"
                )
                series_mappings.append(AnilistCustomMapping(season, anilist_id, start))

            custom_mappings[series_title.lower()] = series_mappings
            for synonym in synonyms:
                custom_mappings[synonym.lower()] = series_mappings
    return custom_mappings


# Get the custom mappings from web then checks if the file is valid first.
def get_custom_mapping_remote():
    if not os.path.isfile(MAPPING_FILE):
        logger.info(f"[MAPPING] {MAPPING_FILE} remote urls found, skipping")
        return None
    else:
        logger.info(f"[MAPPING] {MAPPING_FILE} found, using")
        remote_mappings_urls = []
        custom_mappings_remote = []
        custom_mappings_remote_file_name = []

        schema = yamale.make_schema('./custom_mappings_schema.yaml', parser='ruamel')

        # Create a Data object
        file_mappings = yamale.make_data(MAPPING_FILE, parser='ruamel')

        try:
            # Validate data against the schema same as before.
            yamale.validate(schema, file_mappings)
        except YamaleError as e:
            logger.error('Remote Mappings validation failed!\n')
            for result in e.results:
                for error in result.errors:
                    logger.error(f"{error}\n")
            logger.error("[MAPPING] Remote Mappings validation failed!")
            sys.exit(1)

        try:
            # loop through the remote mappings and add urls to the list
            for url in file_mappings[0][0]['remote-urls']:
                # append urls to  list remote_mappings
                remote_mappings_urls.append(url)
                logger.info(f"[MAPPING] Adding remote mapping url: {url}")

            # check if the array is not empty
            if not remote_mappings_urls:
                logger.info(f"[MAPPING] No remote mapping urls found in {MAPPING_FILE}")
                return None
            # split url and get the file name
            for url in remote_mappings_urls:
                custom_mappings_remote_file_name.append(url.split('/')[-1])
                logger.info(f"[MAPPING] Adding remote mapping file name: {url.split('/')[-1]}")

            # Get url and read the data
            for urls in remote_mappings_urls:
                response = requests.get(urls)
                if response.status_code == 200:
                    custom_mappings_remote.append(response.text)

            # create tuple of file name and data
            custom_mappings_remote = list(zip(custom_mappings_remote_file_name, custom_mappings_remote))

            return custom_mappings_remote
        except (KeyError, TypeError):
            logger.info(f"[MAPPING] No remote mapping urls found in {MAPPING_FILE}")
            return None
