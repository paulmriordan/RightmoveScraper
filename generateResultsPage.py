import os
from subprocess import call

scrapResultsFile = "./results.json"

try:
	os.remove(scrapResultsFile) 
except OSError:
    pass

call('scrapy crawl RightmoveSpider -o results.json', shell=True)

before = """<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.1/jquery.min.js"></script>
<script>
(function($) {

    $(function(){ // ON DOM READY
"""

with open('results.html', 'w') as outputHTML:

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

            $.each(val.images, function (index, value) {
				html += '<a href=' + val.url + ' target="_blank">';
            	html += '<img src ="' + value + '" class="image-styles" />';
            	html += '</a>'
	        })

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