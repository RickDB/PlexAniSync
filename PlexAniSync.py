import click
import os.path
import plexapi
import requests
############################################################
# INIT
############################################################
import schedule
import signal
import sys
from pyfiglet import Figlet

cfg = None
log = None
notify = None

mapping_file = 'custom_mappings.ini'
custom_mappings = []


# Click
@click.group(help='Plex Anilist sync. Sync animes from plex server to Anilist')
@click.version_option('1.2.5', prog_name='PlexAniSync')
@click.option(
    '--config',
    envvar='PLEXANISYNC_CONFIG',
    type=click.Path(file_okay=True, dir_okay=False),
    help='Configuration file',
    show_default=True,
    default=os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "config.json")
)
@click.option(
    '--cachefile',
    envvar='PLEXANISYNC_CACHEFILE',
    type=click.Path(file_okay=True, dir_okay=False),
    help='Cache file',
    show_default=True,
    default=os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "cache.db")
)
@click.option(
    '--logfile',
    envvar='PLEXANISYNC_LOGFILE',
    type=click.Path(file_okay=True, dir_okay=False),
    help='Log file',
    show_default=True,
    default=os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "activity.log")
)
def app(config, cachefile, logfile):
    # Setup global variables
    global cfg, log, notify

    # Load config
    from misc.config import Config
    cfg = Config(configfile=config, cachefile=cachefile, logfile=logfile).cfg

    # Load logger
    from misc.log import logger
    log = logger.get_logger('PlexAniSync')

    # Load notifications
    from notifications import Notifications
    notify = Notifications()

    # Notifications
    init_notifications()


@app.command(help='Plex Connection Method (direct or myplex)', context_settings=dict(max_content_width=100))
@click.option(
    '--connect-method', '-c',
    help="Connect Plex using Direct method use which one you want to use such as direct or myplex",
    required=True
)
@click.option(
    '--home-username', '-h',
    help="Connect to home user with this user name."
)
@click.option(
    '--notifications',
    is_flag=True,
    help='Send notifications.',
    show_default=True
)
@click.option(
    '--sync-now',
    is_flag=True,
    help='Immediately start syncing Animes',
    show_default=True
)
def plex(connect_method,
         home_username=None,
         notifications=False,
         sync_now=False,
         ):
    from plexapi.server import PlexServer
    from plexapi.exceptions import BadRequest
    from plexapi.myplex import MyPlexAccount
    method = cfg.PLEX.authentication_method.lower()
    global plex_auth

    # send notification
    if not notifications and cfg.notifications.verbose:
        notify.send(message="PlexAniSync is now running.")

    if connect_method not in ["direct", "myplex"]:
        print("You need to specify which method you want to connect to such as direct or myplex")
    # Direct Connection
    elif connect_method == 'direct':
        try:
            if method != 'direct':
                log.critical("check config file connection_method is not set to direct")
                return None
            if method == 'direct':
                base_url = cfg.Direct_IP.base_url
                token = cfg.Direct_IP.token
                log.info("Authenticating with Direct Method.")
                plex_auth = PlexServer(base_url, token)

                if plex_auth.myPlexAccount().id:
                    log.info("Authenticated with account: {} and ID: {}".format(plex_auth.account().username,
                                                                                plex_auth.myPlexAccount().id))
                else:
                    log.error("Failed to Authenticated")
                    print("Failed to Authenticate  check token or base_url")
        except plexapi.exceptions.BadRequest as a:
            log.error("Error failed to connect to Plex server Check if the Plex server is running and accessible.")
            print(a)
            log.critical('Authentication failed please check token')

        except requests.exceptions.ConnectionError as err:
            log.error("Error failed to connect to the server.")
            print(err)
            print("\nCheck your base_url and see if it's correct.\n")

    # MyPlex method
    elif connect_method == 'myplex':
        try:
            if method != 'myplex':
                log.critical("check config file connection_method is not set to myplex")
                return None
            if method == 'myplex':
                server = cfg.MyPlex.server
                myplex_user = cfg.MyPlex.myplex_user
                myplex_password = cfg.MyPlex.myplex_password
                home_user_sync = cfg.MyPlex.home_user_sync
                home_user_name = cfg.MyPlex.home_username
                home_server_base_url = cfg.MyPlex.home_server_base_url

                # If home user is True
                if home_user_sync is not False:
                    if home_user_sync == '':
                        log.error('Home authentication cancelled as certain home_user settings are invalid')
                        return None
                    try:
                        log.info(home_user_sync)
                        log.info('Authenticating as admin for MyPlex home user: %s' % myplex_user)
                        plex_account = MyPlexAccount(myplex_user, myplex_password)

                        plex_home_server = PlexServer(home_server_base_url, plex_account.authenticationToken)
                        log.info('Retrieving home user information')

                        # Option to set the home user using the parameter themselves
                        if home_username is not None:
                            plex_user_account = plex_account.user(home_username)
                            log.info(
                                'Successfully retrieved home user : {}'.format(
                                    plex_account.user(home_username).username))

                            log.info('Retrieving user token for MyPlex home user')
                            plex_user_token = plex_user_account.get_token(plex_home_server.machineIdentifier)

                            log.info('Retrieved user token for MyPlex home user')
                            PlexServer(home_server_base_url, plex_user_token)
                            log.info('Successfully authenticated for MyPlex home user')
                        else:
                            plex_user_account_default = plex_account.user(home_user_name)
                            log.info(
                                'Successfully retrieved default home user : {}'.format(
                                    plex_account.user(home_user_name).username))
                            log.info('Retrieving user token for MyPlex default home user')
                            plex_user_token_default = plex_user_account_default.get_token(
                                plex_home_server.machineIdentifier)
                            log.info('Retrieved user token for MyPlex default home user')
                            PlexServer(home_server_base_url, plex_user_token_default)
                            log.info('Successfully authenticated for MyPlex default home user')

                    except plexapi.exceptions.Unauthorized as err:
                        log.error(
                            'Error Unauthorized access meaning wrong password or username check config file: %s' % err)
                    except plexapi.exceptions.BadRequest as badrequest:
                        log.error(
                            'Error BadRequest check plex server is running and accessible such as not blocked by '
                            'firewall ' % badrequest
                        )
                else:
                    account = MyPlexAccount(myplex_user, myplex_password)
                    plex_auth = account.resource(server).connect()
                    if plex_auth.myPlexAccount().id:
                        log.info(
                            "Authenticated with account: {} and ID: {}".format(plex_auth.account().username,
                                                                               plex_auth.myPlexAccount().id))
                    else:
                        log.error("Failed to Authenticated")
                        print("Failed to Authenticate  check token or base_url")
        except Exception as e:
            log.error("Failed to connect to MyPlex Account.")
            print(e)

    else:
        log.critical(
            '[PLEX] Failed to authenticate due to invalid settings or authentication info, exiting...')

    # Start Syncing if flag is provided
    if sync_now:
        # send notification
        if cfg.notifications.verbose:
            notify.send(message="Sync Mode On, starting...")
        # Read the Custom mapping file
        import anilist
        log.info("Looking for custom mapping file.")
        if not os.path.isfile(mapping_file):
            log.warning(
                '[MAPPING] Custom map file not found: %s' % mapping_file)
        else:
            # send notification
            if cfg.notifications.verbose:
                notify.send(message="Reading Custom Mapping file")
            log.warning('[MAPPING] Custom map file found: %s' % mapping_file)
            file = open(mapping_file, "r")
            for line in file:
                try:
                    mapping_split = line.split('^')
                    series_title = mapping_split[0]
                    season = mapping_split[1]
                    anime_id = int(mapping_split[2])

                    log.info(
                        "[MAPPING] Adding custom mapping | title: %s | season: %s | anilist id: %s" %
                        (series_title, season, anime_id))
                    mapping = anilist.AnilistCustomMapping(
                        series_title, season, anime_id)
                    custom_mappings.append(mapping)
                except Exception as err:
                    print(err)
                    log.error(
                        '[MAPPING] Invalid entry found for line: %s' %
                        line)
                    # send notification
                    if cfg.notifications.verbose:
                        notify.send(message='Invalid entry found for line: %s' %
                                            line)
        try:
            if cfg.notifications.verbose:
                notify.send(message='Searching Anime show in Plex')
            # Search for anime shows in Plex
            plex_connection = plex_auth
            if plex_auth is None:
                log.error(
                    'Plex authentication failed, check access to your Plex Media Server and settings')
                return None
            sections = cfg.PLEX.anime_section.split('|')
            shows = []
            for section in sections:
                try:
                    log.info(
                        '[PLEX] Retrieving anime series from section: %s' % section)
                    shows_search = plex_connection.library.section(section.strip()).search()
                    shows += shows_search
                    log.info(
                        '[PLEX] Found %s anime series in section: %s' %
                        (len(shows_search), section))
                    # send notification
                    notify.send(message='[PLEX] Found %s anime series in section: %s' %
                                        (len(shows_search), section))

                except Exception as e:
                    log.critical(e)
                    log.error(
                        'Could not find library [%s] on your Plex Server, check the library name in AniList settings '
                        'file '
                        'and '
                        'also verify that your library name in Plex has no trailing spaces in it' %
                        section)
                    if cfg.notifications.verbose:
                        notify.send(
                            message='Could not find library [%s] on your Plex Server, check the library name in '
                                    'AniList settings '
                                    'file '
                                    'and '
                                    'also verify that your library name in Plex has no trailing spaces in it' %
                                    section)

            # Get Watched Show
            from plexmodule import get_watched_shows
            # ANILIST SECTION
            anilist_skip_list_update = cfg.ANILIST.skip_list_update
            anilist.ANILIST_ACCESS_TOKEN = cfg.ANILIST.access_token.strip()
            anilist.ANILIST_PLEX_EPISODE_COUNT_PRIORITY = cfg.ANILIST.plex_episode_count_priority
            anilist_username = cfg.ANILIST.username
            anilist.custom_mappings = custom_mappings
            anilist_series = anilist.process_user_list(anilist_username)
            if cfg.notifications.verbose:
                notify.send(message='Found %s anime series on Anilist' % (len(anilist_series)))

            if anilist_skip_list_update:
                log.warning('AniList skip list update enabled in settings, will match but NOT update your list')

            exists = os.path.isfile("failed_matches.txt")
            if exists:
                try:
                    os.remove("failed_matches.txt")
                except Exception as err:
                    print(err)

            if anilist_series is None:
                log.error(
                    'Unable to retrieve AniList list, check your username and access token')
            else:
                if not anilist_series:
                    log.error('No items found on your AniList list for additional processing later on')
                plex_anime_series = shows
                if plex_anime_series is None:
                    log.error('Found no Plex shows for processing')
                    plex_watched_show = None
                else:
                    plex_watched_show = get_watched_shows(shows)
                    # send notification
                    if cfg.notifications.verbose:
                        notify.send(message='Found {} watched show starting sync against  Anilist'.format(
                            len(plex_watched_show)))

                if plex_watched_show is None:
                    log.error(
                        'Found no watched shows on Plex for processing')
                    # send notification
                    if cfg.notifications.verbose:
                        notify.send(message='Found no watched shows on Plex for processing')
                else:
                    matched_show = anilist.match_to_plex(anilist_series,
                                                         plex_anime_series,
                                                         plex_watched_show)
            log.info('Plex to AniList sync finished')
            # send notification
            if cfg.notifications.verbose:
                notify.send(message="Plex to Anilist Sync finished.")

        except NameError as err:
            log.critical(err)
            log.error(
                "Try removing the --sync-now flag and check what the error is, most likely it's can't find the home "
                "user: ")


############################################################
# MISC
############################################################

def init_notifications():
    # noinspection PyBroadException
    try:
        for notification_name, notification_config in cfg.notifications.items():
            if notification_name.lower() == 'verbose':
                continue

            notify.load(**notification_config)
    except Exception:
        log.exception("Exception initializing notification agents: ")
    return


# Handles exit signals, cancels jobs and exits cleanly
# noinspection PyUnusedLocal
def exit_handler(signum, frame):
    log.info("Received %s, canceling jobs and exiting.", signal.Signals(signum).name)
    schedule.clear()
    exit()


############################################################
# MAIN
############################################################

if __name__ == '__main__':
    print("")

    f = Figlet(width=100, justify=10, font='epic')
    print(f.renderText("PlexAnisync"))

    print("""
    #########################################################################
    # Author:   RickDB, KaiserBh                                            #
    # URL:      https://github.com/RickDB/PlexAniSync                       #
    # --                                                                    #
    #########################################################################
    #                   GNU General Public License v3.0                     #
    #########################################################################
    """)

    # Register the signal handlers
    signal.signal(signal.SIGTERM, exit_handler)
    signal.signal(signal.SIGINT, exit_handler)

    # Start App
    app()

    # TODO Create TautulliSyncHelper
    # TODO REMOVE AND REFACTOR PLEXMODULE.PY
    # TODO TEST IF --CONFIG PATH is working
