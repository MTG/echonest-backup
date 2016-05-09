import config
import db
import db.data
import util
import time
import datetime


import concurrent.futures
import echonest
import log

def query(songid, token):
    data = echonest.song_by_enid(songid, token)
    return data


def lookup():
    """ returns (done, remaining)"""
    songs = db.data.get_pending_songs()
    songcount = db.data.get_count_pending_songs()

    if not songs:
        return (0, 0)

    # We can use a with statement to ensure threads are cleaned up promptly
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Start the load operations and mark each future with its URL
        i = 0
        future_to_song = {}
        for songchunk in util.chunks(songs, 10):
            future_to_song[executor.submit(query, songchunk, i)] = songchunk
            i = 1 - i

        for future in concurrent.futures.as_completed(future_to_song):
            songchunk = future_to_song[future]
            # For each set of songs, get them from the response
            # for songs not in the response, add an empty response
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (songchunk, exc))
            else:
                gotsongs = set()
                waitings = set(songchunk)
                results = data["response"].get("songs", [])
                for s in results:
                    songid = s["id"]
                    gotsongs.add(songid)
                    response = {"response": {"songs": [s], "status": data["response"]["status"]}}
                    db.data.add_response_if_not_exists(echonest.SONG_PROFILE, songid, response)
                nosongs = waitings-gotsongs
                for s in list(nosongs):
                    db.data.add_response_if_not_exists(echonest.SONG_PROFILE, s, {})

    return (len(songs), songcount-len(songs))


def main():
    db.init_db_engine(config.SQLALCHEMY_DATABASE_URI)
    total = db.data.get_count_pending_songs()
    done = 0
    starttime = time.time()
    thisdone, rem = lookup()
    done += thisdone
    while rem > 0:
        thisdone, rem = lookup()
        done += thisdone
        durdelta, remdelta = util.stats(done, total, starttime)
        log.info("Done %s/%s in %s; %s remaining", done, total, str(durdelta), str(remdelta))

if __name__ == "__main__":
    main()
