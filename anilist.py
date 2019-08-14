import collections
import configparser
import coloredlogs
import inflect
import json
import logging
import os
import re
import requests
import sys
from guessit import guessit

import plexmodule

logger = logging.getLogger('PlexAniSync')
coloredlogs.install(fmt='%(asctime)s %(message)s', logger=logger)

custom_mappings = []
ANILIST_ACCESS_TOKEN = ''
ANILIST_SKIP_UPDATE = 'false'
ANILIST_PLEX_EPISODE_COUNT_PRIORITY = 'false'

# Set this to True for logging failed AniList matches to failed_matches.txt file
ANILIST_LOG_FAILED_MATCHES = False

def to_object(o):
    keys, values = zip(*o.items())
    #print(keys, values)
    return collections.namedtuple('X', keys)(*values)


def int_to_roman_numeral(input):
    if not isinstance(input, type(1)):
        return input
    if not 0 < input < 4000:
        return input
    ints = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
    nums = (
        'M',
        'CM',
        'D',
        'CD',
        'C',
        'XC',
        'L',
        'XL',
        'X',
        'IX',
        'V',
        'IV',
        'I')
    result = []
    for i in range(len(ints)):
        count = int(input / ints[i])
        result.append(nums[i] * count)
        input -= ints[i] * count
    return ''.join(result)

def log_to_file(message):
    f=open("failed_matches.txt", "a+")
    f.write('%s\n' % (message))
    f.close()

class anilist_series:
    def __init__(
            self,
            id,
            sType,
            sFormat,
            source,
            status,
            media_status,
            progress,
            season,
            episodes,
            title_english,
            title_romaji,
            started_year,
            ended_year):
        self.id = id
        self.sType = sType
        self.sFormat = sFormat
        self.source = source
        self.status = status
        self.media_status = media_status
        self.progress = progress
        self.season = season
        self.episodes = episodes
        self.title_english = title_english
        self.title_romaji = title_romaji
        self.started_year = started_year
        self.ended_year = ended_year


class anilist_custom_mapping:
    def __init__(
            self,
            title,
            season,
            anime_id):
        self.title = title
        self.season = season
        self.anime_id = anime_id


def search_by_id(anilist_id):
    query = '''
        query ($id: Int) { # Define which variables will be used in the query (id)
        Media (id: $id, type: ANIME) { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
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
            startDate {
                year
                month
                day
            }
            endDate {
                year
                month
                day
            }
        }
        }
        '''

    variables = {
        'id': anilist_id
    }

    url = 'https://graphql.anilist.co'

    headers = {
        'Authorization': 'Bearer ' + ANILIST_ACCESS_TOKEN,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.post(
        url, headers=headers, json={
            'query': query, 'variables': variables})
    return json.loads(response.content, object_hook=to_object)


def search_by_name(anilist_show_name):
    query = '''
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
                    startDate {
                        year
                        month
                        day
                    }
                    endDate {
                        year
                        month
                        day
                    }
                }
            }
        }
        '''
    variables = {
        'search': anilist_show_name,
        'page': 1,
        'perPage': 50
    }
    url = 'https://graphql.anilist.co'

    headers = {
        'Authorization': 'Bearer ' + ANILIST_ACCESS_TOKEN,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.post(
        url, headers=headers, json={
            'query': query, 'variables': variables})
    return json.loads(response.content, object_hook=to_object)


def fetch_user_list(username):
    query = '''
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
                media{
                id
                type
                format
                status
                source
                season
                episodes
                startDate {
                    year
                    month
                    day
                }
                endDate {
                    year
                    month
                    day
                }
                title {
                    romaji
                    english
                    native
                }
                }
            }
            }
        }
        }
        '''

    variables = {
        'username': username
    }

    url = 'https://graphql.anilist.co'

    headers = {
        'Authorization': 'Bearer ' + ANILIST_ACCESS_TOKEN,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.post(
        url, headers=headers, json={
            'query': query, 'variables': variables})
    return json.loads(response.content, object_hook=to_object)


def process_user_list(username):
    logger.info('[ANILIST] Retrieving AniList list for user: %s' % (username))
    anilist_series = []
    list_items = fetch_user_list(username)
    try:
        if not list_items:
            logger.critical(
                '[ANILIST] Failed to return list for user: %s' %
                (username))
            return None
        else:
            for item in list_items:
                for mediaCollection in item.MediaListCollection.lists:
                    if hasattr(mediaCollection, 'entries'):
                        for list_entry in mediaCollection.entries:
                            if hasattr(list_entry, 'status'):
                                if list_entry.status == 'CURRENT':
                                    if list_entry.media is not None:
                                        series_obj = mediaitem_to_object(
                                            list_entry)
                                        anilist_series.append(series_obj)
                                if list_entry.status == 'PLANNING':
                                    if list_entry.media is not None:
                                        series_obj = mediaitem_to_object(
                                            list_entry)
                                        anilist_series.append(series_obj)
                                if list_entry.status == 'COMPLETED':
                                    if list_entry.media is not None:
                                        series_obj = mediaitem_to_object(
                                            list_entry)
                                        anilist_series.append(series_obj)
                                if list_entry.status == 'DROPPED':
                                    if list_entry.media is not None:
                                        series_obj = mediaitem_to_object(
                                            list_entry)
                                        anilist_series.append(series_obj)
                                if list_entry.status == 'PAUSED':
                                    if list_entry.media is not None:
                                        series_obj = mediaitem_to_object(
                                            list_entry)
                                        anilist_series.append(series_obj)
                                if list_entry.status == 'REPEATING':
                                    if list_entry.media is not None:
                                        series_obj = mediaitem_to_object(
                                            list_entry)
                                        anilist_series.append(series_obj)
    except BaseException:
        logger.critical(
            '[ANILIST] Failed to return list for user: %s' %
            (username))
        return None

    logger.info(
        '[ANILIST] Found %s anime series on list' % (len(anilist_series)))
    return anilist_series


def search_item_to_obj(item):
    try:
        if(item):
            return single_mediaitem_to_object(item.data)
    except BaseException:
        pass
    return None


def mediaitem_to_object(media_item):
    id = media_item.media.id
    sType = ''
    sFormat = ''
    source = ''
    status = ''
    media_status = ''
    progress = ''
    season = ''
    episodes = ''
    title_english = ''
    title_romaji = ''
    started_year = ''
    ended_year = ''

    if hasattr(media_item, 'status'):
        status = media_item.status
    if hasattr(media_item, 'progress'):
        progress = media_item.progress
    if hasattr(media_item.media, 'status'):
        media_status = media_item.media.status
    if hasattr(media_item.media, 'type'):
        sType = media_item.media.type
    if hasattr(media_item.media, 'format'):
        sFormat = media_item.media.format
    if hasattr(media_item.media, 'source'):
        source = media_item.media.source
    if hasattr(media_item.media, 'season'):
        season = media_item.media.season
    if hasattr(media_item.media, 'episodes'):
        episodes = media_item.media.episodes
    if hasattr(media_item.media.title, 'english'):
        title_english = media_item.media.title.english
    if hasattr(media_item.media.title, 'romaji'):
        title_romaji = media_item.media.title.romaji
    if hasattr(media_item.media.startDate, 'year'):
        started_year = media_item.media.startDate.year
    if hasattr(media_item.media.endDate, 'year'):
        ended_year = media_item.media.endDate.year

    series = anilist_series(
        id,
        sType,
        sFormat,
        source,
        status,
        media_status,
        progress,
        season,
        episodes,
        title_english,
        title_romaji,
        started_year,
        ended_year)
    return series


def single_mediaitem_to_object(media_item):
    id = media_item.Media.id
    sType = ''
    sFormat = ''
    source = ''
    status = ''
    media_status = ''
    progress = ''
    season = ''
    episodes = ''
    title_english = ''
    title_romaji = ''
    started_year = ''
    ended_year = ''

    if hasattr(media_item, 'status'):
        status = media_item.status
    if hasattr(media_item, 'progress'):
        progress = media_item.progress
    if hasattr(media_item.Media, 'status'):
        media_status = media_item.Media.status
    if hasattr(media_item.Media, 'type'):
        sType = media_item.Media.type
    if hasattr(media_item.Media, 'format'):
        sFormat = media_item.Media.format
    if hasattr(media_item.Media, 'source'):
        source = media_item.Media.source
    if hasattr(media_item.Media, 'season'):
        season = media_item.Media.season
    if hasattr(media_item.Media, 'episodes'):
        episodes = media_item.Media.episodes
    if hasattr(media_item.Media.title, 'english'):
        title_english = media_item.Media.title.english
    if hasattr(media_item.Media.title, 'romaji'):
        title_romaji = media_item.Media.title.romaji
    if hasattr(media_item.Media.startDate, 'year'):
        started_year = media_item.Media.startDate.year
    if hasattr(media_item.Media.endDate, 'year'):
        ended_year = media_item.Media.endDate.year

    series = anilist_series(
        id,
        sType,
        sFormat,
        source,
        status,
        media_status,
        progress,
        season,
        episodes,
        title_english,
        title_romaji,
        started_year,
        ended_year)
    return series


def match_to_plex(
        anilist_series,
        plex_series_all,
        plex_series_watched):
    logger.info('[ANILIST] Matching Plex series to Anilist')
    for plex_series in plex_series_watched:
        plex_title = plex_series.title
        plex_title_clean = re.sub(
            '[^A-Za-z0-9]+', '', plex_title.lower().strip())
        plex_title_clean_without_year = plex_title_clean
        plex_watched_episode_count = plex_series.episodes_watched
        plex_year = plex_series.year
        plex_total_seasons = plex_series.total_seasons

        try:
            if '(' in plex_title and ')' in plex_title:
                year = re.search(r"(\d{4})", plex_title).group(1)
                yearString = '(%s)' % (year)
                plex_title_clean_without_year = plex_title.replace(
                    yearString, '').strip()
        except BaseException:
            pass

        found_match = False
        matched_anilist_series = []

        potential_titles = [
            plex_title.lower(),
            guessit(plex_title)['title'].lower(),
            plex_title_clean,
            plex_title_clean_without_year]

        logger.info('--------------------------------------------------')
        if(plex_total_seasons == 1):
            custom_mapping_id = retrieve_custom_mapping(
                plex_title, plex_total_seasons)
            for series in anilist_series:
                if custom_mapping_id > 0 and series.id == custom_mapping_id:
                    found_match = True
                    logger.info(
                        '[ANILIST] Used custom mapping id | title: %s | season: %s | anilist id: %s' %
                        (plex_title, plex_total_seasons, custom_mapping_id))
                else:
                    if series.title_english:
                        if series.title_english.lower() in potential_titles:
                            found_match = True
                        else:
                            series_title_english_clean = re.sub(
                                '[^A-Za-z0-9]+', '', series.title_english).lower().strip()
                            if series_title_english_clean in potential_titles:
                                found_match = True
                    if series.title_romaji and not found_match:
                        if series.title_romaji.lower() in potential_titles:
                            found_match = True
                        else:
                            series_title_romaji_clean = re.sub(
                                '[^A-Za-z0-9]+', '', series.title_romaji).lower().strip()
                            if series_title_romaji_clean in potential_titles:
                                found_match = True

                if found_match:
                    matched_anilist_series.append(series)
                    break

            # Series not listed so search for it
            if not all(matched_anilist_series) or not matched_anilist_series:
                logger.warning(
                    '[ANILIST] Plex series was not on your AniList list: %s' %
                    (plex_title))

                if custom_mapping_id > 0:
                    logger.info(
                        '[ANILIST] Used custom mapping id  |  title: %s | season: %s | anilist id: %s' %
                        (plex_title, plex_total_seasons, custom_mapping_id))
                    logger.warning(
                        '[ANILIST] Adding new series id to list: %s | Plex episodes watched: %s' %
                        (custom_mapping_id, plex_watched_episode_count))
                    add_by_id(
                        custom_mapping_id,
                        plex_title,
                        plex_year,
                        plex_watched_episode_count,
                        True)
                else:
                    logger.warning(
                        '[ANILIST] Searching best title / year match for: %s' %
                        (plex_title))
                    media_id_search = find_id_best_match(
                        plex_title, plex_year)

                    if not media_id_search:
                        # try alternative search title (remove year for instance in
                        # case of Plex title)
                        logger.warning(
                            '[ANILIST] Trying alternative title for search: %s' %
                            (plex_title_clean))
                        media_id_search = find_id_best_match(
                            plex_title_clean_without_year, plex_year)
                    if media_id_search:
                        logger.warning(
                            '[ANILIST] Adding new series id to list: %s | Plex episodes watched: %s' %
                            (media_id_search, plex_watched_episode_count))
                        add_by_id(
                            media_id_search,
                            plex_title,
                            plex_year,
                            plex_watched_episode_count,
                            False)
                    else:
                        error_message = '[ANILIST] Failed to find valid match on AniList for: %s' % (plex_title)
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
                    False)
                matched_anilist_series = []
        elif not all(matched_anilist_series) or not matched_anilist_series and plex_total_seasons > 1:
            logger.info(
                'Found multiple seasons so using season search instead for: %s' %
                (plex_title))
            match_series_with_seasons(
                anilist_series,
                plex_series_all,
                plex_title,
                plex_year,
                plex_total_seasons)


def match_series_with_seasons(
        anilist_series,
        plex_series_all,
        plex_title,
        plex_year,
        plex_total_seasons):
        # logger.info('[ANILIST] Plex series has more than 1 season, using alternative season search for total of %s seasons' %
        #  (plex_total_seasons))
    counter_season = 1
    while counter_season <= plex_total_seasons:
        plex_watched_episode_count = plexmodule.get_watched_episodes_for_show_season(
            plex_series_all, plex_title, counter_season)
        matched_anilist_series = []
        # for first season use regular search (some redundant codecan be merged
        # later)
        if(counter_season == 1):
            found_match = False
            plex_title_clean = re.sub(
                '[^A-Za-z0-9]+', '', plex_title.lower().strip())
            plex_title_clean_without_year = plex_title_clean
            potential_titles = [
                plex_title.lower(),
                guessit(plex_title)['title'].lower(),
                plex_title_clean,
                plex_title_clean_without_year]

            custom_mapping_id = retrieve_custom_mapping(
                plex_title, counter_season)

            for series in anilist_series:
                if(custom_mapping_id > 0):
                    found_match = True
                    logger.info(
                        '[ANILIST] Used custom mapping id  |  title: %s | season: %s | anilist id: %s' %
                        (plex_title, counter_season, custom_mapping_id))
                else:
                    if series.title_english:
                        if series.title_english.lower() in potential_titles:
                            found_match = True
                        else:
                            series_title_english_clean = re.sub(
                                '[^A-Za-z0-9]+', '', series.title_english).lower().strip()
                            if series_title_english_clean in potential_titles:
                                found_match = True
                    if series.title_romaji and not found_match:
                        if series.title_romaji.lower() in potential_titles:
                            found_match = True
                        else:
                            series_title_romaji_clean = re.sub(
                                '[^A-Za-z0-9]+', '', series.title_romaji).lower().strip()
                            if series_title_romaji_clean in potential_titles:
                                found_match = True

                if found_match:
                    matched_anilist_series.append(series)
                    update_entry(
                        plex_title,
                        plex_year,
                        plex_watched_episode_count,
                        matched_anilist_series,
                        False)
                    break

            # Series not listed so search for it
            if not all(matched_anilist_series) or not matched_anilist_series:
                logger.error(
                    '[ANILIST] Plex series was not on your AniList list')

                if custom_mapping_id > 0:
                    logger.info(
                        '[ANILIST] Used custom mapping id |  title: %s | season: %s | anilist id: %s' %
                        (plex_title, counter_season, custom_mapping_id))
                    logger.warning(
                        '[ANILIST] Adding new series id to list: %s | Plex episodes watched: %s' %
                        (custom_mapping_id, plex_watched_episode_count))
                    add_by_id(
                        custom_mapping_id,
                        plex_title,
                        plex_year,
                        plex_watched_episode_count,
                        True)
                else:
                    logger.warning(
                        '[ANILIST] Searching best title / year match for: %s' %
                        (plex_title))
                    media_id_search = find_id_best_match(
                        plex_title, plex_year)

                    if not media_id_search:
                        # try alternative search title (remove year for instance in
                        # case of Plex title)
                        logger.warning(
                            '[ANILIST] Trying alternative title for search: %s' %
                            (plex_title_clean))
                        media_id_search = find_id_best_match(
                            plex_title_clean_without_year, plex_year)
                    if media_id_search:
                        logger.warning(
                            '[ANILIST] Adding new series id to list: %s | Plex episodes watched: %s' %
                            (media_id_search, plex_watched_episode_count))
                        add_by_id(
                            media_id_search,
                            plex_title,
                            plex_year,
                            plex_watched_episode_count,
                            False)
                    else:
                        logger.error(
                            '[ANILIST] Failed to find valid match on AniList for: %s' %
                            (plex_title))
        else:
            custom_mapping_id = retrieve_custom_mapping(
                plex_title, counter_season)
            if(custom_mapping_id > 0):
                logger.info(
                    "[MAPPING] Used custom mapping id |  title: %s | season: %s | anilist id: %s" %
                    (plex_title, counter_season, custom_mapping_id))
                media_id_search = custom_mapping_id
            else:
                media_id_search = find_id_season_best_match(
                    plex_title, counter_season, plex_year)

            if media_id_search:
                # check if already on anilist list
                series_already_listed = False
                for series in anilist_series:
                    if series.id == media_id_search:
                        # logger.warning('[ANILIST] Plex series has more than 1 season and is already on list: %s <===>%s ' %
                        # (series.id,media_id_search))
                        series_already_listed = True
                        if series.title_english is not None:
                            plex_title = series.title_english
                        elif series.title_romaji is not None:
                            plex_title = series.title_romaji
                        plex_year = series.started_year
                        matched_anilist_series.append(series)
                        break

                if series_already_listed:
                    update_entry(
                        plex_title,
                        plex_year,
                        plex_watched_episode_count,
                        matched_anilist_series,
                        False)
                    matched_anilist_series = []
                else:
                    logger.warning(
                        '[ANILIST] Adding new series id to list: %s | Plex episodes watched: %s' %
                        (media_id_search, plex_watched_episode_count))
                    add_by_id(
                        media_id_search,
                        plex_title,
                        plex_year,
                        plex_watched_episode_count,
                        False)
            else:
                error_message = '[ANILIST] Failed to find valid season title match on AniList for: %s' % (plex_title)
                logger.error(error_message)

                if ANILIST_LOG_FAILED_MATCHES:
                    log_to_file(error_message)

        counter_season += 1


def update_entry(
        title,
        year,
        watched_episode_count,
        matched_anilist_series,
        ignore_year):
    for series in matched_anilist_series:
        status = ''
        logger.info(
            '[ANILIST] Found AniList entry for Plex title: %s' %
            (title))
        if hasattr(series, 'status'):
            status = series.status
        if status == "COMPLETED":
            logger.info(
                '[ANILIST] Series is already marked as completed on AniList so skipping update')
            continue

        if hasattr(series, 'started_year'):
            if year != series.started_year:         
                if ignore_year == False:
                    logger.error(
                        '[ANILIST] Series year did not match (skipping update) => Plex has %s and AniList has %s' %
                        (year, series.started_year))
                    continue
                elif ignore_year == True:
                    logger.info(
                    '[ANILIST] Series year did not match however skip year check was given so adding anyway => Plex has %s and AniList has %s' %
                    (year, series.started_year))

        anilist_total_episodes = 0
        anilist_episodes_watched = 0
        anilist_media_status = ''

        if hasattr(series, 'media_status'):
            anilist_media_status = series.media_status
        if hasattr(series, 'episodes'):
            if series.episodes is not None:
                try:
                    anilist_total_episodes = int(series.episodes)
                except BaseException:
                    logger.error(
                        'Series has unknown total total episodes on AniList (not an Integer), will most likely not match up properly')
                    anilist_total_episodes = 0
            else:
                logger.error(
                    'Series had no total episodes or invalid info on AniList (NoneType), using Plex watched count as fallback')
                anilist_total_episodes = watched_episode_count
        if hasattr(series, 'progress'):
            try:
                anilist_episodes_watched = int(series.progress)
            except BaseException:
                pass

        if watched_episode_count >= anilist_total_episodes and anilist_total_episodes is not 0 and anilist_media_status == 'FINISHED':
            # series completed watched
            logger.warning(
                '[ANILIST] Plex episode watch count [%s] was higher than the one on AniList total episodes for that series [%s] | gonna update AniList entry to completed' %
                (watched_episode_count, anilist_total_episodes))

            # calculate episode difference and iterate up so activity stream lists episodes watched
            # if episode difference exceeds 32 only update most recent as
            # otherwise will flood the notification feed
            episode_difference = watched_episode_count - anilist_episodes_watched
            if episode_difference == 1 or episode_difference > 32:
                update_series(series.id, watched_episode_count, "COMPLETED")
            else:
                current_episodes_watched = anilist_episodes_watched + 1
                while(current_episodes_watched <= watched_episode_count):
                    update_series(
                        series.id,
                        current_episodes_watched,
                        "COMPLETED")
                    current_episodes_watched += 1
        elif watched_episode_count > anilist_episodes_watched and anilist_total_episodes is not 0:
            # episode watch count higher than plex
            logger.warning(
                '[ANILIST] Plex episode watch count [%s] was higher than the one on AniList [%s] which has total of %s episodes | gonna update AniList entry to currently watching' %
                (watched_episode_count, anilist_episodes_watched, anilist_total_episodes))

            # calculate episode difference and iterate up so activity stream lists episodes watched
            # if episode difference exceeds 32 only update most recent as
            # otherwise will flood the notification feed
            episode_difference = watched_episode_count - anilist_episodes_watched
            if episode_difference == 1 or episode_difference > 32:
                update_series(series.id, watched_episode_count, "CURRENT")
            else:
                current_episodes_watched = anilist_episodes_watched + 1
                while(current_episodes_watched <= watched_episode_count):
                    update_series(
                        series.id, current_episodes_watched, "CURRENT")
                    current_episodes_watched += 1
        elif watched_episode_count == anilist_episodes_watched:
            logger.info(
                '[ANILIST] Episodes watched was the same on AniList and Plex so skipping update')
        elif anilist_episodes_watched > watched_episode_count and ANILIST_PLEX_EPISODE_COUNT_PRIORITY == 'true':
            if watched_episode_count > 0:
                logger.info(
                    '[ANILIST] Episodes watched was higher on AniList [%s] than on Plex [%s] however Plex episode count override is active so updating' %
                    (anilist_episodes_watched, watched_episode_count))
                
                # Since AniList episode count is higher we don't loop thru updating the notification feed and just set the AniList episode count once
                update_series(series.id, watched_episode_count, "CURRENT")
            else:
                logger.info(
                    '[ANILIST] Episodes watched was higher on AniList [%s] than on Plex [%s] with Plex episode count override active however Plex watched count is 0 so skipping update' %
                    (anilist_episodes_watched, watched_episode_count))
        elif anilist_episodes_watched > watched_episode_count:
            logger.info(
                '[ANILIST] Episodes watched was higher on AniList [%s] than on Plex [%s] so skipping update' %
                (anilist_episodes_watched, watched_episode_count))
        elif anilist_total_episodes is 0:
            logger.info(
                '[ANILIST] AniList total episodes was 0 so most likely invalid data')


def find_id_season_best_match(title, season, year):
    media_id = None
    #logger.warning('[ANILIST] Searching  AniList for title: %s | season: %s' % (title, season))
    match_title = re.sub('[^A-Za-z0-9]+', '', title).lower().strip()
    match_year = int(year)

    match_title_season_suffix1 = '%s %s' % (
        match_title, int_to_roman_numeral(season))
    match_title_season_suffix2 = '%s season %s' % (match_title, season)
    match_title_season_suffix3 = '%s %s' % (match_title, season)

    # oridinal season (1st 2nd etc..)
    try:
        pEngine = inflect.engine()
        match_title_season_suffix4 = '%s %s season' % (
            match_title, pEngine.ordinal(season))
    except BaseException:
        logger.error(
            'Error while converting season to ordinal string, make sure Inflect pip package is installed')
        match_title_season_suffix4 = match_title_season_suffix2

    # oridinal season - variation 1 (1st 2nd Thread) - see AniList ID: 21000
    try:
        pEngine = inflect.engine()
        match_title_season_suffix5 = '%s %s thread' % (
            match_title, pEngine.ordinal(season))
    except BaseException:
        logger.error(
            'Error while converting season to ordinal string, make sure Inflect pip package is installed')
        match_title_season_suffix5 = match_title_season_suffix2

    potential_titles = [
        match_title_season_suffix1.lower().strip(),
        match_title_season_suffix2.lower().strip(),
        match_title_season_suffix3.lower().strip(),
        match_title_season_suffix4.lower().strip(),
        match_title_season_suffix5.lower().strip()
    ]

    list_items = search_by_name(title)
    if list_items:
        for item in list_items:
            if item[0].media:
                for media_item in item[0].media:
                    title_english = ''
                    title_english_for_matching = ''
                    title_romaji = ''
                    title_romaji_for_matching = ''
                    started_year = ''

                    if hasattr(media_item.title, 'english'):
                        if media_item.title.english is not None:
                            title_english = media_item.title.english
                            title_english_for_matching = re.sub(
                                '[^A-Za-z0-9]+', '', title_english).lower().strip()
                    if hasattr(media_item.title, 'romaji'):
                        if media_item.title.romaji is not None:
                            title_romaji = media_item.title.romaji
                            title_romaji_for_matching = re.sub(
                                '[^A-Za-z0-9]+', '', title_romaji).lower().strip()
                    if hasattr(media_item.startDate, 'year'):
                        if media_item.startDate.year is not None:
                             started_year = int(media_item.startDate.year)

                    for potential_title in potential_titles:
                        potential_title = re.sub(
                            '[^A-Za-z0-9]+', '', potential_title).lower().strip()
                        # logger.info('Comparing AniList: %s | %s[%s] <===> %s' %
                        #  (title_english_for_matching, title_romaji_for_matching, started_year, potential_title))
                        if title_english_for_matching == potential_title:
                            if started_year < match_year:
                                logger.warning(
                                    '[ANILIST] Found match: %s [%s] | skipping as it was released before first season (%s <==> %s)' %
                                    (title_english, media_id, started_year, match_year))
                            else:
                                media_id = media_item.id
                                logger.info(
                                    '[ANILIST] Found match: %s [%s]' %
                                    (title_english, media_id))
                                break
                        if title_romaji_for_matching == potential_title:
                            if started_year < match_year:
                                logger.warning(
                                    '[ANILIST] Found match: %s [%s] | skipping as it was released before first season (%s <==> %s)' %
                                    (title_romaji, media_id, started_year, match_year))
                            else:
                                media_id = media_item.id
                                logger.info(
                                    '[ANILIST] Found match: %s [%s]' %
                                    (title_romaji, media_id))
                                break
    if media_id == 0:
        logger.error('[ANILIST] No match found for title: %s' % (title))
    return media_id


def find_id_best_match(title, year):
    media_id = None
    #logger.warning('[ANILIST] Searching  AniList for title: %s' % (title))
    match_title = re.sub('[^A-Za-z0-9]+', '', title).lower().strip()
    match_year = str(year)

    list_items = search_by_name(title)
    if list_items:
        for item in list_items:
            if item[0].media:
                for media_item in item[0].media:
                    title_english = ''
                    title_english_for_matching = ''
                    title_romaji = ''
                    title_romaji_for_matching = ''
                    started_year = ''

                    if hasattr(media_item.title, 'english'):
                        if media_item.title.english is not None:
                            title_english = media_item.title.english
                            title_english_for_matching = re.sub(
                                '[^A-Za-z0-9]+', '', title_english).lower().strip()
                    if hasattr(media_item.title, 'romaji'):
                        if media_item.title.romaji is not None:
                            title_romaji = media_item.title.romaji
                            title_romaji_for_matching = re.sub(
                                '[^A-Za-z0-9]+', '', title_romaji).lower().strip()
                    if hasattr(media_item.startDate, 'year'):
                        started_year = str(media_item.startDate.year)

                    #logger.info('Comparing AniList: %s | %s[%s] <===> %s[%s]' % (title_english, title_romaji, started_year, match_title, match_year))
                    if match_title == title_english_for_matching and match_year == started_year:
                        media_id = media_item.id
                        logger.warning(
                            '[ANILIST] Found match: %s [%s]' %
                            (title_english, media_id))
                        break
                    if match_title == title_romaji_for_matching and match_year == started_year:
                        media_id = media_item.id
                        logger.warning(
                            '[ANILIST] Found match: %s [%s]' %
                            (title_romaji, media_id))
                        break
                    if match_title == title_romaji_for_matching and match_year != started_year:
                        logger.info(
                            '[ANILIST] Found match however started year is a mismatch: %s [AL: %s <==> Plex: %s] ' %
                            (title_romaji, started_year, match_year))
                    elif match_title == title_english_for_matching and match_year != started_year:
                        logger.info(
                            '[ANILIST] Found match however started year is a mismatch: %s [AL: %s <==> Plex: %s] ' %
                            (title_english, started_year, match_year))
    if media_id == 0:
        logger.error('[ANILIST] No match found for title: %s' % (title))
    return media_id


def add_by_id(
        anilist_id,
        plex_title,
        plex_year,
        plex_watched_episode_count,
        ignore_year):
    matched_anilist_series = []
    media_lookup_result = search_by_id(anilist_id)
    if(media_lookup_result):
        anilist_obj = search_item_to_obj(media_lookup_result)
        if(anilist_obj):
            matched_anilist_series.append(anilist_obj)
            update_entry(
                plex_title,
                plex_year,
                plex_watched_episode_count,
                matched_anilist_series,
                ignore_year)
        else:
            logger.error(
                '[ANILIST] failed to get anilist object for list adding, skipping series')
    else:
        logger.error(
            '[ANILIST] failed to get anilist search result for id: %s' %
            (anilist_id))


def update_series(mediaId, progress, status):
    if ANILIST_SKIP_UPDATE == 'true':
        logger.warning(
            'Skip update is enabled in settings so not updating this item')
        return
    query = '''
        mutation ($mediaId: Int, $status: MediaListStatus, $progress: Int) {
            SaveMediaListEntry (mediaId: $mediaId, status: $status, progress: $progress) {
                id
                status,
                progress
            }
        }
        '''

    variables = {
        'mediaId': mediaId,
        'status': status,
        'progress': int(progress)
    }

    url = 'https://graphql.anilist.co'

    headers = {
        'Authorization': 'Bearer ' + ANILIST_ACCESS_TOKEN,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.post(
        url, headers=headers, json={
            'query': query, 'variables': variables})
    # print(response.content)

def retrieve_custom_mapping(title, season):
    if custom_mappings:
        for mapping in custom_mappings:
            if mapping.title.lower().strip() == title.lower(
            ).strip() and str(mapping.season) == str(season):
                return mapping.anime_id

    return 0
