# Plex to AniList Sync
[![Build Status](https://travis-ci.com/RickDB/PlexAniSync.svg?branch=master)](https://travis-ci.com/RickDB/PlexAniSync) ![Docker](https://github.com/rickdb/Docker-PlexAniSync/actions/workflows/docker-publish.yml/badge.svg)

[![Discord Shield](https://discordapp.com/api/guilds/903407293541023754/widget.png?style=banner2)](https://discord.gg/a9cu5t5fKc)

![Logo](logo.png)


If you manage your Anime with Plex this will allow you to sync your libraries to [AniList](https://anilist.co)  , recommend using Plex with the [HAMA agent](https://github.com/ZeroQI/Hama.bundle) for best Anime name matches.

Unwatched Anime in Plex will not be synced so only those that have at least one watched episode, updates to AniList are only send with changes so need to worry about messing up watch history.


This version is based on my previous project  [PlexMalSync](https://github.com/RickDB/PlexMALSync) which due to MAL closing their API is no longer working, this might change in the future and if it does will resume working on that again as as well.


**If you want test it out first without updating your actual AniList entries check out ``Skip list updating for testing `` from the ``Optional features`` section of this readme**

## Setup

### Step 1 - install Python

Make sure you have Python 3.8 or higher installed:

[Python homepage](https://www.python.org/)


### Step 2 - Download project files

Get the latest version using your favorite git client or by downloading the latest release from here:

https://github.com/RickDB/PlexAniSync/archive/master.zip


### Step 3 - Configuration

From the project directory rename `settings.ini.example` to `settings.ini`, open `settings.ini` with your favorite text editor and edit where needed.


#### Plex

Only choose one of the authentication methods, MyPlex is the easiest.

##### MyPlex authentication (prefered)

For MyPlex authentication you will need your Plex server name, user name and a Plex token.

The method for obtaining a Plex token is described here: https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/

Here is an example for synchronizing the admin account:

```
[PLEX]
anime_section = Anime
authentication_method = myplex

server = Sadala
myplex_user = Goku
myplex_token = abcdef123456789
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
myplex_token = abcdef123456789

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

The token is only valid for 1 year, so you'll have to repeat this process yearly.

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

#### Duplicate Plex Titles

For Plex shows and movies with the same title, use the optional `guid` field in the mapping.

For example, both of these Rurouni Kenshin shows are shown as "Rurouni Kenshin" in Plex: 

```yaml
  - title: "Rurouni Kenshin"
    guid: plex://show/5d9c07ece264b7001fc38094
    seasons:
      - season: 1
        anilist-id: 45
      - season: 2
        anilist-id: 45
      - season: 3
        anilist-id: 45

  - title: "Rurouni Kenshin (2023)"
    guid: plex://show/6330a57e9705fab2b34f656d
    seasons:
      - season: 1
        anilist-id: 142877
```

When the `guid` field is set, the `title` and `synonyms` fields are ignored. However, you should still use different titles for human readability.

To find the guid, perform the following steps:
1. Open this URL in an **incognito browser window**: https://app.plex.tv/desktop/#!/search?pivot=top&query=
2. Search for your series or movie and click on the correct entry
3. Copy everything after `metadata%2F`, so for https://app.plex.tv/desktop/#!/provider/tv.plex.provider.discover/details?key=%2Flibrary%2Fmetadata%2F6330a57e9705fab2b34f656d copy `6330a57e9705fab2b34f656d`
4. If it's a TV show, add `plex://show/` before that identifier, for movies use `plex://movie/`

#### Community mappings

There are some mappings provided by the Github community at https://github.com/RickDB/PlexAniSync-Custom-Mappings/. You can use them by specifying `remote-urls` like in the example mapping file.

If the local mapping file contains mappings for the same show as the community mapping, the local one will take precedence.

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

### Use Plex ratings for Anilist scores

In Plex you can currently rate shows, seasons and episodes with 1 to 5 stars. On the mobile app and if you're part of the [Discover Together Beta](https://www.plex.tv/de/discover-together-beta/), you can also rate in half star increments.

Set `sync_ratings = True` to automatically set Anilist scores based on the Plex ratings. This will also change the score of shows you've completed in the past.

If one or more Plex seasons are mapped to an Anilist entry, the average of the rated seasons will be used. The raw Anilist score will be `number of Plex stars * 20`. So if you rate 1 season with 3.5 stars and another season with 4 stars, the calculated Anilist score will be 75.

If the seasons are not rated, the show rating will be used as fallback.

Episode ratings are currently not used.

The actual score shown in your anime list depends on the scoring system setting at https://anilist.co/settings/lists

| Scoring system  | Score shown         |
| --------------- | ------------------- |
| 100 Point       | 75                  | 
| 10 Point Decimal| 7.5                 |
| 10 Point        | 7 (rounded down)    |
| 5 Star          | 4 stars (rounded up)|
| 3 Point Smiley  | 🙂                  |

In all cases, Anilist stores the raw value of 75, so you can change the scoring system at any point without data loss. But beware that 3 Point Smiley scores cannot be accurately converted, so you should avoid it as best as you can.

### Skip list updating for testing

In your settings file there's a setting called `skip_list_update` which you can set to True or False, if set to True it will **NOT** update your AniList which is useful if you want to do a test run to check if everything lines up properly.

### Tautulli Sync Helper script

In the project folder you will find `TautulliSyncHelper.py` which you can use to sync a single Plex show to AniList for use in Tautulli script notifcations (trigger on playback stop).

Usage is as follows:

`python TautulliSyncHelper.py <plex show name>`

Depending on your OS make sure to place the show name between single or double quotes, for more information see the wiki page:

https://github.com/RickDB/PlexAniSync/wiki/Tautulli-sync-script

## Docker

PlexAniSync is available as Docker image.

[PlexAniSync](https://github.com/RickDB/PlexAniSync/pkgs/container/plexanisync)<br/>
[Documentation](Docker/PlexAniSync/README.md)

Another docker container for Tautulli with built-in PlexAniSync can be found here:<br/>
[Tautulli-PlexAniSync](https://github.com/RickDB/PlexAniSync/pkgs/container/tautulli-plexanisync)<br/> 
[Documentation](Docker/Tautulli/README.md)

## Requirements

[Python 3.8 or higher](https://www.python.org/)

## Support

**AniList**

https://anilist.co/forum/thread/6443

**Discord**

https://discord.gg/a9cu5t5fKc

## Planned

Currently planned for future releases:

- [ ] XREF title matching based on HAMA which uses custom lists and AniDB
- [ ] Add setting to skip updating shows with dropped state on user list
- [ ] Ignore anime list support (based on content rating and / or title)
- [ ] Improve error handling

## Credits

[Python-PlexAPI](https://github.com/pkkid/python-plexapi)
