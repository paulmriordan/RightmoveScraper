import scrapy


# TODO

# Navigate to property site and search for ground floor and purpose built

# Search the key features section

# Easy to view list
#   html with images and links
#       Copy over the entire element, with images?

# Write an extension to filter out places not meeting word filter criteria (purpose built, ground floor)
#   Also add button to manually discard a result

#   Prevent repeatedly finding the same property
#       Note: must allow price updates to be seen

#   Args for the price and location
#   Setup User Agent


# "div.propertyCard-description span::text" => gets the description summary 


class RightmoveSpider(scrapy.Spider):
    name = 'RightmoveSpider'


    def start_requests(self):

        start_urls = []
        baseURL = "http://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E87490&minBedrooms=2&maxPrice=475000&sortType=6&includeSSTC=false";
        for index in range(0, 24, 24):
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
        _filter = ["purpose built", "purpose-built", "ex-council"]
        if not any(word in s for s in description for word in _filter):
            yield {
                'url': response.url,
                'description': response.css('p[itemprop="description"]').extract(),
                'images': response.css('meta[itemprop="contentUrl"]::attr(content)').extract()
            }

    # def parse_author(self, response):
    #     def extract_with_css(query):
    #         return response.css(query).extract_first().strip()

    #     yield {
    #         'name': extract_with_css('h3.author-title::text'),
    #         'birthdate': extract_with_css('.author-born-date::text'),
    #         'bio': extract_with_css('.author-description::text'),
    #     }

