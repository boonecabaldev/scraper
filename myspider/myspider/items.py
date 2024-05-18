from scrapy import Item, Field

class HatNodeItem(Item):
    url = Field()
    hat_cat_name = Field()
    img_src = Field()
    image_urls = Field()
    images = Field()

class HatLeafItem(Item):
    node_url = Field()
    h3_title = Field()
    date_string = Field()
    src = Field()