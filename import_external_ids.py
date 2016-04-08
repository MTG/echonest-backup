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
"""

import config
import db
import argparse
from sqlalchemy import text

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import external ids into the database")
    parser.add_argument("source", choices=["musicbrainz", "discogs"])
    parser.add_argument("filename")
    args = parser.parse_args()
    main(args)


