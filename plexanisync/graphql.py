# coding=utf-8
from configparser import SectionProxy
import logging
import time
import requests

from sgqlc.endpoint.requests import RequestsEndpoint
from sgqlc.operation import Operation

from plexanisync.anilist_schema import anilist_schema as schema
from plexanisync.logger_adapter import PrefixLoggerAdapter

logger = PrefixLoggerAdapter(logging.getLogger("PlexAniSync"), {"prefix": "GRAPHQL"})


class GraphQL:
    def __init__(self, anilist_settings: SectionProxy):
        self.anilist_settings = anilist_settings
        anilist_token = anilist_settings["access_token"].strip()
        self.endpoint = RequestsEndpoint(
            url="https://graphql.anilist.co",
            base_headers={
                "Authorization": f"Bearer {anilist_token}",
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            timeout=10,  # seconds,
            session=requests.Session()
        )
        self.endpoint.logger = logger
        self.skip_list_update = self.anilist_settings.getboolean("skip_list_update", False)
        self.sync_scores = self.anilist_settings.getboolean("sync_scores", True)

    def search_by_id(self, anilist_id: int):
        operation = Operation(schema.Query)
        media = operation.media(id=anilist_id, type="ANIME")
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

        data = self.__send_graphql_request(operation)

        media = (operation + data).media
        return media

    def search_by_name(self, anilist_show_name: str):
        operation = Operation(schema.Query)
        page = operation.page(page=1, per_page=50)
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

        data = self.__send_graphql_request(operation)

        media = (operation + data).page.media
        return media

    def fetch_user_list(self, username: str):
        operation = Operation(schema.Query)
        lists = operation.media_list_collection(user_name=username, type="ANIME").lists
        lists.__fields__('name', 'status', 'is_custom_list')
        lists.entries.__fields__('id', 'progress', 'status', 'repeat')
        lists.entries.score(format="POINT_100")
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

        data = self.__send_graphql_request(operation)
        return (operation + data).media_list_collection

    def update_series(self, media_id: int, progress: int, status: str, score_raw: int):
        if self.skip_list_update:
            logger.warning("Skip update is enabled in settings so not updating this item")
            return

        op = Operation(schema.Mutation)
        if score_raw and self.sync_scores:
            op.save_media_list_entry(
                media_id=media_id,
                status=status,
                progress=progress,
                score_raw=score_raw
            )
        else:
            op.save_media_list_entry(
                media_id=media_id,
                status=status,
                progress=progress
            )
        self.__send_graphql_request(op)

    def update_score(self, media_id, score_raw: int):
        if self.skip_list_update:
            logger.warning("Skip update is enabled in settings so not updating this item")
            return

        op = Operation(schema.Mutation)
        op.save_media_list_entry(
            media_id=media_id,
            score_raw=score_raw
        )
        self.__send_graphql_request(op)

    def __send_graphql_request(self, operation):
        while True:
            data = self.endpoint(operation)
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
