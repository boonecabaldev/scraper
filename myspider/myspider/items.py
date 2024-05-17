from scrapy import Item, Field

class HatNodeItem(Item):
    url = Field()
    img_src = Field()

class HatLeafItem(Item):
    node_url = Field()
    h3_title = Field()
    date_string = Field()
    src = Field()