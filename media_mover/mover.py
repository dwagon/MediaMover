#!/usr/bin/env python3

import click

import os
import re
import pipes


default_srcdir = '/data/sabnzbd/Downloads/complete/'
default_dstdir = '/Music/TV'


##############################################################################
def demangle_showname(name):
    m = re.match(r'(?P<name>.*)[Ss](?P<season>\d+)[Ee](?P<episode>\d+)(.*)', name)
    if not m:
        print("Didn't understand {}".format(name))
        return None, None, None
    sname = m.group('name').replace('.', ' ').strip()
    m2 = re.match(r'(?P<sname>.*)(?P<year>\d{4})', sname)
    if m2:
        sname = m2.group('sname').strip()
    if sname.startswith('_UNPACK_'):
        sname = sname.replace('_UNPACK_', '')
    season = int(m.group('season').lstrip('0'))
    episode = int(m.group('episode').lstrip('0'))
    return sname, season, episode


##############################################################################
def make_show_dirs(ctx, showname, season):
    dest = os.path.join(ctx.obj['destdir'], showname)
    if not os.path.exists(dest):
        if ctx.obj['kidding']:
            print("mkdir {}".format(dest))
        else:
            os.mkdir(dest)

    seasondir = os.path.join(dest, 'Season {}'.format(season))
    if not os.path.exists(seasondir):
        if ctx.obj['kidding']:
            print("mkdir {}".format(seasondir))
        else:
            os.mkdir(seasondir)
    return seasondir


##############################################################################
def move_show(ctx, fname, destdir, destfile):
    dest = pipes.quote("{}/{}".format(destdir, destfile))
    fname = pipes.quote(fname)
    if ctx.obj['kidding']:
        print("mv {} {}".format(fname, dest))
    else:
        if ctx.obj['verbose']:
            print("Moving {} to {}".format(fname, dest))
        os.system("mv {} {}".format(fname, dest))


##############################################################################
@click.command()
@click.option('-v', '--verbose', default=False, is_flag=True)
@click.option('-k', '--kidding', default=False, is_flag=True, help="Don't actually do anything")
@click.option('--srcdir', default=default_srcdir, help="Where to get files from")
@click.option('--destdir', default=default_dstdir, help="Where to put files to")
@click.pass_context
def cli(ctx, verbose, kidding, srcdir, destdir):
    ctx.obj['verbose'] = verbose
    ctx.obj['kidding'] = kidding
    ctx.obj['srcdir'] = srcdir
    ctx.obj['destdir'] = destdir
    for root, dirs, files in os.walk(ctx.obj['srcdir']):
        if files:
            m_showname = root.replace(ctx.obj['srcdir'], '')
            showname, season, episode = demangle_showname(m_showname)
            destdir = make_show_dirs(ctx, showname, season)
            for fname in files:
                srcfile = os.path.join(root, fname)
                ext = os.path.splitext(srcfile)[-1]
                if ext not in ('.mkv',):
                    if ext in ('.srt', '.nfo', '.sfv', '.srr', '.nzb', '.jpg'):
                        if ctx.obj['kidding']:
                            print("Deleting {} due to filetype {}".format(fname, ext))
                            os.unlink(srcfile)
                        else:
                            print("Would delete {} due to filetype {}".format(fname, ext))
                    else:
                        print("Skipping {} due to filetype {}".format(fname, ext))
                    continue
                destfile = "{}.S{:02d}E{:02d}{}".format(showname, season, episode, ext)
                move_show(ctx, srcfile, destdir, destfile)


##############################################################################
if __name__ == "__main__":
    cli(obj={})

# EOF
