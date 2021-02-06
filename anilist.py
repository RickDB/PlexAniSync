# coding=utf-8
import collections
import json
import logging
import re
import time
from typing import Dict, List, Optional
from dataclasses import dataclass

import inflect
import requests
from guessit import guessit

from plexmodule import PlexSeason, PlexWatchedSeries
from custom_mappings import AnilistCustomMapping

logger = logging.getLogger("PlexAniSync")
custom_mappings: Dict[str, List[AnilistCustomMapping]] = {}
ANILIST_ACCESS_TOKEN = ""
ANILIST_SKIP_UPDATE = "false"
ANILIST_PLEX_EPISODE_COUNT_PRIORITY = "false"

# Set this to True for logging failed AniList matches to
# failed_matches.txt file
ANILIST_LOG_FAILED_MATCHES = False


def to_object(obj):
    keys, values = zip(*obj.items())
    # print(keys, values)
    return collections.namedtuple("X", keys)(*values)


def int_to_roman_numeral(decimal: int) -> str:
    if not isinstance(decimal, type(1)):
        return decimal
    if not 0 < decimal < 4000:
        return str(decimal)
    ints = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
    nums = ("M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I")
    result = []
    for i, number in enumerate(ints):
        count = int(decimal / number)
        result.append(nums[i] * count)
        decimal -= number * count
    return "".join(result)


def log_to_file(message: str):
    file = open("failed_matches.txt", "a+")
    file.write(f"{message}\n")
    file.close()


@dataclass
class AnilistSeries:
    anilist_id: int
    series_type: str
    series_format: str
    source: str
    status: str
    media_status: str
    progress: int
    season: str
    episodes: int
    title_english: str
    title_romaji: str
    synonyms: List[str]
    started_year: int
    ended_year: int


def search_by_id(anilist_id):
    query = """
        query ($id: Int) {
          # Define which variables will be used in the query (id)
          media: Media (id: $id, type: ANIME) {
            # Insert our variables into the query arguments
            # (id) (type: ANIME is hard-coded in the query)
            id
            type
            format
            status
            source
            season
            episodes
            title {
                romaji
                english
                native
            }
            synonyms
            startDate {
                year
            }
            endDate {
                year
            }
          }
        }
        """

    variables = {"id": anilist_id}

    url = "https://graphql.anilist.co"

    headers = {
        "Authorization": "Bearer " + ANILIST_ACCESS_TOKEN,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    response = requests.post(
        url, headers=headers, json={"query": query, "variables": variables}
    )
    check_anilist_rate_limit(response)
    return json.loads(response.content, object_hook=to_object)


def search_by_name(anilist_show_name):
    query = """
        query ($id: Int, $page: Int, $perPage: Int, $search: String) {
            Page (page: $page, perPage: $perPage) {
                pageInfo {
                    total
                    currentPage
                    lastPage
                    hasNextPage
                    perPage
                }
                media (id: $id, search: $search, type: ANIME) {
                    id
                    type
                    format
                    status
                    source
                    season
                    episodes
                    title {
                        romaji
                        english
                        native
                    }
                    synonyms
                    startDate {
                        year
                    }
                    endDate {
                        year
                    }
                }
            }
        }
        """
    variables = {"search": anilist_show_name, "page": 1, "perPage": 50}
    url = "https://graphql.anilist.co"

    headers = {
        "Authorization": "Bearer " + ANILIST_ACCESS_TOKEN,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    response = requests.post(
        url, headers=headers, json={"query": query, "variables": variables}
    )
    check_anilist_rate_limit(response)
    return json.loads(response.content, object_hook=to_object)


def fetch_user_list(username):
    query = """
        query ($username: String) {
            MediaListCollection(userName: $username, type: ANIME) {
                lists {
                    name
                    status
                    isCustomList
                    entries {
                        id
                        progress
                        status
                        repeat
                        media {
                            id
                            type
                            format
                            status
                            source
                            season
                            episodes
                            startDate {
                                year
                            }
                            endDate {
                                year
                            }
                            title {
                                romaji
                                english
                                native
                            }
                            synonyms
                        }
                    }
                }
            }
        }
        """

    variables = {"username": username}

    url = "https://graphql.anilist.co"

    headers = {
        "Authorization": "Bearer " + ANILIST_ACCESS_TOKEN,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    response = requests.post(
        url, headers=headers, json={"query": query, "variables": variables}
    )
    check_anilist_rate_limit(response)
    return json.loads(response.content, object_hook=to_object)


def process_user_list(username: str) -> Optional[List[AnilistSeries]]:
    logger.info(f"[ANILIST] Retrieving AniList list for user: {username}")
    anilist_series = []
    list_items = fetch_user_list(username)
    try:
        if not list_items:
            logger.critical(f"[ANILIST] Failed to return list for user: {username}")
            return None
        else:
            for item in list_items:
                for media_collection in item.MediaListCollection.lists:
                    if hasattr(media_collection, "entries"):
                        for list_entry in media_collection.entries:
                            if (hasattr(list_entry, "status")
                                    and list_entry.status in ["CURRENT", "PLANNING", "COMPLETED", "DROPPED", "PAUSED", "REPEATING"]
                                    and list_entry.media is not None):
                                series_obj = mediaitem_to_object(list_entry)
                                anilist_series.append(series_obj)
    except BaseException as exception:
        logger.critical(f"[ANILIST] Failed to return list for user: {username}", exception)
        return None

    logger.info(f"[ANILIST] Found {len(anilist_series)} anime series on list")
    return anilist_series


def check_anilist_rate_limit(response):
    if response.headers.get('x-ratelimit-remaining') == '0':
        logger.warning("[ANILIST] Waiting for 60 seconds because of Anilist rate-limiting")
        time.sleep(60)
    else:
        # wait a bit to not overload AniList API
        time.sleep(0.20)


def search_item_to_obj(item) -> Optional[AnilistSeries]:
    try:
        if item:
            return mediaitem_to_object(item.data)
    except BaseException:
        pass
    return None


def mediaitem_to_object(media_item) -> AnilistSeries:
    anilist_id = media_item.media.id
    series_type = ""
    series_format = ""
    source = ""
    status = ""
    media_status = ""
    progress = 0
    season = ""
    episodes = 0
    title_english = ""
    title_romaji = ""
    synonyms = []
    started_year = 0
    ended_year = 0

    if hasattr(media_item, "status"):
        status = media_item.status
    if hasattr(media_item, "progress"):
        progress = media_item.progress
    if hasattr(media_item.media, "status"):
        media_status = media_item.media.status
    if hasattr(media_item.media, "type"):
        series_type = media_item.media.type
    if hasattr(media_item.media, "format"):
        series_format = media_item.media.format
    if hasattr(media_item.media, "source"):
        source = media_item.media.source
    if hasattr(media_item.media, "season"):
        season = media_item.media.season
    if hasattr(media_item.media, "episodes"):
        episodes = media_item.media.episodes
    if hasattr(media_item.media.title, "english"):
        title_english = media_item.media.title.english
    if hasattr(media_item.media.title, "romaji"):
        title_romaji = media_item.media.title.romaji
    if hasattr(media_item.media, "synonyms"):
        synonyms = media_item.media.synonyms
    if hasattr(media_item.media.startDate, "year"):
        started_year = media_item.media.startDate.year
    if hasattr(media_item.media.endDate, "year"):
        ended_year = media_item.media.endDate.year

    series = AnilistSeries(
        anilist_id,
        series_type,
        series_format,
        source,
        status,
        media_status,
        progress,
        season,
        episodes,
        title_english,
        title_romaji,
        synonyms,
        started_year,
        ended_year,
    )
    return series


def match_to_plex(anilist_series: List[AnilistSeries], plex_series_watched: List[PlexWatchedSeries]):
    logger.info("[ANILIST] Matching Plex series to Anilist")
    for plex_series in plex_series_watched:
        plex_title = plex_series.title
        plex_title_sort = plex_series.title_sort
        plex_title_original = plex_series.title_original
        plex_title_clean = clean_title(plex_title)
        plex_title_sort_clean = clean_title(plex_title_sort)
        plex_title_original_clean = clean_title(plex_title_original)
        plex_title_clean_without_year = plex_title_clean
        plex_title_sort_clean_without_year = plex_title_sort_clean
        plex_title_original_clean_without_year = plex_title_original_clean
        plex_year = plex_series.year
        plex_seasons = plex_series.seasons

        try:
            if "(" in plex_title and ")" in plex_title:
                year = re.search(r"(\d{4})", plex_title).group(1)
                year_string = f"({year})"
                plex_title_clean_without_year = plex_title.replace(
                    year_string, ""
                ).strip()
            if "(" in plex_title_sort and ")" in plex_title_sort:
                year = re.search(r"(\d{4})", plex_title_sort).group(1)
                year_string = f"({year})"
                plex_title_sort_clean_without_year = plex_title_sort.replace(
                    year_string, ""
                ).strip()
            if "(" in plex_title_original and ")" in plex_title_original:
                year = re.search(r"(\d{4})", plex_title_original).group(1)
                year_string = f"({year})"
                plex_title_original_clean_without_year = plex_title_original.replace(
                    year_string, ""
                ).strip()
        except BaseException:
            pass

        found_match = False
        skip_year_check = False
        matched_anilist_series: List[AnilistSeries] = []

        plex_title_guessit = plex_title
        plex_title_sort_guessit = plex_title_sort
        plex_title_original_guessit = plex_title_original

        try:
            plex_title_guessit = guessit(plex_title.lower())["title"].lower()
            plex_title_sort_guessit = guessit(plex_title_sort.lower())["title"].lower()
            plex_title_original_guessit = guessit(plex_title_original.lower())[
                "title"
            ].lower()
        except Exception:
            logger.exception(
                f"Error parsing parsing guessit title for: {plex_title} | {plex_title_sort} | {plex_title_original}"
            )

        # For linting, the variable is currently unused by might be useful in
        # the future
        assert plex_title_original_guessit

        potential_titles = [
            plex_title.lower(),
            plex_title_sort.lower(),
            plex_title_original.lower(),
            plex_title_guessit,
            plex_title_sort_guessit,
            plex_title_clean,
            plex_title_sort_clean,
            plex_title_clean_without_year,
            plex_title_sort_clean_without_year,
            plex_title_original_clean_without_year,
        ]

        # Remove duplicates from potential title list
        potential_titles_cleaned = [
            i for n, i in enumerate(potential_titles) if i not in potential_titles[:n]
        ]
        potential_titles = list(potential_titles_cleaned)

        logger.info("--------------------------------------------------")
        if len(plex_seasons) == 1:
            plex_watched_episode_count = plex_seasons[0].watched_episodes
            season_mappings = retrieve_season_mappings(plex_title, 1)

            # Custom mapping check - check user list
            if season_mappings:
                watchcounts = map_watchcount_to_seasons(plex_title, season_mappings, plex_seasons[0].watched_episodes)

                for anime_id in watchcounts:
                    logger.info(
                        f"[ANILIST] Used custom mapping | title: {plex_title} | season: {1} | anilist id: {anime_id}"
                    )

                    series = find_mapped_series(anilist_series, anime_id)
                    if series:
                        logger.info(
                            f"[ANILIST] Updating series id to list: {anime_id} | Episodes watched: {watchcounts[anime_id]}"
                        )

                        update_entry(
                            plex_title,
                            plex_year,
                            watchcounts[anime_id],
                            [series],
                            True,
                        )

                    else:
                        logger.warning(
                            f"[ANILIST] Adding new series id to list: {anime_id} | Episodes watched: {watchcounts[anime_id]}"
                        )
                        add_by_id(
                            anime_id,
                            plex_title,
                            plex_year,
                            watchcounts[anime_id],
                            skip_year_check,
                        )

                # If custom match found continue to next
                continue

            # Regular matching
            if found_match is False:
                for series in anilist_series:
                    match_series_against_potential_titles(series, potential_titles, matched_anilist_series)

            # Series not listed so search for it
            if not all(matched_anilist_series) or not matched_anilist_series:
                logger.warning(f"[ANILIST] Plex series was not on your AniList list: {plex_title}")

                potential_titles_search = [
                    plex_title.lower(),
                    plex_title_sort.lower(),
                    plex_title_original.lower(),
                    plex_title_clean_without_year,
                    plex_title_sort_clean_without_year,
                    plex_title_original_clean_without_year,
                ]

                # Remove duplicates from potential title list
                potential_titles_search_cleaned = [
                    i
                    for n, i in enumerate(potential_titles_search)
                    if i not in potential_titles_search[:n]
                ]
                potential_titles_search = []
                potential_titles_search = list(potential_titles_search_cleaned)

                media_id_search = None
                for potential_title in potential_titles_search:
                    logger.warning(
                        f"[ANILIST] Searching best match using title: {potential_title}"
                    )
                    media_id_search = find_id_best_match(potential_title, plex_year)

                    if media_id_search:
                        logger.warning(
                            f"[ANILIST] Adding new series id to list: {media_id_search} | Plex episodes watched: {plex_watched_episode_count}"
                        )
                        add_by_id(
                            media_id_search,
                            plex_title,
                            plex_year,
                            plex_watched_episode_count,
                            False,
                        )
                        break

                if not media_id_search:
                    error_message = (
                        f"[ANILIST] Failed to find valid match on AniList for: {plex_title}"
                    )
                    logger.error(error_message)
                    if ANILIST_LOG_FAILED_MATCHES:
                        log_to_file(error_message)

            # Series exists on list so checking if update required
            else:
                update_entry(
                    plex_title,
                    plex_year,
                    plex_watched_episode_count,
                    matched_anilist_series,
                    skip_year_check,
                )
                matched_anilist_series = []
        elif (
            not all(matched_anilist_series)
            or not matched_anilist_series
            and len(plex_seasons) > 1
        ):
            logger.info(
                f"Found multiple seasons so using season search instead for: {plex_title}"
            )
            match_series_with_seasons(
                anilist_series,
                plex_title,
                plex_title_sort,
                plex_title_original,
                plex_year,
                plex_seasons,
            )


def match_series_with_seasons(
    anilist_series: List[AnilistSeries],
    plex_title: str,
    plex_title_sort: str,
    plex_title_original: str,
    plex_year: int,
    plex_seasons: List[PlexSeason],
):
    counter_season = 1
    counter_season_custom_mapping = 1
    custom_mapping_seasons_anilist_id = 0
    custom_mapping_season_count = 0
    plex_watched_episode_count_custom_mapping = 0

    # Check if we have custom mappings for all seasons (One Piece for example)
    if len(plex_seasons) > 1:
        while counter_season_custom_mapping <= len(plex_seasons):
            season_mappings = retrieve_season_mappings(
                plex_title, counter_season_custom_mapping
            )
            matched_id = 0
            if season_mappings:
                matched_id = season_mappings[0].anime_id
                if custom_mapping_seasons_anilist_id == 0 or matched_id == custom_mapping_seasons_anilist_id:
                    plex_watched_episode_count_custom_mapping += plex_seasons[counter_season_custom_mapping - 1].watched_episodes
                    custom_mapping_season_count += 1

            custom_mapping_seasons_anilist_id = matched_id
            counter_season_custom_mapping += 1

        # If we had custom mappings for multiple seasons with the same ID use
        # cumulative episode count and skip per season processing
        if custom_mapping_season_count > 1:
            logger.warning(
                "[ANILIST] Found same custom mapping id for multiple seasons "
                "so not using per season processing but updating as one | "
                f"title: {plex_title} anilist id: {custom_mapping_seasons_anilist_id}"
            )

            matched_anilist_series: List[AnilistSeries] = []
            for series in anilist_series:
                if custom_mapping_seasons_anilist_id == series.anilist_id:
                    matched_anilist_series.append(series)

            if matched_anilist_series:
                logger.info(
                    f"[ANILIST] Updating series id to list: {custom_mapping_seasons_anilist_id} | "
                    f"Plex episodes watched for all seasons: {plex_watched_episode_count_custom_mapping}"
                )

                update_entry(
                    plex_title,
                    plex_year,
                    plex_watched_episode_count_custom_mapping,
                    matched_anilist_series,
                    True,
                )
            else:
                logger.warning(
                    f"[ANILIST] Adding new series id to list: {custom_mapping_seasons_anilist_id} | "
                    f"Plex episodes watched for all seasons: {plex_watched_episode_count_custom_mapping}"
                )

                add_by_id(
                    custom_mapping_seasons_anilist_id,
                    plex_title,
                    plex_year,
                    plex_watched_episode_count_custom_mapping,
                    True,
                )

            if custom_mapping_season_count == len(plex_seasons):
                return

            # Start processing of any remaining seasons
            counter_season = custom_mapping_season_count + 1

    while counter_season <= len(plex_seasons):
        plex_watched_episode_count = plex_seasons[counter_season - 1].watched_episodes
        if plex_watched_episode_count == 0:
            logger.info(f"[ANILIST] Series {plex_title} has 0 watched episodes for season {counter_season}, skipping")
            counter_season += 1
            break

        matched_anilist_series = []
        skip_year_check = False
        # for first season use regular search (some redundant codecan be merged
        # later)
        if counter_season == 1:
            found_match = False
            plex_title_clean = clean_title(plex_title)
            plex_title_clean_without_year = plex_title_clean
            plex_title_sort_clean = clean_title(plex_title_sort)
            plex_title_original_clean = clean_title(plex_title_original)
            plex_title_sort_clean_without_year = plex_title_sort_clean
            plex_title_original_clean_without_year = plex_title_original_clean

            try:
                if "(" in plex_title and ")" in plex_title:
                    year = re.search(r"(\d{4})", plex_title).group(1)
                    year_string = f"({year})"
                    plex_title_clean_without_year = plex_title.replace(
                        year_string, ""
                    ).strip()
                if "(" in plex_title_sort and ")" in plex_title_sort:
                    year = re.search(r"(\d{4})", plex_title_sort).group(1)
                    year_string = f"({year})"
                    plex_title_sort_clean_without_year = plex_title_sort.replace(
                        year_string, ""
                    ).strip()
                if "(" in plex_title_original and ")" in plex_title_original:
                    year = re.search(r"(\d{4})", plex_title_original).group(1)
                    year_string = f"({year})"
                    plex_title_original_clean_without_year = plex_title_original.replace(
                        year_string, ""
                    ).strip()
            except Exception:
                logger.exception("Uncaught exception")

            plex_title_guessit = plex_title
            plex_title_sort_guessit = plex_title_sort
            plex_title_original_guessit = plex_title_original

            try:
                plex_title_guessit = guessit(plex_title.lower())["title"].lower()
                plex_title_sort_guessit = guessit(plex_title_sort.lower())[
                    "title"
                ].lower()
                plex_title_original_guessit = guessit(plex_title_original.lower())[
                    "title"
                ].lower()
            except Exception:
                logger.exception(
                    f"Error parsing parsing guessit title for: {plex_title} | {plex_title_sort} | {plex_title_original}"
                )

            # For linting, the variable is currently unused by might be useful in
            # the future
            assert plex_title_original_guessit

            potential_titles = [
                plex_title.lower(),
                plex_title_sort.lower(),
                plex_title_original.lower(),
                plex_title_guessit,
                plex_title_sort_guessit,
                plex_title_clean,
                plex_title_sort_clean,
                plex_title_clean_without_year,
                plex_title_sort_clean_without_year,
                plex_title_original_clean_without_year,
            ]

            # Remove duplicates from potential title list
            potential_titles_cleaned = [
                i
                for n, i in enumerate(potential_titles)
                if i not in potential_titles[:n]
            ]
            potential_titles = list(potential_titles_cleaned)

            season_mappings = retrieve_season_mappings(plex_title, counter_season)
            # Custom mapping check - check user list
            if season_mappings:
                watchcounts = map_watchcount_to_seasons(plex_title, season_mappings, plex_seasons[counter_season - 1].watched_episodes)

                for anime_id in watchcounts:
                    logger.info(
                        f"[ANILIST] Used custom mapping |  title: {plex_title} | season: {counter_season} | anilist id: {anime_id}"
                    )

                    series = find_mapped_series(anilist_series, anime_id)
                    if series:
                        logger.info(
                            f"[ANILIST] Updating series id to list: {anime_id} | Episodes watched: {watchcounts[anime_id]}"
                        )

                        update_entry(
                            plex_title,
                            plex_year,
                            watchcounts[anime_id],
                            [series],
                            True,
                        )

                    else:
                        logger.warning(
                            f"[ANILIST] Adding new series id to list: {anime_id} | Episodes watched: {watchcounts[anime_id]}"
                        )
                        add_by_id(
                            anime_id,
                            plex_title,
                            plex_year,
                            watchcounts[anime_id],
                            skip_year_check,
                        )

                # If custom match found continue to next
                counter_season += 1
                continue

            # Regular matching
            if found_match is False:
                for series in anilist_series:
                    match_series_against_potential_titles(series, potential_titles, matched_anilist_series)

                if found_match:
                    matched_anilist_series.append(series)
                    update_entry(
                        plex_title,
                        plex_year,
                        plex_watched_episode_count,
                        matched_anilist_series,
                        skip_year_check,
                    )
                    break

            # Series not listed so search for it
            if not all(matched_anilist_series) or not matched_anilist_series:
                logger.warning(f"[ANILIST] Plex series was not on your AniList list: {plex_title}")

                potential_titles_search = [
                    plex_title.lower(),
                    plex_title_sort.lower(),
                    plex_title_original.lower(),
                    plex_title_clean_without_year,
                    plex_title_sort_clean_without_year,
                    plex_title_original_clean_without_year,
                ]

                # Remove duplicates from potential title list
                potential_titles_search_cleaned = [
                    i
                    for n, i in enumerate(potential_titles_search)
                    if i not in potential_titles_search[:n]
                ]
                potential_titles_search = []
                potential_titles_search = list(potential_titles_search_cleaned)

                media_id_search = None
                for potential_title in potential_titles_search:
                    logger.warning(
                        f"[ANILIST] Searching best match using title: {potential_title}"
                    )
                    media_id_search = find_id_best_match(potential_title, plex_year)

                    if media_id_search:
                        logger.warning(
                            f"[ANILIST] Adding new series id to list: {media_id_search} | Plex episodes watched: {plex_watched_episode_count}"
                        )
                        add_by_id(
                            media_id_search,
                            plex_title,
                            plex_year,
                            plex_watched_episode_count,
                            False,
                        )
                        break
                    else:
                        # wait a bit to not overload AniList API
                        time.sleep(0.10)

                if not media_id_search:
                    logger.error(
                        "[ANILIST] Failed to find valid match on AniList for: %s"
                        % (plex_title)
                    )
        else:
            media_id_search = None
            # ignore the Plex year since Plex does not have years for seasons
            skip_year_check = True
            season_mappings = retrieve_season_mappings(plex_title, counter_season)
            if season_mappings:
                watchcounts = map_watchcount_to_seasons(plex_title, season_mappings, plex_seasons[counter_season - 1].watched_episodes)

                for anime_id in watchcounts:
                    logger.info(
                        f"[ANILIST] Used custom mapping |  title: {plex_title} | season: {counter_season} | anilist id: {anime_id}"
                    )

                    series = find_mapped_series(anilist_series, anime_id)
                    if series:
                        logger.info(
                            f"[ANILIST] Updating series id to list: {anime_id} | Episodes watched: {watchcounts[anime_id]}"
                        )

                        update_entry(
                            plex_title,
                            plex_year,
                            watchcounts[anime_id],
                            [series],
                            True,
                        )

                    else:
                        logger.warning(
                            f"[ANILIST] Adding new series id to list: {anime_id} | Episodes watched: {watchcounts[anime_id]}"
                        )
                        add_by_id(
                            anime_id,
                            plex_title,
                            plex_year,
                            watchcounts[anime_id],
                            skip_year_check,
                        )

                # If custom match found continue to next
                counter_season += 1
                continue
            else:
                if plex_year is not None:
                    media_id_search = find_id_season_best_match(
                        plex_title, counter_season, plex_year
                    )
                else:
                    logger.error(
                        "[ANILIST] Skipped season lookup as Plex did not supply "
                        "a show year for {plex_title}, recommend checking Plex Web "
                        "and correcting the show year manually."
                    )

            plex_title_lookup = plex_title
            if media_id_search:
                # check if already on anilist list
                series_already_listed = False
                for series in anilist_series:
                    if series.anilist_id == media_id_search:
                        # logger.warning('[ANILIST] Plex series has more than 1 season and is already on list: %s <===>%s ' %
                        # (series.id,media_id_search))
                        series_already_listed = True
                        if series.title_english is not None:
                            plex_title_lookup = series.title_english
                        elif series.title_romaji is not None:
                            plex_title_lookup = series.title_romaji

                        matched_anilist_series.append(series)
                        break

                if series_already_listed:
                    update_entry(
                        plex_title_lookup,
                        plex_year,
                        plex_watched_episode_count,
                        matched_anilist_series,
                        skip_year_check,
                    )
                    matched_anilist_series = []
                else:
                    logger.warning(
                        f"[ANILIST] Adding new series id to list: {media_id_search} | Plex episodes watched: {plex_watched_episode_count}"
                    )
                    add_by_id(
                        media_id_search,
                        plex_title_lookup,
                        plex_year,
                        plex_watched_episode_count,
                        skip_year_check,
                    )
            else:
                error_message = (
                    f"[ANILIST] Failed to find valid season title match on AniList for: {plex_title_lookup}"
                )
                logger.error(error_message)

                if ANILIST_LOG_FAILED_MATCHES:
                    log_to_file(error_message)

        counter_season += 1


def find_mapped_series(anilist_series: List[AnilistSeries], anime_id: int):
    return next(filter(lambda s: s.anilist_id == anime_id, anilist_series), None)


def match_series_against_potential_titles(
    series: AnilistSeries, potential_titles: List[str], matched_anilist_series: List[AnilistSeries]
):
    if series.title_english:
        if series.title_english.lower() in potential_titles:
            matched_anilist_series.append(series)
        else:
            series_title_english_clean = clean_title(series.title_english)
            if series_title_english_clean in potential_titles:
                matched_anilist_series.append(series)
    if series.title_romaji:
        if series.title_romaji.lower() in potential_titles:
            if series not in matched_anilist_series:
                matched_anilist_series.append(series)
        else:
            series_title_romaji_clean = clean_title(series.title_romaji)
            if series_title_romaji_clean in potential_titles:
                if series not in matched_anilist_series:
                    matched_anilist_series.append(series)
    if series.synonyms:
        for synonym in series.synonyms:
            if synonym.lower() in potential_titles:
                if series not in matched_anilist_series:
                    matched_anilist_series.append(series)
            else:
                synonym_clean = clean_title(synonym)
                if synonym_clean in potential_titles:
                    matched_anilist_series.append(series)


def update_entry(
    title: str, year: int, watched_episode_count: int, matched_anilist_series: List[AnilistSeries], ignore_year: bool
):
    for series in matched_anilist_series:
        status = ""
        logger.info(f"[ANILIST] Found AniList entry for Plex title: {title}")
        if hasattr(series, "status"):
            status = series.status
        if status == "COMPLETED":
            logger.info(
                "[ANILIST] Series is already marked as completed on AniList so skipping update"
            )
            continue

        if hasattr(series, "started_year") and year != series.started_year:
            if ignore_year is False:
                logger.error(
                    f"[ANILIST] Series year did not match (skipping update) => Plex has {year} and AniList has {series.started_year}"
                )
                continue
            elif ignore_year is True:
                logger.info(
                    f"[ANILIST] Series year did not match however skip year check was given so adding anyway => "
                    f"Plex has {year} and AniList has {series.started_year}"
                )

        anilist_total_episodes = 0
        anilist_episodes_watched = 0
        anilist_media_status = ""

        if hasattr(series, "media_status"):
            anilist_media_status = series.media_status
        if hasattr(series, "episodes"):
            if series.episodes is not None:
                try:
                    anilist_total_episodes = int(series.episodes)
                except BaseException:
                    logger.error(
                        "Series has unknown total total episodes on AniList "
                        "(not an Integer), will most likely not match up properly"
                    )
                    anilist_total_episodes = 0
            else:
                logger.error(
                    "Series has no total episodes which is normal for shows "
                    "with undetermined end-date otherwise can be invalid info "
                    "on AniList (NoneType), using Plex watched count as fallback"
                )
                anilist_total_episodes = watched_episode_count
        if hasattr(series, "progress"):
            try:
                anilist_episodes_watched = int(series.progress)
            except BaseException:
                pass

        if (
            watched_episode_count >= anilist_total_episodes
            and anilist_total_episodes > 0
            and anilist_media_status == "FINISHED"
        ):
            # series completed watched
            logger.warning(
                f"[ANILIST] Plex episode watch count [{watched_episode_count}] was higher than the "
                f"one on AniList total episodes for that series [{anilist_total_episodes}] | updating "
                "AniList entry to completed"
            )

            # calculate episode difference and iterate up so activity stream
            # lists episodes watched if episode difference exceeds 32 only
            # update most recent as otherwise will flood the notification feed
            episode_difference = watched_episode_count - anilist_episodes_watched
            if episode_difference == 1 or episode_difference > 32:
                update_series(series.anilist_id, watched_episode_count, "COMPLETED")
            else:
                current_episodes_watched = anilist_episodes_watched + 1
                while current_episodes_watched <= watched_episode_count:
                    update_series(series.anilist_id, current_episodes_watched, "COMPLETED")
                    current_episodes_watched += 1
        elif (
            watched_episode_count > anilist_episodes_watched
            and anilist_total_episodes > 0
        ):
            # episode watch count higher than plex
            logger.warning(
                f"[ANILIST] Plex episode watch count [{watched_episode_count}] was higher than the one"
                f" on AniList [{anilist_episodes_watched}] which has total of {anilist_total_episodes} "
                "episodes | updating AniList entry to currently watching"
            )

            # calculate episode difference and iterate up so activity stream lists
            # episodes watched if episode difference exceeds 32 only update most
            # recent as otherwise will flood the notification feed
            episode_difference = watched_episode_count - anilist_episodes_watched
            if episode_difference == 1 or episode_difference > 32:
                update_series(series.anilist_id, watched_episode_count, "CURRENT")
            else:
                current_episodes_watched = anilist_episodes_watched + 1
                while current_episodes_watched <= watched_episode_count:
                    update_series(series.anilist_id, current_episodes_watched, "CURRENT")
                    current_episodes_watched += 1
        elif watched_episode_count == anilist_episodes_watched:
            logger.info(
                "[ANILIST] Episodes watched was the same on AniList and Plex so skipping update"
            )
        elif (
            anilist_episodes_watched > watched_episode_count
            and ANILIST_PLEX_EPISODE_COUNT_PRIORITY == "true"
        ):
            if watched_episode_count > 0:
                logger.info(
                    f"[ANILIST] Episodes watched was higher on AniList [{anilist_episodes_watched}] than on Plex [{watched_episode_count}] "
                    "however Plex episode count override is active so updating"
                )

                # Since AniList episode count is higher we don't loop thru
                # updating the notification feed and just set the AniList
                # episode count once
                update_series(series.anilist_id, watched_episode_count, "CURRENT")
            else:
                logger.info(
                    f"[ANILIST] Episodes watched was higher on AniList [{anilist_episodes_watched}] than "
                    f"on Plex [{watched_episode_count}] with Plex episode count override active however "
                    "Plex watched count is 0 so skipping update"
                )
        elif anilist_episodes_watched > watched_episode_count:
            logger.info(
                f"[ANILIST] Episodes watched was higher on AniList [{anilist_episodes_watched}] than on Plex [{watched_episode_count}] so skipping update"
            )
        elif anilist_total_episodes <= 0:
            logger.info(
                "[ANILIST] AniList total episodes was 0 so most likely invalid data"
            )


def find_id_season_best_match(title: str, season: int, year: int) -> Optional[int]:
    media_id = None
    # logger.warning('[ANILIST] Searching  AniList for title: %s | season: %s' % (title, season))
    match_title = clean_title(title)
    match_year = int(year)

    match_title_season_suffix1 = f"{match_title} {int_to_roman_numeral(season)}"
    match_title_season_suffix2 = f"{match_title} season {season}"
    match_title_season_suffix3 = f"{match_title} {season}"

    # oridinal season (1st 2nd etc..)
    try:
        p_engine = inflect.engine()
        match_title_season_suffix4 = f"{match_title} {p_engine.ordinal(season)} season"
    except BaseException:
        logger.error(
            "Error while converting season to ordinal string, make sure Inflect pip package is installed"
        )
        match_title_season_suffix4 = match_title_season_suffix2

    # oridinal season - variation 1 (1st 2nd Thread) - see AniList ID: 21000
    try:
        p_engine = inflect.engine()
        match_title_season_suffix5 = f"{match_title} {p_engine.ordinal(season)} thread"
    except BaseException:
        logger.error(
            "Error while converting season to ordinal string, make sure Inflect pip package is installed"
        )
        match_title_season_suffix5 = match_title_season_suffix2

    potential_titles = [
        match_title_season_suffix1.lower().strip(),
        match_title_season_suffix2.lower().strip(),
        match_title_season_suffix3.lower().strip(),
        match_title_season_suffix4.lower().strip(),
        match_title_season_suffix5.lower().strip(),
    ]

    list_items = search_by_name(title)
    if list_items:
        for item in list_items:
            if item[0] is not None and item[0].media:
                for media_item in item[0].media:
                    title_english = ""
                    title_english_for_matching = ""
                    title_romaji = ""
                    title_romaji_for_matching = ""
                    started_year = ""

                    if hasattr(media_item.title, "english") and media_item.title.english is not None:
                        title_english = media_item.title.english
                        title_english_for_matching = clean_title(title_english)
                    if hasattr(media_item.title, "romaji") and media_item.title.romaji is not None:
                        title_romaji = media_item.title.romaji
                        title_romaji_for_matching = clean_title(title_romaji)
                    if hasattr(media_item.startDate, "year") and media_item.startDate.year is not None:
                        started_year = int(media_item.startDate.year)
                    else:
                        logger.warning(
                            "[ANILIST] Anilist series did not have year attribute so skipping this result and moving to next: "
                            f"{title_english} | {title_romaji}"
                        )
                        continue

                    for potential_title in potential_titles:
                        potential_title = clean_title(potential_title)
                        # logger.info('Comparing AniList: %s | %s[%s] <===> %s' %
                        #  (title_english_for_matching, title_romaji_for_matching, started_year, potential_title))
                        if title_english_for_matching == potential_title:
                            if started_year < match_year:
                                logger.warning(
                                    f"[ANILIST] Found match: {title_english} [{media_id}] | "
                                    f"skipping as it was released before first season ({started_year} <==> {match_year})"
                                )
                            else:
                                media_id = media_item.id
                                logger.info(
                                    f"[ANILIST] Found match: {title_english} [{media_id}]"
                                )
                                break
                        if title_romaji_for_matching == potential_title:
                            if started_year < match_year:
                                logger.warning(
                                    f"[ANILIST] Found match: {title_romaji} [{media_id}] | "
                                    f"skipping as it was released before first season ({started_year} <==> {match_year})"
                                )
                            else:
                                media_id = media_item.id
                                logger.info(
                                    f"[ANILIST] Found match: {title_romaji} [{media_id}]"
                                )
                                break
    if media_id == 0:
        logger.error(f"[ANILIST] No match found for title: {title}")
    return media_id


def find_id_best_match(title: str, year: int) -> Optional[int]:
    media_id = None
    # logger.warning('[ANILIST] Searching  AniList for title: %s' % (title))
    match_title = clean_title(title)
    match_year = str(year)

    list_items = search_by_name(title)
    if list_items:
        for item in list_items:
            if item[0] is not None and item[0].media:
                for media_item in item[0].media:
                    title_english = ""
                    title_english_for_matching = ""
                    title_romaji = ""
                    title_romaji_for_matching = ""
                    synonyms = ""
                    synonyms_for_matching = ""
                    started_year = ""

                    if hasattr(media_item.title, "english") and media_item.title.english is not None:
                        title_english = media_item.title.english
                        title_english_for_matching = clean_title(title_english)
                    if hasattr(media_item.title, "romaji") and media_item.title.romaji is not None:
                        title_romaji = media_item.title.romaji
                        title_romaji_for_matching = clean_title(title_romaji)
                    if hasattr(media_item.startDate, "year"):
                        started_year = str(media_item.startDate.year)

                    # logger.info('Comparing AniList: %s | %s[%s] <===> %s[%s]' % (title_english, title_romaji, started_year, match_title, match_year))
                    if (
                        match_title == title_english_for_matching
                        and match_year == started_year
                    ):
                        media_id = media_item.id
                        logger.warning(
                            f"[ANILIST] Found match: {title_english} [{media_id}]"
                        )
                        break
                    if (
                        match_title == title_romaji_for_matching
                        and match_year == started_year
                    ):
                        media_id = media_item.id
                        logger.warning(
                            f"[ANILIST] Found match: {title_romaji} [{media_id}]"
                        )
                        break
                    if hasattr(media_item, "synonyms") and media_item.synonyms is not None:
                        for synonym in media_item.synonyms:
                            synonyms = synonym
                            synonyms_for_matching = clean_title(synonyms)
                            if (
                                match_title == synonyms_for_matching
                                and match_year == started_year
                            ):
                                media_id = media_item.id
                                logger.warning(
                                    f"[ANILIST] Found match in synonyms: {synonyms} [{media_id}]"
                                )
                                break
                    if (
                        match_title == title_romaji_for_matching
                        and match_year != started_year
                    ):
                        logger.info(
                            f"[ANILIST] Found match however started year is a mismatch: {title_romaji} [AL: {started_year} <==> Plex: {match_year}] "
                        )
                    elif (
                        match_title == title_english_for_matching
                        and match_year != started_year
                    ):
                        logger.info(
                            f"[ANILIST] Found match however started year is a mismatch: {title_english} [AL: {started_year} <==> Plex: {match_year}] "
                        )
    if media_id is None:
        logger.error(f"[ANILIST] No match found for title: {title}")
    return media_id


def add_by_id(
    anilist_id: int, plex_title: str, plex_year: int, plex_watched_episode_count: int, ignore_year: bool
):
    matched_anilist_series = []
    media_lookup_result = search_by_id(anilist_id)
    if media_lookup_result:
        anilist_obj = search_item_to_obj(media_lookup_result)
        if anilist_obj:
            matched_anilist_series.append(anilist_obj)
            update_entry(
                plex_title,
                plex_year,
                plex_watched_episode_count,
                matched_anilist_series,
                ignore_year,
            )
        else:
            logger.error(
                "[ANILIST] failed to get anilist object for list adding, skipping series"
            )
    else:
        logger.error(
            f"[ANILIST] failed to get anilist search result for id: {anilist_id}"
        )


def update_series(media_id: int, progress: int, status: str):
    if ANILIST_SKIP_UPDATE == "true":
        logger.warning("Skip update is enabled in settings so not updating this item")
        return
    query = """
        mutation ($mediaId: Int, $status: MediaListStatus, $progress: Int) {
            SaveMediaListEntry (mediaId: $mediaId, status: $status, progress: $progress) {
                id
                status,
                progress
            }
        }
        """

    variables = {"mediaId": media_id, "status": status, "progress": int(progress)}

    url = "https://graphql.anilist.co"

    headers = {
        "Authorization": "Bearer " + ANILIST_ACCESS_TOKEN,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    response = requests.post(
        url, headers=headers, json={"query": query, "variables": variables}
    )
    check_anilist_rate_limit(response)


def retrieve_season_mappings(title: str, season: int) -> List[AnilistCustomMapping]:
    season_mappings: List[AnilistCustomMapping] = []

    if custom_mappings and title.lower() in custom_mappings:
        season_mappings = custom_mappings[title.lower()]
        # filter mappings by season
        season_mappings = [e for e in season_mappings if e.season == season]

    return season_mappings


def map_watchcount_to_seasons(title: str, season_mappings: List[AnilistCustomMapping], watched_episodes: int) -> Dict[int, int]:
    # mapping from anilist-id to watched episodes
    episodes_in_anilist_entry: Dict[int, int] = {}
    total_mapped_episodes = 0
    season = season_mappings[0].season

    for mapping in season_mappings:
        if watched_episodes >= mapping.start:
            episodes_in_season = (watched_episodes - mapping.start + 1)
            total_mapped_episodes += episodes_in_season
            episodes_in_anilist_entry[mapping.anime_id] = episodes_in_season

    if total_mapped_episodes < watched_episodes:
        logger.warning(
            f"[ANILIST] Custom mapping is incomplete for {title} season {season}. "
            f"Watch count is {watched_episodes}, but number of mapped episodes is {total_mapped_episodes}"
        )

    return episodes_in_anilist_entry


def clean_title(title: str) -> str:
    return re.sub("[^A-Za-z0-9]+", "", title.lower().strip())
