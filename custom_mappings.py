# coding=utf-8
import os
import logging
from typing import List
from dataclasses import dataclass

from ruyaml import YAML


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
        file = open(MAPPING_FILE, "r")
        yaml = YAML(typ='safe')
        file_mappings = yaml.load(file)

        for file_entry in file_mappings['entries']:
            series_title = str(file_entry['title']).lower()
            series_mappings: List[AnilistCustomMapping] = []
            for file_season in file_entry['seasons']:
                season = file_season['season']
                anilist_id = file_season['anilist-id']
                start = 1
                if 'start' in file_season:
                    start = file_season['start']

                logger.info(
                    f"[MAPPING] Adding custom mapping | title: {series_title} | season: {season} | anilist id: {anilist_id} | start: {start}"
                )
                series_mappings.append(AnilistCustomMapping(season, anilist_id, start))

            custom_mappings[series_title] = series_mappings
    return custom_mappings
