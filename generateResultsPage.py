import os
import argparse
from subprocess import call
from htmlGenerator import writeResultsToHTML

def scrapeResultsToHTMLforURL(searchName, baseURL):
	scrapResultsFile = "results.json"
	try:
		os.remove("./" + scrapResultsFile) 
	except OSError:
	    pass

	call('scrapy crawl RightmoveSpider -a baseURL=' + baseURL + ' -a searchName=' + searchName + ' -o ' + scrapResultsFile, shell=True)

	writeResultsToHTML(searchName, scrapResultsFile)

	try:
		os.remove("./" + scrapResultsFile) 
	except OSError:
	    pass


parser = argparse.ArgumentParser(description='generate easy to read html pages from scraped rightmove results')
parser.add_argument('-d','--days', help='Days since added on rightmove (must be 1,3,7,14)',required=True)
parser.add_argument('-p','--price', help='Max price (eg, 500000)',required=True)
parser.add_argument('-b','--bedrooms', help='Min bedrooms (eg, 2)',required=True)
args = parser.parse_args()

days = str(args.days)

areas = {}
with open("searchAreas.txt") as searchAreasFile:
    for line in searchAreasFile:
        name, areaID = line.partition(",")[::2]
        areas[name.strip()] = areaID.strip()

urls = {}
for name, areaID in areas.items():
	urls[name] = ("\"http://www.rightmove.co.uk/property-for-sale/find.html?" + "locationIdentifier=USERDEFINEDAREA%5E%7B%22id%22%3A" + areaID + "%7D" + "&minBedrooms=" + args.bedrooms + "&maxPrice=" + args.price + "&sortType=6" + "&maxDaysSinceAdded=" + days + "\"")

for key, value in urls.items():
	scrapeResultsToHTMLforURL(key, value)


