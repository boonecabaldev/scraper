import scrapy
from myspider.items import MyspiderItem

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://newtrade6699.x.yupoo.com/albums']

    def parse(self, response):
        links = response.xpath("//div[@class='showindex__children']//a[@class='album__main']/@href").getall()
        for link in links:
            yield scrapy.Request(response.urljoin(link), callback=self.parse_link)

    def parse_link(self, response):
        for quote in response.css('div.quote'):
            item = MyspiderItem()
            item['title'] = quote.css('span.text::text').get()
            item['link'] = quote.css('span a::attr(href)').get()
            yield item

#class HatLeafSpider(scrapy.Spider):
#    name = 'HatLeafSpider'
#    start_urls = ['https://newtrade6699.x.yupoo.com/albums/156268944?uid=1&isSubCate=false&referrercate=3515821']
#
#    def parse(self, response):
#        for div in response.css('div.image__imagewrap'):
#            yield {
#                'data_src': div.css('img::attr(data-src)').get(),
#                'data_origin_src': div.css('img::attr(data-origin-src)').get(),
#                'data_path': div.css('img::attr(data-path)').get(),
#                'src': div.css('img::attr(src)').get(),
#            }

class HatLeafSpider(scrapy.Spider):
    name = 'HatLeafSpider'
    start_urls = ['https://newtrade6699.x.yupoo.com/albums/156268944?uid=1&isSubCate=false&referrercate=3515821']

    def parse(self, response):
        for div in response.css('div.image__imagewrap'):
            data_src = div.css('img::attr(data-src)').get()
            data_origin_src = div.css('img::attr(data-origin-src)').get()
            data_path = div.css('img::attr(data-path)').get()
            src = div.css('img::attr(src)').get()

            print(f"data_src: {data_src}, data_origin_src: {data_origin_src}, data_path: {data_path}, src: {src}")