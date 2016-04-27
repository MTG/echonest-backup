import config
import db
import db.data
import logging
import util
#logging.basicConfig(level=logging.DEBUG)

import concurrent.futures
import echonest

def query(songid, token):
    data = echonest.song_by_enid(songid, token)
    return data


def lookup():
    songs = db.data.get_pending_songs()
    if not songs:
        return False
    # We can use a with statement to ensure threads are cleaned up promptly
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        # Start the load operations and mark each future with its URL
        i = 0
        future_to_song = {}
        for ss in util.chunks(songs, 10):
            future_to_song[executor.submit(query, ss, i)] = ss
            i = 1 - i

        for future in concurrent.futures.as_completed(future_to_song):
            ss = future_to_song[future]
            # For each set of songs, get them from the response
            # for songs not in the response, add an empty response
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
            else:
                gotsongs = set()
                waitings = set(ss)
                results = data["response"].get("songs", [])
                for s in results:
                    songid = s["id"]
                    gotsongs.add(songid)
                    db.data.add_response_if_not_exists(echonest.SONG_PROFILE, songid, s)
                nosongs = waitings-gotsongs
                for s in list(nosongs):
                    db.data.add_response_if_not_exists(echonest.SONG_PROFILE, s, {})
    return True

def main():
    db.init_db_engine(config.SQLALCHEMY_DATABASE_URI)
    res = lookup()
    i = 0
    while res:
        print("{}".format(i))
        res = lookup()
        i += 1

if __name__ == "__main__":
    main()
