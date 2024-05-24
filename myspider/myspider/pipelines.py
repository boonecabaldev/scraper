from sqlalchemy.orm import sessionmaker

from scrapy.pipelines.images import ImagesPipeline

from urllib.parse import urlparse
import os

from scrapy.exceptions import DropItem

from myspider.items import HatComponentItem, HatLeafItem
from .models import HatComponent, HatLeaf, Base
from .database import create_engine

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
        if isinstance(item, HatComponentItem):
            node = HatComponent(url=item['url'], img_src=item['img_src'], img_file_path=item['img_file_path'])
            session.add(node)
            session.commit()
        elif isinstance(item, HatLeafItem):
            node = session.query(HatComponent).filter_by(url=item['node_url']).first()
            if node is not None:
                item['node_url'] = node.url
                del item['node_url']  # remove the temporary node_url field
                #leaf = HatLeaf(**item)
                leaf = HatLeaf(h3_title=item['h3_title'], date_string=item['date_string'], img_src=item['img_src'], node_id=node.id, img_file_path=item['img_file_path'])
                node.leaves.append(leaf)
                session.add(node)
                session.commit()
        return item

class CustomImagesPipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None, *, item):
        print('In call to file_path')

        img_folder_name = 'HatComponents' if isinstance(item, HatComponentItem) else 'HatLeaves'
        hat_cat_name = item['hat_cat_name']

        # Create the absolute path for img_folder_path
        img_folder_path = os.path.join(img_folder_name, hat_cat_name, get_filename_from_url(item['img_src']))
        #print(f'img_folder_path: {img_folder_path}')

        return img_folder_path