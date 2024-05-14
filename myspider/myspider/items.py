from scrapy import Item, Field

class HatNodeItem(Item):
    url = Field()
    local_file_path = Field()

class HatLeafItem(Item):
    url = Field()
    local_file_path = Field()
    node_url = Field()
    data_src = Field()
    data_origin_src = Field()
    data_path = Field()
    src = Field()