#!/usr/bin/env python

import xml.parsers.expat
import csv

DISCOGS_DB_DUMP = '/home/andres/Downloads/discogs_20160401_artists.xml'

curr_tag = None
curr_level = 0
curr_values = []
curr_value = []
curr_id = ''

def start_element(name, attrs):
    global curr_tag, curr_level, curr_value, curr_id
    if name == 'artist':
        curr_level = 1
        curr_value = []
        curr_id = ''
    else:
        curr_level += 1
    curr_tag = name


def char_data(value):
    global curr_values, curr_level, curr_value, curr_id
    if curr_level == 2 and curr_tag == 'name':
        if value == 'John Tejada':
            print value
        curr_value.append(value.encode('utf-8'))
    if curr_level == 2 and curr_tag == 'id':
        curr_id = value.encode('utf-8')

def end_element(name):
    global curr_level, curr_values, curr_value, curr_id 
    curr_level -= 1
    if name == 'artist':
        curr_values.append({'id':curr_id, 'name': curr_value})

p = xml.parsers.expat.ParserCreate()
p.StartElementHandler = start_element
p.EndElementHandler = end_element
p.CharacterDataHandler = char_data

f = open(DISCOGS_DB_DUMP)
p.ParseFile(f)
print len(curr_values)

with open('/tmp/artist_discogs_20160401.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for value in curr_values:
        writer.writerow([value['id'], ' '.join(value['name'])])
