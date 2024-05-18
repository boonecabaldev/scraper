import scrapy
from myspider.items import HatNodeItem, HatLeafItem

from sqlalchemy.orm import sessionmaker
from myspider.models import db_connect, create_table, HatNode, HatLeaf
from urllib.parse import urlparse

import os
import shutil

def extract_hat_cat_name(hat_cat_name):
    try:
        # Convert bytes to string
        hat_cat_name = hat_cat_name.decode('utf-8')
    except AttributeError:
        pass
    parsed_url = urlparse(hat_cat_name)
    path_parts = parsed_url.path.split('/')
    new_hat_cat_name = path_parts[-2]  # hat_cat_name is the second last part of the path
    return new_hat_cat_name

# nodes = response.xpath("//div[@class='showindex__children']")
# url = nodes.xpath("//a[@class='album__main']/@href").get()
# img_src = nodes.xpath("//a[@class='album__main']//div[@class='album__imgwrap']//img[@class='album__absolute album__img autocover']/@data-src").get()

class MySpider(scrapy.Spider):
    name = 'myspider'
    handle_httpstatus_list = [301, 302]
    start_urls = ['https://newtrade6699.x.yupoo.com/albums']
    # ...

    def start_requests(self):
        # prevent 302 when downloading images
        headers = self.settings.getdict('DEFAULT_REQUEST_HEADERS')

        # delete images
        self.delete_images_folder('hatnodes')

        #
        # Recreate all tables in the database
        #
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
            print("\nIn call to parse\n")
            url = response.urljoin(node.xpath("a[@class='album__main']/@href").get())
            img_src = node.xpath("a[@class='album__main']//div[@class='album__imgwrap']//img[@class='album__absolute album__img autocover']/@data-src").get()
            if img_src.startswith('//'):
                img_src = 'https:' + img_src
            print(f"img_src: {img_src}")

            # Example usage:
            hat_cat_name = extract_hat_cat_name(img_src) if not isinstance(img_src, bytes) else None
            print(f"hat_cat_name: {hat_cat_name}\n")

            #print(f"url: {url}, img_src: {img_src}")

            item = HatNodeItem(url=url, hat_cat_name=hat_cat_name, img_src=img_src, image_urls=[img_src])
            if img_src:
                # Add scheme to the URL if it's missing
                item['img_src'] = img_src
                item['image_urls'] = [img_src]
            yield item

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
            img_src = div.xpath("div[@class='image__imagewrap']/img/@src").get()
            if img_src.startswith('//'):
                img_src = 'https:' + img_src

            #print(f"h3_title: {h3_title}, date_string: {date_string}, src: {src}")

            hat_cat_name = extract_hat_cat_name(img_src) if not isinstance(img_src, bytes) else None
            item = HatLeafItem(
                node_url=node['url'],
                h3_title=h3_title,
                date_string=date_string,
                hat_cat_name=hat_cat_name,
                )
            if img_src:
                # Add scheme to the URL if it's missing
                item['img_src'] = img_src
                item['image_urls'] = [img_src]
            yield item

    def delete_images_folder(self, folder_name):
        dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images', folder_name)
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            shutil.rmtree(dir_path)