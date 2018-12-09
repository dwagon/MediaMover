#!/usr/bin/env python

import os
import re
import pipes


srcdir = '/data/sabnzbd/Downloads/complete/'
dstdir = '/Music/TV'
kiddingFlag = True


##############################################################################
def demangle_showname(name):
    m = re.match(r'(?P<name>.*)S(?P<season>\d+)E(?P<episode>\d+)(.*)', name)
    if not m:
        print("Didn't understand {}".format(name))
        return None, None
    sname = m.group('name').replace('.', ' ').strip()
    if sname.startswith('_UNPACK_'):
        sname = sname.replace('_UNPACK_', '')
    season = int(m.group('season').lstrip('0'))
    episode = int(m.group('episode').lstrip('0'))
    return sname, season, episode


##############################################################################
def make_show_dirs(showname, season):
    dest = os.path.join(dstdir, showname)
    if not os.path.exists(dest):
        if kiddingFlag:
            print("mkdir {}".format(dest))
        else:
            os.mkdir(dest)

    seasondir = os.path.join(dest, 'Season {}'.format(season))
    if not os.path.exists(seasondir):
        if kiddingFlag:
            print("mkdir {}".format(seasondir))
        else:
            os.mkdir(seasondir)
    return seasondir


##############################################################################
def move_show(fname, destdir, destfile):
    dest = pipes.quote("{}/{}".format(destdir, destfile))
    fname = pipes.quote(fname)
    if kiddingFlag:
        print("mv {} {}".format(fname, dest))
    else:
        os.system("mv {} {}".format(fname, dest))


##############################################################################
def main():
    for root, dirs, files in os.walk(srcdir):
        if files:
            m_showname = root.replace(srcdir, '')
            showname, season, episode = demangle_showname(m_showname)
            destdir = make_show_dirs(showname, season)
            for fname in files:
                srcfile = os.path.join(root, fname)
                ext = os.path.splitext(srcfile)[-1]
                destfile = "{}.S{:02d}E{:02d}{}".format(showname, season, episode, ext)
                move_show(srcfile, destdir, destfile)


##############################################################################
if __name__ == "__main__":
    main()

# EOF
