# coding=utf-8
import logging
import re
from dataclasses import dataclass
from typing import Dict, List, Optional

import inflect

from custom_mappings import AnilistCustomMapping
from graphql import fetch_user_list, search_by_name, search_by_id, update_series
from plexmodule import PlexWatchedSeries

logger = logging.getLogger("PlexAniSync")
CUSTOM_MAPPINGS: Dict[str, List[AnilistCustomMapping]] = {}
ANILIST_PLEX_EPISODE_COUNT_PRIORITY = False

# Set this to True for logging failed AniList matches to
# failed_matches.txt file
ANILIST_LOG_FAILED_MATCHES = False


def int_to_roman_numeral(decimal: int) -> str:
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
    file = open("failed_matches.txt", "a+", encoding="utf-8")
    file.write(f"{message}\n")
    file.close()


def clean_failed_matches_file():
    try:
        # create or overwrite the file with empty content
        open("failed_matches.txt", 'w', encoding="utf-8").close()
    except BaseException:
        pass


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


def process_user_list(username: str) -> Optional[List[AnilistSeries]]:
    logger.info(f"[ANILIST] Retrieving AniList list for user: {username}")
    anilist_series = []
    try:
        list_items = fetch_user_list(username)
        if not list_items:
            logger.critical(f"[ANILIST] Failed to return list for user: {username}")
            return None
        else:
            for item in list_items:
                for media_collection in item.MediaListCollection.lists:
                    if hasattr(media_collection, "entries"):
                        for list_entry in media_collection.entries:
                            if (hasattr(list_entry, "status")
                                    and list_entry.status in ["CURRENT", "PLANNING", "COMPLETED", "DROPPED", "PAUSED",
                                                              "REPEATING"]
                                    and list_entry.media is not None):
                                series_obj = mediaitem_to_object(list_entry)
                                anilist_series.append(series_obj)
    except BaseException as exception:
        logger.critical(f"[ANILIST] Failed to return list for user: {username}", exception)
        return None

    logger.info(f"[ANILIST] Found {len(anilist_series)} anime series on list")
    return anilist_series


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
        plex_year = plex_series.year
        plex_seasons = plex_series.seasons
        plex_anilist_id = plex_series.anilist_id

        custom_mapped_seasons = []

        logger.info("--------------------------------------------------")

        # Check if we have custom mappings for all seasons (One Piece for example)
        if len(plex_seasons) > 1:
            anilist_matches = []
            for plex_season in plex_seasons:

                season_mappings: List[AnilistCustomMapping] = retrieve_season_mappings(
                    plex_title, plex_season.season_number
                )
                if season_mappings:
                    matched_id = season_mappings[0].anime_id
                    mapped_start = season_mappings[0].start

                    custom_mapped_seasons.append(plex_season.season_number)
                    match = next(
                        (item for item in anilist_matches if item['anilist_id'] == matched_id),
                        None,
                    )

                    if not match:
                        # Create first match dict for this anilist id
                        anilist_matches.append({
                            "anilist_id": matched_id,
                            "watched_episodes": plex_season.watched_episodes - mapped_start + 1,
                            "total_episodes": plex_season.last_episode,
                            "mapped_seasons": [plex_season.season_number],
                        })
                        continue
                    # For multiple seasons with the same id
                    # If the start of this season has been mapped use that.
                    if mapped_start > 1:
                        match["watched_episodes"] = (plex_season.watched_episodes - mapped_start + 1)
                    else:
                        match["watched_episodes"] += plex_season.watched_episodes

                    # TODO support using number of last episode of the last season as a start
                    match["mapped_seasons"].append(plex_season.season_number)

            for match in anilist_matches:
                logger.info(
                    "[MAPPING] Custom Mapping of Title found | "
                    f"title: {plex_title} | anilist id: {match['anilist_id']} | "
                    f"total watched episodes: {match['watched_episodes']} | "
                    f"seasons with the same anilist id: {match['mapped_seasons']}"
                )

                add_or_update_show_by_id(
                    anilist_series, plex_title,
                    plex_year,
                    True, match['watched_episodes'],
                    match['anilist_id']
                )

        # Start processing of any remaining seasons
        for plex_season in plex_seasons:
            season_number = plex_season.season_number
            if season_number in custom_mapped_seasons:
                continue

            plex_watched_episode_count = plex_season.watched_episodes
            if plex_watched_episode_count == 0:
                logger.info(
                    f"[ANILIST] Series {plex_title} has 0 watched episodes for "
                    f"season {season_number}, skipping"
                )
                continue

            matched_anilist_series = []
            skip_year_check = False

            # for first season use regular search
            if season_number == 1:
                found_match = False
                plex_title_clean = clean_title(plex_title)
                plex_title_sort_clean = clean_title(plex_title_sort)
                plex_title_original_clean = clean_title(plex_title_original)
                plex_title_without_year = re.sub(r"\(\d{4}\)", "", plex_title).strip()
                plex_title_sort_without_year = re.sub(r"\(\d{4}\)", "", plex_title_sort).strip()
                plex_title_original_without_year = re.sub(r"\(\d{4}\)", "", plex_title_original).strip()

                potential_titles = [
                    plex_title.lower(),
                    plex_title_sort.lower(),
                    plex_title_original.lower(),
                    plex_title_clean,
                    plex_title_sort_clean,
                    plex_title_original_clean,
                    plex_title_without_year,
                    plex_title_sort_without_year,
                    plex_title_original_without_year,
                ]

                # Remove duplicates from potential title list
                potential_titles_cleaned = [
                    i
                    for n, i in enumerate(potential_titles)
                    if i not in potential_titles[:n]
                ]
                potential_titles = list(potential_titles_cleaned)

                season_mappings = retrieve_season_mappings(plex_title, season_number)
                # Custom mapping check - check user list
                if season_mappings:
                    watchcounts = map_watchcount_to_seasons(plex_title, season_mappings, plex_season.watched_episodes)

                    for anime_id, watchcount in watchcounts.items():
                        logger.info(
                            f"[ANILIST] Used custom mapping | title: {plex_title} | season: {season_number} | anilist id: {anime_id}"
                        )

                        add_or_update_show_by_id(anilist_series, plex_title, plex_year, True, watchcount, anime_id)

                    # If custom match found continue to next
                    continue

                # Reordered checks from above to ensure that custom mappings always take precedent
                if plex_anilist_id:
                    logger.info(
                        f"[ANILIST] Series {plex_title} has Anilist ID {plex_anilist_id} in its metadata, using that for updating")
                    add_or_update_show_by_id(anilist_series, plex_title, plex_year, True, plex_watched_episode_count,
                                             plex_anilist_id)
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
                        plex_title_without_year,
                        plex_title_sort_without_year,
                        plex_title_original_without_year,
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
            else:
                media_id_search = None
                # ignore the Plex year since Plex does not have years for seasons
                skip_year_check = True
                season_mappings = retrieve_season_mappings(plex_title, season_number)
                if season_mappings:
                    watchcounts = map_watchcount_to_seasons(plex_title, season_mappings, plex_season.watched_episodes)

                    for anime_id, watchcount in watchcounts.items():
                        logger.info(
                            f"[ANILIST] Used custom mapping |  title: {plex_title} | season: {season_number} | anilist id: {anime_id}"
                        )
                        add_or_update_show_by_id(anilist_series, plex_title, plex_year, True, watchcount, anime_id)

                    # If custom match found continue to next
                    continue
                else:
                    if plex_year is not None:
                        media_id_search = find_id_season_best_match(
                            plex_title, season_number, plex_year
                        )
                    else:
                        logger.error(
                            "[ANILIST] Skipped season lookup as Plex did not supply "
                            "a show year for {plex_title}, recommend checking Plex Web "
                            "and correcting the show year manually."
                        )

                plex_title_lookup = plex_title
                if media_id_search:
                    add_or_update_show_by_id(anilist_series, plex_title, plex_year, skip_year_check,
                                             plex_watched_episode_count, media_id_search)
                else:
                    error_message = (
                        f"[ANILIST] Failed to find valid season title match on AniList for: {plex_title_lookup} season {season_number}"
                    )
                    logger.error(error_message)

                    if ANILIST_LOG_FAILED_MATCHES:
                        log_to_file(error_message)


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


def find_id_season_best_match(title: str, season: int, year: int) -> Optional[int]:
    media_id = None
    # logger.warning('[ANILIST] Searching  AniList for title: %s | season: %s' % (title, season))
    match_title = clean_title(title)
    match_year = int(year)

    match_title_season_suffix1 = f"{match_title} {int_to_roman_numeral(season)}"
    match_title_season_suffix2 = f"{match_title} season {season}"
    match_title_season_suffix3 = f"{match_title} part {season}"
    match_title_season_suffix4 = f"{match_title} {season}"

    # oridinal season (1st 2nd etc..)
    try:
        p_engine = inflect.engine()
        match_title_season_suffix5 = f"{match_title} {p_engine.ordinal(season)} season"
    except BaseException:
        logger.error(
            "Error while converting season to ordinal string, make sure Inflect pip package is installed"
        )
        match_title_season_suffix5 = match_title_season_suffix2

    # oridinal season - variation 1 (1st 2nd Thread) - see AniList ID: 21000
    try:
        p_engine = inflect.engine()
        match_title_season_suffix6 = f"{match_title} {p_engine.ordinal(season)} thread"
    except BaseException:
        logger.error(
            "Error while converting season to ordinal string, make sure Inflect pip package is installed"
        )
        match_title_season_suffix6 = match_title_season_suffix2

    potential_titles = [
        match_title_season_suffix1.lower().strip(),
        match_title_season_suffix2.lower().strip(),
        match_title_season_suffix3.lower().strip(),
        match_title_season_suffix4.lower().strip(),
        match_title_season_suffix5.lower().strip(),
        match_title_season_suffix6.lower().strip(),
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


def add_or_update_show_by_id(anilist_series: List[AnilistSeries], plex_title: str, plex_year: int,
                             skip_year_check: bool, watched_episodes: int, anime_id: int):
    series = find_mapped_series(anilist_series, anime_id)
    if series:
        logger.info(
            f"[ANILIST] Updating series: {series.title_english} | Episodes watched: {watched_episodes}"
        )
        update_entry(
            plex_title,
            plex_year,
            watched_episodes,
            [series],
            skip_year_check,
        )
    else:
        logger.warning(
            f"[ANILIST] Adding new series id to list: {anime_id} | Episodes watched: {watched_episodes}"
        )
        add_by_id(
            anime_id,
            plex_title,
            plex_year,
            watched_episodes,
            skip_year_check,
        )


def add_by_id(
        anilist_id: int, plex_title: str, plex_year: int, plex_watched_episode_count: int, ignore_year: bool
):
    media_lookup_result = search_by_id(anilist_id)
    if media_lookup_result:
        anilist_obj = search_item_to_obj(media_lookup_result)
        if anilist_obj:
            update_entry(
                plex_title,
                plex_year,
                plex_watched_episode_count,
                [anilist_obj],
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


def update_entry(
        title: str, year: int, watched_episode_count: int, matched_anilist_series: List[AnilistSeries],
        ignore_year: bool
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
            return

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
                watched_episode_count >= anilist_total_episodes > 0
                and anilist_media_status == "FINISHED"
        ):
            # series completed watched
            logger.warning(
                f"[ANILIST] Plex episode watch count [{watched_episode_count}] was higher than the "
                f"one on AniList total episodes for that series [{anilist_total_episodes}] | updating "
                "AniList entry to completed"
            )

            update_episode_incremental(series, watched_episode_count, anilist_episodes_watched, "COMPLETED")
            return
        elif (
                watched_episode_count > anilist_episodes_watched
                and anilist_total_episodes > 0
        ):
            # episode watch count higher than plex
            new_status = status if status == "REPEATING" else "CURRENT"
            logger.warning(
                f"[ANILIST] Plex episode watch count [{watched_episode_count}] was higher than the one"
                f" on AniList [{anilist_episodes_watched}] which has total of {anilist_total_episodes} "
                f"episodes | updating AniList entry to {new_status}"
            )

            update_episode_incremental(series, watched_episode_count, anilist_episodes_watched, new_status)
            return

        elif watched_episode_count == anilist_episodes_watched:
            logger.info(
                "[ANILIST] Episodes watched was the same on AniList and Plex so skipping update"
            )
            return
        elif (
                anilist_episodes_watched > watched_episode_count
                and ANILIST_PLEX_EPISODE_COUNT_PRIORITY
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
                return
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


def update_episode_incremental(series: AnilistSeries, watched_episode_count: int, anilist_episodes_watched: int,
                               new_status: str):
    # calculate episode difference and iterate up so activity stream lists
    # episodes watched if episode difference exceeds 32 only update most
    # recent as otherwise will flood the notification feed
    episode_difference = watched_episode_count - anilist_episodes_watched
    if episode_difference > 32:
        update_series(series.anilist_id, watched_episode_count, new_status)
    else:
        for current_episodes_watched in range(anilist_episodes_watched + 1, watched_episode_count + 1):
            update_series(series.anilist_id, current_episodes_watched, new_status)


def retrieve_season_mappings(title: str, season: int) -> List[AnilistCustomMapping]:
    season_mappings: List[AnilistCustomMapping] = []

    if CUSTOM_MAPPINGS and title.lower() in CUSTOM_MAPPINGS:
        season_mappings = CUSTOM_MAPPINGS[title.lower()]
        # filter mappings by season
        season_mappings = [e for e in season_mappings if e.season == season]

    return season_mappings


def map_watchcount_to_seasons(title: str, season_mappings: List[AnilistCustomMapping], watched_episodes: int) -> Dict[
        int, int]:
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
