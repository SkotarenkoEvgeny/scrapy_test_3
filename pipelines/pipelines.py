# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging

from sqlalchemy.orm import sessionmaker
from database.conection import db_connect, create_table
from database.models.tescodb import TescoDB


class ProductTescoPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save deals in the database.
        This method is called for every item pipeline component.
        """
        session = self.Session()
        tesco_db = TescoDB()
        tesco_db.product_url = item['product_url']
        tesco_db.product_id = item['product_id']
        tesco_db.image_url = item['image_url']
        tesco_db.product_title = item['product_title']
        tesco_db.category = item['category']
        tesco_db.price = item['price']
        tesco_db.product_description = item['product_description']
        tesco_db.name_and_address = item['name_and_address']
        tesco_db.return_address = item['return_address']
        tesco_db.review = item['review']
        tesco_db.net_contents = item['net_contents']
        tesco_db.usually_bought_next_products = item['usually_bought_next_products']

        try:
            session.add(tesco_db)
            session.commit()
            logger = logging.getLogger()
            logger.info(f'Product {tesco_db.product_id} success saved to the database')
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
