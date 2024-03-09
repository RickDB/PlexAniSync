# coding=utf-8
from configparser import SectionProxy
from dataclasses import dataclass
from typing import Dict, List, Optional
import logging
import regex as re
from statistics import mean
import inflect

from plexanisync.custom_mappings import AnilistCustomMapping
from plexanisync.graphql import AnilistSeries, GraphQL
from plexanisync.plexmodule import PlexWatchedSeries
from plexanisync.logger_adapter import PrefixLoggerAdapter

logger = PrefixLoggerAdapter(logging.getLogger("PlexAniSync"), {"prefix": "ANILIST"})


@dataclass
class AnilistMatch:
    anilist_id: int
    watched_episodes: int
    total_episodes: int
    mapped_seasons: List[int]
    ratings: List[int]


class Anilist:
    def __init__(self, anilist_settings: SectionProxy, custom_mappings: Dict[str, List[AnilistCustomMapping]]):
        self.anilist_settings = anilist_settings
        self.custom_mappings = custom_mappings
        self.graphql = GraphQL(anilist_settings)
        self.__clean_failed_matches_file()

    def process_user_list(self) -> Optional[List[AnilistSeries]]:
        username = self.anilist_settings["username"]
        logger.info(f"Retrieving AniList list for user: {username}")
        anilist_series = []
        try:
            anilist_series = self.graphql.fetch_user_list()
        except BaseException as exception:
            logger.critical(f"Failed to return list for user: {username}", exception)
            return None

        logger.info(f"Found {len(anilist_series)} anime series on list")
        return anilist_series

    def match_to_plex(self, anilist_series: List[AnilistSeries], plex_series_watched: List[PlexWatchedSeries]):
        logger.info("Matching Plex series to Anilist")
        for plex_series in plex_series_watched:
            plex_title = plex_series.title
            plex_title_sort = plex_series.title_sort
            plex_title_original = plex_series.title_original
            plex_guid = plex_series.guid
            plex_year = plex_series.year
            plex_seasons = plex_series.seasons
            plex_show_rating = plex_series.rating
            plex_anilist_id = plex_series.anilist_id

            custom_mapped_seasons = []

            logger.info("--------------------------------------------------")

            # Check if we have custom mappings for all seasons (One Piece for example)
            if len(plex_seasons) > 1:
                anilist_matches: List[AnilistMatch] = []
                for plex_season in plex_seasons:

                    season_mappings: List[AnilistCustomMapping] = self.__retrieve_season_mappings(
                        plex_title, plex_guid, plex_season.season_number
                    )
                    # split season -> handle it in "any remaining seasons" section
                    if season_mappings and len(season_mappings) == 1:
                        matched_id = season_mappings[0].anime_id
                        mapped_start = season_mappings[0].start

                        custom_mapped_seasons.append(plex_season.season_number)
                        match = next(
                            (item for item in anilist_matches if item.anilist_id == matched_id),
                            None,
                        )

                        if not match:
                            # Create first match dict for this anilist id
                            anilist_matches.append(AnilistMatch(
                                matched_id,
                                plex_season.watched_episodes - mapped_start + 1,
                                plex_season.last_episode,
                                [plex_season.season_number],
                                [plex_season.rating]
                            ))
                            continue
                        # For multiple seasons with the same id
                        # If the start of this season has been mapped use that.
                        # Also use the watched episode count directly for series like TMDB One Piece
                        if mapped_start != 1 or plex_season.first_episode > match.watched_episodes:
                            match.watched_episodes = plex_season.watched_episodes - mapped_start + 1
                        else:
                            match.watched_episodes += plex_season.watched_episodes

                        # TODO support using number of last episode of the last season as a start
                        match.mapped_seasons.append(plex_season.season_number)
                        match.ratings.append(plex_season.rating)

                for match in anilist_matches:
                    logger.info(
                        "Custom Mapping of Title found | "
                        f"title: {plex_title} | anilist id: {match.anilist_id} | "
                        f"total watched episodes: {match.watched_episodes} | "
                        f"seasons with the same anilist id: {match.mapped_seasons}"
                    )

                    # filter out unrated seasons
                    season_ratings = [r for r in match.ratings if r != 0]
                    # mean only works on non-empty lists
                    average_season_rating = round(mean(season_ratings)) if season_ratings else 0

                    self.__add_or_update_show_by_id(
                        anilist_series,
                        plex_title,
                        plex_year,
                        True,
                        match.watched_episodes,
                        match.anilist_id,
                        average_season_rating or plex_show_rating
                    )

            # Start processing of any remaining seasons
            for plex_season in plex_seasons:
                season_number = plex_season.season_number
                if season_number in custom_mapped_seasons:
                    continue

                plex_rating = plex_season.rating or plex_show_rating
                plex_watched_episode_count = plex_season.watched_episodes
                if plex_watched_episode_count == 0:
                    logger.info(
                        f"Series {plex_title} has 0 watched episodes for "
                        f"season {season_number}, skipping"
                    )
                    continue

                matched_anilist_series = []
                skip_year_check = False

                # for first season use regular search
                if season_number == 1:
                    found_match = False
                    plex_title_clean = self.__clean_title(plex_title)
                    plex_title_sort_clean = self.__clean_title(plex_title_sort)
                    plex_title_original_clean = self.__clean_title(plex_title_original)
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

                    season_mappings = self.__retrieve_season_mappings(plex_title, plex_guid, season_number)
                    # Custom mapping check - check user list
                    if season_mappings:
                        watchcounts = self.__map_watchcount_to_seasons(plex_title, season_mappings, plex_season.watched_episodes)

                        for anime_id, watchcount in watchcounts.items():
                            logger.info(
                                f"Used custom mapping | title: {plex_title} | season: {season_number} | anilist id: {anime_id}"
                            )

                            self.__add_or_update_show_by_id(
                                anilist_series, plex_title, plex_year, True, watchcount, anime_id, plex_rating
                            )

                        # If custom match found continue to next
                        continue

                    # Reordered checks from above to ensure that custom mappings always take precedent
                    if plex_anilist_id:
                        logger.info(
                            f"Series {plex_title} has Anilist ID {plex_anilist_id} in its metadata, using that for updating")
                        self.__add_or_update_show_by_id(anilist_series, plex_title, plex_year, True, plex_watched_episode_count,
                                                        plex_anilist_id, plex_rating)
                        continue

                    # Regular matching
                    if not found_match:
                        for series in anilist_series:
                            self.__match_series_against_potential_titles(series, potential_titles, matched_anilist_series)

                    # Series not listed so search for it
                    if not all(matched_anilist_series) or not matched_anilist_series:
                        logger.warning(f"Plex series was not on your AniList list: {plex_title}")

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
                                f"Searching best match using title: {potential_title}"
                            )
                            media_id_search = self.__find_id_best_match(potential_title, plex_year)

                            if media_id_search:
                                logger.warning(
                                    f"Adding new series id to list: {media_id_search} | Plex episodes watched: {plex_watched_episode_count}"
                                )
                                self.__add_by_id(
                                    media_id_search,
                                    plex_title,
                                    plex_year,
                                    plex_watched_episode_count,
                                    False,
                                    plex_rating
                                )
                                break

                        if not media_id_search:
                            self.__log_failed_match(f"Failed to find valid match on AniList for: {plex_title}")

                    # Series exists on list so checking if update required
                    else:
                        self.__update_entry(
                            plex_title,
                            plex_year,
                            plex_watched_episode_count,
                            matched_anilist_series,
                            skip_year_check,
                            plex_rating
                        )
                        matched_anilist_series = []
                else:
                    media_id_search = None
                    # ignore the Plex year since Plex does not have years for seasons
                    skip_year_check = True
                    season_mappings = self.__retrieve_season_mappings(plex_title, plex_guid, season_number)
                    if season_mappings:
                        watchcounts = self.__map_watchcount_to_seasons(plex_title, season_mappings, plex_season.watched_episodes)

                        for anime_id, watchcount in watchcounts.items():
                            logger.info(
                                f"Used custom mapping |  title: {plex_title} | season: {season_number} | anilist id: {anime_id}"
                            )
                            self.__add_or_update_show_by_id(
                                anilist_series, plex_title, plex_year, True, watchcount, anime_id, plex_rating
                            )

                        # If custom match found continue to next
                        continue
                    else:
                        if plex_year:
                            media_id_search = self.__find_id_season_best_match(
                                plex_title, season_number, plex_year
                            )
                        else:
                            logger.error(
                                "Skipped season lookup as Plex did not supply "
                                "a show year for {plex_title}, recommend checking Plex Web "
                                "and correcting the show year manually."
                            )

                    plex_title_lookup = plex_title
                    if media_id_search:
                        self.__add_or_update_show_by_id(
                            anilist_series, plex_title, plex_year, skip_year_check,
                            plex_watched_episode_count, media_id_search, plex_rating
                        )
                    else:
                        self.__log_failed_match(f"Failed to find valid season title match on AniList for: {plex_title_lookup} season {season_number}")

    def __int_to_roman_numeral(self, decimal: int) -> str:
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

    def __log_failed_match(self, message: str):
        logger.error(message)
        if self.anilist_settings.getboolean("log_failed_matches", False):
            with open("failed_matches.txt", "a+", encoding="utf-8") as file:
                file.write(f"{message}\n")

    def __clean_failed_matches_file(self):
        try:
            # create or overwrite the file with empty content
            with open("failed_matches.txt", 'w', encoding="utf-8"):
                pass
        except BaseException:
            pass

    def __find_mapped_series(self, anilist_series: List[AnilistSeries], anime_id: int):
        return next(filter(lambda s: s.anilist_id == anime_id, anilist_series), None)

    def __match_series_against_potential_titles(
        self, series: AnilistSeries, potential_titles: List[str], matched_anilist_series: List[AnilistSeries]
    ):
        for title in series.titles():
            if (title.lower() in potential_titles
                    or self.__clean_title(title) in potential_titles):
                if series not in matched_anilist_series:
                    matched_anilist_series.append(series)

    def __find_id_season_best_match(self, title: str, season: int, year: int) -> Optional[int]:
        media_id = None
        # logger.warning('Searching  AniList for title: %s | season: %s' % (title, season))
        match_title = self.__clean_title(title)
        match_year = int(year)

        match_title_season_suffix1 = f"{match_title} {self.__int_to_roman_numeral(season)}"
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

        matches = self.graphql.search_by_name(title)
        if matches:
            for match in matches:
                started_year = match.started_year
                if not started_year:
                    logger.warning(
                        "Anilist series did not have year attribute so skipping this result and moving to next: "
                        f"{match.title_english} | {match.title_romaji}"
                    )
                    continue

                # key = cleaned title, value = original title
                titles_for_matching = {self.__clean_title(t): t for t in match.titles()}
                for potential_title in potential_titles:
                    potential_title = self.__clean_title(potential_title)
                    # logger.info('Comparing AniList: %s | %s[%s] <===> %s' %
                    #  (titles_for_matching, started_year, potential_title))
                    if potential_title in titles_for_matching:
                        # Use original title for logging
                        original_title = titles_for_matching[potential_title]
                        if started_year < match_year:
                            logger.warning(
                                f"Found match: {original_title} [{media_id}] | "
                                f"skipping as it was released before first season ({started_year} <==> {match_year})"
                            )
                        else:
                            media_id = match.anilist_id
                            logger.info(
                                f"Found match: {original_title} [{media_id}]"
                            )
                            break
        if media_id == 0:
            logger.error(f"No match found for title: {title}")
        return media_id

    def __find_id_best_match(self, title: str, year: int) -> Optional[int]:
        media_id = None
        # logger.warning('Searching  AniList for title: %s' % (title))
        match_title = self.__clean_title(title)

        matches = self.graphql.search_by_name(title)
        if matches:
            for match in matches:
                started_year = match.started_year

                # key = cleaned title, value = original title
                titles_for_matching = {self.__clean_title(t): t for t in match.titles()}

                # logger.info('Comparing AniList: %s | %s[%s] <===> %s[%s]' % (title_english, title_romaji, started_year, match_title, match_year))
                if match_title in titles_for_matching:
                    # Use original title for logging
                    original_title = titles_for_matching[match_title]
                    if year == started_year:
                        media_id = match.anilist_id
                        logger.warning(
                            f"Found match: {original_title} [{media_id}]"
                        )
                        break
                    else:
                        logger.info(
                            f"Found match however started year is a mismatch: {original_title} [AL: {started_year} <==> Plex: {year}] "
                        )
        if media_id is None:
            logger.error(f"No match found for title: {title}")
        return media_id

    def __add_or_update_show_by_id(
        self, anilist_series: List[AnilistSeries], plex_title: str, plex_year: int,
        skip_year_check: bool, watched_episodes: int, anime_id: int, plex_rating: int
    ):
        series = self.__find_mapped_series(anilist_series, anime_id)
        if series:
            if series.progress < watched_episodes:
                logger.info(
                    f"Updating series: {series.title_english} | Episodes watched: {watched_episodes}"
                )
                self.__update_entry(
                    plex_title,
                    plex_year,
                    watched_episodes,
                    [series],
                    skip_year_check,
                    plex_rating
                )
            elif series.progress == watched_episodes:
                logger.debug("Episodes watched was the same on AniList and Plex so skipping update")
            else:
                logger.debug(
                    f"Episodes watched was higher on AniList [{series.progress}] than on Plex [{watched_episodes}] so skipping update"
                )
        else:
            logger.warning(
                f"Adding new series id to list: {anime_id} | Episodes watched: {watched_episodes}"
            )
            self.__add_by_id(
                anime_id,
                plex_title,
                plex_year,
                watched_episodes,
                skip_year_check,
                plex_rating
            )

    def __add_by_id(
        self, anilist_id: int, plex_title: str, plex_year: int, plex_watched_episode_count: int, ignore_year: bool, plex_rating: int
    ):
        media_lookup_result = self.graphql.search_by_id(anilist_id)
        if media_lookup_result:
            self.__update_entry(
                plex_title,
                plex_year,
                plex_watched_episode_count,
                [media_lookup_result],
                ignore_year,
                plex_rating
            )
        else:
            logger.error(
                f"failed to get anilist search result for id: {anilist_id}"
            )

    def __update_entry(
        self, title: str, year: int, watched_episode_count: int, matched_anilist_series: List[AnilistSeries],
        ignore_year: bool, plex_rating: int
    ):
        for series in matched_anilist_series:
            status = ""
            logger.info(f"Found AniList entry for Plex title: {title}")
            if hasattr(series, "status"):
                status = series.status

            if status == "COMPLETED":
                if plex_rating and series.score != plex_rating and self.graphql.sync_ratings:
                    logger.info(
                        "Series is completed, but Plex rating is different than Anilist score. "
                        "The Anilist score will be updated to the Plex rating."
                    )
                    self.graphql.update_score(series.anilist_id, plex_rating)
                else:
                    logger.debug(
                        "Series is already marked as completed on AniList so skipping update"
                    )
                return

            if hasattr(series, "started_year") and year != series.started_year:
                if not ignore_year:
                    logger.error(
                        f"Series year did not match (skipping update) => Plex has {year} and AniList has {series.started_year}"
                    )
                    continue
                else:
                    logger.info(
                        f"Series year did not match however skip year check was given so adding anyway => "
                        f"Plex has {year} and AniList has {series.started_year}"
                    )

            anilist_total_episodes = 0
            anilist_episodes_watched = 0
            anilist_media_status = ""

            if hasattr(series, "media_status"):
                anilist_media_status = series.media_status
            if hasattr(series, "episodes"):
                if series.episodes:
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
                    f"Plex episode watch count [{watched_episode_count}] was higher than the "
                    f"one on AniList total episodes for that series [{anilist_total_episodes}] | updating "
                    "AniList entry to completed"
                )

                self.__update_episode_incremental(series, watched_episode_count, anilist_episodes_watched, "COMPLETED", plex_rating)
                return
            elif (
                watched_episode_count > anilist_episodes_watched
                and anilist_total_episodes > 0
            ):
                # episode watch count higher than plex
                new_status = status if status == "REPEATING" else "CURRENT"
                logger.warning(
                    f"Plex episode watch count [{watched_episode_count}] was higher than the one "
                    f"on AniList [{anilist_episodes_watched}] which has total of {anilist_total_episodes} "
                    f"episodes | updating AniList entry to {new_status}"
                )

                self.__update_episode_incremental(series, watched_episode_count, anilist_episodes_watched, new_status, plex_rating)
                return
            elif watched_episode_count == anilist_episodes_watched:
                if plex_rating and series.score != plex_rating and self.graphql.sync_ratings:
                    logger.info(
                        "Episode count was up to date, but Plex score is different than Anilist score. "
                        "The Anilist score will be updated to the Plex rating."
                    )
                    self.graphql.update_score(series.anilist_id, plex_rating)
                else:
                    logger.debug(
                        "Episodes watched was the same on AniList and Plex so skipping update"
                    )
                return
            elif (
                anilist_episodes_watched > watched_episode_count
                and self.anilist_settings.getboolean("plex_episode_count_priority", False)
            ):
                if watched_episode_count > 0:
                    logger.info(
                        f"Episodes watched was higher on AniList [{anilist_episodes_watched}] than on Plex [{watched_episode_count}]. "
                        "However, Plex episode count override is active so updating."
                    )

                    # Since AniList episode count is higher we don't loop thru
                    # updating the notification feed and just set the AniList
                    # episode count once
                    self.graphql.update_series(series.anilist_id, watched_episode_count, "CURRENT", plex_rating)
                    return
                else:
                    logger.info(
                        f"Episodes watched was higher on AniList [{anilist_episodes_watched}] than "
                        f"on Plex [{watched_episode_count}] with Plex episode count override active. "
                        "However, the Plex watched count is 0 so the update is skipped."
                    )
            elif anilist_episodes_watched > watched_episode_count:
                if plex_rating and series.score != plex_rating and self.graphql.sync_ratings:
                    logger.info(
                        f"Episodes watched was higher on AniList [{anilist_episodes_watched}] than on Plex [{watched_episode_count}]. "
                        "However, the Plex rating is different than the Anilist The Anilist score will be updated to the Plex rating."
                    )
                    self.graphql.update_score(series.anilist_id, plex_rating)
                else:
                    logger.debug(
                        f"Episodes watched was higher on AniList [{anilist_episodes_watched}] than on Plex [{watched_episode_count}] so skipping update"
                    )
            elif anilist_total_episodes <= 0:
                logger.info(
                    "AniList total episodes was 0 so most likely invalid data"
                )

    def __update_episode_incremental(
        self, series: AnilistSeries, watched_episode_count: int, anilist_episodes_watched: int, new_status: str,
        plex_rating: int
    ):
        # calculate episode difference
        episode_difference = watched_episode_count - anilist_episodes_watched
        # If episode difference exceeds 32 only update most recent as otherwise will flood the notification feed.
        # Also set it to the max episode count directly if the series was completed.
        if episode_difference > 32 or new_status == "COMPLETED":
            self.graphql.update_series(series.anilist_id, watched_episode_count, new_status, plex_rating)
        else:
            # send 1 update per watched episode for the activity feed
            for current_episodes_watched in range(anilist_episodes_watched + 1, watched_episode_count + 1):
                self.graphql.update_series(series.anilist_id, current_episodes_watched, new_status, plex_rating)

    def __retrieve_season_mappings(self, title: str, guid: str, season: int) -> List[AnilistCustomMapping]:
        season_mappings: List[AnilistCustomMapping] = []

        if self.custom_mappings:
            if guid in self.custom_mappings:
                season_mappings = self.custom_mappings[guid]
            elif title.lower() in self.custom_mappings:
                season_mappings = self.custom_mappings[title.lower()]

        # filter mappings by season
        season_mappings = [e for e in season_mappings if e.season == season]
        return season_mappings

    def __map_watchcount_to_seasons(
        self, title: str, season_mappings: List[AnilistCustomMapping], watched_episodes: int
    ) -> Dict[int, int]:
        # mapping from anilist-id to watched episodes
        episodes_in_anilist_entry: Dict[int, int] = {}
        total_mapped_episodes = 0
        season = season_mappings[0].season

        # sort mappings so the one with the highest start comes first
        sorted_mapping = sorted(season_mappings, key=lambda x: x.start, reverse=True)

        for mapping in sorted_mapping:
            if watched_episodes >= mapping.start:
                episodes_in_season = watched_episodes - mapping.start - total_mapped_episodes + 1
                total_mapped_episodes += episodes_in_season
                episodes_in_anilist_entry[mapping.anime_id] = episodes_in_season

        if total_mapped_episodes < watched_episodes:
            logger.warning(
                f"Custom mapping is incomplete for {title} season {season}. "
                f"Watch count is {watched_episodes}, but number of mapped episodes is {total_mapped_episodes}"
            )

        return episodes_in_anilist_entry

    def __clean_title(self, title: str) -> str:
        return re.sub(r'[^A-Za-z0-9\p{IsHan}\p{IsBopo}\p{IsHira}\p{IsKatakana}]+', "", title.lower().strip())
