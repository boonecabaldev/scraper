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
        from sqlalchemy import MetaData

        engine = db_connect()
        metadata = MetaData()
        metadata.reflect(bind=engine)

        try:
            # Delete all tables in the database
            metadata.drop_all(engine)
            # Recreate all tables in the database
            HatNode.metadata.create_all(engine)
            HatLeaf.metadata.create_all(engine)
        except:
            raise

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

    # https://newtrade6699.x.yupoo.com/albums/162803814?uid=1&isSubCate=false&referrercate=3515821
    #
    # Selectors:
    # divs = response.xpath("//div[@class='showalbum__children image__main']")
    # h3_title = response.xpath("//div[@class='image__decwrap']/h3/@title").get()
    # date_string = response.xpath("normalize-space(//div[@class='image__decwrap']/time/text())").get()
    def parse_link(self, response):
        node = response.meta['node']
        for div in response.xpath("//div[@class='showalbum__children image__main']"):
            h3_title = div.xpath("div[@class='image__decwrap']/h3/@title").get()
            date_string = div.xpath("normalize-space(div[@class='image__decwrap']/time/text())").get()
            src = div.xpath("div[@class='image__imagewrap']/img/@src").get()

            #print(f"h3_title: {h3_title}, date_string: {date_string}, src: {src}")

            leaf = HatLeafItem(
                node_url=node['url'],
                h3_title=h3_title,
                date_string=date_string,
                src=src
            )

            yield leaf
#            leaf = HatLeafItem(
#                url=url,
#                node_url=node['url'],
#                data_src=data_src,
#                data_origin_src=data_origin_src,
#                data_path=data_path,
#                src=src
#            )
#            yield leaf