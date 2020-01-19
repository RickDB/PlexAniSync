# Plex to AniList Sync
[![Build Status](https://travis-ci.org/RickDB/PlexAniSync.svg?branch=master)](https://travis-ci.org/RickDB/PlexAniSync)[![Build Status](https://img.shields.io/docker/cloud/build/rickdb/plexanisync.svg)](https://hub.docker.com/r/rickdb/plexanisync)

![Logo](logo.png)

If you manage your Anime with Plex this will allow you to sync your libraries to [AniList](https://anilist.co)  , recommend using Plex with the [HAMA agent](https://github.com/ZeroQI/Hama.bundle) for best Anime name matches.

Unwatched Anime in Plex will not be synced so only those that have at least one watched episode, updates to AniList are only send with changes so need to worry about messing up watch history.


This version is based on my previous project  [PlexMalSync](https://github.com/RickDB/PlexMALSync) which due to MAL closing their API is no longer working, this might change in the future and if it does will resume working on that again as as well.


**If you want test it out first without updating your actual AniList entries check out ``Skip list updating for testing `` from the ``Optional features`` section of this readme**

## Setup

### Step 1 - install Python

Make sure you have Python 3 installed:

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

Depending on library size and server can take a few minutes to finish, for scheduled syncing you can create a cronjob or windows task which runs it every 30 minutes for instance.


## Optional features

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

[Python 3](https://www.python.org/)

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
