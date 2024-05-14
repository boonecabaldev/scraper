import scrapy
from myspider.items import HatNodeItem, HatLeafItem

from sqlalchemy.orm import sessionmaker
from myspider.models import db_connect, create_table, HatNode, HatLeaf

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://newtrade6699.x.yupoo.com/albums']

    def start_requests(self):
        """
        This method is called when the spider opens.
        """
        engine = db_connect()
        create_table(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            # Delete all HatNode and HatLeaf instances
            session.query(HatNode).delete()
            session.query(HatLeaf).delete()
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        # Continue with the default start_requests behavior
        return super().start_requests()

    def parse(self, response):

        links = response.xpath("//div[@class='showindex__children']//a[@class='album__main']/@href").getall()
        for link in links:
            node = HatNodeItem(url=response.urljoin(link))
            yield node
            yield scrapy.Request(response.urljoin(link), callback=self.parse_link, meta={'node': node})

    def parse_link(self, response):
        node = response.meta['node']
        for div in response.css('div.image__imagewrap'):
            data_src = div.css('img::attr(data-src)').get()
            data_origin_src = div.css('img::attr(data-origin-src)').get()
            data_path = div.css('img::attr(data-path)').get()
            src = div.css('img::attr(src)').get()

            leaf = HatLeafItem(
                url=response.url,
                node_url=node['url'],
                data_src=data_src,
                data_origin_src=data_origin_src,
                data_path=data_path,
                src=src
            )
            yield leaf
            #print(f"data_src: {data_src}, data_origin_src: {data_origin_src}, data_path: {data_path}, src: {src}")