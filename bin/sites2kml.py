#!python3

from datetime import date
import frontmatter
import os
from pathlib import Path
import simplekml

class Location:
	def __init__(self, name, latitude, longitude):
		self.Name = name
		self.Latitude = latitude
		self.Longitude = longitude

	def __lt__(self, other):
		if(self.Latitude < other.Latitude):
			return True
		if(self.Latitude > other.Latitude):
			return False
		return self.Longitude < other.Longitude

	def __eq__(self, other):
		return self.Latitude == other.Latitude and self.Longitude == other.Longitude

def GetLocations():
	""" Retrieve Locations from markdown frontmatter annotations"""
	locations = list()

	# Load locations from markdown
	p = Path('_sites')
	for d in p.iterdir() :
		print("Loading on " + str(d))
		with open(d) as f:
			site = frontmatter.load(f)
			l = Location(site['Title'], site['WABird']['Coordinates']['Latitude'], site['WABird']['Coordinates']['Longitude'])
			locations.append(l)

	# sort the list of locations (sort is by Lat, then Long) so that they appear in a consistent order
	locations.sort(reverse=True)
	return locations

def LocationsToKML(locations):
	""" Convert locations to a KML file """
	sites = simplekml.Kml(name="Washington Birding Site Impressions, " + date.today().strftime("%Y/%m/%d"))
	for l in locations:
		sites.newpoint(name=l.Name, coords=[(l.Longitude, l.Latitude)])
	sites.save("sites.kml")

def main(): 
	locations = GetLocations()
	LocationsToKML(locations)

main()