# Plex to AniList Sync
[![Build Status](https://travis-ci.com/RickDB/PlexAniSync.svg?branch=master)](https://travis-ci.com/RickDB/PlexAniSync)[![Docker Pulls](https://img.shields.io/docker/pulls/rickdb/plexanisync)](https://hub.docker.com/r/rickdb/plexanisync)

![Logo](logo.png)

If you manage your Anime with Plex this will allow you to sync your libraries to [AniList](https://anilist.co)  , recommend using Plex with the [HAMA agent](https://github.com/ZeroQI/Hama.bundle) for best Anime name matches.

Unwatched Anime in Plex will not be synced so only those that have at least one watched episode, updates to AniList are only send with changes so need to worry about messing up watch history.


This version is based on my previous project  [PlexMalSync](https://github.com/RickDB/PlexMALSync) which due to MAL closing their API is no longer working, this might change in the future and if it does will resume working on that again as as well.


**If you want test it out first without updating your actual AniList entries check out ``Skip list updating for testing `` from the ``Optional features`` section of this readme**

## Setup

### Step 1 - install Python

Make sure you have Python 3.7 or higher installed:

[Python homepage](https://www.python.org/)


### Step 2 - Download project files

Get the latest version using your favorite git client or by downloading the latest release from here:

https://github.com/RickDB/PlexAniSync/archive/master.zip


### Step 3 - Configuration

## Sample Configuration

```json
{
  "ANILIST": {
    "access_token": "",
    "plex_episode_count_priority": false,
    "skip_list_update": false,
    "username": ""
  },
  "Direct_IP": {
    "base_url": "",
    "token": ""
  },
  "MyPlex": {
    "home_server_base_url": "http://127.0.0.1:32400",
    "home_user_sync": false,
    "home_username": "Megumin",
    "myplex_password": "",
    "myplex_user": "",
    "server": ""
  },
  "PLEX": {
    "anime_section": "",
    "authentication_method": "direct"
  },
  "core": {
    "debug": false,
    "logFailedMatches": true,
    "notify_failed_matches": true
  },
  "notifications": {
    "verbose": true
  }
}
```
## Core

```json
  "core": {
    "debug": false
  },
```

`debug` - Toggle debug messages in the log. Default is `false`.

- Set to `true`, if you are having issues and want to diagnose why.

## ANILIST

```json
"ANILIST": {
    "access_token": "",
    "plex_episode_count_priority": false,
    "skip_list_update": false,
    "username": ""
  },
```

You will need `access_token` which can be grab using from https://anilist.co/api/v2/oauth/authorize?client_id=1549&response_type=token
_Note: Make sure to copy the entire key as it is pretty long and paste that in the config file under `access_token` make sure to enclose it._

Afterwards make sure to also fill in your AniList username as well which is your actual username not your e-mail address like for example:

```json
"ANILIST": {
    "access_token": "iLikeToastyGoblins",
    "username": "Netsplite"
  },
```

## Direct_IP

```json
"Direct_IP": {
    "base_url": "",
    "token": ""
  },
```

you can use direct IP to connect to Plex Server you just need the base_url by default it should be `http://127.0.0.1:32400` if the server is a local machine.

Then you can grab the toke by following this https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/

_Note: This is quite advance and it's recommended to use myplex method but if you feel ballsy then go ahead._

## MyPlex

```json
"MyPlex": {
    "home_server_base_url": "",
    "home_user_sync": false,
    "home_username": "",
    "myplex_password": "",
    "myplex_user": "",
    "server": ""
  },
```

Myplex method is one of the easiest way to connect all you have to do is insert `myplex_password` which is your plex password.
then just pass the `myplex_user` which will be your username for Plex

If you want to sync home user then set `home_user_sync` to `true` and fill in `home_username`, `home_server_base_url`
which should be the same with the `base_url` then the Plex `server` name.

Also For MyPlex authentication you will need your Plex server name and Plex account login information, for example:

```json
"MyPlex": {
    "home_server_base_url": "http://127.0.0.1:32400",
    "myplex_password": "TooOpAlwaysWin",
    "myplex_user": "Goku",
    "server": "RemBestWaifu"
  },
```

This completes the MyPlex authentication

_Note: Again if you want to sync againts home user which is not the admin then just fill in the rest and set `home_user_sync` to `true`._

## PLEX

```json
"PLEX": {
    "anime_section": "",
    "authentication_method": "direct"
  },
```

**THIS IS REALLY IMPORTANT SPECIALLY `anime_section`** you will need to specify which library you have your Animes, Otherwise it will fail to work.
**Also you will need to set the authentication method either `direct or myplex` choose one otherwise it will throw an error.**
Multiple libraries are now supported and you separate them by using the pipeline ("|") character like so:

```json
"PLEX": {
    "anime_section": "Weeb|HomeWork",
    "authentication_method": "direct"
  },
```

## Notifications

```json
"notifications": {
  "Apprise": {
    "service": "apprise",
    "url": "",
    "title": ""
  },
  "verbose": false
},
```

Notification alerts for PlexAniSync tasks using apprise and etc you can send notification directly to the discord server.

For manual (i.e. CLI) commands, you need to add the `--notifications` flag.

Supported `services`:

- `apprise`
- `pushover`
- `slack`

_Note: The key name can be anything, but the `service` key must be must be the exact service name (e.g. `pushover`). See below for example._

```json
"notifications": {
  "anyname": {
    "service": "pushover",
  }
},
```

### General

`verbose` - Toggle detailed notifications.

- Default is `true`.

- Set to `false` if you want to reduce the amount of detailed notifications (e.g. just the total vs detailed log).

```json
"notifications": {
  "verbose": true
},
```

### Apprise

```json
"notifications": {
  "Apprise": {
    "service": "apprise",
    "url": "",
    "title": ""
  },
  "verbose": false
},
```

`url` - Apprise service URL (see [here](https://github.com/caronc/apprise)).

- Required.

`title` - Notification Title.

- Optional.

- Default is ` ` is empty.

### Pushover

```json
"notifications": {
  "pushover": {
    "service": "pushover",
    "app_token": "",
    "user_token": "",
    "priority": 0
  },
  "verbose": false
},
```

`app_token` - App Token from [Pushover.net](https://pushover.net).

- Required.

`user_token` - User Token from [Pushover.net](https://pushover.net).

- Required.

`priority` - [Priority](https://pushover.net/api#priority) of the notifications.

- Optional.

- Choices are: `-2`, `-1`, `0`, `1`, `2`.

- Values are not quoted.

- Default is `0`.

### Slack

```json
"notifications": {
  "slack": {
    "service": "slack",
    "webhook_url": "",
    "channel": "",
    "sender_name": "",
    "sender_icon": ""
  },
  "verbose": false
},
```

`webhook_url` - [Webhook URL](https://my.slack.com/services/new/incoming-webhook/).

- Required.

`channel` - Slack channel to send the notifications to.

- Optional.

- Default is blank.

`sender_name` - Sender's name for the notifications.

- Optional.

- Default is `` is empty.

`sender_icon` - Icon to use for the notifications.

- Optional.

- Default is `:movie_camera:`


### Step 4 - Install requirements

Install the addtional requirements using the Python package installer (pip) from within the project folder:

`pip install -r requirements.txt`


### Step 5 - Start syncing

Now that configuration is finished and requirements have been installed we can finally start the sync script:

`python PlexAniSync.py`

Depending on library size and server can take a few minutes to finish, for scheduled syncing you can create a cronjob or windows task which runs it every 30 minutes for instance.


## Optional features

### Custom anime mapping

You can manually link a Plex title and season to an AniList ID, to do so:

- From the project folder copy `custom_mappings.yaml.example` to `custom_mappings.yaml`
- Add new entries there in the following format:

```yaml
  - title: "Plex title for series"
    seasons:
      - season: Plex season
        anilist-id: AniList series ID
      - season: Plex season
        anilist-id: AniList series ID
```

If the Plex season should be split into 2 seasons, add an optional `start` parameter to each season like this:

```yaml
  - title: "Re:ZERO -Starting Life in Another World-"
    seasons:
      - season: 2
        anilist-id: 108632
        start: 1
      - season: 2
        anilist-id: 119661
        start: 14
```

Episodes 1-13 will be mapped to Re:Zero 2nd Season Part 1, episodes 14 and higher will be mapped to Re:Zero 2nd Season Part 2.

- To find out the AniList ID you can visit the series page and copy it from the site url, like for example My Shield hero has ID 99263:

https://anilist.co/anime/99263/Tate-no-Yuusha-no-Nariagari

- You can remove any existing entries from the example file as they are purely instructional
- Upon startup it will check if the file is a valid YAML file. The most likely reason it's not is because you didn't put quotes around an anime title with special characters (e.g. ":") in it.

### Custom settings file location

If you want to load a different settings.in file you can do so by supplying it in the first argument like so:

`python PlexAniSync.py settings_alternate.ini`

In case of the Tautulli sync helper script you can do as well, first argument will then be settings filename and second will be the series name like so:

`python TautulliSyncHelper.py  settings_alternate.ini <plex show name>`

### Make Plex watched episode count take priority

By default if AniList episode count watched is higher than that of Plex it will skip over, this can be overriden with the setting `plex_episode_count_priority`

When set to True it will update the AniList entry if Plex watched episode count is higher than 0 and will not take into account the AniList watched episode count even if that is higher.

**Use this with caution as normally this isn't required and only meant for certain use cases.**

### Skip list updating for testing

In your settings file there's a setting called `skip_list_update` which you can set to True or False, if set to True it will **NOT** update your AniList which is useful if you want to do a test run to check if everything lines up properly.

### Tautulli Sync Helper script

In the project folder you will find `TautulliSyncHelper.py` which you can use to sync a single Plex show to AniList for use in Tautulli script notifcations (trigger on playback stop).

Usage is as follows:

`python TautulliSyncHelper.py <plex show name>`

Depending on your OS make sure to place the show name between single or double quotes, for more information see the wiki page:

https://github.com/RickDB/PlexAniSync/wiki/Tautulli-sync-script

## Docker

There's also a Docker version based on [Thundernerd's](https://github.com/Thundernerd) which you can find here:

[Docker](https://hub.docker.com/r/rickdb/plexanisync)

If you are still on the Thundernerd docker image recommend switching to this one as it will be kept in sync with latest PlexAniSync changes.

## Requirements

[Python 3.7 or higher](https://www.python.org/)

## Support

Support thread is located on AniList:

https://anilist.co/forum/thread/6443

Optionally also on Plex forums but less active there:

https://forums.plex.tv/t/plexanisync-sync-your-plex-library-to-anilist/365826

## Planned

Currently planned for future releases:

- [ ] XREF title matching based on HAMA which uses custom lists and AniDB
- [ ] Add setting to skip updating shows with dropped state on user list
- [ ] Ignore anime list support (based on content rating and / or title)
- [ ] Improve error handling

## Credits

[Python-PlexAPI](https://github.com/pkkid/python-plexapi)
