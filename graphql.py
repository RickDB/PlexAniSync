# coding=utf-8
import collections
import json
import logging
import time
from typing import Any, Dict

import requests


logger = logging.getLogger("PlexAniSync")


ANILIST_ACCESS_TOKEN = ""
ANILIST_SKIP_UPDATE = False


def search_by_id(anilist_id: int):
    query = """
        query ($id: Int) {
        media: Media (id: $id, type: ANIME) {
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
            synonyms
            startDate {
                year
            }
            endDate {
                year
            }
        }
        }
        """

    variables = {"id": anilist_id}

    response = send_graphql_request(query, variables)
    return json.loads(response.content, object_hook=to_object)


def search_by_name(anilist_show_name: str):
    query = """
        query ($page: Int, $perPage: Int, $search: String) {
            Page (page: $page, perPage: $perPage) {
                pageInfo {
                    total
                    currentPage
                    lastPage
                    hasNextPage
                    perPage
                }
                media (search: $search, type: ANIME) {
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
                    synonyms
                    startDate {
                        year
                    }
                    endDate {
                        year
                    }
                }
            }
        }
        """
    variables = {"search": anilist_show_name, "page": 1, "perPage": 50}

    response = send_graphql_request(query, variables)
    return json.loads(response.content, object_hook=to_object)


def fetch_user_list(username: str):
    query = """
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
                            }
                            endDate {
                                year
                            }
                            title {
                                romaji
                                english
                                native
                            }
                            synonyms
                        }
                    }
                }
            }
        }
        """

    variables = {"username": username}

    response = send_graphql_request(query, variables)
    return json.loads(response.content, object_hook=to_object)


def update_series(media_id: int, progress: int, status: str):
    if ANILIST_SKIP_UPDATE:
        logger.warning("[ANILIST] Skip update is enabled in settings so not updating this item")
        return
    query = """
        mutation ($mediaId: Int, $status: MediaListStatus, $progress: Int) {
            SaveMediaListEntry (mediaId: $mediaId, status: $status, progress: $progress) {
                id
                status,
                progress
            }
        }
        """

    variables = {"mediaId": media_id, "status": status, "progress": int(progress)}

    send_graphql_request(query, variables)


def send_graphql_request(query: str, variables: Dict[str, Any]):
    url = "https://graphql.anilist.co"
    headers = {
        "Authorization": "Bearer " + ANILIST_ACCESS_TOKEN,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    while True:
        response = requests.post(
            url, headers=headers, json={"query": query, "variables": variables}
        )
        if response.status_code == 429:
            wait_time = int(response.headers.get('retry-after', 0))
            logger.warning(f"[ANILIST] Rate limit hit, waiting for {wait_time}s")
            time.sleep(wait_time + 1)

        else:
            response.raise_for_status()

            # wait a bit to not overload AniList API
            time.sleep(0.20)
            return response


def to_object(obj):
    keys, values = zip(*obj.items())
    # print(keys, values)
    return collections.namedtuple("X", keys)(*values)
