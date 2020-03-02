import logging
import re
import sys

from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer

plex_settings = dict()


class PlexWatchedSeries:

    def __init__(self, title, year, episodes_watched, total_seasons):
        self.series_id = id
        self.title = title
        self.year = year
        self.episodes_watched = episodes_watched
        self.total_seasons = total_seasons


def authenticate():
    method = plex_settings['authentication_method'].lower()
    try:
        home_user_sync = plex_settings['home_user_sync'].lower()
        home_username = plex_settings['home_username']
        home_server_base_url = plex_settings['home_server_base_url']
    except Exception as e:
        home_user_sync = 'false'
        home_username = ''
        home_server_base_url = ''

    try:
        # Direct connection
        if method == 'direct':
            base_url = plex_settings['base_url']
            token = plex_settings['token']
            plex = PlexServer(base_url, token)

        # Myplex connection
        elif method == 'myplex':
            plex_server = plex_settings['server']
            plex_user = plex_settings['myplex_user']
            plex_password = plex_settings['myplex_password']

            if home_user_sync == 'true':
                if home_username == '':
                    logging.error('Home authentication cancelled as certain home_user settings are invalid')
                    return None
                try:
                    logging.warning('Authenticating as admin for MyPlex home user: %s' % home_username)
                    plex_account = MyPlexAccount(plex_user, plex_password)
                    plex_server_home = PlexServer(home_server_base_url, plex_account.authenticationToken)

                    logging.warning('Retrieving home user information')
                    plex_user_account = plex_account.user(home_username)

                    logging.warning('Retrieving user token for MyPlex home user')
                    plex_user_token = plex_user_account.get_token(plex_server_home.machineIdentifier)

                    logging.warning('Retrieved user token for MyPlex home user')
                    plex = PlexServer(home_server_base_url, plex_user_token)
                    logging.warning('Successfully authenticated for MyPlex home user')
                except Exception as e:
                    logging.error('Error occured during Plex Home user lookup or server authentication: %s' % e)
            else:
                account = MyPlexAccount(plex_user, plex_password)
                plex = account.resource(plex_server).connect()
        else:
            logging.critical(
                '[PLEX] Failed to authenticate due to invalid settings or authentication info, exiting...')
            sys.exit()
        return plex
    except Exception as e:
        logging.error(
            'Unable to authenticate to Plex Media Server, traceback: %s' %
            (e))
        return None


def get_anime_shows():
    plex = authenticate()
    if plex is None:
        logging.error(
            'Plex authentication failed, check access to your Plex Media Server and settings')
        return None

    sections = plex_settings['anime_section'].split('|')
    shows = []
    for section in sections:
        try:
            logging.info(
                '[PLEX] Retrieving anime series from section: %s' %
                section)
            shows_search = plex.library.section(section.strip()).search()
            shows += shows_search
            logging.info(
                '[PLEX] Found %s anime series in section: %s' %
                (len(shows_search), section))
        except BaseException:
            logging.error(
                'Could not find library [%s] on your Plex Server, check the library name in AniList settings file and '
                'also verify that your library name in Plex has no trailing spaces in it' %
                section)

    return shows


def get_anime_shows_filter(show_name):
    shows = get_anime_shows()

    shows_filtered = []
    for show in shows:
        show_title_clean_without_year = show.title
        filter_title_clean_without_year = re.sub(
            '[^A-Za-z0-9]+', '', show_name)

        try:
            if '(' in show.title and ')' in show.title:
                year = re.search(r"(\d{4})", show.title).group(1)
                year_string = '(%s)' % year
                show_title_clean_without_year = show.title.replace(
                    year_string, '').strip()
                show_title_clean_without_year = re.sub(
                    '[^A-Za-z0-9]+', '', show_title_clean_without_year)
        except BaseException:
            pass

        if show.title.lower().strip() == show_name.lower().strip():
            shows_filtered.append(show)
        elif show_title_clean_without_year.lower().strip() == filter_title_clean_without_year.lower().strip():
            shows_filtered.append(show)

    if len(shows_filtered) > 0:
        logging.info(
            '[PLEX] Found matching anime series')
    else:
        logging.info(
            '[PLEX] Did not find %s in anime series' % (show_name))
    return shows_filtered


def get_watched_shows(shows):
    logging.info('[PLEX] Retrieving watch count for series')
    watched_series = []
    ovas_found = 0

    for show in shows:
        season_total = 1
        season_watched = 1
        episodes_watched = 0

        if hasattr(show, 'episodes'):
            for episode in show.episodes():
                try:
                    # If season not defined set to season 1
                    season = 1 if not episode.seasonNumber else episode.seasonNumber
                    n_episode = episode.index
                    if episode.isWatched and n_episode:
                        if (n_episode > episodes_watched and season_watched == season) or (season > season_watched):
                            season_watched = season
                            episodes_watched = n_episode
                            season_total = season
                        else:
                            episodes_watched = 0
                except Exception as e:
                    logging.error(
                        'Error during lookup_result processing, traceback: %s' %
                        e)
                    pass
            if episodes_watched > 0:
                # Add year if we have one otherwise fallback
                year = 1900
                if show.year:
                    year = show.year

                watched_show = PlexWatchedSeries(
                    show.title.strip(), year, episodes_watched, season_total)
                watched_series.append(watched_show)

                # logger.info(
                #    'Watched %s episodes of show: %s' % (
                #        episodes_watched, show.title))
        else:
            # Probably OVA but adding as series with 1 episode and season
            # Needs proper solution later on and requires changing AniList
            # class to support it properly

            if hasattr(show, 'isWatched'):
                if show.isWatched:
                    year = 1900
                    if show.year:
                        year = show.year

                    watched_show = PlexWatchedSeries(
                        show.title.strip(), show.year, 1, 1)
                    watched_series.append(watched_show)
                    ovas_found += 1

    logging.info('[PLEX] Found %s watched series' % (len(watched_series)))

    if ovas_found > 0:
        logging.info(
            '[PLEX] Watched series also contained %s releases with no episode attribute (probably movie / OVA), '
            'support for this is still experimental' %
            ovas_found)

    if watched_series is not None and len(watched_series) == 0:
        return None
    else:
        return watched_series


def get_watched_episodes_for_show_season(
        shows, watched_show_title, watched_season):
    logging.info(
        '[PLEX] Retrieving episode watch count for show: %s | season: %s' %
        (watched_show_title, watched_season))

    episodes_watched = 0
    for show in shows:
        if show.title.lower().strip() == watched_show_title.lower().strip():
            for episode in show.episodes():
                try:
                    season = 1 if not episode.seasonNumber else episode.seasonNumber
                    if season == watched_season:
                        if episode.isWatched:
                            episodes_watched += 1
                except Exception as e:
                    logging.error(
                        'Error during lookup_result processing, traceback: %s' %
                        e)
                    pass

    # logger.info('[PLEX] %s episodes watched for season: %s' % (episodes_watched, watched_season))
    return episodes_watched
