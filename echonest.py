import requests
from requests.adapters import HTTPAdapter
import json
import sys

import config

import logging

buckets = ["id:7digital-US",
"id:7digital-AU",
"id:7digital-UK",
"id:facebook",
"id:fma",
"id:twitter",
"id:spotify-WW",
"id:seatwave",
"id:lyricfind-US",
"id:jambase",
"id:musixmatch-WW",
"id:seatgeek",
"id:openaura",
"id:spotify",
"id:spotify-WW",
"id:tumblr"]


# Use 5 retries for EN queries
s = requests.Session()
s.mount("http://developer.echonest.com", HTTPAdapter(max_retries=5))

def en_query(url, params):
    params["api_key"] =  config.ECHONEST_KEY
    params["format"] = "json"
    r = requests.get(url, params=params)
    if r.status_code == 429:
        logging.info("sleeping because ratelimit exceeded")
        time.sleep(30)
        return en_query(url, params)
    else:
        headers = r.headers
        remaining = int(headers.get("x-ratelimit-remaining", "0"))
        if remaining < 10:
            logging.info("sleeping because less than 10 remaining this minute")
            time.sleep(5)
        d = r.json()
        return d

def artist_by_mbid(artistid):
    params = {"id": "musicbrainz:artist:%s" % artistid,
              "bucket": buckets}
    url = "http://developer.echonest.com/api/v4/artist/profile"
    d = en_query(url, params)
    return d

def song_by_enid(songid):
    params = {"id": songid,
              "bucket": buckets}
    url = "http://developer.echonest.com/api/v4/song/profile"
    d = en_query(url, params)
    return d

def track_by_enid(trackid):
    params = {"id": trackid,
              "bucket": buckets}
    url = "http://developer.echonest.com/api/v4/track/profile"
    d = en_query(url, params)
    return d

def artist_by_enid(artistid):
    params = {"id": trackid,
              "bucket": buckets}
    url = "http://developer.echonest.com/api/v4/artist/profile"
    d = en_query(url, params)
    return d

def songs_for_artist(artistid):
    params = {"id": artistid, "results": 100}
    url = "http://developer.echonest.com/api/v4/artist/songs"
    d = en_query(url, params)
    return d
    pass
