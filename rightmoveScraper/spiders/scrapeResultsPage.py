import scrapy


class RightmoveSpider(scrapy.Spider):
    name = 'RightmoveSpider'


    def start_requests(self):

        batterseaSearch = "http://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=USERDEFINEDAREA%5E%7B%22id%22%3A4711964%7D&minBedrooms=2&maxPrice=500000&sortType=6"
        hackney         = "http://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=USERDEFINEDAREA%5E%7B%22id%22%3A4711961%7D&minBedrooms=2&maxPrice=500000&sortType=6"
        finsbury        = "http://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=USERDEFINEDAREA%5E%7B%22id%22%3A4711952%7D&minBedrooms=2&maxPrice=500000&sortType=6"
        baseURL = finsbury
        
        start_urls = []
        for index in range(0, 1000, 24):
            start_urls.append(baseURL + '&index=' + str(index))

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):

        # yield response.follow(response.css('a.propertyCard-link::attr(href)')[0], self.parse_property)

        # follow links to author pages
        for href in response.css('a.propertyCard-link::attr(href)'):
            yield response.follow(href, self.parse_property)

        # for property in response.css('div.l-searchResult'):
        #     yield {
        #         'description': property.css('div.propertyCard-description span::text').extract_first()
        #     }

        # next_page = response.css('li.next a::attr(href)').extract_first()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)

    # def parse(self, response):
    #     # follow links to author pages
    #     for href in response.css('.author + a::attr(href)'):
    #         yield response.follow(href, self.parse_author)

    #     # follow pagination links
    #     for href in response.css('li.next a::attr(href)'):
    #         yield response.follow(href, self.parse)

    def parse_property(self, response):

        description = response.css('p[itemprop="description"]::text').extract()
        # TODO  custom filter args
        _filter = ["purpose built", "purpose-built", "ex-council", "ground floor", "ground-floor", "ground flat", "ex-local", "ex local"]
        if not any(word in s for s in description for word in _filter):
            yield {
                'title': response.css("head > title::text").extract(),
                'price': response.css("#propertyHeaderPrice > strong::text").extract(),
                'floorplan': response.css("div.zoomableimagewrapper > img::attr(src)").extract(),
                'url': response.url,
                'description': response.css('p[itemprop="description"]').extract(),
                'images': response.css('meta[itemprop="contentUrl"]::attr(content)').extract(),
                'map': response.css('a[class="block js-tab-trigger js-ga-minimap"] img::attr(src)').extract()
            }

    # def parse_author(self, response):
    #     def extract_with_css(query):
    #         return response.css(query).extract_first().strip()

    #     yield {
    #         'name': extract_with_css('h3.author-title::text'),
    #         'birthdate': extract_with_css('.author-born-date::text'),
    #         'bio': extract_with_css('.author-description::text'),
    #     }

