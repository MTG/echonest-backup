BEGIN;

CREATE TABLE echonest_artist (
  artistid    TEXT NOT NULL
);

CREATE TABLE echonest_song (
  songid      TEXT NOT NULL
);

CREATE TABLE musicbrainz_artist (
  mbid           UUID,
  echonest_query VARCHAR -- use this to join to echonest_response.query
  -- in the format musicbrainz:artist:mbid
);

CREATE TABLE discogs_artist (
  name           VARCHAR
);

CREATE TABLE echonest_response (
  id          SERIAL,
  url         VARCHAR NOT NULL,
  query       VARCHAR NOT NULL,
  date        TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE echonest_response_json (
  id          INTEGER, -- FK to echonest_response.id
  data        JSONB    NOT NULL
);


COMMIT;
