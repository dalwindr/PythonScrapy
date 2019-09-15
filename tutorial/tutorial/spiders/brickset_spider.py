import scrapy
# scrapy shell https://brickset.com/sets/year-2016


class QuotesSpider(scrapy.Spider):
    name = "bricksetSpider"
    # scrapy crawl bricksetSpider -o bricksetSpider.json
    # scrapy crawl bricksetSpider -o bricksetSpider.csv
    # scrapy crawl bricksetSpider -o bricksetSpider.xml
    # scrapy crawl bricksetSpider -o bricksetSpider.jl

    def start_requests(self):
        allowed_domains = ['http://brickset.com/sets/year-2016']
        urls = [
            'http://brickset.com/sets/year-2016'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse1(self, response):
        title = response.css("title::text").get()
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse(self, response):
        for responseSet in response.css('.set'):
            header_data = responseSet.css('h1 ::text').get()
            # responseSet.css('dl a::text').getall()
            # string0 = responseSet.css('dl dt::text')[0].get()
            # string0_val = responseSet.css('dl a::text')[0].get()
            #
            # string1 = responseSet.css('dl dt::text')[1].get()
            # string1_val = responseSet.css('dl a::text')[1].get()
            #
            # string2 = responseSet.css('dl dt::text')[2].get()
            # string2_val = responseSet.css('dl dd')[2].css('dd::text').get()
            #

            PIECES_SELECTOR = './/dl[dt/text() = "Pieces"]/dd/a/text()'
            p_data = responseSet.xpath(PIECES_SELECTOR).get()

            MINIFIGS_SELECTOR = './/dl[dt/text() = "Minifigs"]/dd[2]/a/text()'
            m_data = responseSet.xpath(MINIFIGS_SELECTOR).get()

            RRP_SELECTOR = './/dl[dt/text() = "RRP"]/dd[3]'
            rrp_data = responseSet.xpath(RRP_SELECTOR).css('dd::text').get()

            PPP_SELECTOR = './/dl[dt/text() = "PPP"]/dd[4]'
            ppp_data = responseSet.xpath(PPP_SELECTOR).css('dd::text').get()

            rating_data = responseSet.css('div.rating a::text').get()

            yield {
                    'header':  header_data,
                    'pieces': p_data,
                    'Minifigs': m_data,
                    'RRP': rrp_data,
                    'PPP': ppp_data,
                    'rating': rating_data
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
