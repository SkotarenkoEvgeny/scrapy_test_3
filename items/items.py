# Define here the database for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductTescoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_url = scrapy.Field() # str
    product_id = scrapy.Field() # int
    image_url = scrapy.Field() # str
    product_title = scrapy.Field() # str
    category = scrapy.Field() # str
    price = scrapy.Field() # float
    product_description = scrapy.Field()  # str
    name_and_address = scrapy.Field() # str
    return_address = scrapy.Field() # str
    net_contents = scrapy.Field() # str
    review = scrapy.Field() # list: Review Title (str),Stars Count (int), Author (str), Date (str),Review Text (str)
    usually_bought_next_products = scrapy.Field() # list: Product URL(str), Product Title(str)
