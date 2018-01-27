import scrapy

class RightmoveSpider(scrapy.Spider):

    MAX_PROPERTIES = 1000

    name = 'RightmoveSpider'
    baseURL = ''
    searchName = ''
    exclude_list = []

    def __init__(self, baseURL='', searchName='', **kwargs):

        self.baseURL = baseURL
        self.searchName = searchName
        # super().__init__(**kwargs)  # python3
        super(RightmoveSpider, self).__init__(**kwargs)  # python2

    def start_requests(self):

        self.exclude_list = [line.rstrip() for line in open('excludeList.txt','r')]
        #print "exclude list"
        #for p in self.exclude_list: print p

        start_urls = []
        for index in range(0, self.MAX_PROPERTIES, 24):
            start_urls.append(self.baseURL + '&index=' + str(index))

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        # self.num_properties = int(response.css('span[class="searchHeader-resultCount"]::text').extract_first().replace(',', ''))
        # print "\n***************************\n"
        # print "\n searchName " + self.searchName + " \n num properties " + str(self.num_properties) + " \n"
        # print "\n***************************\n"

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