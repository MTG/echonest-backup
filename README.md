Echo Nest API scraper
=====================

The Echo Nest API will stop serving requests on May 31, 2016. This means
that it will no longer be possible to resolve Echo Nest IDs to metadata
using a public service.

We are scraping as much metadata as possible, using the Million Song Dataset
as a starting point.

Usage
=====
We use python 3. Dependencies are provided in `requirements` and can be
installed with `pip`.

Copy `config.py.sample` to `config.py` and fill in your Echo Nest API Key.

Download the [MSD track metadata sqlite file](http://labrosa.ee.columbia.edu/millionsong/sites/default/files/AdditionalFiles/track_metadata.db).

Song lookup
-----------

`lookup.py` will search Echo Nest Song IDs from the `track_metadata.db`
database and save profile information including IDs from all known
Rosetta Stone buckets.
Run it like this:

    python lookup.py track_metadata.db

Additional sources of data
==========================

 * We can query Echo Nest API using IDs from other rosetta stone ID spaces.
  * To start with, get all artist MBIDs from MusicBrainz and map to EN Artist IDs
  * Use Discogs artist list to search EN for artist ids
 * Use `/artist/songs` to get other songs that Echo Nest knows about (starting with artists in MSD)
 * Get other datasets/lists of IDs from other sources

Status
======
 * April 8: MSD lookup finished. Interestingly, lookups seem to have failed for ~20% of the available IDs
 * April 8: We have collected MusicBrainz artist ids to look up on EN

Help us
=======
We still need development effort on the following tasks:
 * Search EN using artist names from Discogs ([#1](https://github.com/MTG/echonest-backup/issues/1))
 * Find all songs by an artist ([#3](https://github.com/MTG/echonest-backup/issues/3))

License
=======

This code is Copyright 2016 Music Technology Group, Universitat Pompeu Fabra.
It is released under the GNU General Public License, v3 or later.
See COPYING for more details.
