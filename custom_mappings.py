# coding=utf-8
import logging
import os
import sys
from dataclasses import dataclass
from typing import Dict, List

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


def read_custom_mappings() -> Dict[str, List[AnilistCustomMapping]]:
    custom_mappings: Dict[str, List[AnilistCustomMapping]] = {}
    if not os.path.isfile(MAPPING_FILE):
        logger.info(f"[MAPPING] Custom map file not found: {MAPPING_FILE}")
        return custom_mappings

    logger.info(f"[MAPPING] Custom mapping found locally, using: {MAPPING_FILE}")

    schema = yamale.make_schema('./custom_mappings_schema.yaml', parser='ruamel')

    # Create a Data object
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        file_mappings_local = yamale.make_data(content=f.read(), parser='ruamel')
    try:
        # Validate data against the schema same as before.
        yamale.validate(schema, file_mappings_local)
    except YamaleError as e:
        logger.error('[MAPPING] Custom Mappings validation failed!\n')
        for result in e.results:
            for error in result.errors:
                logger.error(f"{error}\n")
        sys.exit(1)

    remote_custom_mapping = get_custom_mapping_remote(file_mappings_local)

    # loop through list tuple
    for value in remote_custom_mapping:
        mapping_location = value[0]
        yaml_content = value[1]
        try:
            file_mappings_remote = yamale.make_data(content=yaml_content, parser='ruamel')
            yamale.validate(schema, file_mappings_remote)
        except YamaleError as e:
            logger.error(f'[MAPPING] Custom Mappings {mapping_location} validation failed!\n')
            for result in e.results:
                for error in result.errors:
                    logger.error(f"{error}\n")
            sys.exit(1)
        add_mappings(custom_mappings, mapping_location, file_mappings_remote)

    add_mappings(custom_mappings, MAPPING_FILE, file_mappings_local)

    return custom_mappings


def add_mappings(custom_mappings, mapping_location, file_mappings):
    # handles missing and empty 'entries'
    entries = file_mappings[0][0].get('entries', []) or []
    for file_entry in entries:
        series_title = str(file_entry['title'])
        synonyms: List[str] = file_entry.get('synonyms', [])
        series_mappings: List[AnilistCustomMapping] = []
        for file_season in file_entry['seasons']:
            season = file_season['season']
            anilist_id = file_season['anilist-id']
            start = file_season.get('start', 1)
            logger.info(
                f"[MAPPING] Adding custom mapping from {mapping_location} "
                f"| title: {series_title} | season: {season} | anilist id: {anilist_id}"
            )
            series_mappings.append(AnilistCustomMapping(season, anilist_id, start))
        if synonyms:
            logger.info(f"[MAPPING] {series_title} has synonyms: {synonyms}")
        for title in [series_title] + synonyms:
            title_lower = title.lower()
            if title_lower in custom_mappings:
                logger.info(f"[MAPPING] Overwriting previous mapping for {title}")
            custom_mappings[title_lower] = series_mappings


# Get the custom mappings from the web.
def get_custom_mapping_remote(file_mappings) -> List[tuple[str, str]]:
    custom_mappings_remote: List[tuple[str, str]] = []
    # handles missing and empty 'remote-urls'
    remote_mappings_urls: List[str] = file_mappings[0][0].get('remote-urls', []) or []

    # Get url and read the data
    for url in remote_mappings_urls:
        file_name = url.split('/')[-1]
        logger.info(f"[MAPPING] Adding remote mapping url: {url}")

        response = requests.get(url)
        if response.status_code == 200:
            custom_mappings_remote.append((file_name, response.text))
        else:
            logger.error(f"[MAPPING] Could not download mapping file, received {response.reason}.")

    return custom_mappings_remote
