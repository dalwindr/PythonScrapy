import scrapy
# scrapy shell https://www.geeksforgeeks.org


class QuotesSpider(scrapy.Spider):
    name = "geeksforgeeks"
    # scrapy crawl bricksetSpider -o bricksetSpider.json
    # scrapy crawl bricksetSpider -o bricksetSpider.csv
    # scrapy crawl bricksetSpider -o bricksetSpider.xml
    # scrapy crawl bricksetSpider -o bricksetSpider.jl

    def start_requests(self):
        allowed_domains = ['https://www.geeksforgeeks.org']
        urls = [
            'https://www.geeksforgeeks.org/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        header = response.css('header.entry-header h1::text').get()
        content = response.css('div.entry-content').css('p::text').getall()
        link = response.url
        if len(content) > 0:
            yield {
                'link': link,
                'title': header,
                'page_content': content
            }
        for responseSet in response.css('a'):
            href = responseSet.css('a::attr(href)').get()
            if 'geeksforgeeks' in href:
                yield scrapy.Request(url=href, callback=self.parse)
