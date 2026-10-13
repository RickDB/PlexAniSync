# AGENTS.md

Instructions for AI coding agents (Claude Code, GitHub Copilot, etc.) working in this repository.

## Project overview

PlexAniSync syncs a user's watched Anime episodes from a Plex library to their [AniList](https://anilist.co) account. It matches Plex show/season titles to AniList entries (via direct AniList IDs from the HAMA agent, custom user mappings, or fuzzy title/year search) and pushes progress/score updates through the AniList GraphQL API.

- `PlexAniSync.py` — main entry point, run as `python PlexAniSync.py [settings_file]`
- `TautulliSyncHelper.py` — syncs a single show, invoked from Tautulli notification scripts on playback stop
- `plexanisync/` — the actual package:
  - `plexmodule.py` — talks to Plex (via `python-plexapi`), builds `PlexWatchedSeries`/`PlexSeason` dataclasses
  - `anilist.py` — matching/update logic between Plex data and AniList lists (`Anilist` class)
  - `graphql.py` — thin AniList GraphQL client (via `sgqlc`), `GraphQL` class, retry/rate-limit handling
  - `anilist_schema.py` — generated `sgqlc` schema bindings, ~3200 lines, do not hand-edit
  - `custom_mappings.py` — loads/validates `custom_mappings.yaml` (+ optional remote community mapping URLs) against `custom_mappings_schema.json`
  - `logger_adapter.py` — `PrefixLoggerAdapter`, prefixes log lines with a subsystem tag (`[PLEX]`, `[ANILIST]`, `[GRAPHQL]`, `[MAPPING]`)
- `Docker/`, `Helm/` — container images and Helm chart for deployment, mostly independent of the Python logic
- `tests/` — pytest suite

## Setup

- Requires Python 3.9+ (README) — CI actually runs on 3.14; keep new code compatible with 3.9+ syntax unless told otherwise.
- The real floor is whatever Python version `Docker/Tautulli/Dockerfile`'s base image (`FROM tautulli/tautulli`) bundles — an upstream image PlexAniSync doesn't control the version of. That Dockerfile and `Docker/Tautulli/run/start.sh` derive the site-packages path dynamically at build/runtime (via `site.getusersitepackages()`) rather than hardcoding a version, specifically so upstream Python bumps don't silently break it — don't reintroduce a hardcoded `pythonX.Y` path there. Run `docker run --rm tautulli/tautulli python --version` if you need to know the current floor.
- Install deps: `pip install -r requirements.txt` (or `uv pip install -r requirements.txt` for a faster install — same `requirements.txt`, no project/lockfile changes)
- Copy `settings.ini.example` → `settings.ini` (Plex + AniList credentials) and, if needed, `custom_mappings.yaml.example` → `custom_mappings.yaml`. Both real files are gitignored — **never commit them or paste real tokens into commits, logs, or chat.**

## Build / lint / test

Mirror exactly what CI (`.github/workflows/CI.yml`) does:

```
flake8 .
pylint PlexAniSync.py TautulliSyncHelper.py ./plexanisync
pytest
```

- `flake8` is configured in `setup.cfg`, `pylint` in `.pylintrc` — check those files for the active rules rather than assuming defaults, they're allowed to diverge from stock config over time.
- Run lint/tests before considering a change done; CI will fail the same way locally.

### Testing caveat

`tests/test_graphql.py` calls the **real** AniList GraphQL API using a live token for a dedicated test account (`plexanisynctest`), not mocks. Expect it to be slower and network-dependent. Don't "fix" it by mocking unless asked — that's the existing, intentional pattern. Be aware the embedded token is scoped to a throwaway test account.

## Code conventions

- Keep code beginner-friendly — this is a hobby project maintained by volunteers and relies on outside contributors being able to understand and extend it. Prefer straightforward, explicit control flow over clever/dense one-liners, avoid introducing new abstractions (metaclasses, decorators, advanced typing tricks) unless the codebase already leans on them, and pick descriptive names over terse ones.
- Dataclasses for plain data models (`PlexSeason`, `PlexWatchedSeries`, `AnilistSeries`, `AnilistCustomMapping`, ...).
- Name-mangled double-underscore methods (`__find_id_best_match`, `__update_entry`, ...) are the established convention for "private" helpers on a class — match this, don't switch to single-underscore.
- Logging goes through the module-level `logger = PrefixLoggerAdapter(logging.getLogger("PlexAniSync"), {"prefix": "..."})`, not `print()`. Reuse the existing prefix per module.
- f-strings for message formatting; type hints via `typing` (`List`, `Optional`, `Dict`) rather than bare builtins (this predates PEP 585 generics being idiomatic here).
- Broad `except Exception` / `except BaseException` is an accepted, intentional pattern here (external API/library calls that shouldn't crash the sync run) — don't narrow these to specific exception types unless asked.
- Settings are read via `configparser.SectionProxy` (`settings["SECTION"]`), not a separate config object/model — follow this if touching settings handling.
- Comments in this codebase tend to explain *why* a workaround exists (e.g. disabled `originalTitle` logic in `plexmodule.py`) — keep that pattern, don't add narrative comments describing *what* the code does, except for code that is hard to understand for beginners.

## Dependencies

- `requirements.txt` has pinned versions. Version bumps are almost entirely automated by Renovate (`renovate.json5`) — pip deps update monthly and automerge. Don't manually bump versions in `requirements.txt` unless specifically asked; let Renovate handle it or note that you're deviating from the norm.
- `plexanisync/anilist_schema.py` is generated from AniList's GraphQL schema via `sgqlc` — regenerate rather than hand-edit if the schema needs to change.

## Releases

- Version string lives in `plexanisync/_version.py` (`__version__`).
- Pushing a `v*.*.*` tag on `master` triggers CI to build and publish the Docker images (`Docker/PlexAniSync`, `Docker/Tautulli`) per `.github/workflows/CI.yml` / `build-docker-image.yml`.

## Git / PRs

- No CONTRIBUTING.md exists; there's no enforced commit message convention beyond what Renovate auto-generates (`Update dependency X to vY (#NNN)`) for dependency PRs. Keep human commit messages short and descriptive of the change's purpose.