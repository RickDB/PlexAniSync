# Docker-PlexAniSync

![Docker](https://github.com/rickdb/PlexAniSync/actions/workflows/docker-publish-plexanisync.yml/badge.svg)

## Usage

### Docker

```
docker run -d \
  --name=plexanisync \
  --restart unless-stopped \
  -e PLEX_SECTION=Anime \
  -e PLEX_URL=http://127.0.0.1:32400 \
  -e PLEX_TOKEN=SomePlexToken \
  -e ANI_USERNAME=SomeUser \
  -e ANI_TOKEN=SomeToken \
  -e INTERVAL=3600 \
  -v /etc/localtime:/etc/localtime:ro \
  ghcr.io/rickdb/plexanisync:latest
```

### docker custom setting file

```
docker run -d \
  --name=plexanisync \
  --restart unless-stopped \
  -v /etc/localtime:/etc/localtime:ro \
  -v /host/path/folder:/config \
  -e SETTINGS_FILE="/config/settings.ini" \
  ghcr.io/rickdb/plexanisync:latest
```

### Environment Variables

| ID                          | Default                | Required | Note                                                                                                                                                     |
| --------------------------- | ---------------------- | :------: | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PLEX_SECTION                | Anime                  | &#10003; | The library where your anime resides                                                                                                                     |
| PLEX_URL                    | http://127.0.0.1:32400 | &#10003; | The address to your Plex Media Server, for example: http://127.0.0.1:32400                                                                               |
| PLEX_TOKEN                  | -                      | &#10003; | Follow [this guide](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/)                                            |
| ANI_USERNAME                | -                      | &#10003; | Your [AniList.co](http://www.anilist.co) username                                                                                                        |
| ANI_TOKEN                   | -                      | &#10003; | Get it [here](https://anilist.co/api/v2/oauth/authorize?client_id=1549&response_type=token)                                                              |
| SETTINGS_FILE               | -                      | &#10003; | If path to file is given it will use that setting file.                                                                                                  |
| INTERVAL                    | 3600                   | &#10005; | The time in between syncs                                                                                                                                |
| PLEX_EPISODE_COUNT_PRIORITY | -                      | &#10005; | If set to True, Plex episode watched count will take priority over AniList (default = False)                                                             |
| SKIP_LIST_UPDATE            | -                      | &#10005; | If set to True, it will NOT update your AniList which is useful if you want to do a test run to check if everything lines up properly. (default = False) |
| LOG_FAILED_MATCHES          | -                      | &#10005; | If set to True, failed matches will be written to /plexanisync/failed_matches.txt (default = False)                                                      |

### Note

You don't need to provide other environment variables if you have included one for `SETTINGS_FILE`. check [custom setting](###Docker-custom-setting-file)

### Custom mappings

In order to provide a [custom_mappings.yaml file](https://github.com/RickDB/PlexAniSync#custom-anime-mapping), mount the file on your host to `/plexanisync/custom_mappings.yaml` like this:

```
-v /path/to/your/custom_mappings.yaml:/plexanisync/custom_mappings.yaml
```

You can modify the file on the host system anytime and it will be used during the next run. Restarting the container is not necessary.
