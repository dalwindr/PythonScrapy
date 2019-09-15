import scrapy

# scrapy shell https://myanimelist.net/manga.php?letter=B


class QuotesSpider(scrapy.Spider):
    name = "myanimallist"
    # scrapy crawl myanimallist -o bricksetSpider.json
    # scrapy crawl myanimallist -o bricksetSpider.csv
    # scrapy crawl myanimallist -o bricksetSpider.xml
    # scrapy crawl myanimallist -o bricksetSpider.jl

    def start_requests(self):
        allowed_domains = ['https://myanimelist.net']
        urls = [
            'https://myanimelist.net/manga.php?letter=B'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_get(self, response, num):
        url = response.url
        score = response.xpath('//div[@class="fl-l score"]//text()').get().strip()
        title = response.xpath('//span[@itemprop="name"]//text()').get()
        href = response.css('a.hoverinfo_trigger').css('a::attr(href)').get()
        synopsis_d = response.xpath('//span[@itemprop="description"]/text()').get()
        ranked = response.xpath('//div[@class="po-a di-ib ml12 pl20 pt8"]//text()').getall()[0]
        ranked_num = response.xpath('//div[@class="po-a di-ib ml12 pl20 pt8"]//text()').getall()[1]
        popularity = response.xpath('//div[@class="po-a di-ib ml12 pl20 pt8"]//text()').getall()[2]
        popularity_num = response.xpath('//div[@class="po-a di-ib ml12 pl20 pt8"]//text()').getall()[3]
        member = response.xpath('//div[@class="po-a di-ib ml12 pl20 pt8"]//text()').getall()[4]
        member_num = response.xpath('//div[@class="po-a di-ib ml12 pl20 pt8"]//text()').getall()[5]
        yield {
                'url': url,
                'Title': title,
                'Synopsis': synopsis_d,
                'Score': score,
                'Ranked': ranked_num,
                'Popularity': popularity_num,
                'Members': member_num,
                'Episode_vol': num
              }

    def parse(self, response):
        title = response.css("title::text").get()
        for response_sel in response.css('div.js-categories-seasonal tr ~ tr'):
            href = response_sel.css('a.hoverinfo_trigger').css('a::attr(href)').get()
            num = response_sel.css('td.borderClass').css('td.borderClass.ac.bgColor0::text').getall()
            num1 = 1
            if len(num) == 0:
                num1 = 1
            elif len(num) == 2:
                num1 = num[0].strip()
            elif len(num) == 3:
                num1 = num[1].strip()

            yield scrapy.Request(url=href, callback=self.parse_get, cb_kwargs={'num': num1})
        next_page = response.css('div.spaceit').css('a::attr(href)').getall()
        if len(next_page) > 0:
            for page in next_page:
                if page is not None:
                    page = response.urljoin(page)
                    yield scrapy.Request(page, callback=self.parse)

