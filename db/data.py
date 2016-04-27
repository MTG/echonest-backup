import db
from sqlalchemy import text
import json

def get_pending_musicbrainz_artists():
    """Get 100 MusicBrainz Artist ids which have not been mapped
       to Echo Nest ids."""
    q = text("""
        SELECT mba.echonest_query
          FROM musicbrainz_artist mba
     LEFT JOIN echonest_response enr
            ON mba.echonest_query = enr.query
           AND enr.url = :artist_profile
         WHERE enr.id is null
         LIMIT 100""")
    with db.engine.begin() as connection:
        res = connection.execute(q, {"artist_profile": "/artist/profile"})
        return [r[0] for r in res.fetchall()]

def get_pending_songs():
    """Get 100 pending Echo Nest song ids which haven't been looked up
    """
    q = text("""
        SELECT ens.songid
          FROM echonest_song ens
     LEFT JOIN echonest_response enr
            ON ens.songid = enr.query
           AND enr.url = :song_profile
         WHERE enr.id is NULL
         LIMIT 100""")
    with db.engine.begin() as connection:
        res = connection.execute(q, {"song_profile": "/song/profile"})
        return [r[0] for r in res.fetchall()]



def add_response_if_not_exists(url, query, data):
    with db.engine.begin() as connection:
        if not response_exists(connection, url, query):
            add_response(connection, url, query, data)


def response_exists(connection, url, query):
    q = text("""
        SELECT id
          FROM echonest_response
         WHERE query = :query
           AND url = :url""")
    res = connection.execute(q, {"query": query, "url": url})
    if res.rowcount:
        return True
    else:
        return False


def add_response(connection, url, query, data):
    q = text("""
        INSERT INTO echonest_response
                    (query, url)
             VALUES (:query, :url)
          RETURNING id""")
    res = connection.execute(q, {"query": query, "url": url})
    id = res.fetchone()[0]
    if data:
        q = text("""
            INSERT INTO echonest_response_json
                        (id, data)
                 VALUES (:id, :data)""")
        connection.execute(q, {"id": id, "data": json.dumps(data)})


def add_echonest_artist_id(artistid):
    """ Add an artist id if it isn't in the `echonest_artists` table """
    check = text("""
        SELECT *
          FROM echonest_artist
         WHERE artistid = :artistid""")
    insert = text("""
        INSERT INTO echonest_artist
                    (artistid)
             VALUES (:artistid)""")

    with db.engine.begin() as connection:
        res = connection.execute(check, {"artistid": artistid})
        if not res.rowcount:
            connection.execute(insert, {"artistid": artistid})

def add_echonest_song_ids(songids):
    """ Add an song id if it isn't in the `echonest_songs` table """
    check = text("""
        SELECT *
          FROM echonest_song
         WHERE songid = :songid""")
    insert = text("""
        INSERT INTO echonest_song
                    (songid)
             VALUES (:songid)""")

    with db.engine.begin() as connection:
        for songid in songids:
            res = connection.execute(check, {"songid": songid})
            if not res.rowcount:
                connection.execute(insert, {"songid": songid})
