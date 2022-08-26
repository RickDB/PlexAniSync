# coding=utf-8
import json
import logging
import os
import sys
from dataclasses import dataclass
from typing import Dict, List, Tuple

import requests
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from ruamel.yaml import YAML

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

    yaml = YAML(typ='safe')
    with open('./custom_mappings_schema.json', 'r', encoding='utf-8') as f:
        schema = json.load(f)

    # Create a Data object
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        file_mappings_local = yaml.load(f)
    try:
        # Validate data against the schema same as before.
        validate(file_mappings_local, schema)
    except ValidationError as e:
        logger.error('[MAPPING] Custom Mappings validation failed!\n')
        logger.error(f"{e.message} at entry {e.instance}")
        sys.exit(1)

    remote_custom_mapping = get_custom_mapping_remote(file_mappings_local)

    # loop through list tuple
    for value in remote_custom_mapping:
        mapping_location = value[0]
        yaml_content = value[1]
        try:
            file_mappings_remote = yaml.load(yaml_content)
            validate(file_mappings_local, schema)
        except ValidationError as e:
            logger.error(f'[MAPPING] Custom Mappings {mapping_location} validation failed!\n')
            logger.error(f"{e.message} at entry {e.instance}")
            sys.exit(1)
        add_mappings(custom_mappings, mapping_location, file_mappings_remote)

    add_mappings(custom_mappings, MAPPING_FILE, file_mappings_local)

    return custom_mappings


def add_mappings(custom_mappings, mapping_location, file_mappings):
    # handles missing and empty 'entries'
    entries = file_mappings.get('entries', []) or []
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
def get_custom_mapping_remote(file_mappings) -> List[Tuple[str, str]]:
    custom_mappings_remote: List[Tuple[str, str]] = []
    # handles missing and empty 'remote-urls'
    remote_mappings_urls: List[str] = file_mappings.get('remote-urls', []) or []

    # Get url and read the data
    for url in remote_mappings_urls:
        file_name = url.split('/')[-1]
        logger.info(f"[MAPPING] Adding remote mapping url: {url}")

        response = requests.get(url, timeout=10)  # 10 second timeout
        if response.status_code == 200:
            custom_mappings_remote.append((file_name, response.text))
        else:
            logger.error(f"[MAPPING] Could not download mapping file, received {response.reason}.")

    return custom_mappings_remote
