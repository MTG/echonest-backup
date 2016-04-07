import os
import time
import datetime
import errno
import argparse
import sqlite3
import json

import logging
logfmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

lookuplog = logging.Logger('lookup')
ch = logging.StreamHandler()
ch.setFormatter(logfmt)
lookuplog.setLevel(logging.INFO)
lookuplog.addHandler(ch)

import echonest

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def save(folder, id, data):
    outdir = os.path.join(folder, id[:4])
    outfile = os.path.join(outdir, "%s.json" % id)
    mkdir_p(outdir)
    json.dump(data, open(outfile, "w"))

def load_songs(sqlfname):
    conn = sqlite3.connect(sqlfname)
    c = conn.cursor()
    q = "select distinct(song_id) from songs"
    songs = []
    for row in c.execute(q):
        songs.append(row[0])
    return songs

def lookup_song(songid):
    output_dir = "songs"
    #lookuplog.info(songid)
    outdir = os.path.join(output_dir, songid[:4])
    outfile = os.path.join(outdir, "%s.json" % songid)
    if os.path.exists(outfile):
        pass
    else:
        data = echonest.song_by_enid(songid)
        save(output_dir, songid, data)

def status_iter(iterable, callback, reportsize=1):
    itersize = len(iterable)
    starttime = time.time()
    for i, item in enumerate(iterable, 1):
        callback(item)
        if i % reportsize == 0:
            nowtime = time.time()
            numblocks = itersize * 1.0 / reportsize
            curblock = i / reportsize
            position = curblock / numblocks
            duration = round(nowtime - starttime)
            durdelta = datetime.timedelta(seconds=duration)
            remaining = round((duration / position) - duration)
            remdelta = datetime.timedelta(seconds=remaining)
            lookuplog.info("Done %s/%s in %s; %s remaining", i, itersize, str(durdelta), str(remdelta))
    lookuplog.info("Finished")

def main(args):
    lookuplog.info("loading...")
    songs = load_songs(args.sqldb)
    lookuplog.info("got %s songs to process", len(songs))

    status_iter(songs, lookup_song, 10)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Look up echonest data")
    parser.add_argument("sqldb", type=str, help="The MSD sqlite metadata file")
    args = parser.parse_args()
    main(args)

