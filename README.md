# Plex to AniList Sync
[![Build Status](https://travis-ci.org/RickDB/PlexAniSync.svg?branch=master)](https://travis-ci.org/RickDB/PlexAniSync)

![Logo](logo.png)

If you manage your Anime with Plex this will allow you to sync your libraries to [AniList](https://anilist.co)  , recommend using Plex with the [HAMA agent](https://github.com/ZeroQI/Hama.bundle) for best Anime name matches.

Unwatched Anime in Plex will not be synced so only those that have at least one watched episode, updates to AniList are only send with changes so need to worry about messing up watch history.


This version is based on my previous project  [PlexMalSync](https://github.com/RickDB/PlexMALSync) which due to MAL closing their API is no longer working, this might change in the future and if it does will resume working on that again as as well.


**If you want test it out first without updating your actual AniList entries check out ``Skip list updating for testing `` from the ``Optional features`` section of this readme**

## Setup

### Step 1 - Download project files

Get the latest version using your favorite git client or by downloading the latest release from here:

https://github.com/RickDB/PlexAniSync/archive/master.zip


### Step 2 - Configuration

From the project directory copy the example settings file `settings.ini.example` to `settings.ini`, open `settings.ini` with your favorite editor and edit where needed.

#### Plex

##### Direct IP authentication

The Direct IP authentication method is preferred as it's the fastest method, for this you need to find your token manually:

https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/

Afterwards can enter your full Plex site url and above authentication token, for example:

```
[PLEX]
anime_section = Anime
authentication_method = direct

base_url = http://192.168.1.234:32400
token = abcdef123456789
```

##### MyPlex authentication

For MyPlex authentication you will need your Plex server name and Plex account login information, for example:

```
[PLEX]
anime_section = Anime
authentication_method = myplex

server = Sadala
myplex_user = Goku
myplex_password = kamehameha
```

This completes this part and **only** if you want to sync against a specific Plex Home user follow the below instructions:

##### MyPlex - sync with Plex Home user instead

First find your Plex authentication token:

https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/

Afterwards can enter your full Plex site url and above authentication token, for example:

```
[PLEX]
anime_section = Anime
authentication_method = myplex

# MyPlex
server = Sadala
myplex_user = John
myplex_password = Doe

# if you enable home_user_sync it will only sync against that specific Plex home user, it requires the same info as direct IP method (url + token)
# home_username is the actual Plex home username and not their e-mail address, this is also case sensitive

home_user_sync = True
home_username = Megumin
home_admin_token = abcdef123456789
home_server_base_url = http://127.0.0.1:32400
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

### Step 3 - Install requirements

Make sure you have Python 3.6 or higher installed and install the addtional requirements using this Python command from within the project folder:

`pip install -r requirements.txt`

### Step 4 - Start syncing

Now that configuration is finished and requirements have been installed we can finally start the sync script:

`python PlexAniSync.py`

Depending on library size and server can take a few minutes to finish, for scheduled syncing you can create a cronjob or windows task which runs it every 30 minutes for instance.

## Optional features

### Custom settings file location

If you want to load a different settings.in file you can do so by supplying it in the first argument like so:

`python PlexAniSync.py settings_alternate.ini`

In case of the Tautulli sync helper script you can do as well, first argument will then be settings filename and second will be the series name like so:

`python TautulliSyncHelper.py  settings_alternate.ini <plex show name>`

### Custom anime mapping

You can manually link a Plex title and season to an AniList ID, to do so:

- From the project folder copy `custom_mappings.ini.example` to `custom_mappings.ini`
- Add new entries there in the following format:

`Plex title for series`^`Plex season`^`AniList series ID`

As shown above the values are seperated by a ^

- To find out the AniList ID you can visit the series page and copy it from the site url, like for example My Shield hero has ID 99263:

https://anilist.co/anime/99263/Tate-no-Yuusha-no-Nariagari

- You can remove any existing entries from the example file as they are purely instructional
- Upon startup it will list all valid custom mappings, incorrect onces are shown as errors and are skipped

### Skip list updating for testing

In your settings file there's a setting called `skip_list_update` which you can set to True or False, if set to True it will **NOT** update your AniList which is useful if you want to do a test run to check if everything lines up properly.

### Tautulli Sync Helper script

In the project folder you will find `TautulliSyncHelper.py` which you can use to sync a single Plex show to AniList for use in Tautulli script notifcations (trigger on playback stop).

Usage is as follows:

`python TautulliSyncHelper.py <plex show name>`

Depending on your OS make sure to place the show name between single or double quotes, for more information see the wiki page:

https://github.com/RickDB/PlexAniSync/wiki/Tautulli-sync-script


## Requirements

[Python 3 (tested with 3.6.4)](https://www.python.org/)

## Support

Support thread is located on AniList:

https://anilist.co/forum/thread/6443

Optionally also on Plex forums but less active there:

https://forums.plex.tv/t/plexanisync-sync-your-plex-library-to-anilist/365826

## Planned

Currently planned for future releases:

- [ ] Ignore anime list support (based on content rating and / or title)
- [ ] Improve error handling

## Credits

[Python-PlexAPI](https://github.com/pkkid/python-plexapi)
