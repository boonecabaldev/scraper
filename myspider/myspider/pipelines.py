from sqlalchemy.orm import sessionmaker
from myspider.items import HatNodeItem, HatLeafItem
from .models import HatNode, HatLeaf, Base, create_engine

import scrapy
from scrapy.pipelines.images import ImagesPipeline

from urllib.parse import urlparse
import os

from scrapy.exceptions import DropItem

def get_filename_from_url(url):
    return os.path.basename(urlparse(url).path)

class SQLAlchemyPipeline(object):
    def __init__(self, settings):
        engine = create_engine(settings.get('CONNECTION_STRING'))
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_item(self, item, spider):
        session = self.Session()
        if isinstance(item, HatNodeItem):
            node = HatNode(url=item['url'], img_src=item['img_src'])
            session.add(node)
            session.commit()
        elif isinstance(item, HatLeafItem):
            node = session.query(HatNode).filter_by(url=item['node_url']).first()
            if node is not None:
                item['node_url'] = node.url
                del item['node_url']  # remove the temporary node_url field
                leaf = HatLeaf(**item)
                node.leaves.append(leaf)
                session.add(node)
                session.commit()
        return item

class CustomImagesPipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None, *, item):
        print('In call to file_path')

        img_folder_name = 'hatnodes' if isinstance(item, HatNodeItem) else 'hatleaves'
        hat_cat_name = item['hat_cat_name']

        # Create the absolute path for img_folder_path
        img_folder_path = os.path.join(img_folder_name, hat_cat_name, get_filename_from_url(item['img_src']))
        #print(f'img_folder_path: {img_folder_path}')

        return img_folder_path