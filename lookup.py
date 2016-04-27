import os
import time
import datetime
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
import util

def save(folder, id, data):
    outdir = os.path.join(folder, id[:4])
    outfile = os.path.join(outdir, "%s.json" % id)
    util.mkdir_p(outdir)
    json.dump(data, open(outfile, "w"))

def load_songs(sqlfname, offset):
    conn = sqlite3.connect(sqlfname)
    c = conn.cursor()
    q = "select distinct(song_id) from songs limit -1 offset %s" % (offset, )
    songs = []
    for row in c.execute(q):
        songs.append(row[0])
    return songs

def lookup_song(songid):
    output_dir = "songs"
    lookuplist = []
    for s in songid:
        outdir = os.path.join(output_dir, s[:4])
        outfile = os.path.join(outdir, "%s.json" % s)
        if not os.path.exists(outfile):
            lookuplist.append(s)
    if lookuplist:
        data = echonest.song_by_enid(songid)
        results = data["response"].get("songs", [])
        for s in results:
            songid = s["id"]
            outdir = os.path.join(output_dir, songid[:4])
            save(output_dir, songid, s)

def status_iter(iterable, callback, chunksize=1, reportsize=10):
    itersize = len(iterable)
    starttime = time.time()
    for i, item in enumerate(util.chunks(iterable, chunksize), 1):
        callback(item)
        if i % reportsize == 0:
            done = i * chunksize
            nowtime = time.time()
            numblocks = itersize * 1.0 / (reportsize*chunksize)
            curblock = done / (reportsize*chunksize)
            position = curblock / numblocks
            duration = round(nowtime - starttime)
            durdelta = datetime.timedelta(seconds=duration)
            remaining = round((duration / position) - duration)
            remdelta = datetime.timedelta(seconds=remaining)
            lookuplog.info("Done %s/%s in %s; %s remaining", done, itersize, str(durdelta), str(remdelta))
    lookuplog.info("Finished")

def main(args):
    lookuplog.info("loading...")
    songs = load_songs(args.sqldb, args.offset)
    lookuplog.info("got %s songs to process", len(songs))

    status_iter(songs, lookup_song, 10, 10)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Look up echonest data")
    parser.add_argument("sqldb", type=str, help="The MSD sqlite metadata file")
    parser.add_argument("offset", type=int, nargs='?', default=0, help="offset into the song db")
    args = parser.parse_args()
    main(args)

