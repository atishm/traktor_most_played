#!/usr/bin/env python

"""Parses a directory of traktor histories to determine most played tracks

My Traktor history directory is here: python most-played.py ~/Documents/Native\ Instruments/Traktor\ 2.11.0/History/
So my command-line looks like:
python most-played.py ~/Documents/Native\ Instruments/Traktor\ 2.11.0/History/ 2016
"""

import sys
from os import listdir
from os.path import isfile, join
import HTMLParser

if len(sys.argv) < 2:
	print "usage: python most-play.py [traktor history path] [year]"
	sys.exit()
DIR_PATH = sys.argv[1]

YEAR = "2016"
if len(sys.argv) > 2:
	YEAR = str(sys.argv[2])

print "Finding tracks from " + YEAR + " in directory: " + DIR_PATH
tracksMap = {}

class MyTrack:
	def __init__(self, audioid, artist, title):
		self.audioid = audioid
		self.artist = artist
		self.title = title
		self.count = 0
	
	def __str__(self):
		return str("(" +  str(self.count) + ") " + self.artist + " - " + self.title)



class MyHTMLParser(HTMLParser.HTMLParser):
    def handle_starttag(self, tag, attrs):
    	if tag == 'entry':
    		
    		audioid = ""
    		artist = ""
    		title = ""

	        for name, value in attrs:
	        	if name == 'audio_id':
	        		audioid = value.encode('utf-8')
	        	if name == 'title':
	        		title = value.encode('utf-8')
	        	if name =='artist':
	        		artist = value.encode('utf-8')
	        		
	        if audioid:
	        	if audioid not in tracksMap:
		        	track = MyTrack(audioid, artist, title)
		        	tracksMap[audioid] = track
		        else:
		        	tracksMap[audioid].count += 1 

def count_tracks(filename):
	fullpath = DIR_PATH + filename
	file = open(fullpath, 'r')
	data= file.read().replace('\n', '').decode("utf8")
	parser = MyHTMLParser()
	parser.feed(data)
	file.close()

def summarize():
	sortedtracks = sorted(tracksMap, key=lambda x: tracksMap[x].count, reverse=True)
	count = 1
	for track in sortedtracks:
			print "[", count, "]", tracksMap[track]
			count += 1

onlyfiles = [f for f in listdir(DIR_PATH) if isfile(join(DIR_PATH, f))]
count = 0
for filename in onlyfiles:
	if YEAR in filename:
		count_tracks(filename)
		count += 1

summarize()		



