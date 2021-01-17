from itertools import zip_longest
import json
import scrapy
import logging

from items.items import ProductTescoItem

array_test = lambda i:(None if len(i) == 0 else '\n'.join(i))


class TescoSpider(scrapy.Spider):
    name = 'tesco'
    allowed_domains = ['tesco.com']
    start_urls = ['https://www.tesco.com/groceries/en-GB/shop/household/kitchen-roll-and-tissues/all?page=1',
                  'https://www.tesco.com/groceries/en-GB/shop/pets/cat-food-and-accessories/all?page=1'
                  ]
    count = 0

    def product_data(self, response):

        item = ProductTescoItem()
        item['product_url'] = response.url
        item['product_id'] = int(response.url.split('/')[-1])
        item['image_url'] = response.xpath('//div[@class="product-image--clickable"]/div/img/@src').get()
        item['product_title'] = response.xpath('//h1[@class="product-details-tile__title"]/text()').get()
        item['category'] = \
            response.xpath('//div/a/span[@class="styled__Text-sc-1xizymv-1 fGKZGz beans-link__text"]/text()').getall()[
                -1]
        item['price'] = float(response.xpath('//span[@data-auto="price-value"]/text()').getall()[0])

        # a part of description
        raw_product_description = response.xpath('//div[@id="product-marketing"]/ul/li/text()').getall() + \
                                  response.xpath('//div[@id="product-description"]/ul/li/text()').getall() + \
                                  response.xpath('//div[@id="features"]/ul/li/text()').getall() + \
                                  response.xpath('//div[@id="other-information"]/ul/li/text()').getall()
        item['product_description'] = array_test(raw_product_description)

        item['name_and_address'] = array_test(response.xpath('//div[@id="manufacturer-address"]/ul/li/text()').getall())
        item['return_address'] = array_test(response.xpath('//div[@id="return-address"]/ul/li/text()').getall())
        item['net_contents'] = array_test(
            response.xpath('//div[@id="net-contents"]/p/text()|//div[@id="pack-size"]/ul/li/text()').getall())

        # a part of review
        review = []
        review_list_keys = ['review_title', 'stars_count', 'author', 'date', 'review_text']
        review_title = response.xpath('//div[@id="review-data"]/article/section/h4/text()').getall()
        stars_count = [int(i.split(' ')[0]) for i in
                       response.xpath('//div[@id="review-data"]/article/section/div/span/text()').getall()]

        raw_author = response.xpath(
            '//section[@class="styled__StyledReview-sxgbrl-0 gMpPCJ"]/p[1]/span[1]/text()').getall()
        date = response.xpath('//span[@class="submission-time"]/text()').getall()
        author = [raw_author[i] if raw_author[i] != date[i] else None for i in range(len(raw_author))]

        review_text = response.xpath(
            '//section[@class="styled__StyledReview-sxgbrl-0 gMpPCJ"]/p[2]/text()|//section[@class="styled__StyledReview-sxgbrl-0 gMpPCJ"]/p[3]/text()').getall()
        if len(review_text) == 0:
            item['review'] = None
        else:
            for i in zip_longest(review_title, stars_count, author, date, review_text):
                review.append(dict(zip((review_list_keys), i)))
            item['review'] = json.dumps(review)

        # a part of usually bought products
        usually_bought_product_url = response.xpath('//div[@class="product-tile-wrapper"]/div/div/div/a/@href').getall()
        usually_bought_product_title = response.xpath(
            '//div[@class="product-tile-wrapper"]/div/div/div/div/div/h3/a/text()').getall()
        if len(usually_bought_product_url) == 0 or len(usually_bought_product_title) == 0:
            item['usually_bought_next_products'] = None
        else:
            usually_bought_next_products = []
            usually_bought_products_keys = ['product_url', 'product_title']
            for i in zip_longest(usually_bought_product_url, usually_bought_product_title):
                usually_bought_next_products.append(dict(zip((usually_bought_products_keys), i)))
            item['usually_bought_next_products'] = json.dumps(usually_bought_next_products)

        logger = logging.getLogger()
        logger.info('Parse function called on %s', response.url)

        yield item

    def parse(self, response):

        NEXT_PAGE_SELECTOR = "//*[@name='go-to-results-page']/@href"
        PRODUCT_ON_PAGE_SELECTOR = "//*[@data-auto='product-tile--title']/@href"
        next_page = response.xpath(NEXT_PAGE_SELECTOR).get()
        product_list_on_page = response.xpath(PRODUCT_ON_PAGE_SELECTOR).getall()
        for product_link in product_list_on_page:
            yield scrapy.Request(response.urljoin(product_link), callback=self.product_data)

        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
