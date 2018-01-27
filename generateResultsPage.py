import os
import datetime
import argparse
from subprocess import call

def writeResultsToHTML(searchName):

	now = datetime.datetime.now()
	fileName = 'results/results_' + searchName + '_' + now.strftime("%Y-%m-%d")

	before = """<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.1/jquery.min.js"></script>
	<script>
	(function($) {

	    $(function(){ // ON DOM READY
	"""

	with open(fileName + '.html', 'w') as outputHTML:

		outputHTML.write(before)
		outputHTML.write("var data=")

		with open('./results.json', 'r') as jsonResults:
			jsonString = jsonResults.read()
			outputHTML.write(jsonString)

		outputHTML.write(""", data = data,
	            target = $('#target'),
	            html;

	        $.each(data, function (key, val) {
	            html = '<div class="resultsList">';

	            html += '<p class="image-title">' + val.title + '</p>';
	            html += '<p class="image-title">' + val.price + '</p>';

	            $.each(val.images, function (index, value) {
					html += '<a href=' + val.url + ' target="_blank">';
	            	html += '<img src ="' + value + '" class="image-styles" />';
	            	html += '</a>'
		        })

		        if (val.floorplan.length != 0) {
		        	html += '<img src ="' + val.floorplan + '" class="image-styles" />';
	            }

	            html += '<img src ="http:' + val.map + '" class="image-styles" />';

	            html += '<p class="image-title">' + val.description + '</p>';
	            
	            html += '</div>';
	            target.append(html);
	        });

	    }); // end of on DOM READY

	}(jQuery));
	</script>
	<div id="target"></div>
	<style>
	.resultsList{
	    text-align:left;
	    border:20px solid #666;
	}
	img{
	    width:100%;
	    max-width:200px;
	}
	.images-styles{
	    display:inline-block;
	    margin:10px 10px;
	    padding:5px;
	    border:5px solid #CCC;
	}
	.image-title {
	    background:#000;
	    width:80%;
	    position:relative;
	    bottom:15px;
	    left:15px;
	    color:#f7f7f7;
	    text-align:center;
	    padding:2px;
	    opacity:0.6;
	    filter:alpha(opacity=60);
	    /* For IE8 and earlier */
	}
	</style>""")

def scrapeResultsToHTMLforURL(searchName, baseURL):
	scrapResultsFile = "./results.json"
	try:
		os.remove(scrapResultsFile) 
	except OSError:
	    pass
	call('scrapy crawl RightmoveSpider -a baseURL=' + baseURL + ' -a searchName=' + searchName + ' -o results.json', shell=True)

	writeResultsToHTML(searchName)


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
	urls[name] = ("\"http://www.rightmove.co.uk/property-for-sale/find.html?" + "locationIdentifier=USERDEFINEDAREA%5E%7B%22id%22%3A" + areaID + "%7D" + "&minBedrooms=" + args.bedrooms + "&maxPrice=" + args.bedrooms + "&sortType=6" + "&maxDaysSinceAdded=" + days + "\"")

for key, value in urls.items():
	scrapeResultsToHTMLforURL(key, value)


