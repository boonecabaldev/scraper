from scrapy import Item, Field

class HatComponentItem(Item):
    url = Field()
    hat_cat_name = Field()
    img_src = Field()
    image_urls = Field()
    images = Field()
    img_file_path = Field()

class HatLeafItem(Item):
    node_url = Field()
    h3_title = Field()
    date_string = Field()
    hat_cat_name = Field()
    img_src = Field()
    image_urls = Field()
    images = Field()
    img_file_path = Field()