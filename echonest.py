import requests
from requests.adapters import HTTPAdapter
import json
import sys
import time
import os

import config

import logging

rosetta_buckets = ["id:7digital-US",
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
"id:tumblr",
"id:musicbrainz",
"id:discogs",
"id:eventful",
"id:songkick",
"id:songmeanings",
"id:whosampled"
]

# Use 5 retries for EN queries
s = requests.Session()
s.mount("http://developer.echonest.com", HTTPAdapter(max_retries=5))

def en_query(url_fragment, params, token):
    if not isinstance(config.ECHONEST_KEY, list):
        key = config.ECHONEST_KEY
    else:
        key = config.ECHONEST_KEY[token]
    params["api_key"] = key
    params["format"] = "json"
    url = "http://developer.echonest.com/api/v4" + url_fragment
    r = s.get(url, params=params)
    if r.status_code == 429:
        logging.info("sleeping because ratelimit exceeded")
        time.sleep(15)
        return en_query(url, params, token)
    else:
        headers = r.headers
        remaining = int(headers.get("x-ratelimit-remaining", "0"))
        if remaining < 10:
            logging.info("sleeping because less than 10 remaining this minute")
            time.sleep(5)
        d = r.json()
        if d["response"]["status"]["code"] == 0:
            return d
        else:
            raise Exception(json.dumps(d["response"]["status"]))

SONG_PROFILE = "/song/profile"
def song_by_enid(songid, token=0):
    buckets = rosetta_buckets + ["tracks"]
    params = {"id": songid,
              "bucket": buckets}
    d = en_query(SONG_PROFILE, params, token)
    return d

TRACK_PROFILE = "/track/profile"
def track_by_enid(trackid):
    buckets = rosetta_buckets + ["tracks"]
    params = {"id": trackid,
              "bucket": buckets}
    d = en_query(TRACK_PROFILE, params)
    return d

ARTIST_PROFILE = "/artist/profile"
def artist_profile(artistid, token=0):
    params = {"id": artistid,
              "bucket": rosetta_buckets}
    d = en_query(ARTIST_PROFILE, params, token)
    return d

ARTIST_SONGS = "/artist/songs"
def songs_for_artist(artistid, token=0):
    numresults = 100
    start = 0
    count = numresults
    songs = []

    params = {"id": artistid, "results": numresults, "start": start}
    d = en_query(ARTIST_SONGS, params, token)
    total = d["response"]["total"]
    songs.extend(d["response"]["songs"])
    # API returns an error if start >= 2000, so we stop here.
    while count <= total and start < 2000-numresults:
        start += numresults
        params = {"id": artistid, "results": numresults, "start": start}
        d = en_query(ARTIST_SONGS, params, token)
        ss = d["response"]["songs"]
        count += numresults
        songs.extend(ss)
    return songs
