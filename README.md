# Plex to AniList Sync
[![Build Status](https://travis-ci.com/RickDB/PlexAniSync.svg?branch=master)](https://travis-ci.com/RickDB/PlexAniSync)![Docker](https://github.com/rickdb/Docker-PlexAniSync/actions/workflows/docker-publish.yml/badge.svg)


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

From the project directory rename `settings.ini.example` to `settings.ini`, open `settings.ini` with your favorite text editor and edit where needed.


#### Plex

Only choose one of the authentication methods, MyPlex is the easiest.

##### MyPlex authentication (prefered)

For MyPlex authentication you will need your Plex server name and Plex account login information, for example:

```
[PLEX]
anime_section = Anime
authentication_method = myplex

server = Sadala
myplex_user = Goku
myplex_password = kamehameha
```

This completes the MyPlex authentication and **only** if you want to sync against a specific Plex Home user which isn't the admin user follow the below instructions:

For this to work lookup the home username on your Plex server and also fill in your full Plex server URL, for example:

```
[PLEX]
anime_section = Anime
authentication_method = myplex

# MyPlex
server = Sadala
myplex_user = John # has to be the Plex admin user acount
myplex_password = Doe

# if you enable home_user_sync it will only sync against that specific Plex home user, it requires the full url of your Plex server just like with the Direct IP method
# home_username is the actual Plex home username and not their e-mail address, this is also case sensitive

home_user_sync = True
home_username = Megumin # the home user account you want to sync with and can not be the admin user
home_server_base_url = http://127.0.0.1:32400
```

##### Direct Plex authentication (advanced users)

The direct authentication method is for users that don't want to use Plex its online authentication system however is more complex to setup, for this you need to find your token manually:

https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/

Afterwards can enter your full Plex site url and above authentication token, for example:

```
[PLEX]
anime_section = Anime
authentication_method = direct

base_url = http://192.168.1.234:32400
token = abcdef123456789
```

##### Section configuration

In the settings file enter your Plex library / section name containing your Anime, for example:

```
[PLEX]
anime_section = Anime
```

Multiple libraries are now supported and you separate them by using the pipeline ("|") character like so:

```
[PLEX]
anime_section = Anime|Anime2
```

#### AniList

For AniList you need get a so called `access_token` which you can retrieve via this link and if not logged in will ask you to do so:

https://anilist.co/api/v2/oauth/authorize?client_id=1549&response_type=token

Make sure to copy the entire key as it is pretty long and paste that in the settings file under 'access_token', no need to enclose it just paste it as-is.

Afterwards make sure to also fill in your AniList username as well which is your actual username not your e-mail address like for example:

```
[ANILIST]
username = GoblinSlayer
access_token = iLikeToastyGoblins.
```

### Step 4 - Install requirements

Install the addtional requirements using the Python package installer (pip) from within the project folder:

`pip install -r requirements.txt`


### Step 5 - Start syncing

Now that configuration is finished and requirements have been installed we can finally start the sync script:

`python PlexAniSync.py`

Depending on library size and server can take a few minutes to finish, for scheduled syncing you can create a cronjob, systemd timer or windows task which runs it every 30 minutes for instance.

See [Systemd service](https://github.com/RickDB/PlexAniSync/wiki/Systemd-service) for a tutorial on how to set up a timer with systemd.

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

#### Community mappings

There are some mappings provided by the Github community at https://github.com/RickDB/PlexAniSync-Custom-Mappings/. For now you can use the mapping files by copying parts into your own mapping file.

The feature of synonyms was introduced for the community mappings where you can specify that a show can have one of multiple titles but should be mapped the same way. See Shaman King (2021) in the example mapping file.

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

### Telegram Integration

We can inform you via Telegram about start / errors / finish of the sync process. This is especially useful for automatic daily syncs. In case an error occurs or a new anime got added that needs a custom mapping you are always informed.

To enable this you first have to create a new Telegram Bot by talking to the neat helper [BotFather](https://t.me/BotFather). From him you get a "bot_token" which you have to save in the `settings.ini`. After that you also need a chat
where to send the messages to. For that add the bot to any chatroom and use a bot like [IDBot](https://t.me/myidbot) to get the chats id. Save this to `chat_id` in the `settings.ini`.

Last but not least you have to enable the integration by settings `eneabled` in the `[TELEGRAM]` section of `settings.ini` to `True`.

## Docker

Docker version is located here: [PlexAniSync](https://github.com/RickDB/PlexAniSync/pkgs/container/plexanisync)

Another docker container for Tautulli with built-in PlexAniSync can be found here: [Tautulli-PlexAniSync](https://github.com/RickDB/PlexAniSync/pkgs/container/tautulli-plexanisync)


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
