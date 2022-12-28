import sys
import csv
from os import listdir
from os.path import isfile, join
from html.parser import HTMLParser

if len(sys.argv) < 2:
	print ("usage: python most-play.py [traktor history path] [year]")
	sys.exit()
DIR_PATH = sys.argv[1]

YEAR = "2022"
if len(sys.argv) > 2:
	YEAR = str(sys.argv[2])

print ("Finding tracks from " + YEAR + " in directory: " + DIR_PATH)
tracksMap = {}

class MyTrack:
	def __init__(self, audioid, artist, title):
		self.audioid = audioid
		self.artist = artist
		self.title = title
		self.count = 1
	
	def __str__(self):
		return "(" +  str(self.count) + ") - " + self.artist.decode() + " " + self.title.decode()


class MyHTMLParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		
		if tag == 'entry':
			audioid = ""
			artist = "".encode('utf-8')
			title = "".encode('utf-8')

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

def parse_serato(fullpath):
	with open(fullpath, 'rb') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		for row in csvreader:
			print (', '.join(row))

def parse_traktor(fullpath):
	file = open(fullpath, 'r')
	data = file.read().replace('\n', '')
	parser = MyHTMLParser()
	parser.feed(data)
	file.close()		

def count_tracks(filename):
	fullpath = DIR_PATH + filename
	
	if ".nml" in filename:
		parse_traktor(fullpath)
	elif ".csv" in filename:
		parse_serato(fullpath)
			
		

def summarize():
	sortedtracks = sorted(tracksMap, key=lambda x: tracksMap[x].count, reverse=True)
	count = 1
	for track in sortedtracks:
			print ("[", count, "]", tracksMap[track])
			count += 1

onlyfiles = [f for f in listdir(DIR_PATH) if isfile(join(DIR_PATH, f))]
count = 0
for filename in onlyfiles:
	
	if YEAR in filename:
		count_tracks(filename)
		count += 1

summarize()		
