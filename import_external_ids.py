"""
Used to import external data into the local database, to be used as a seed
to search Echo Nest for artists and songs.


MusicBrainz:

Put the result of these two queries in a text file. One per line
    select gid from artist;
    select gid from artist_gid_redirect;

Run

    import_external_ids.py musicbrainz <datafile>


Discogs:
    Artist names one per line

Run

    import_external_ids.py discogs <datafile>

MSD Song:
    Song ids from the MSD metadata db

Run
    import_external_ids.py msdsong track_metadata.db

MSD Artist:
    Artist ids from the MSD metadata db

Run
    import_external_ids.py msdartist track_metadata.db
"""

import config
import db
import db.data
import argparse
from sqlalchemy import text
import sqlite3

def get_sqlite_cursor(sqlfname):
    conn = sqlite3.connect(sqlfname)
    return conn.cursor()

def import_msd_artists(sqlfname):
    q = "select distinct(artist_id) from songs"
    c = get_sqlite_cursor(sqlfname)
    artists = []
    for row in c.execute(q):
        db.data.add_echonest_artist_id(row[0])


def import_msd_songs(sqlfname):
    q = "select distinct(song_id) from songs"
    c = get_sqlite_cursor(sqlfname)
    songs = []
    for row in c.execute(q):
        songs.append(row[0])
    db.data.add_echonest_song_ids(songs)


def import_musicbrainz(fname):
    mbids = open(fname).read().splitlines()
    with db.engine.begin() as connection:
        for m in mbids:
            query = text("""INSERT INTO musicbrainz_artist
                                        (mbid, echonest_query)
                                 VALUES (:mbid, :query)""")
            connection.execute(query, {"mbid": m, "query": "musicbrainz:artist:%s" % m})

def import_discogs(fname):
    names = open(fname).read().splitlines()
    with db.engine.begin() as connection:
        for n in names:
            query = text("""INSERT INTO discogs_artist
                                        (name)
                                 VALUES (:name)""")
            connection.execute(query, {"name": n})

def main(args):
    db.init_db_engine(config.SQLALCHEMY_DATABASE_URI)
    if args.source == "musicbrainz":
        import_musicbrainz(args.filename)
    elif args.source == "discogs":
        import_discogs(args.filename)
    elif args.source == "msdartist":
        import_msd_artists(args.filename)
    elif args.source == "msdsong":
        import_msd_songs(args.filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import external ids into the database")
    parser.add_argument("source", choices=["musicbrainz", "discogs", "msdsong", "msdartist"])
    parser.add_argument("filename")
    args = parser.parse_args()
    main(args)


