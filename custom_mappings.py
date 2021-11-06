# coding=utf-8
import os
import logging
import sys
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


def read_custom_mappings():
    custom_mappings = {}
    if not os.path.isfile(MAPPING_FILE):
        logger.info(f"[MAPPING] Custom map file not found: {MAPPING_FILE}")
    else:
        logger.info(f"[MAPPING] Custom map file found: {MAPPING_FILE}")
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
            series_title = str(file_entry['title']).lower()
            synonyms = file_entry.get('synonyms', [])
            series_mappings: List[AnilistCustomMapping] = []
            for file_season in file_entry['seasons']:
                season = file_season['season']
                anilist_id = file_season['anilist-id']
                start = file_season.get('start', 1)

                logger.info(
                    f"[MAPPING] Adding custom mapping | title: {file_entry['title']} | season: {season} | anilist id: {anilist_id} | start: {start}"
                )
                series_mappings.append(AnilistCustomMapping(season, anilist_id, start))

            custom_mappings[series_title] = series_mappings
            for synonym in synonyms:
                custom_mappings[synonym] = series_mappings
    return custom_mappings
