import collections
import configparser
import coloredlogs
import json
import logging
import os
import re
import requests
import sys
from guessit import guessit
from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer

# Logger settings
logger = logging.getLogger('PlexAniSync')
coloredlogs.install(fmt='%(asctime)s %(message)s', logger=logger)

# Enable this if you want to also log all messages coming from imported libraries
# coloredlogs.install(level='DEBUG')


## Settings section

# when enabled will not update your lists (for testing purposes)
emulate_list_updates = False

def read_settings(file):
    # File exists
    if not os.path.isfile(file):
        logger.critical(
            '[CONFIG] Settings file file not found: {}'.format(file))
        sys.exit()
    settings = configparser.ConfigParser()
    settings.read(file)
    return settings
settings_file = 'settings.ini'

settings = read_settings(settings_file)
anilist_settings = settings['ANILIST']
plex_settings = settings['PLEX']
ANILIST_ACCESS_TOKEN = anilist_settings['access_token']


## Plex section

class plex_watched_series:
  def __init__(self, title, year, episodes_watched,  total_seasons):
    self.series_id = id
    self.title = title
    self.year = year
    self.episodes_watched = episodes_watched
    self.total_seasons =total_seasons


def plex_authenticate():
    method = plex_settings['authentication_method'].lower()
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
        account = MyPlexAccount(plex_user, plex_password)
        plex = account.resource(plex_server).connect()
    else:
        logger.critical(
            '[PLEX] Failed to authenticate due to invalid settings or authentication info, exiting...')
        sys.exit()
    return plex


plex = plex_authenticate()

def plex_get_anime_shows():
    logger.info('[PLEX] Retrieving anime shows...')
    section = plex_settings['anime_section']
    shows = plex.library.section(section).search()
    logger.info(
        '[PLEX] Retrieving of {} anime shows completed'.format(
            len(shows)))
    return shows


def plex_get_watched_shows(shows):
    logger.info('[PLEX] Retrieving watch count for shows...')
    watched_shows =[]
    
    for show in shows:  
        season_total = 1
        season_watched = 1
        episodes_watched = 0
        for episode in show.episodes():
            try:
                # If not season defined, season 1
                season = 1 if not episode.seasonNumber else episode.seasonNumber
                n_episode = episode.index
                if episode.isWatched and n_episode:
                    if (n_episode > episodes_watched and season ==
                            season_watched) or (season > season_watched):
                        season_watched = season  
                        episodes_watched = n_episode
                        season_total = season
                    else:
                        episodes_watched = 0
            except BaseException:
                logger.error('Error during lookup_result processing')
                pass
        if episodes_watched > 0:
            # Add year if we have one otherwise fallback
            year = 1970
            if show.year:
                year = show.year
        
            watched_show = plex_watched_series(show.title, year, episodes_watched, season_total)
            watched_shows.append(watched_show)

            #logger.info(
            #    'Watched {} episodes of show: {}'.format(
            #        episodes_watched, show.title))
    logger.info('[PLEX] Retrieving watch count for shows finished')
    return watched_shows

def plex_get_watched_episodes_for_show_season(shows, watched_show_title, watched_season):
    logger.info('[PLEX] Retrieving episode watch count for show: %s | season: %s' % (watched_show_title, watched_season))
    
    episodes_watched = 0
    for show in shows:
        if show.title.lower().strip() == watched_show_title.lower().strip():    
            for episode in show.episodes():
                try:
                    season = 1 if not episode.seasonNumber else episode.seasonNumber
                    if season == watched_season:
                        if episode.isWatched:
                                episodes_watched += 1
                except BaseException:
                    logger.error('Error during lookup_result processing')
                    pass

    #logger.info('[PLEX] %s episodes watched for season: %s' % (episodes_watched, watched_season))
    return episodes_watched

## Anilist section

def to_object(o):
    keys, values = zip(*o.items())
    #print(keys, values)
    return collections.namedtuple('X', keys)(*values)


def int_to_roman_numeral(input):
    if not isinstance(input, type(1)):
        return input
    if not 0 < input < 4000:
        return input
    ints = (1000, 900,  500, 400, 100,  90, 50,  40, 10,  9,   5,  4,   1)
    nums = ('M',  'CM', 'D', 'CD','C', 'XC','L','XL','X','IX','V','IV','I')
    result = []
    for i in range(len(ints)):
        count = int(input / ints[i])
        result.append(nums[i] * count)
        input -= ints[i] * count
    return ''.join(result)

class anilist_series:
  def __init__(self, id, sType,  sFormat, source, status, media_status, progress, season, episodes, title_english, title_romaji, started_year, ended_year):
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


def anilist_search_by_id(anilist_id):
    query = '''
    query ($id: Int) { # Define which variables will be used in the query (id)
    Media (id: $id, type: ANIME) { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
        id
        type
        format
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
        'Authorization':  'Bearer ' + ANILIST_ACCESS_TOKEN,
        'Accept':  'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.post(url,headers=headers, json={'query': query, 'variables': variables})
    return json.loads(response.content, object_hook=to_object)


def anilist_search_by_name(anilist_show_name):
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
        'Authorization':  'Bearer ' + ANILIST_ACCESS_TOKEN,
        'Accept':  'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.post(url,headers=headers, json={'query': query, 'variables': variables})
    return json.loads(response.content, object_hook=to_object)

def fetch_anilist_list(username):
    query = '''
        query ($username: String) {
        MediaListCollection(userName: $username, type: ANIME) {
            statusLists {
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
                    month
                    day
                }
                endDate {
                    year
                    month
                    day
                }
                title { romaji, english, native}
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
        'Authorization':  'Bearer ' + ANILIST_ACCESS_TOKEN,
        'Accept':  'application/json',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(url, headers=headers,json={'query': query, 'variables': variables})
    #print(response.content)
    return json.loads(response.content, object_hook=to_object)


def anilist_user_list(username):
    logger.info('[AniList] Fetching AniList list for user: %s'  % (username))
    anilist_series = []
    list_items = fetch_anilist_list(username)
    try:
        if not list_items:
                logger.critical('[AniList] failed to return list for user: %s'  % (username))
        else:
            for item in list_items:
                for mediaCollection in item.MediaListCollection:
                    if hasattr(mediaCollection, 'completed'):
                        for media_item in mediaCollection.completed:
                            if media_item is not None:
                                series_obj = anilist_mediaitem_to_object(media_item)
                                anilist_series.append(series_obj)
                    if hasattr(mediaCollection, 'current'):
                        for media_item in mediaCollection.current:
                            if media_item is not None:
                                series_obj = anilist_mediaitem_to_object(media_item)
                                anilist_series.append(series_obj)
                    if hasattr(mediaCollection, 'dropped'):
                        for media_item in mediaCollection.dropped:
                            if media_item is not None:
                                series_obj = anilist_mediaitem_to_object(media_item)
                                anilist_series.append(series_obj)
                    if hasattr(mediaCollection, 'paused'):
                        for media_item in mediaCollection.paused:
                            if media_item is not None:
                                series_obj = anilist_mediaitem_to_object(media_item)
                                anilist_series.append(series_obj)
                    if hasattr(mediaCollection, 'planning'):
                        for media_item in mediaCollection.planning:
                            if media_item is not None:
                                series_obj = anilist_mediaitem_to_object(media_item)
                                anilist_series.append(series_obj)
                    if hasattr(mediaCollection, 'repeating'):
                        for media_item in mediaCollection.repeating:
                            if media_item is not None:
                                series_obj = anilist_mediaitem_to_object(media_item)
                                anilist_series.append(series_obj)    
    except:
        logger.critical('[AniList] failed to return list for user: %s'  % (username))
        
    return anilist_series

def anilist_mediaitem_to_object(media_item):
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

    series = anilist_series(id, sType, sFormat, source, status, media_status,progress, season, episodes, title_english, title_romaji, started_year, ended_year)
    return series

def match_anilist_to_plex(anilist_series, plex_series_all, plex_series_watched):
    for plex_series in plex_series_watched:
        plex_title = plex_series.title
        plex_title_clean = re.sub('[^A-Za-z0-9]+', '', plex_title.lower().strip())
        plex_title_clean_without_year = plex_title_clean
        plex_watched_episode_count = plex_series.episodes_watched
        plex_year = plex_series.year
        plex_total_seasons = plex_series.total_seasons

        try:
            if '(' in plex_title and ')' in plex_title:
                year = re.search(r"(\d{4})", plex_title).group(1)
                yearString = '(%s)' % (year)
                plex_title_clean_without_year = plex_title.replace(yearString, '').strip()
        except:
            pass

        found_match = False
        matched_anilist_series = []

        potential_titles = [
            plex_title.lower(),
            guessit(plex_title)['title'].lower(),
            plex_title_clean,
            plex_title_clean_without_year]
        
        if(plex_total_seasons == 1):
            for series in anilist_series:
                if series.title_english:
                    if series.title_english.lower() in potential_titles:
                        found_match = True
                    else:
                        series_title_english_clean =  re.sub('[^A-Za-z0-9]+', '', series.title_english).lower().strip()
                        if series_title_english_clean in potential_titles:
                            found_match = True
                if series.title_romaji and not found_match:
                    if series.title_romaji.lower() in potential_titles:
                        found_match = True
                    else:
                        series_title_romaji_clean =  re.sub('[^A-Za-z0-9]+', '', series.title_romaji).lower().strip()
                        if series_title_romaji_clean in potential_titles:
                            found_match = True

                if found_match:
                    matched_anilist_series.append(series)
                    break
                
            # Series not listed so search for it
            if not all(matched_anilist_series) or not matched_anilist_series:
                logger.error('[AniList] Plex series was not on your AniList list')
                logger.warning('[AniList] Searching best title / year match for: %s' % (plex_title)) 
                media_id_search = anilist_find_id_best_match(plex_title, plex_year)

                if not media_id_search:
                    # try alternative search title (remove year for instance in case of Plex title)
                    logger.warning('[AniList] Trying alternative title for search: %s' % (plex_title_clean))
                    media_id_search = anilist_find_id_best_match(plex_title_clean_without_year, plex_year)
                if media_id_search:
                    logger.warning('[AniList] Adding new series id to list: %s | Plex episodes watched: %s' % (media_id_search, plex_watched_episode_count))
                    anilist_series_update(media_id_search, plex_watched_episode_count, "CURRENT")
                else:
                    logger.error('[AniList] Failed to find valid match on AniList for: %s' % (plex_title))
        
            # Series exists on list so checking if update required
            else:
                update_anilist_entry(plex_title, plex_year, plex_watched_episode_count, matched_anilist_series)
                matched_anilist_series = []
        elif  not all(matched_anilist_series) or not matched_anilist_series and plex_total_seasons > 1:
            logger.info('Found multiple seasons so using season search instead')
            match_anilist_series_with_seasons(anilist_series, plex_series_all, plex_title, plex_year, plex_total_seasons)
        
def match_anilist_series_with_seasons(anilist_series, plex_series_all, plex_title, plex_year, plex_total_seasons):
        #logger.info('[AniList] Plex series has more than 1 season, using alternative season search for total of %s seasons' % (plex_total_seasons))
        counter_season = 1
        while counter_season <= plex_total_seasons:
            plex_watched_episode_count = plex_get_watched_episodes_for_show_season(plex_series_all, plex_title, counter_season)
            matched_anilist_series = [] 
            # for first season use regular search (some redundant codecan be merged later)
            if(counter_season == 1):
                found_match = False
                plex_title_clean = re.sub('[^A-Za-z0-9]+', '', plex_title.lower().strip())
                plex_title_clean_without_year = plex_title_clean
                potential_titles = [
                    plex_title.lower(),
                    guessit(plex_title)['title'].lower(),
                    plex_title_clean,
                    plex_title_clean_without_year]

                for series in anilist_series:
                    if series.title_english:
                        if series.title_english.lower() in potential_titles:
                            found_match = True
                        else:
                            series_title_english_clean =  re.sub('[^A-Za-z0-9]+', '', series.title_english).lower().strip()
                            if series_title_english_clean in potential_titles:
                                found_match = True
                    if series.title_romaji and not found_match:
                        if series.title_romaji.lower() in potential_titles:
                            found_match = True
                        else:
                            series_title_romaji_clean =  re.sub('[^A-Za-z0-9]+', '', series.title_romaji).lower().strip()
                            if series_title_romaji_clean in potential_titles:
                                found_match = True

                    if found_match:
                        matched_anilist_series.append(series)
                        update_anilist_entry(plex_title, plex_year, plex_watched_episode_count, matched_anilist_series)
                        break
                
                # Series not listed so search for it
                if not all(matched_anilist_series) or not matched_anilist_series:
                    logger.error('[AniList] Plex series was not on your AniList list')
                    logger.warning('[AniList] Searching best title / year match for: %s' % (plex_title)) 
                    media_id_search = anilist_find_id_best_match(plex_title, plex_year)

                    if not media_id_search:
                        # try alternative search title (remove year for instance in case of Plex title)
                        logger.warning('[AniList] Trying alternative title for search: %s' % (plex_title_clean))
                        media_id_search = anilist_find_id_best_match(plex_title_clean_without_year, plex_year)
                    if media_id_search:
                        logger.warning('[AniList] Adding new series id to list: %s | Plex episodes watched: %s' % (media_id_search, plex_watched_episode_count))
                        anilist_series_update(media_id_search, plex_watched_episode_count, "CURRENT")
                    else:
                        logger.error('[AniList] Failed to find valid match on AniList for: %s' % (plex_title))
            else:
                media_id_search = anilist_find_id_season_best_match(plex_title, counter_season, plex_year)
                if media_id_search:
                    # check if already on anilist list
                    series_already_listed = False
                    for series in anilist_series:
                        if series.id == media_id_search:
                            #logger.warning('[AniList] Plex series has more than 1 season and is already on list: %s <===>%s ' % (series.id,media_id_search))
                            series_already_listed = True
                            if series.title_english is not None:
                                plex_title = series.title_english
                            elif series.title_romaji is not None:
                                plex_title = series.title_romaji
                            plex_year = series.started_year
                            matched_anilist_series.append(series)
                            break

                    if series_already_listed:
                        update_anilist_entry(plex_title, plex_year, plex_watched_episode_count, matched_anilist_series)
                        matched_anilist_series = []
                    else:
                        logger.warning('[AniList] Adding new series id to list: %s | Plex episodes watched: %s' % (media_id_search, plex_watched_episode_count))
                        anilist_series_update(media_id_search, plex_watched_episode_count, "CURRENT")
                else:
                    logger.error('[AniList] Failed to find valid season title match on AniList for: %s' % (plex_title))

            counter_season += 1

def update_anilist_entry(title,  year, watched_episode_count, matched_anilist_series):
     for series in matched_anilist_series:
            status = ''
            logger.info('[AniList] Found AniList entry for plex title: %s' % (title))
            if series.status:
                status = series.status
            if status == "COMPLETED":
                logger.info('[AniList] Series is already marked as completed on AniList so skipping update')
                continue

            if year != series.started_year:
                logger.error('[AniList] Series year did not match (skipping update) => Plex has %s and AniList has %s' %  (year, series.started_year))
                continue

            anilist_total_episodes = 0
            anilist_episodes_watched = 0
            anilist_media_status = ''

            if series.media_status:
                anilist_media_status = series.media_status
            if series.episodes:
                anilist_total_episodes = int(series.episodes)
            if series.progress:
                anilist_episodes_watched = int(series.progress)

            if watched_episode_count >=  anilist_total_episodes and anilist_total_episodes is not 0 and anilist_media_status == 'FINISHED':
                # series completed watched
                logger.warning('[AniList] Plex episode watch count %s was higher than the one on AniList total episodes for that series %s, gonna update AniList entry to completed' %  (watched_episode_count, anilist_total_episodes))
                anilist_series_update(series.id, watched_episode_count, "COMPLETED")
            elif watched_episode_count > anilist_episodes_watched:
                # episode watch count higher than plex
                logger.warning('[AniList] Plex episode watch count %s was higher than the one on AniList %s, gonna update AniList entry to currently watching' %  (watched_episode_count, anilist_episodes_watched))
                anilist_series_update(series.id, watched_episode_count, "CURRENT")
            elif watched_episode_count == anilist_episodes_watched:
                logger.info('[AniList] Episodes watched was the same on AniList and Plex so skipping update')
            elif anilist_episodes_watched > watched_episode_count:
                logger.info('[AniList] Episodes watched was higher on AniList than on Plex so skipping update')

def anilist_find_id_season_best_match(title, season, year):
    media_id = None
    #logger.warning('[AniList] Searching  AniList for title: %s | season: %s' % (title, season))
    match_title =  re.sub('[^A-Za-z0-9]+', '', title).lower().strip()
    match_year = str(year)

    match_title_season_suffix1 =  '%s %s' % (match_title, int_to_roman_numeral(season))
    match_title_season_suffix2=  '%s season %s' % (match_title, season)
    match_title_season_suffix3=  '%s %s' % (match_title, season)

    potential_titles = [
        match_title_season_suffix1.lower().strip(),
        match_title_season_suffix2.lower().strip(),
        match_title_season_suffix3.lower().strip()
        ]

    list_items = anilist_search_by_name(title)
    if list_items:
        for item in list_items:
            if item[0].media:
                for media_item in item[0].media:
                    title_english = ''
                    title_romaji = ''
                    started_year = ''
                    
                    if hasattr(media_item.title, 'english'):
                        if media_item.title.english is not None:
                            title_english = media_item.title.english
                            title_english =  re.sub('[^A-Za-z0-9]+', '', title_english).lower().strip()
                    if hasattr(media_item.title, 'romaji'):
                        if media_item.title.romaji is not None:
                            title_romaji = media_item.title.romaji
                            title_romaji =  re.sub('[^A-Za-z0-9]+', '', title_romaji).lower().strip()
                    if hasattr(media_item.startDate, 'year'):
                        started_year = str(media_item.startDate.year)

                    for potential_title in potential_titles:
                        potential_title =  re.sub('[^A-Za-z0-9]+', '', potential_title).lower().strip()
                        #logger.info('Comparing AniList: %s | %s[%s] <===> %s' % (title_english, title_romaji, started_year, potential_title))
                        if title_english ==  potential_title:
                            media_id = media_item.id
                            logger.info('[AniList] Found match: %s [%s]' % (title_english, media_id))
                            break
                        if title_romaji == potential_title:
                            media_id = media_item.id
                            logger.info('[AniList] Found match: %s [%s]' % (title_romaji, media_id))
                            break
    if media_id == 0:
         logger.error('[AniList] No match found for title: %s' % (title))
    return media_id


def anilist_find_id_best_match(title, year):
    media_id = None
    #logger.warning('[AniList] Searching  AniList for title: %s' % (title))
    match_title =  re.sub('[^A-Za-z0-9]+', '', title).lower().strip()
    match_year = str(year)

    list_items = anilist_search_by_name(title)
    if list_items:
        for item in list_items:
            if item[0].media:
                for media_item in item[0].media:
                    title_english = ''
                    title_romaji = ''
                    started_year = ''
                    
                    if hasattr(media_item.title, 'english'):
                        if media_item.title.english is not None:
                            title_english = media_item.title.english
                            title_english =  re.sub('[^A-Za-z0-9]+', '', title_english).lower().strip()
                    if hasattr(media_item.title, 'romaji'):
                        if media_item.title.romaji is not None:
                            title_romaji = media_item.title.romaji
                            title_romaji =  re.sub('[^A-Za-z0-9]+', '', title_romaji).lower().strip()
                    if hasattr(media_item.startDate, 'year'):
                        started_year = str(media_item.startDate.year)

                    #logger.info('Comparing AniList: %s | %s[%s] <===> %s[%s]' % (title_english, title_romaji, started_year, match_title, match_year))
                    if match_title == title_english and match_year == started_year:
                        media_id = media_item.id
                        logger.info('[AniList] Found match: %s [%s]' % (title_english, media_id))
                        break
                    if match_title == title_romaji and match_year == started_year:
                        media_id = media_item.id
                        logger.info('[AniList] Found match: %s [%s]' % (title_romaji, media_id))
                        break
    if media_id == 0:
         logger.error('[AniList] No match found for title: %s' % (title))
    return media_id


def anilist_series_update(mediaId, progress, status):
    if anilist_settings['skip_list_update'].lower() == 'true':
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
        'Authorization':  'Bearer ' + ANILIST_ACCESS_TOKEN,
        'Accept':  'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.post(url,headers=headers, json={'query': query, 'variables': variables})
    #print(response.content)

## Startup section

def start():
    # AniList
    if anilist_settings['skip_list_update'].lower() == 'true':
        logger.warning('AniList skip list update enabled in settings, will match but NOT update your  list')

    anilist_username = anilist_settings['username']
    anilist_series = anilist_user_list(anilist_username)

    # Plex
    if not anilist_series:
        logger.error('Unable to retrieve AniList list, check your username and access token')
    else:
        plex_anime_series = plex_get_anime_shows()
        plex_series_watched = plex_get_watched_shows(plex_anime_series)
        match_anilist_to_plex(anilist_series, plex_anime_series, plex_series_watched)

        logger.info('Plex to AniList sync finished')

if __name__ == '__main__':
    start()