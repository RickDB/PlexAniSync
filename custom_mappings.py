# coding=utf-8
import os
import logging
import sys
import requests
from typing import List
from dataclasses import dataclass

import yamale
from yamale.yamale_error import YamaleError



logger = logging.getLogger("PlexAniSync")
MAPPING_FILE = "custom_mappings.yaml"


@dataclass
class AnilistCustomMapping:
    season: int
    anime_id: int
    start: int


def read_custom_mappings(url):
    if url is not None or url != "":
        web_custom_mapping = get_custom_mapping_web(url)
        
    custom_mappings = {}
    if web_custom_mapping is not None:
        logger.info(f"[MAPPING] Custom mapping found on web, using: {url}")
        with open(MAPPING_FILE, "w") as f:
            f.write(web_custom_mapping)
    elif not os.path.isfile(MAPPING_FILE):
        logger.info(f"[MAPPING] Custom map file not found: {MAPPING_FILE}")
        return
    else:
        logger.info(f"[MAPPING] Custom mapping found locally, using: {MAPPING_FILE}")
        
    schema = yamale.make_schema('./custom_mappings_schema.yaml', parser='ruamel')

    # Create a Data object
    file_mappings = yamale.make_data(MAPPING_FILE, parser='ruamel')

    try:
        # Validate data against the schema same as before.
        yamale.validate(schema, file_mappings)
    except YamaleError as e:
        logger.error('Custom Mappings validation failed!\n')
        for result in e.results:
            for error in result.errors:
                logger.error(f"{error}\n")
        sys.exit(1)

    for file_entry in file_mappings[0][0]['entries']:
        series_title = str(file_entry['title'])
        synonyms: List[str] = file_entry.get('synonyms', [])
        series_mappings: List[AnilistCustomMapping] = []
        for file_season in file_entry['seasons']:
            season = file_season['season']
            anilist_id = file_season['anilist-id']
            start = file_season.get('start', 1)

            logger.info(
                f"[MAPPING] Adding custom mapping | title: {series_title} | season: {season} | anilist id: {anilist_id} | start: {start}"
            )
            series_mappings.append(AnilistCustomMapping(season, anilist_id, start))

        custom_mappings[series_title.lower()] = series_mappings
        for synonym in synonyms:
            custom_mappings[synonym.lower()] = series_mappings
    return custom_mappings


# Get the custom mappings from web then checks if the file is valid first.
def get_custom_mapping_web(url):
    # Check if url is present
    if url is None or url == "":
        logger.info("[MAPPING] No custom mapping url provided, skipping")
        logger.info("[MAPPING] Using default mapping file: {}".format(MAPPING_FILE))
        return
    # Get url and read the data
    response = requests.get(url)
    if response.status_code == 200:
        try:
            # temporary file to store the data and check if it is valid
            with open("temp_valid.yaml", "w") as f:
                f.write(response.text)

            schema = yamale.make_schema('./custom_mappings_schema.yaml', parser='ruamel')
            file_mappings = yamale.make_data("temp_valid.yaml", parser='ruamel')
            # Validate data against the schema same as before.
            yamale.validate(schema, file_mappings)
            # remove the temporary file
            if os.path.exists("temp_valid.yaml"):
                os.remove("temp_valid.yaml")
            return response.text
        except BaseException as e :
            logger.error(f'Custom Mappings url validation failed!\n Check the url: {url} \n if it\'s a valid yaml file.')
            if os.path.exists("temp_valid.yaml"):
                os.remove("temp_valid.yaml")
            return None
    else:
        logger.error(f"Failed to get custom mapping from web: {url}")
        return None
