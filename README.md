Identify downloaded media and move it into place for serving up.

Data is pulled from http://thetvdb.com and you need to get your API details from them


# Options and Environment Variables
Most of the options can be specified both on the command line or by setting environment variables

| Option | Env Var | Meaning |
| ------ | ------- | ------- |
| `--srcdir <dir>` | `MEDIA_SRCDIR` |   Where to find the media files |
| `--dstdir <dir>` | `MEDIA_DSTDIR` |   Where to put the media files (`$MEDIA_DSTDIR/<showname>/Season <season>/<Episode>`) |
| `--tvdb_username <str>`| `TVDB_USERNAME` | Username from TVDB |
| `--tvdb_userkey <str>`| `TVDB_USERKEY` | User key from TVDB |
| `--tvdb_apikey <str>`| `TVDB_APIKEY` | API key from TVDB |
