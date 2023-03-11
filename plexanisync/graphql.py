# coding=utf-8
import logging
import time
import requests

from sgqlc.endpoint.requests import RequestsEndpoint
from sgqlc.operation import Operation

from plexanisync.anilist_schema import anilist_schema as schema
from plexanisync.logger_adapter import PrefixLoggerAdapter

logger = PrefixLoggerAdapter(logging.getLogger("PlexAniSync"), dict(prefix='GRAPHQL'))

ANILIST_ACCESS_TOKEN = ""
ANILIST_SKIP_UPDATE = False

endpoint = None


def search_by_id(anilist_id: int):
    op = Operation(schema.Query)
    media = op.media(id=anilist_id, type="ANIME")
    media.__fields__(
        'id',
        'type',
        'format',
        'status',
        'source',
        'season',
        'episodes',
        'synonyms'
    )
    media.title.__fields__('romaji', 'english', 'native')
    media.start_date.year()
    media.end_date.year()

    data = send_graphql_request(op)

    media = (op + data).media
    return media


def search_by_name(anilist_show_name: str):
    op = Operation(schema.Query)
    page = op.page(page=1, per_page=50)
    media = page.media(search=anilist_show_name, type="ANIME")
    media.__fields__(
        'id',
        'type',
        'format',
        'status',
        'source',
        'season',
        'episodes',
        'synonyms'
    )
    media.title.__fields__('romaji', 'english', 'native')
    media.start_date.year()
    media.end_date.year()

    data = send_graphql_request(op)

    media = (op + data).page.media
    return media


def fetch_user_list(username: str):
    op = Operation(schema.Query)
    lists = op.media_list_collection(user_name=username, type="ANIME").lists
    lists.__fields__('name', 'status', 'is_custom_list')
    lists.entries.__fields__('id', 'progress', 'status', 'repeat')
    lists.entries.media.__fields__(
        'id',
        'type',
        'format',
        'status',
        'source',
        'season',
        'episodes',
        'synonyms'
    )
    lists.entries.media.start_date.year()
    lists.entries.media.end_date.year()
    lists.entries.media.title.__fields__('romaji', 'english', 'native')

    data = send_graphql_request(op)
    return (op + data).media_list_collection


def update_series(media_id: int, progress: int, status: str):
    if ANILIST_SKIP_UPDATE:
        logger.warning("Skip update is enabled in settings so not updating this item")
        return

    op = Operation(schema.Mutation)
    op.save_media_list_entry(
        media_id=media_id,
        status=status,
        progress=progress
    )
    send_graphql_request(op)


def send_graphql_request(op):
    global endpoint
    if not endpoint:
        endpoint = RequestsEndpoint(
            url="https://graphql.anilist.co",
            base_headers={
                "Authorization": f"Bearer {ANILIST_ACCESS_TOKEN}",
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            timeout=10,  # seconds,
            session=requests.Session()
        )
        endpoint.logger = logger

    while True:
        data = endpoint(op)
        if hasattr(data, 'errors'):
            error = data["errors"][0]
            status = error.status
            if status == 429:
                wait_time = int(error.headers.get('retry-after', 0))
                logger.warning(f"Rate limit hit, waiting for {wait_time}s")
                time.sleep(wait_time + 1)

            else:
                raise error.exception
        else:
            # wait a bit to not overload AniList API
            time.sleep(0.20)
            return data
