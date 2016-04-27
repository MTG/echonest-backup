BEGIN;

CREATE UNIQUE INDEX echonest_artist_ndx_artistid ON echonest_artist (artistid);
CREATE UNIQUE INDEX echonest_song_ndx_songid ON echonest_song (songid);
CREATE UNIQUE INDEX musicbrainz_artist_ndx_echonest_query ON musicbrainz_artist (echonest_query);
CREATE UNIQUE INDEX musicbrainz_artist_ndx_mbid ON musicbrainz_artist (mbid);
CREATE UNIQUE INDEX discogs_artist_ndx_name ON discogs_artist (name);

CREATE INDEX echonest_response_date ON echonest_response (date);
CREATE INDEX echonest_response_query ON echonest_response (query);
CREATE INDEX echonest_response_url ON echonest_response (url);

CREATE INDEX echonest_response_json_id ON echonest_response_json (id);

COMMIT;
