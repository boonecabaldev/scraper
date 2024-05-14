import scrapy
from myspider.items import HatNodeItem, HatLeafItem

from sqlalchemy.orm import sessionmaker
from myspider.models import db_connect, create_table, HatNode, HatLeaf

# nodes = response.xpath("//div[@class='showindex__children']")
# url = nodes.xpath("//a[@class='album__main']/@href").get()
# img_src = nodes.xpath("//a[@class='album__main']//div[@class='album__imgwrap']//img[@class='album__absolute album__img autocover']/@data-src").get()

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
        nodes = response.xpath("//div[@class='showindex__children']")
        for node in nodes:
            url = response.urljoin(node.xpath("a[@class='album__main']/@href").get())
            img_src = node.xpath("a[@class='album__main']//div[@class='album__imgwrap']//img[@class='album__absolute album__img autocover']/@data-src").get()

            #print(f"url: {url}, img_src: {img_src}")

            yield HatNodeItem(url=url, img_src=img_src)
            yield response.follow(url, self.parse_link, meta={'node': {'url': url}})

    def parse_link(self, response):
        node = response.meta['node']
        for div in response.css('div.image__imagewrap'):
            url = response.urljoin(div.css('a::attr(href)').get())
            data_src = div.css('img::attr(data-src)').get()
            data_origin_src = div.css('img::attr(data-origin-src)').get()
            data_path = div.css('img::attr(data-path)').get()
            src = div.css('img::attr(src)').get()

            #print(f"url: {url}, data_src: {data_src}, data_origin_src: {data_origin_src}, data_path: {data_path}, src: {src}")

            leaf = HatLeafItem(
                url=url,
                node_url=node['url'],
                data_src=data_src,
                data_origin_src=data_origin_src,
                data_path=data_path,
                src=src
            )
            yield leaf