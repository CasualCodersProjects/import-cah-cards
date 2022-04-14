# Import CAH Cards

Allows you to create your own Cards Against Humanity cards to Pretend You're Xyzzy on a local network directly to the database.

## Current issues

- Successfully adds all cards to the database.
- Cards do not display on the UI.
- The cards displayed ARE NOT hard coded anywhere.

## What could be going on

- It could still be getting data from the SQLite file rather than PostgreSQL
- I tried to override the values in `overrides/build.properties` but I'm not confident that it actually switched to PostgreSQL. Will try again later.