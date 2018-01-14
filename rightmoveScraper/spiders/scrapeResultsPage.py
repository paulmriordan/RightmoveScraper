import scrapy

class RightmoveSpider(scrapy.Spider):
    name = 'RightmoveSpider'

    exclude_list = []

    def start_requests(self):

        self.exclude_list = [line.rstrip() for line in open('excludeList.txt','r')]
        #print "exclude list"
        #for p in self.exclude_list: print p

        batterseaSearch = "http://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=USERDEFINEDAREA%5E%7B%22id%22%3A4711964%7D&minBedrooms=2&maxPrice=500000&sortType=6"
        hackney         = "http://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=USERDEFINEDAREA%5E%7B%22id%22%3A4711961%7D&minBedrooms=2&maxPrice=500000&sortType=6"
        finsbury        = "http://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=USERDEFINEDAREA%5E%7B%22id%22%3A4711952%7D&minBedrooms=2&maxPrice=500000&sortType=6"
        baseURL = finsbury
        
        start_urls = []
        max_properties = 1000
        for index in range(0, max_properties, 24):
            start_urls.append(baseURL + '&index=' + str(index))

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for href in response.css('a.propertyCard-link::attr(href)'):
            yield response.follow(href, self.parse_property)

    def parse_property(self, response):

        description = response.css('p[itemprop="description"]::text').extract()
        # for des in description: print des
        # for p in self.exclude_list: print p
        # description = ["test", "ex-local"]
        failedExcludeTest = self.doesStringListContainAnyTerms(description, self.exclude_list)
        print "exclude test failed: " + str(failedExcludeTest)

        if not failedExcludeTest:
            yield {
                'title': response.css("head > title::text").extract(),
                'price': response.css("#propertyHeaderPrice > strong::text").extract(),
                'floorplan': response.css("div.zoomableimagewrapper > img::attr(src)").extract(),
                'url': response.url,
                'description': response.css('p[itemprop="description"]').extract(),
                'images': response.css('meta[itemprop="contentUrl"]::attr(content)').extract(),
                'map': response.css('a[class="block js-tab-trigger js-ga-minimap"] img::attr(src)').extract()
            }

    def doesStringListContainAnyTerms(self, stringList, searchTerms):
        for searchIn in stringList:
            for searchFor in searchTerms:
                # print "searchFor " + searchFor + " searchIn " + searchIn + " result " + str(searchFor in searchIn)
                if searchFor in searchIn:
                    return True
        return False
        #return any(word in s for s in stringList for word in searchTerms)