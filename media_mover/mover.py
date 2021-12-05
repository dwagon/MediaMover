#!/home/dwagon/.venvs/media_mover/bin/python3
""" Move media files to their appropriate location """

import os
import re
import pipes

import click
from tvdb_api_client import TVDBClient

default_srcdir = '/var/snap/sabnzbd/common/Downloads/complete/'
default_dstdir = '/Music/TV'

non_video_extensions = ('.srt', '.nfo', '.sfv', '.srr', '.nzb', '.jpg', '.srs', '.idx', '.sub')
video_extensions = ('.mkv', '.m4v', '.avi', '.mp4')

OPTIONS = {
        'kidding': False
        }


##############################################################################
def demangle_showname(name):
    """ Convert a filename to a showname, year, episode, season if possible """
    try:
        year = None
        m = re.match(r'(?P<name>.*?)[Ss](?P<season>\d+)[Ee](?P<episode>\d+)(.*)', name)
        if not m:
            print("Didn't understand {}".format(name))
            return None, None, None, None
        sname = m.group('name').replace('.', ' ').strip()
        m2 = re.match(r'(?P<sname>.*)(?P<year>\d{4})', sname)
        if m2:
            sname = m2.group('sname')
            year = m2.group('year')
        if sname.startswith('_UNPACK_'):
            sname = sname.replace('_UNPACK_', '')
        season = int(m.group('season').lstrip('0'))
        episode = int(m.group('episode').lstrip('0'))
    except Exception as exc:
        print(f"Failed with {exc} for {name}")
        raise
    return sname.strip(), year, season, episode


##############################################################################
def make_show_dirs(showname, season):
    """ Make the destination directory for a show """
    dest = os.path.join(OPTIONS['destdir'], showname)
    print(dest)
    if not os.path.exists(dest):
        if OPTIONS['kidding']:
            print("mkdir {}".format(dest))
        else:
            os.mkdir(dest)

    seasondir = os.path.join(dest, 'Season {}'.format(season))
    if not os.path.exists(seasondir):
        if OPTIONS['kidding']:
            print("mkdir {}".format(seasondir))
        else:
            os.mkdir(seasondir)
    return seasondir


##############################################################################
def move_show(fname, destdir, destfile):
    """ Move a show into place """
    dest = pipes.quote("{}/{}".format(destdir, destfile))
    fname = pipes.quote(fname)
    if OPTIONS['kidding']:
        print("cp {} {}".format(fname, dest))
    else:
        print("Copying {} to {}".format(fname, dest))
        os.system("cp {} {}".format(fname, dest))


##############################################################################
def get_show_details(tvdb, root):
    """ Return show details based on the filename
    Try a more specific show (with year) before being more
    general """
    m_showname = root.replace(OPTIONS['srcdir'], '')
    showname, _, season, episodenum = demangle_showname(m_showname)
    try:
        tvdb_show = tvdb.find_series_by_name(showname)
    except Exception as exc:
        print(f"Failure on {root}: {exc}")
        return None, None, None
        
    for series in tvdb_show:
        try:
            episodes = tvdb.get_episodes_by_series(series['tvdb_id'])
        except Exception as exc:
            print(f"Failure on {root}, {series}: {exc}")
            return None, None, None
        for episode in episodes:
            if episode['airedSeason'] == season and episode['airedEpisodeNumber'] == episodenum:
                epname = episode['episodeName']
                destfile = "S{:02d}E{:02d}_{}".format(season, episodenum, epname)
                return showname, season, destfile
    return None, None, None


##############################################################################
def process_file(fname, root, destfile, destdir):
    """ Process file """
    if 'sample' in fname:
        print("Skipping {} due to sample".format(fname))
        return
    srcfile = os.path.join(root, fname)
    ext = os.path.splitext(srcfile)[-1]
    if ext in non_video_extensions:
        if OPTIONS['kidding']:
            print("Would delete {} due to filetype {}".format(fname, ext))
        else:
            try:
                os.unlink(srcfile)
            except Exception as exc:    # pylint: disable=broad-except
                print(f"Failed to remove {srcfile}: {exc}")
    elif ext in video_extensions:
        destfileext = "{}{}".format(destfile, ext)
        move_show(srcfile, destdir, destfileext)
    else:
        print("Skipping {} due to unknown filetype {}".format(fname, ext))


##############################################################################
@click.command()
@click.option('-k', '--kidding', default=False, is_flag=True, help="Don't actually do anything")
@click.option(
    '--srcdir',
    default=default_srcdir, help="Where to get files from", envvar='MEDIA_SRCDIR')
@click.option(
    '--destdir',
    default=default_dstdir, help="Where to put files to", envvar='MEDIA_DSTDIR')
@click.option('--username', envvar='TVDB_USERNAME')
@click.option('--userkey', envvar='TVDB_USERKEY')
@click.option('--apikey', envvar='TVDB_APIKEY')
def cli(kidding, srcdir, destdir, username, userkey, apikey):   # pylint: disable=too-many-arguments
    """ CLI interface """
    OPTIONS['kidding'] = kidding
    OPTIONS['srcdir'] = srcdir
    OPTIONS['destdir'] = destdir
    OPTIONS['apikey'] = apikey
    OPTIONS['username'] = username
    OPTIONS['userkey'] = userkey
    print(OPTIONS)
    process()


##############################################################################
def process():
    """ Do the processing """
    tvdb = TVDBClient(
                api_key=OPTIONS['apikey'],
                username=OPTIONS['username'],
                user_key=OPTIONS['userkey']
    )
    for root, _, files in os.walk(OPTIONS['srcdir']):
        if not files:
            continue
        showname, season, destfile = get_show_details(tvdb, root)
        if showname is None:
            print(f"Couldn't find season details for {root}")
            continue
        destdir = make_show_dirs(showname, season)
        for fname in files:
            process_file(fname, root, destfile, destdir)


##############################################################################
if __name__ == "__main__":
    cli()   # pylint: disable=no-value-for-parameter

# EOF
