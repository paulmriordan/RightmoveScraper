# Rightmove Scraper

Scrape properties from rightmove and creates an easy to read html page with the results.

Filter results with custom key-words (eg, don't show results which have 'ground floor' in the description)

Resulting html page has **all** pictures, description, map, price, and floor plan for each result, and shows **every** result on one page.

![Result Example](https://github.com/paulmriordan/RightmoveScraper/raw/master/exampleScreenshot.PNG "Example screenshot")

[Result page example](https://github.com/paulmriordan/rightmovescraper/exampleResultsPeckham)

## Running the script

Execute the following python script

```
generateResultsPage.py -d 1 -p 500000 -b 2
```

Arguments:

- -d = Days since added on rightmove (must be 1,3,7,14)
- -p = Max price (eg, 500000)
- -b = Min bedrooms (eg, 2)

Properties containing any of terms in **excludeList.txt** will be excluded. Update this list with your preferences.

Only the areas specified in **searchAreas.txt** will be searched. Update this with your areas id. This ID can be found the URL for your drawn area, here:

![Search area ID](https://github.com/paulmriordan/RightmoveScraper/raw/master/searchAreaID.PNG "Search area ID")

Results are exported as HTML pages in the *results* subfolder

## Saved properities KML export

Rightmove doesn't offer an way to view your saved properties on a map. 

With this command, you can export all your saved properties to a KML file, which you can view via Google Maps:

```
generateSavedPropertiesKML.py -u [USERNAME] -p [PASSWORD]
```

A KML file is exported into the *results* subfolder

You can view KML files in Google Maps following [this guide](https://support.google.com/mymaps/answer/3024836)

## Requirements

- Python 3.x
- [Scrapy](https://scrapy.org/) - web scraping framework

## Things to do

- Should check number of results for an area before looping over subsequent pages. Currently loops over 1000 for every area, resulting in many unnecessary requests.
- Prevent repeatedly finding the same property. 
	- Add button to HTML results page to discard a property. This button add property to a list, and any property on this list is never shown again.
- Remove results which less than X pictures
- Improve filtering (eg, case insensitive search, use regex)
- Add EPC to results page
- Add the 'key features' to the results page
- Exported saved properties KML is hard-coded to a max of 200 properties.
