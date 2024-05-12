# Docker-PlexAniSync

## Usage

### Docker Run

```
docker run -d \
  --name=plexanisync \
  --restart unless-stopped \
  -e PLEX_SECTION="Anime|Anime Movies" \
  -e PLEX_URL=http://127.0.0.1:32400 \
  -e PLEX_TOKEN=SomePlexToken \
  -e ANI_USERNAME=SomeUser \
  -e ANI_TOKEN=SomeToken \
  -e INTERVAL=3600 \
  -v /etc/localtime:/etc/localtime:ro \
  -v /path/to/your/custom_mappings.yaml:/plexanisync/custom_mappings.yaml \
  ghcr.io/rickdb/plexanisync:latest
```

### Docker Compose

```yaml
version: '3.7'
services:
  plexanisync:
    container_name: plexanisync
    image: 'ghcr.io/rickdb/plexanisync:latest'
    restart: unless-stopped
    environment:
      - PLEX_SECTION=Anime|Anime Movies
      - 'PLEX_URL=http://127.0.0.1:32400'
      - PLEX_TOKEN=SomePlexToken
      - ANI_USERNAME=SomeUser
      - ANI_TOKEN=SomeToken
      - INTERVAL=3600
    volumes:
      - '/etc/localtime:/etc/localtime:ro'
      - '/path/to/your/custom_mappings.yaml:/plexanisync/custom_mappings.yaml'
```

### Environment Variables

| ID                          | Default                | Required  | Note                                                                                                                                                     |
| --------------------------- | ---------------------- | :-------: | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PLEX_SECTION                | Anime                  | &#10003;* | The library where your anime resides.<br /><br />You can specify multiple values by seperating the library names with &#124; .                           | 
| PLEX_URL                    | http://127.0.0.1:32400 | &#10003;* | The address to your Plex Media Server, for example: http://127.0.0.1:32400                                                                               |
| PLEX_TOKEN                  | -                      | &#10003;* | Follow [this guide](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/)                                                                        |
| ANI_USERNAME                | -                      | &#10003;* | Your [AniList.co](http://www.anilist.co) username                                                                                                                                    |
| ANI_TOKEN                   | -                      | &#10003;* | Get it [here](https://anilist.co/api/v2/oauth/authorize?client_id=1549&response_type=token)                                                                                          |
| PLEX_EPISODE_COUNT_PRIORITY | -                      | &#10005;  | If set to True, Plex episode watched count will take priority over AniList (default = False)                                                                                         |
| SYNC_RATINGS                | -                      | &#10005;  | If set to True, Plex ratings will be used for Anilist scores. Make sure to read the [extended description](https://github.com/RickDB/PlexAniSync#use-plex-ratings-for-anilist-scores)|
| SKIP_LIST_UPDATE            | -                      | &#10005;  | If set to True, it will NOT update your AniList which is useful if you want to do a test run to check if everything lines up properly. (default = False)                             |
| LOG_FAILED_MATCHES          | -                      | &#10005;  | If set to True, failed matches will be written to /plexanisync/failed_matches.txt (default = False)                                                                                  |
| SETTINGS_FILE               | -                      | &#10005;  | Location of a custom settings.ini for more advanced configuration. Makes all settings above obsolete. See section below for usage.                                                   |
| INTERVAL                    | 3600                   | &#10005;  | The time in between syncs in seconds. If this value is set to <= 0, the container will stop after the first sync.                                                                    |

### Custom mappings

In order to provide a [custom_mappings.yaml file](https://github.com/RickDB/PlexAniSync#custom-anime-mapping), mount the file on your host to `/plexanisync/custom_mappings.yaml` like this:

```
-v /path/to/your/custom_mappings.yaml:/plexanisync/custom_mappings.yaml
```

You can modify the file on the host system anytime and it will be used during the next run. Restarting the container is not necessary.

### Custom settings.ini

If you want to use other Plex login mechanisms, you can use your own settings.ini file by mapping it into the container and setting the environment variable `SETTINGS_FILE` with the path to the file inside the container.

If the settings file is located at `/docker/plexanisync/settings.ini` and you want to place it to `/config/settings.ini`, use the following volume mapping and environment variable:

```
-v '/docker/plexanisync/settings.ini:/config/settings.ini:ro'
-e 'SETTINGS_FILE=/config/settings.ini'
```
