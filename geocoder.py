#!/usr/bin/python
import cmd, sys, requests

class prompter(cmd.Cmd):
	def do_getFiles(self, args):
		"""[sourceFileName] [outputFileName]: Gets lat and long for a list of addresses using Google's Geocoder API."""
		l = args.split()
		if len(l) != 2:
			print "*** invalid number of arguments (source and dest file names are needed)."
			return
			
		getGeoCodings(l)

	def do_quit(self, args):
		"""Quits the program"""
		print "Quitting."
		raise SystemExit


def getGeoCodings(args):


	googleGeoCodingURL = "https://maps.googleapis.com/maps/api/geocode/json"
	
	print args[0]
	sourceFile = open(args[0], 'r')
	destFile = open(args[1], 'w')

	destFile.write("LOCATION, LAT, LNG\n")

	for line in sourceFile:

		print "Getting lat long for " + line

		#here's the meat: get JSON object from requests and parse out the lat longs

		geoCodingArgs =  {'address': line, 'sensor': 'false'}
		httpsRequest = requests.get(googleGeoCodingURL, params=geoCodingArgs)
		geoCodingJSON = httpsRequest.json()

		if geoCodingJSON["status"] == "OK":
			for item in geoCodingJSON["results"]: 

				latLong = item["geometry"]["location"]
				destFile.write("\"" + line + "\",%f,%f\n" % (latLong["lat"], latLong["lng"]))
				
		else:
			print "Error getting geoCoding for: " + line

		
	#closing all files
	sourceFile.close()
	destFile.close()
	
	
if __name__ == '__main__':
	prompt = prompter()
	prompt.prompt = ": "
	prompt.cmdloop('Type getFiles [sourceFileName] and [outputFileName] to get geocodings (Limit of 2500/day per Google\'s API')
