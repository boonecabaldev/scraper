import scrapy
from myspider.items import MyspiderItem

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['http://example.com']

    def parse(self, response):
        for quote in response.css('div.quote'):
            item = MyspiderItem()
            item['title'] = quote.css('span.text::text').get()
            item['link'] = quote.css('span a::attr(href)').get()
            yield item
