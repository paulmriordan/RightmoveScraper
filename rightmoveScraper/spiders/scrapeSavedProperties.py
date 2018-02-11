import scrapy
import urlparse
from scrapy.utils.response import open_in_browser

class RightmoveSavedPropertiesSpider(scrapy.Spider):

    #TODO, scrape num pages from first page
    MAX_PROPERTIES = 200
    name = 'RightmoveSavedPropertiesSpider'
    start_urls = ['https://www.rightmove.co.uk/login.html']
    baseURL = 'http://www.rightmove.co.uk/user/shortlist.html?type=BUYING&propertyShortlistOrder=DATE_SAVED_DESCENDING'
    username = ""
    password = ""

    def __init__(self, username='', password='', **kwargs):

        print("******** init ************")
        self.username = username
        self.password = password
        # super().__init__(**kwargs)  # python3
        super(RightmoveSavedPropertiesSpider, self).__init__(**kwargs)  # python2

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'email': self.username, 'password': self.password},
            callback=self.after_login
        )

    def after_login(self, response):

        if "authentication failed" in response.body:
            self.logger.error("Login failed")
            return

        saved_urls = []
        for index in range(0, self.MAX_PROPERTIES, 10):
            saved_urls.append(self.baseURL + '&index=' + str(index))

        for url in saved_urls:
            yield scrapy.Request(url=url, callback=self.parse_list)

    def parse_list(self, response):

        for href in response.css('h2[class="address bedrooms"] > a::attr(href)'):
           yield response.follow(href, self.parse_property_kml)

    def parse_property_geojson(self, response):

        mapURL = response.css('a[class="block js-tab-trigger js-ga-minimap"] img::attr(src)').extract_first()
        splitQueries = urlparse.parse_qs(urlparse.urlsplit(mapURL).query)
        
        geometry = {}
        geometry['type'] = "Point"
        geometry['coordinates'] = [float(splitQueries['longitude'][0]), float(splitQueries['latitude'][0])]

        properties = {}
        properties['name'] = response.css("head > title::text").extract_first()
        properties['price'] = response.css("#propertyHeaderPrice > strong::text").extract_first()
        properties['url'] = response.url

        yield {
            'type' : "Feature",
            'geometry' : geometry,
            'properties' : properties
        }


    def parse_property_kml(self, response):

        mapURL = response.css('a[class="block js-tab-trigger js-ga-minimap"] img::attr(src)').extract_first()
        splitQueries = urlparse.parse_qs(urlparse.urlsplit(mapURL).query)
        
        point = {}
        point['coordinates'] = (float(splitQueries['longitude'][0]), float(splitQueries['latitude'][0]),0)

        yield {
            'Point' : point,
            'name' : response.css("#propertyHeaderPrice > strong::text").extract_first() + " " + response.css("head > title::text").extract_first(),
            'description' : response.url
        }
