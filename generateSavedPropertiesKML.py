import os
import argparse
from subprocess import call

scrapResultsFile = "saveResults.xml"
scrapResultsOutput = "results/savedProperties.kml"

parser = argparse.ArgumentParser(description='generate kml of all your rightmove saved properties')
parser.add_argument('-u', '--username', help='Specify username', required=True)
parser.add_argument('-p', '--password', help='Specify password', required=True)
args = parser.parse_args()

# remove any xml content
try:
	os.remove("./" + scrapResultsFile) 
except OSError:
    pass

# perform scrape
call('scrapy crawl RightmoveSavedPropertiesSpider ' + ' -a username=' + args.username + ' -a password=' + args.password + ' -o ' + scrapResultsFile, shell=True)

# read all lines from xml
f = open("./" + scrapResultsFile, "r")
contents = f.readlines()
f.close()

# add kml tags
contents.insert(1, "<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n")
contents.insert(len(contents), "</kml>\n")

# convert to kml format
i = 0
for line in contents:
   	contents[i] = contents[i].replace("items", "Document")
   	contents[i] = contents[i].replace("item", "Placemark")
   	contents[i] = contents[i].replace("</value><value>",",")
   	contents[i] = contents[i].replace("<value>","")
   	contents[i] = contents[i].replace("</value>","")
   	i = i + 1

# write kml
f = open("./" + scrapResultsOutput, "w")
contents = "".join(contents)
f.write(contents)
f.close()

# remove the xml file
try:
	os.remove("./" + scrapResultsFile) 
except OSError:
    pass