import configparser
import os

config = configparser.ConfigParser()

config['PLEX'] = {
    'anime_section': os.environ.get('PLEX_SECTION'),
    'authentication_method': 'direct',
    'base_url': os.environ.get('PLEX_URL'),
    'token': os.environ.get('PLEX_TOKEN'),
}

config['ANILIST'] = {
    'username': os.environ.get('ANI_USERNAME'),
    'access_token': os.environ.get('ANI_TOKEN'),
    'plex_episode_count_priority': os.environ.get('PLEX_EPISODE_COUNT_PRIORITY') or False,
    'skip_list_update': os.environ.get('SKIP_LIST_UPDATE') or False,
    'log_failed_matches': os.environ.get('LOG_FAILED_MATCHES') or False,
    'sync_ratings': os.environ.get('SYNC_RATINGS') or False
}

with open('/plexanisync/settings.ini', 'w', encoding="UTF-8") as configfile:
    config.write(configfile)
