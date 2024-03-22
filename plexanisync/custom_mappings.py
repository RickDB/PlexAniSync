# pylint: disable=attribute-defined-outside-init
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
from ruyaml import YAML
import ruyaml
from plexanisync.logger_adapter import PrefixLoggerAdapter

logger = PrefixLoggerAdapter(logging.getLogger("PlexAniSync"), {"prefix": "MAPPING"})
MAPPING_FILE = "custom_mappings.yaml"
REMOTE_MAPPING_FILE = "remote_mappings.yaml"


@dataclass
class AnilistCustomMapping:
    season: int
    anime_id: int
    start: int

# Some classes for parsing YAML with line numbers


class Str(ruyaml.scalarstring.ScalarString):
    __slots__ = ("lc", )

    style = ""

    # pylint: disable-next=arguments-differ
    def __new__(cls, value):
        return ruyaml.scalarstring.ScalarString.__new__(cls, value)


class MyPreservedScalarString(ruyaml.scalarstring.PreservedScalarString):
    __slots__ = ("lc", )


class MyDoubleQuotedScalarString(ruyaml.scalarstring.DoubleQuotedScalarString):
    __slots__ = ("lc", )


class MySingleQuotedScalarString(ruyaml.scalarstring.SingleQuotedScalarString):
    __slots__ = ("lc", )


class MyConstructor(ruyaml.constructor.RoundTripConstructor):
    def construct_scalar(self, node):
        if not isinstance(node, ruyaml.nodes.ScalarNode):
            raise ruyaml.constructor.ConstructorError(
                None, None,
                f"expected a scalar node, but found {node.id}",
                node.start_mark)

        if node.style == '|' and isinstance(node.value, str):
            ret_val = MyPreservedScalarString(node.value)
        elif bool(self._preserve_quotes) and isinstance(node.value, str):
            if node.style == "'":
                ret_val = MySingleQuotedScalarString(node.value)
            elif node.style == '"':
                ret_val = MyDoubleQuotedScalarString(node.value)
            else:
                ret_val = Str(node.value)
        else:
            ret_val = Str(node.value)
        ret_val.lc = ruyaml.comments.LineCol()
        ret_val.lc.line = node.start_mark.line + 1
        ret_val.lc.col = node.start_mark.column
        return ret_val


def read_custom_mappings() -> Dict[str, List[AnilistCustomMapping]]:
    custom_mappings: Dict[str, List[AnilistCustomMapping]] = {}
    title_guid_mappings: Dict[str, str] = {}
    if not os.path.isfile(MAPPING_FILE):
        logger.info(f"Custom map file not found: {MAPPING_FILE}")
        return custom_mappings

    logger.info(f"Custom mapping found locally, using: {MAPPING_FILE}")

    yaml = YAML(typ='safe')
    yaml.Constructor = MyConstructor
    with open('./custom_mappings_schema.json', 'r', encoding='utf-8') as f:
        schema = json.load(f)

    # Create a Data object
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        file_mappings_local = yaml.load(f)
    try:
        # Validate data against the schema same as before.
        validate(file_mappings_local, schema)
    except ValidationError as e:
        logger.error('Custom Mappings validation failed!')

        __handle_yaml_error(file_mappings_local, e)

    remote_custom_mapping = __get_custom_mapping_remote(file_mappings_local)

    # loop through list tuple
    for value in remote_custom_mapping:
        mapping_location = value[0]
        yaml_content = value[1]
        file_mappings_remote = yaml.load(yaml_content)
        try:
            validate(file_mappings_remote, schema)
        except ValidationError as e:
            logger.error(f'Custom Mappings {mapping_location} validation failed!')
            __handle_yaml_error(file_mappings_remote, e)

        __add_mappings(custom_mappings, title_guid_mappings, mapping_location, file_mappings_remote)

    __add_mappings(custom_mappings, title_guid_mappings, MAPPING_FILE, file_mappings_local)

    return custom_mappings


def __handle_yaml_error(file_mappings_local, error):
    value = file_mappings_local
    key = None
    line = 0
    while len(error.path) > 0:
        key = error.path.popleft()
        # only objects and strings have line numbers
        if hasattr(value[key], 'lc'):
            line = value.lc.line
        value = value[key]

    if hasattr(value, 'lc'):
        logger.error(f"Line {line}: {error.message}")
    else:
        logger.error(f"Line {line}, Attribute '{key}': {error.message}")
    sys.exit(1)


def __add_mappings(custom_mappings: Dict[str, List[AnilistCustomMapping]],
                   title_guid_mappings: Dict[str, str],
                   mapping_location, file_mappings):
    # handles missing and empty 'entries'
    entries = file_mappings.get('entries', []) or []
    for file_entry in entries:
        series_title = str(file_entry['title'])
        synonyms: List[str] = file_entry.get('synonyms', [])
        guid: str = str(file_entry.get('guid', ""))
        series_mappings: List[AnilistCustomMapping] = []
        for file_season in file_entry['seasons']:
            season = file_season['season']
            anilist_id = file_season['anilist-id']
            start = file_season.get('start', 1)
            logger.debug(
                f"Adding custom mapping from {mapping_location} "
                f"| title: {series_title} | season: {season} | anilist id: {anilist_id}"
            )
            series_mappings.append(AnilistCustomMapping(season, anilist_id, start))
        if synonyms:
            logger.debug(f"{series_title} has synonyms: {synonyms}")

        if guid:
            # store the mapping under the guid if one is set
            custom_mappings[guid] = series_mappings

        for title in [series_title] + synonyms:
            title_lower = title.lower()
            if title_lower in custom_mappings:
                logger.info(f"Overwriting previous mapping for {title}")
                if title_lower in title_guid_mappings and not guid:
                    # if the current mapping doesn't have a guid, remove the guid mapping with the same title
                    # this ensures that users can override community mappings without specifying the guid field
                    custom_mappings.pop(title_guid_mappings[title_lower], None)
            custom_mappings[title_lower] = series_mappings

            if guid:
                title_guid_mappings[title_lower] = guid


# Get the custom mappings from the web.
def __get_custom_mapping_remote(file_mappings) -> List[Tuple[str, str]]:
    custom_mappings_remote: List[Tuple[str, str]] = []
    # handles missing and empty 'remote-urls'
    remote_mappings_urls: List[str] = file_mappings.get('remote-urls', []) or []

    # Get url and read the data
    for url in remote_mappings_urls:
        file_name = url.split('/')[-1]
        logger.info(f"Adding remote mapping url: {url}")

        response = requests.get(url, timeout=10)  # 10 second timeout
        if response.status_code == 200:
            custom_mappings_remote.append((file_name, response.text))
        else:
            logger.error(f"Could not download mapping file, received {response.reason}.")

    return custom_mappings_remote
