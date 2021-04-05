# coding=utf-8
import logging
import re
import sys
from typing import List, Optional
from dataclasses import dataclass

from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager

from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer
from plexapi.video import Episode, Season, Show

logger = logging.getLogger("PlexAniSync")
plex_settings = dict()


@dataclass
class PlexSeason:
    season_number: int
    watched_episodes: int


@dataclass
class PlexWatchedSeries:
    title: str
    title_sort: str
    title_original: str
    year: int
    seasons: List[PlexSeason]
    anilist_id: Optional[int]


class HostNameIgnoringAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=..., **pool_kwargs):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       assert_hostname=False,
                                       **pool_kwargs)


def authenticate():
    method = plex_settings["authentication_method"].lower()
    try:
        home_user_sync = plex_settings["home_user_sync"].lower()
        home_username = plex_settings["home_username"]
        home_server_base_url = plex_settings["home_server_base_url"]
    except Exception:
        home_user_sync = "false"
        home_username = ""
        home_server_base_url = ""

    try:
        session = Session()
        session.mount("https://", HostNameIgnoringAdapter())

        # Direct connection
        if method == "direct":
            base_url = plex_settings["base_url"]
            token = plex_settings["token"]
            plex = PlexServer(base_url, token, session)

        # Myplex connection
        elif method == "myplex":
            plex_server = plex_settings["server"]
            plex_user = plex_settings["myplex_user"]
            plex_password = plex_settings["myplex_password"]

            if home_user_sync == "true":
                if home_username == "":
                    logger.error(
                        "Home authentication cancelled as certain home_user settings are invalid"
                    )
                    return None

                logger.warning(
                    f"Authenticating as admin for MyPlex home user: {home_username}"
                )
                plex_account = MyPlexAccount(plex_user, plex_password)
                plex_server_home = PlexServer(
                    home_server_base_url, plex_account.authenticationToken, session
                )

                logger.warning("Retrieving home user information")
                plex_user_account = plex_account.user(home_username)

                logger.warning("Retrieving user token for MyPlex home user")
                plex_user_token = plex_user_account.get_token(
                    plex_server_home.machineIdentifier
                )

                logger.warning("Retrieved user token for MyPlex home user")
                plex = PlexServer(home_server_base_url, plex_user_token, session)
                logger.warning("Successfully authenticated for MyPlex home user")
            else:
                account = MyPlexAccount(plex_user, plex_password, session=session)
                plex = account.resource(plex_server).connect()
        else:
            logger.critical(
                "[PLEX] Failed to authenticate due to invalid settings or authentication info, exiting..."
            )
            sys.exit(1)
        return plex
    except Exception:
        logger.exception("Unable to authenticate to Plex Media Server")
        sys.exit(1)


def get_anime_shows() -> List[Show]:
    plex = authenticate()

    sections = plex_settings["anime_section"].split("|")
    shows: List[Show] = []
    for section in sections:
        try:
            logger.info(f"[PLEX] Retrieving anime series from section: {section}")
            shows_search = plex.library.section(section.strip()).search()
            shows += shows_search
            logger.info(
                f"[PLEX] Found {len(shows_search)} anime series in section: {section}"
            )
        except BaseException:
            logger.error(
                f"Could not find library [{section}] on your Plex Server, check the library "
                "name in AniList settings file and also verify that your library "
                "name in Plex has no trailing spaces in it"
            )

    return shows


def get_anime_shows_filter(show_name):
    shows = get_anime_shows()

    shows_filtered = []
    for show in shows:
        show_title_clean_without_year = show.title
        filter_title_clean_without_year = re.sub("[^A-Za-z0-9]+", "", show_name)

        try:
            if "(" in show.title and ")" in show.title:
                year = re.search(r"(\d{4})", show.title).group(1)
                year_string = f"({year})"
                show_title_clean_without_year = show.title.replace(
                    year_string, ""
                ).strip()
                show_title_clean_without_year = re.sub(
                    "[^A-Za-z0-9]+", "", show_title_clean_without_year
                )
        except BaseException:
            pass

        if show.title.lower().strip() == show_name.lower().strip():
            shows_filtered.append(show)
        elif (
            show_title_clean_without_year.lower().strip()
            == filter_title_clean_without_year.lower().strip()
        ):
            shows_filtered.append(show)

    if shows_filtered:
        logger.info("[PLEX] Found matching anime series")
    else:
        logger.info(f"[PLEX] Did not find {show_name} in anime series")
    return shows_filtered


def get_watched_shows(shows: List[Show]) -> Optional[List[PlexWatchedSeries]]:
    logger.info("[PLEX] Retrieving watch count for series")
    watched_series: List[PlexWatchedSeries] = []
    ovas_found = 0

    for show in shows:
        try:
            anilist_id = None
            match = re.search(r"me\.sachaw\.agents\.anilist://([0-9]+)", show.guid)
            if match:
                anilist_id = int(match.group(1))

            if hasattr(show, "seasons"):
                show_seasons = show.seasons()
                # ignore season 0 and unwatched seasons
                show_seasons = filter(lambda season: season.seasonNumber > 0 and season.viewedLeafCount > 0, show_seasons)

                seasons = []
                for season in show_seasons:
                    season_watchcount = get_watched_episodes_for_show_season(season)
                    seasons.append(PlexSeason(season.seasonNumber, season_watchcount))

                if seasons:
                    # Add year if we have one otherwise fallback
                    year = 1900
                    if show.year:
                        year = int(show.year)

                    if not hasattr(show, "titleSort"):
                        show.titleSort = show.title
                    elif show.titleSort == "":
                        show.titleSort = show.title

                    # Disable original title for now, results in false positives for yet unknown reason

                    # if not hasattr(show, 'originalTitle'):
                    #    show.originalTitle = show.title
                    # elif show.originalTitle == '':
                    #    show.originalTitle = show.title
                    show.originalTitle = show.title

                    watched_show = PlexWatchedSeries(
                        show.title.strip(),
                        show.titleSort.strip(),
                        show.originalTitle.strip(),
                        year,
                        seasons,
                        anilist_id
                    )
                    watched_series.append(watched_show)

                    # logger.info(
                    #    'Watched %s episodes of show: %s' % (
                    #        episodes_watched, show.title))
            else:
                # Probably OVA but adding as series with 1 episode and season
                # Needs proper solution later on and requires changing AniList
                # class to support it properly

                if hasattr(show, "isWatched") and show.isWatched:
                    year = 1900
                    if show.year:
                        year = int(show.year)

                    if not hasattr(show, "titleSort"):
                        show.titleSort = show.title
                    elif show.titleSort == "":
                        show.titleSort = show.title

                    # Disable original title for now, results in false positives for yet unknown reason

                    # if not hasattr(show, 'originalTitle'):
                    #    show.originalTitle = show.title
                    # elif show.originalTitle == '':
                    #    show.originalTitle = show.title
                    show.originalTitle = show.title

                    watched_show = PlexWatchedSeries(
                        show.title.strip(),
                        show.titleSort.strip(),
                        show.originalTitle.strip(),
                        year,
                        [PlexSeason(1, 1)],
                        anilist_id
                    )
                    watched_series.append(watched_show)
                    ovas_found += 1
        except Exception:
            logger.exception(f"[PLEX] Error occured during episode processing of show {show}")

    logger.info(f"[PLEX] Found {len(watched_series)} watched series")

    if ovas_found > 0:
        logger.info(
            f"[PLEX] Watched series also contained {ovas_found} releases with no episode attribute (probably movie / OVA), "
            "support for this is still experimental"
        )

    if watched_series is not None and len(watched_series) == 0:
        return None
    else:
        return watched_series


def get_watched_episodes_for_show_season(season: Season) -> int:
    watched_episodes_of_season: List[Episode] = season.watched()
    # len(watched_episodes_of_season) only works when the user didn't skip any episodes
    episodes_watched = max(map(lambda e: int(e.index), watched_episodes_of_season), default=0)

    logger.info(f'[PLEX] {episodes_watched} episodes watched for {season.parentTitle} season {season.seasonNumber}')
    return episodes_watched
